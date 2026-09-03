# Route-Matched Style Reference Library

Use these images only during the final style edit. They are style examples, not extra
views of the user's scene.

## Assets

Perspective and frontal:

- `../assets/style-perspective-living-room.png`
- `../assets/style-frontal-bedroom.png`
- `../assets/style-frontal-workspace.png`

Overhead and plan:

- `../assets/style-overhead-apartment.png`
- `../assets/style-overhead-office.png`
- `../assets/style-overhead-living-room.png`

Resolve selected assets to absolute local paths before the image-edit call.

## Selection

Attach the accepted base first, followed by up to two references from the matching
projection family. Do not attach all six.

- `OVERHEAD` or `PLAN`: choose from the overhead group.
- `FRONTAL`, `CORNER`, or `PRESERVE_VIEW`: choose from the perspective and frontal
  group.
- `PRESERVE_PROJECTION`: use frontal examples for elevations. For axonometric,
  cutaway, or model views, use one closest example only when it will not encourage a
  projection change; otherwise rely on the textual style specification.

Prefer references with similar object scale or scene density. When two references are
used, favor complementary examples rather than two with the same dominant palette.

## Image Roles

The accepted base controls the scene: camera, projection, crop, architecture,
furniture, objects, spatial relationships, and broad lighting. It is also the primary
evidence for color identity and overall color temperature.

The references demonstrate warm-white outline coverage, loose hand-drawn line quality,
flat matte shapes, object simplification, restrained paper texture, and palette
cohesion. They may guide saturation, contrast, and accent distribution while keeping
the source's major colors recognizable. Treat their walls, floors, objects, and light
as example content rather than facts about the user's scene.

## Prompt Role Block

Insert this near the beginning of the style-edit prompt:

    Image 1 is the CONTENT BASE. Preserve its view, projection, crop, architecture,
    furniture, spatial relationships, broad lighting, recognizable major colors, and
    overall warm-neutral-cool character. The remaining images are STYLE REFERENCES.
    Use them for the warm-white outline language, flat matte shapes, object
    simplification, restrained paper texture, and palette harmony. They may guide
    saturation and contrast, but do not copy their rooms, objects, composition, or
    impose a uniform color cast unsupported by Image 1.
