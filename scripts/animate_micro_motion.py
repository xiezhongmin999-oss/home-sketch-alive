#!/usr/bin/env python3
"""Render scene-aware, seamless micro-motion over a finished illustration."""

from __future__ import annotations

import argparse
import copy
import json
import math
import random
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter


ALIASES = {
    "steam": "particle_flow",
    "light_breathe": "pulse",
    "sway": "masked_transform",
}
PRIMITIVES = {"particle_flow", "pulse", "shimmer", "ripple", "masked_transform"}


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def px_point(value: list[float], size: tuple[int, int]) -> tuple[int, int]:
    return round(value[0] * size[0]), round(value[1] * size[1])


def px_box(value: list[float], size: tuple[int, int]) -> tuple[int, int, int, int]:
    x0, y0 = px_point(value[:2], size)
    x1, y1 = px_point(value[2:], size)
    return min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)


def rgba(color: list[int], alpha: int) -> tuple[int, int, int, int]:
    rgb = [int(clamp(component, 0, 255)) for component in color[:3]]
    return rgb[0], rgb[1], rgb[2], int(clamp(alpha, 0, 255))


def normalized_effect(effect: dict) -> dict:
    item = copy.deepcopy(effect)
    raw_name = item.get("primitive", item.get("type"))
    primitive = ALIASES.get(raw_name, raw_name)
    item["primitive"] = primitive

    if raw_name == "steam":
        anchor_x, anchor_y = item["anchor"]
        width = float(item.get("width", 0.06))
        height = float(item.get("height", 0.14))
        item.setdefault(
            "box",
            [anchor_x - width / 2, anchor_y - height, anchor_x + width / 2, anchor_y],
        )
        item.setdefault("direction", [0.08, -1.0])
        item.setdefault("particle_style", "wisp")
        item.setdefault("count", item.get("wisps", 5))
        item.setdefault("distribution", "edge")
    elif raw_name == "light_breathe":
        item.setdefault("shape", "ellipse")
        item.setdefault("waveform", "sine")
    elif raw_name == "sway":
        item.setdefault("mode", "oscillate")
        item.setdefault("rotation_degrees", item.get("amplitude_degrees", 1.2))

    return item


def validate_box(value: object, name: str) -> None:
    if not isinstance(value, list) or len(value) != 4:
        raise ValueError(f"{name} must be [x0, y0, x1, y1]")
    if not all(0 <= float(component) <= 1 for component in value):
        raise ValueError(f"{name} coordinates must be between 0 and 1")


def validate_plan(plan: dict) -> list[dict]:
    duration = float(plan.get("duration", 4.0))
    fps = int(plan.get("fps", 12))
    effects = [normalized_effect(effect) for effect in plan.get("effects", [])]
    if not 1.0 <= duration <= 12.0:
        raise ValueError("duration must be between 1 and 12 seconds")
    if not 4 <= fps <= 30:
        raise ValueError("fps must be between 4 and 30")
    max_edge = int(plan.get("max_edge", 0))
    if max_edge and not 320 <= max_edge <= 3840:
        raise ValueError("max_edge must be 0 or between 320 and 3840 pixels")
    if not 1 <= len(effects) <= 2:
        raise ValueError("motion plan must contain one or two effects")

    for effect in effects:
        primitive = effect.get("primitive")
        if primitive not in PRIMITIVES:
            raise ValueError(f"unsupported primitive: {primitive}")
        if primitive in {"particle_flow", "pulse", "shimmer", "ripple"}:
            validate_box(effect.get("box"), f"{primitive}.box")
        if primitive == "particle_flow":
            direction = effect.get("direction", [0, -1])
            if not isinstance(direction, list) or len(direction) != 2:
                raise ValueError("particle_flow.direction must be [x, y]")
            if effect.get("particle_style", "wisp") not in {"wisp", "dot"}:
                raise ValueError("particle_style must be wisp or dot")
        if primitive == "pulse":
            if effect.get("shape", "ellipse") not in {"ellipse", "rectangle"}:
                raise ValueError("pulse.shape must be ellipse or rectangle")
            if effect.get("waveform", "sine") not in {"sine", "flicker"}:
                raise ValueError("pulse.waveform must be sine or flicker")
        if primitive == "shimmer" and effect.get("direction", "diagonal") not in {
            "horizontal",
            "vertical",
            "diagonal",
        }:
            raise ValueError("shimmer.direction is invalid")
        if primitive == "masked_transform":
            if "mask" not in effect:
                raise ValueError("masked_transform requires mask")
            if "box" in effect:
                validate_box(effect["box"], "masked_transform.box")
            mode = effect.get("mode", "oscillate")
            if mode not in {"oscillate", "continuous"}:
                raise ValueError("masked_transform.mode must be oscillate or continuous")
            if mode == "continuous":
                total = float(effect.get("rotation_degrees", 360)) * float(
                    effect.get("cycles", 1)
                )
                if abs(total % 360) > 1e-6:
                    raise ValueError(
                        "continuous masked rotation must complete whole 360-degree turns"
                    )
    return effects


