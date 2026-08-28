# Scene-Aware Code Micro-Motion

Use this reference only when the user requests animation. Animate the accepted final
still with code; do not send the whole image through another generative image or video
pass.

## Plan Semantics Before Effects

Do not search for one of a few hard-coded objects. First inventory plausible motion in
the actual scene, then select one primary subject and at most one subordinate subject.
For each candidate record:

1. `subject`: the visible object or atmospheric region;
2. `evidence`: why motion is natural in this scene;
3. `behavior`: the real-world action being implied;
4. `primitive`: the code operation that can express it;
5. `region` or `mask`: the smallest affected area;
6. `amplitude`, `period`, and `role`: how quiet and how important the motion is.

Choose by semantic fit, not by effect availability. Motion should reinforce the still's
storytelling highlight when possible.

## Generic Primitive Library

| Primitive | Appropriate scene behavior | Needs mask |
|---|---|---|
| `particle_flow` | steam, dust, smoke, bubbles, snow, sparks, drifting pollen | No |
| `pulse` | lamp glow, screen glow, indicator blink, candle breathing, changing daylight | No |
| `shimmer` | glass reflection, water highlight, polished edge, sunlight sliding over a plane | No |
| `ripple` | water, bath, sink, aquarium, reflective liquid surface | No |
| `masked_transform` | plant/curtain sway, clock hand, fan, hanging object, pet ear or tail | Yes |

The legacy names `steam`, `light_breathe`, and `sway` remain accepted as aliases for
`particle_flow`, `pulse`, and `masked_transform`.

`masked_transform` can oscillate or rotate continuously. Use it only with a clean
full-size mask. When the movement exposes the object's original position, also provide
a same-size `background_plate` with that object removed; otherwise keep the movement
small enough that the original does not create a visible ghost.

## Selection and Fallback

Use this order without forcing a result:

1. Animate a visible object whose normal function implies motion.
2. Animate a supported environmental cue such as light, reflection, water, dust, or
   air movement.
3. Use a nearly imperceptible paper-grain or print shimmer only when it suits the fixed
   illustration style and does not make the whole image flicker.
4. If every option would feel invented or distracting, return the still and state that
   no credible micro-motion was found.

Never add an unrelated moving prop merely to satisfy an animation request.

## Motion Plan Schema

Use normalized coordinates from `0` to `1`. Include semantic fields so the plan remains
reviewable even though the renderer only needs the primitive parameters.

```json
{
  "duration": 4.0,
  "fps": 12,
  "max_edge": 960,
  "seed": 7,
  "effects": [
    {
      "subject": "warm drink",
      "evidence": "a cup is visible on the desk",
      "behavior": "thin steam rises and disperses",
      "role": "primary",
      "primitive": "particle_flow",
      "box": [0.43, 0.60, 0.53, 0.79],
      "direction": [0.05, -1.0],
      "particle_style": "wisp",
      "color": [255, 250, 235],
      "opacity": 0.5,
      "count": 6
    },
    {
      "subject": "window reflection",
      "evidence": "daylight enters through the visible window",
      "behavior": "a narrow reflection slowly crosses the glass",
      "role": "secondary",
      "primitive": "shimmer",
      "box": [0.58, 0.18, 0.82, 0.52],
      "direction": "diagonal",
      "color": [218, 238, 235],
      "opacity": 0.05,
      "band_width": 0.18
    }
  ]
}
```

### Primitive Parameters

- `particle_flow`: `box`, `direction`, `particle_style` (`wisp` or `dot`), `count`,
  `color`, `opacity`, optional `size`, `drift`, and `blur`.
- `pulse`: `box`, `shape` (`ellipse` or `rectangle`), `color`, `opacity`, `softness`,
  optional `cycles` and `waveform` (`sine` or `flicker`).
- `shimmer`: `box`, `direction` (`horizontal`, `vertical`, or `diagonal`), `color`,
  `opacity`, `band_width`, and optional `softness`.
- `ripple`: `box`, `color`, `opacity`, `rings`, `stroke`, and optional `cycles`.
- `masked_transform`: `mask`, `pivot`, `mode` (`oscillate` or `continuous`), optional
  `rotation_degrees`, `translate`, `cycles`, `box`, and `background_plate`.

## Render

Run:

```powershell
python scripts/animate_micro_motion.py --input <still.png> --plan <plan.json> --output <loop.webp>
```

The script supports `.gif` and animated `.webp`. Prefer 3–6 seconds at 10–15 fps and
use `max_edge` to keep previews manageable. Animated WebP is usually smaller and keeps
the fixed illustration palette more faithfully.

## Acceptance

- The camera, crop, background, architecture, furniture, linework, and unselected
  objects remain pixel-stable.
- No more than two subjects move, and the secondary motion is quieter.
- Motion is supported by visible scene evidence and noticeable only on a second look.
- The first and last frames join without a visible jump.
- The still remains a separate deliverable.
- If no credible motion exists, the workflow stops at the still instead of inventing
  one.
