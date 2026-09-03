---
name: home-sketch-alive
description: >
  Transform a user-provided interior photo, floor plan, elevation, overhead view,
  axonometric, cutaway, or model image into a hand-drawn architectural editorial
  illustration with flat color blocks, warm-white outlines, restrained paper texture,
  and one scene-supported storytelling highlight. Use when the user wants light
  cleanup and view correction followed by a stylized still interior illustration.
---

# Home Sketch Alive

## Objective

Turn one interior source into a recognizable architectural editorial illustration.
Tidy and correct the existing view first, then change its visual language without
redesigning the space.

## Workflow

Default to two image edits. For an already tidy plan, elevation, model, axonometric, or
photo, combine the edits only when the same spatial and cleanup constraints can be
preserved reliably.

### 1. Create a Lightly Curated Base

Read [references/input-routing.md](references/input-routing.md). Use the original image
as the authority for architecture, proportions, openings, zones, major furniture, and
observation type. Apply only the selected route's geometric correction. Group or omit
temporary small clutter only; retain representative lived-in objects.

### 2. Apply the Fixed Illustration Style

Read [references/style-paper-cut-white-line.md](references/style-paper-cut-white-line.md),
[references/story-highlights.md](references/story-highlights.md), and
[references/style-reference.md](references/style-reference.md). Use the accepted base
as the authority for the scene and as the primary color evidence. Use up to two
route-matched references as examples of linework, flatness, object simplification,
texture, and palette harmony. The references may help compress saturation and contrast
but must not impose an unsupported global cast or recolor major surfaces.

Do not use style references during the base edit. Choose one primary storytelling
highlight supported by the scene, with at most one subordinate cue.

## Non-Negotiable Locks

- Preserve the source observation type, crop, room outline, openings, functional
  zones, and major furniture relationships.
- Apply only the geometric correction allowed by the selected route; do not invent
  hidden space or convert the source to another projection.
- Cleanup may simplify temporary small clutter but may not move, replace, or redesign
  architecture or major furniture.
- Change visual expression rather than spatial content. Do not add people, captions,
  arrows, or watermarks.

## Final Check

Accept the still only when it:

1. remains unmistakably the same interior and observation type;
2. preserves recognizable major color identities and the scene's broad warm-neutral-
   cool character while allowing restrained palette harmonization;
3. uses flat matte shapes, a visible warm-white outline network, and subtle neutral
   paper texture without photographic or model-like rendering;
4. retains some lived-in evidence and uses one natural storytelling highlight;
5. contains no unrelated additions or text.

If the style check fails, retry the style edit once with the same accepted base and
route-matched references, stating the observed failure. Regenerate the base only when
its geometry failed. If the retry still misses a requirement, disclose the mismatch
instead of describing the result as compliant.