def resolve_asset(path_value: str, plan_dir: Path) -> Path:
    path = Path(path_value)
    return path if path.is_absolute() else plan_dir / path


def prepare_assets(
    effects: list[dict], base: Image.Image, plan_dir: Path
) -> list[dict]:
    prepared: list[dict] = []
    for effect in effects:
        item = copy.deepcopy(effect)
        if item["primitive"] == "masked_transform":
            mask = Image.open(resolve_asset(item["mask"], plan_dir)).convert("L")
            if mask.size != base.size:
                mask = mask.resize(base.size, Image.Resampling.LANCZOS)
            if "box" in item:
                bounded = Image.new("L", base.size, 0)
                ImageDraw.Draw(bounded).rectangle(px_box(item["box"], base.size), fill=255)
                mask = ImageChops.multiply(mask, bounded)
            item["_mask"] = mask
            if item.get("background_plate"):
                plate = Image.open(
                    resolve_asset(item["background_plate"], plan_dir)
                ).convert("RGBA")
                if plate.size != base.size:
                    plate = plate.resize(base.size, Image.Resampling.LANCZOS)
                item["_background_plate"] = plate
        prepared.append(item)
    return prepared


def particle_flow_layer(
    size: tuple[int, int], effect: dict, phase: float, seed: int
) -> Image.Image:
    x0, y0, x1, y1 = px_box(effect["box"], size)
    field_w, field_h = max(1, x1 - x0), max(1, y1 - y0)
    direction = effect.get("direction", [0, -1])
    length = math.hypot(float(direction[0]), float(direction[1])) or 1.0
    dx, dy = float(direction[0]) / length, float(direction[1]) / length
    count = int(clamp(int(effect.get("count", 6)), 1, 40))
    opacity = float(effect.get("opacity", 0.45))
    color = effect.get("color", [255, 250, 235])
    style = effect.get("particle_style", "wisp")
    distribution = effect.get("distribution", "edge" if style == "wisp" else "field")
    drift = float(effect.get("drift", 0.12))
    size_px = max(1, round(min(size) * float(effect.get("size", 0.0024))))
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    rng = random.Random(seed)

    for index in range(count):
        age = (phase + rng.random() + index / count) % 1.0
        fade = math.sin(math.pi * age) ** 1.7
        alpha = round(255 * opacity * fade)
        if alpha <= 1:
            continue
        if distribution == "field":
            start_x = x0 + rng.random() * field_w
            start_y = y0 + rng.random() * field_h
            travel = 0.45
        else:
            start_x = x0 + rng.random() * field_w
            start_y = y1 if dy < 0 else y0 if dy > 0 else y0 + rng.random() * field_h
            if abs(dx) > abs(dy):
                start_x = x1 if dx < 0 else x0
            travel = 1.0
        move_x = dx * field_w * age * travel
        move_y = dy * field_h * age * travel
        cross_x, cross_y = -dy, dx
        wobble = math.sin(math.tau * (age * 1.6 + rng.random()))
        center_x = start_x + move_x + cross_x * wobble * field_w * drift
        center_y = start_y + move_y + cross_y * wobble * field_h * drift

        if style == "dot":
            radius = size_px * (0.65 + rng.random() * 0.7)
            draw.ellipse(
                (
                    round(center_x - radius),
                    round(center_y - radius),
                    round(center_x + radius),
                    round(center_y + radius),
                ),
                fill=rgba(color, alpha),
            )
        else:
            points: list[tuple[int, int]] = []
            segments = 18
            wisp_length = field_h * 0.32
            for step in range(segments):
                u = step / (segments - 1)
                along_x = -dx * wisp_length * u
                along_y = -dy * wisp_length * u
                wave = math.sin(math.tau * (u * 1.4 + age + rng.random()))
                across = wave * field_w * drift * (0.35 + u)
                points.append(
                    (
                        round(center_x + along_x + cross_x * across),
                        round(center_y + along_y + cross_y * across),
                    )
                )
            draw.line(points, fill=rgba(color, alpha), width=size_px, joint="curve")

    blur = max(0.0, min(size) * float(effect.get("blur", 0.0012)))
    rendered = layer.filter(ImageFilter.GaussianBlur(blur)) if blur else layer
    clipped = Image.new("RGBA", size, (0, 0, 0, 0))
    clipped.paste(rendered.crop((x0, y0, x1, y1)), (x0, y0))
    return clipped


