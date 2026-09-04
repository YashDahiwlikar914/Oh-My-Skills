# Motion And Spatial Design

## Give Motion A Job

Motion should orient, explain, confirm, connect, or set an intentional atmosphere. Name its job before choosing an easing, duration, or library.

| Motion Role | Useful Example | Bad Substitute |
| --- | --- | --- |
| Orientation | Keep a selected image visible while its project page opens | A full page flash that loses the selection context |
| Feedback | Make a selected finish visibly update the watch material | A button bounce unrelated to the change |
| Continuity | Move a card into its detail view while preserving its identity | Repeated fade-out and fade-in transitions |
| Atmosphere | Add quiet movement to a background that supports the product world | Constant motion competing with reading |

Interaction feedback should feel immediate. Scene transitions can take longer when they preserve context and do not delay the next action. Every sequence needs a resting state and a clear interruption behavior.

## Use 2.5D Before Real-Time 3D

Many cinematic sites need depth, not a renderer. Use layers of text, images, masks, shadows, CSS perspective, clipping, and transforms when the desired effect is an editorial composition.

Good 2.5D patterns include image stacks that separate on hover, content panels that move through a controlled depth field, card galleries with distinct front and background planes, and typography that reveals a new scene without leaving the reading flow.

Keep the content rail stable. Depth should direct attention around the content, not turn reading into a camera ride.

## Design A Real-Time Scene Deliberately

Use real-time 3D only for a spatial task. Define these parts before writing the scene.

| Part | Decision |
| --- | --- |
| Subject | The object or environment people need to inspect or understand |
| Camera | The opening framing, allowed range, preset views, and reset path |
| Light | The material information the lighting must reveal |
| Interaction | The precise result of hover, tap, drag, scroll, or keyboard input |
| Content rail | The DOM content that stays readable while the scene changes |
| Fallback | The useful static image, video, or standard UI path |

Do not use a floating abstract object as a substitute for a premise. A 3D object should reveal shape, scale, material, configuration, location, or narrative state that plain content cannot show as well.

## Scroll And Camera

Let normal document scrolling remain normal unless a pinned section creates clear value. A scroll-linked scene should have named content chapters. Each chapter changes the camera, material, object state, or information density for a reason.

Avoid scroll hijacking. Avoid motion that requires precise scrolling to discover essential content. Stop decorative camera motion when the user interacts, loses focus, or requests reduced motion.

## Input And Comfort

Pointer movement, tilt, drag, and scroll are enhancements. Provide visible controls for meaningful outcomes such as view presets, rotation, zoom, and slide navigation. Keep page scrolling available around an embedded scene. Handle touch cancellation and interrupted gestures.

For reduced motion, replace automatic camera travel, parallax, scaling, and looping ambience with a stable frame, simple dissolve, or direct state change. Preserve meaning and controls.

## Red Flags

- The same rise and fade reveal on every element
- A camera that moves before the user understands what it is looking at
- A cursor follower used instead of clear navigation or feedback
- A drag-only interaction with no preset, button, click, or keyboard path
- A full-screen scene that makes text and calls to action harder to use
- A transition that looks impressive in a recording but feels slow when repeated
