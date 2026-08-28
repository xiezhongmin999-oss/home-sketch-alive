---
name: home-sketch-alive
description: >
  Transform a user-provided interior photo, floor plan, elevation, overhead view,
  axonometric, cutaway, or model image into one fixed hand-drawn abstract graphic
  architectural illustration with flat color blocks, white outlines, and restrained
  paper-collage texture, a scene-supported storytelling highlight, and optional subtle
  code-generated loop animation. Use when the user wants light cleanup and view
  correction followed by a stylized still or gently animated interior illustration.
---

# Home Sketch Alive

## Objective

Turn one interior image into a recognizable architectural editorial illustration in
the single style defined by this skill. First create a tidier, deliberately corrected
spatial base; then add one natural storytelling highlight while changing its visual
language. When motion is requested, animate only one or two scene-supported elements
with code.

## Workflow

Default to two image edits and a still result. For an already tidy photo, plan,
elevation, model, or axonometric image, combine the edits when the same constraints can
be preserved reliably. Add the third, code-animation stage only when the user requests
motion or an animated deliverable.

### 1. Create a Lightly Curated Base

Read [references/input-routing.md](references/input-routing.md). Use the original image
as the authority for architecture, spatial proportions, openings, functional zones,
major furniture, and the kind of observation being used. Apply only the selected
route's geometric correction; do not convert the source into another view type or
invent unseen space.

Group, reduce, or omit temporary small clutter that interferes with reading the space.
Retain a few representative objects that communicate function and lived-in character.
Do not redesign the layout, lighting, furniture, architecture, or circulation.

### 2. Apply the Fixed Illustration Style

Read [references/style-paper-cut-white-line.md](references/style-paper-cut-white-line.md)
and [references/story-highlights.md](references/story-highlights.md). Apply the fixed
style and choose one scene-supported primary highlight, with at most one subordinate
secondary cue. The accepted curated base is the sole authority for view, projection,
composition, crop, architecture, spatial relationships, and furniture during this
step; the highlight may enhance or add only a small, plausible atmospheric or lived-in
cue.

Do not offer or silently substitute another style. Always retain the accepted still as
a deliverable.

### 3. Add Optional Code Micro-Motion

When motion is requested, read [references/motion-animation.md](references/motion-animation.md).
Inventory plausible motion from the actual scene, choose one primary subject and
optionally one quiet supporting subject, then map their natural behaviors to generic
code primitives. Write a semantic motion-plan JSON and run
`scripts/animate_micro_motion.py` against the final still. Keep the camera, background,
architecture, furniture, linework, and all unselected regions pixel-stable. Return the
still and the animated output. If no credible motion exists, stop at the still rather
than inventing a moving prop.

## Spatial Locks

Across both edits, preserve the original:

- observation type, room outline, scale, and spatial proportions;
- walls, openings, doors, windows, and relationships between zones;
- major furniture identity, position, orientation, relative size, and function.

The first edit may correct roll, lens distortion, vertical convergence, page skew, or
inconsistent perspective only as defined by the selected route. Keep orthographic
sources orthographic, axonometric sources axonometric, elevations frontal, overhead
views overhead, and perspective scenes perspective. Once the curated base is accepted,
lock its camera, projection, perspective, vanishing points, composition, and crop for
the style edit. The animation stage must not move the camera or globally regenerate,
warp, zoom, pan, or relight the illustration.

## Cleanup Boundary

Reduce clutter without erasing life. It is acceptable to consolidate excess cups,
cables, packaging, utensils, shoes, clothing, bottles, tools, and shelf contents into
fewer representative objects or simple groups. Preserve useful identity cues such as
a computer, lamp, books, plants, a cup, shoes, or cookware when supported by the
source.

Never move, rotate, resize, replace, or redesign major furniture or architecture as
part of cleanup. Do not clear every surface or turn the home into a showroom.

## Final Check

Before delivery, confirm that the image:

1. is unmistakably the same interior using the selected correction route and layout;
2. changes no architecture, opening, functional zone, or major furniture relationship;
3. reduces only distracting small clutter and retains some lived-in evidence;
4. uses the fixed flat color-block, warm-white-line, restrained paper-collage style;
5. contains one natural storytelling highlight rather than an unrelated decorative
   gimmick;
6. contains no people, captions, arrows, or watermarks.

For animated delivery, also confirm that the loop moves no more than two supported
elements, starts and ends seamlessly, and leaves the rest of the image stable.