def pulse_value(effect: dict, phase: float) -> float:
    cycles = max(1, int(effect.get("cycles", 1)))
    theta = math.tau * cycles * phase
    if effect.get("waveform", "sine") == "flicker":
        value = 0.62 + 0.20 * math.sin(theta) + 0.10 * math.sin(3 * theta + 0.4)
        return clamp(value, 0.15, 1.0)
    return 0.55 + 0.45 * (0.5 - 0.5 * math.cos(theta))


def pulse_layer(size: tuple[int, int], effect: dict, phase: float) -> Image.Image:
    x0, y0, x1, y1 = px_box(effect["box"], size)
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    shape = effect.get("shape", "ellipse")
    if shape == "rectangle":
        draw.rectangle((x0, y0, x1, y1), fill=255)
    else:
        draw.ellipse((x0, y0, x1, y1), fill=255)
    softness = max(0.0, float(effect.get("softness", 0.18)))
    blur = round(max(x1 - x0, y1 - y0) * softness)
    if blur:
        mask = mask.filter(ImageFilter.GaussianBlur(blur))
    opacity = float(effect.get("opacity", 0.08)) * pulse_value(effect, phase)
    mask = mask.point(lambda value: round(value * opacity))
    layer = Image.new("RGBA", size, rgba(effect.get("color", [255, 222, 168]), 255))
    layer.putalpha(mask)
    return layer


def shimmer_layer(size: tuple[int, int], effect: dict, phase: float) -> Image.Image:
    x0, y0, x1, y1 = px_box(effect["box"], size)
    local_w, local_h = max(1, x1 - x0), max(1, y1 - y0)
    mask = Image.new("L", (local_w, local_h), 0)
    draw = ImageDraw.Draw(mask)
    band = max(2, round(float(effect.get("band_width", 0.18)) * max(local_w, local_h)))
    travel = phase * (max(local_w, local_h) + 2 * band) - band
    direction = effect.get("direction", "diagonal")
    if direction == "horizontal":
        draw.rectangle((round(travel - band), 0, round(travel + band), local_h), fill=255)
    elif direction == "vertical":
        draw.rectangle((0, round(travel - band), local_w, round(travel + band)), fill=255)
    else:
        center = round(travel)
        draw.polygon(
            [
                (center - band, 0),
                (center + band, 0),
                (center - local_h + band, local_h),
                (center - local_h - band, local_h),
            ],
            fill=255,
        )
    softness = max(0.0, float(effect.get("softness", 0.12)))
    if softness:
        mask = mask.filter(ImageFilter.GaussianBlur(max(1, round(band * softness))))
    visibility = math.sin(math.pi * phase) ** 2
    opacity = float(effect.get("opacity", 0.06)) * visibility
    mask = mask.point(lambda value: round(value * opacity))
    local = Image.new("RGBA", (local_w, local_h), rgba(effect.get("color", [255, 255, 245]), 255))
    local.putalpha(mask)
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    layer.alpha_composite(local, dest=(x0, y0))
    return layer


def ripple_layer(size: tuple[int, int], effect: dict, phase: float) -> Image.Image:
    x0, y0, x1, y1 = px_box(effect["box"], size)
    center_x, center_y = (x0 + x1) / 2, (y0 + y1) / 2
    width, height = x1 - x0, y1 - y0
    rings = int(clamp(int(effect.get("rings", 3)), 1, 8))
    cycles = max(1, int(effect.get("cycles", 1)))
    opacity = float(effect.get("opacity", 0.18))
    stroke = max(1, round(min(size) * float(effect.get("stroke", 0.0016))))
    color = effect.get("color", [235, 245, 240])
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    for index in range(rings):
        age = (phase * cycles + index / rings) % 1.0
        fade = math.sin(math.pi * age) ** 1.6
        ring_w = width * age
        ring_h = height * age
        draw.ellipse(
            (
                round(center_x - ring_w / 2),
                round(center_y - ring_h / 2),
                round(center_x + ring_w / 2),
                round(center_y + ring_h / 2),
            ),
            outline=rgba(color, round(255 * opacity * fade)),
            width=stroke,
        )
    return layer.filter(ImageFilter.GaussianBlur(max(0.3, stroke * 0.35)))


