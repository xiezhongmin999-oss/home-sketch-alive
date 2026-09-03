# Fixed Style: Abstract Graphic Interior Illustration

Apply this style after accepting the curated base. Read
[story-highlights.md](story-highlights.md) and select references through
[style-reference.md](style-reference.md) before writing the final prompt.

## Visual Language

- Aim for roughly 90% flat editorial graphic design and 10% handmade texture.
- Build architecture, furniture, and retained objects from simplified interlocking
  matte color shapes. Preserve their category, position, orientation, and proportion.
- Organize walls, openings, major furniture, fixtures, and selected small objects with
  clearly visible white or warm-white outlines. Use moderately bold lines with slight
  wobble, retracing, offsets, soft corners, and occasional incomplete joins.
- Dark colors may be fills or sparse internal marks, but must not become the dominant
  outer contour of major objects.
- Build a compact palette primarily from the accepted base. Keep major color identities
  and the scene's broad color temperature recognizable; use references to harmonize
  saturation, contrast, and a few source-supported accents.
- Replace photographic material detail with broad color, sparse marks, and subtle
  neutral paper, gouache, screen-print, or collage texture. Texture must not behave as
  a global color filter.
- Express existing depth through overlap, plane hierarchy, object massing, and minimal
  flat contact shadows. Keep orthographic sources flat and perspective sources
  perspectival.

## Style Edit Prompt

Use the role block from `style-reference.md`, add the scene locks from the source brief,
then use this core instruction:

    Transform the accepted base into a hand-drawn abstract graphic architectural
    interior illustration. Preserve its camera, projection, crop, room proportions,
    architecture, openings, zones, major furniture, retained objects, and broad color
    relationships. Establish this scene-supported primary highlight: [PRIMARY
    HIGHLIGHT]. Add this subordinate cue only if it supports the same quiet story:
    [SECONDARY CUE OR NONE].

    Use simplified interlocking matte color blocks, a compact harmonious palette, and
    restrained neutral paper or gouache texture. Keep major source colors and overall
    color temperature recognizable while allowing gentle saturation and contrast
    compression. Draw a clearly visible, slightly irregular white or warm-white
    outline network across architecture, major furniture, fixtures, and selected
    identity objects. Use dark tones only as fills or sparse internal marks. Remove
    photographic material detail and express depth only through overlap, plane
    hierarchy, object massing, and minimal flat shadows. Do not restore removed
    clutter, redesign the scene, add people or text, or borrow content from the style
    references.

## Reject If

- the view, crop, architecture, zones, or major furniture relationships drift;
- major source colors become unrecognizable or the image gains an unsupported uniform
  cast;
- dark contours dominate major objects or warm-white lines appear only on walls;
- photographic materials, deep shadows, 3D-model volume, CAD precision, or excessive
  micro-detail dominate;
- cleaned clutter returns, lived-in evidence disappears, or the highlight competes
  with the space;
- reference objects, layouts, people, captions, arrows, or watermarks appear.