def masked_transform(
    base: Image.Image, frame: Image.Image, effect: dict, phase: float
) -> tuple[Image.Image, Image.Image]:
    mask: Image.Image = effect["_mask"]
    if "_background_plate" in effect:
        frame.paste(effect["_background_plate"], (0, 0), mask)
    moving = Image.new("RGBA", base.size, (0, 0, 0, 0))
    moving.paste(base, (0, 0), mask)
    pivot = px_point(effect.get("pivot", [0.5, 0.5]), base.size)
    cycles = max(1, int(effect.get("cycles", 1)))
    mode = effect.get("mode", "oscillate")
    if mode == "continuous":
        angle = float(effect.get("rotation_degrees", 360)) * cycles * phase
        movement = 0.0
    else:
        movement = math.sin(math.tau * cycles * phase)
        angle = float(effect.get("rotation_degrees", 1.2)) * movement
    moving = moving.rotate(
        angle,
        resample=Image.Resampling.BICUBIC,
        center=pivot,
        expand=False,
    )
    translate = effect.get("translate", [0, 0])
    dx = round(float(translate[0]) * base.width * movement)
    dy = round(float(translate[1]) * base.height * movement)
    if dx or dy:
        moving = moving.transform(
            base.size,
            Image.Transform.AFFINE,
            (1, 0, -dx, 0, 1, -dy),
            resample=Image.Resampling.BICUBIC,
        )
    return frame, moving


def render(input_path: Path, plan_path: Path, output_path: Path) -> None:
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    effects = validate_plan(plan)
    base = Image.open(input_path).convert("RGBA")
    max_edge = int(plan.get("max_edge", 0))
    if max_edge and max(base.size) > max_edge:
        scale = max_edge / max(base.size)
        base = base.resize(
            (round(base.width * scale), round(base.height * scale)),
            Image.Resampling.LANCZOS,
        )
    effects = prepare_assets(effects, base, plan_path.parent)
    duration = float(plan.get("duration", 4.0))
    fps = int(plan.get("fps", 12))
    seed = int(plan.get("seed", 7))
    frame_count = max(2, round(duration * fps))
    frames: list[Image.Image] = []

    for index in range(frame_count):
        phase = index / frame_count
        frame = base.copy()
        for effect_index, effect in enumerate(effects):
            primitive = effect["primitive"]
            if primitive == "particle_flow":
                overlay = particle_flow_layer(
                    base.size, effect, phase, seed + effect_index * 101
                )
            elif primitive == "pulse":
                overlay = pulse_layer(base.size, effect, phase)
            elif primitive == "shimmer":
                overlay = shimmer_layer(base.size, effect, phase)
            elif primitive == "ripple":
                overlay = ripple_layer(base.size, effect, phase)
            else:
                frame, overlay = masked_transform(base, frame, effect, phase)
            frame = Image.alpha_composite(frame, overlay)
        frames.append(frame.convert("RGB"))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    frame_ms = round(1000 / fps)
    suffix = output_path.suffix.lower()
    if suffix == ".gif":
        palette_frame = frames[0].quantize(colors=256, method=Image.Quantize.MEDIANCUT)
        gif_frames = [
            frame.quantize(palette=palette_frame, dither=Image.Dither.NONE)
            for frame in frames
        ]
        gif_frames[0].save(
            output_path,
            save_all=True,
            append_images=gif_frames[1:],
            duration=frame_ms,
            loop=0,
            optimize=False,
            disposal=2,
        )
    elif suffix == ".webp":
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=frame_ms,
            loop=0,
            lossless=True,
            method=6,
        )
    else:
        raise ValueError("output extension must be .gif or .webp")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="final still image")
    parser.add_argument("--plan", type=Path, required=True, help="semantic motion-plan JSON")
    parser.add_argument("--output", type=Path, required=True, help=".gif or .webp")
    args = parser.parse_args()
    render(args.input, args.plan, args.output)
    print(args.output.resolve())


if __name__ == "__main__":
    main()
