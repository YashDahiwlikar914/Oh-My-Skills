# Implementation Choices

## Select The Smallest Useful Tool

| Requirement | Preferred Tool | Notes |
| --- | --- | --- |
| Layout, state, hover depth, short transitions | HTML, CSS, and native browser behavior | Keep controls and content semantic |
| Sequenced DOM and SVG motion | CSS first, then GSAP for explicit timelines | One system owns each animated property |
| Fixed cinematic visual | Responsive video or image sequence | Provide a poster and do not block content on playback |
| Interactive object or environment | Three.js with WebGL | Build a useful fallback before scene polish |
| React scene composition | React Three Fiber when the project already uses React | Mutate refs in frame work and keep high-frequency updates out of React state |
| WebGPU feature | A measured optional enhancement | Feature-detect it and keep a tested WebGL or static path |

Do not install a 3D library until the existing stack and selected experience level make it necessary. Do not write raw WebGL when Three.js already provides the needed scene behavior.

## Build For Progressive Delivery

1. Ship meaningful HTML, controls, and a stable first visual state.
2. Show a poster image or low-cost preview while optional media or a scene loads.
3. Load the scene when it is visible or when the user signals interest.
4. Keep the static path usable when WebGL fails, a context is lost, JavaScript is delayed, or the device cannot sustain the chosen quality.

Use glTF 2.0 or GLB for web models. Remove unused meshes, animations, materials, and texture channels before shipping. Use Draco, Meshopt, or KTX2 only after measuring transfer size, decode time, memory, and visual quality on target devices.

## Render With A Budget

Let CSS own the canvas size. Resize the drawing buffer only when the displayed dimensions change, then update the camera projection. Cap the internal pixel count or quality scale instead of rendering blindly at the full device pixel ratio.

Render continuously only while something needs to move. For input-driven React Three Fiber scenes, prefer demand rendering and invalidate when external animation changes the scene. Use `useFrame` for direct ref mutation with delta time. Do not call React state setters, allocate vectors, or create materials inside a frame loop.

Reuse geometries, materials, textures, and loaded assets. Instance repeated meshes. Dispose of geometries, materials, textures, render targets, and removed models according to ownership. A scene that mounts and unmounts repeatedly must not grow GPU memory.

Reduce complexity before reducing readability. Remove post-processing, lower texture resolution, reduce transparent layers, instance repeated objects, or lower the render scale before sacrificing essential content.

## Coordinate Motion Systems

Keep clear ownership boundaries.

- React owns infrequent application state and semantic UI.
- CSS owns simple presentational transitions.
- GSAP owns deliberate DOM or scene timelines and cleans them up on unmount.
- The renderer or frame loop owns per-frame object and camera transforms.

In React, clean up GSAP timelines and event-created animations. Do not let GSAP and a render loop both write the same object transform. If GSAP drives a demand-rendered React Three Fiber scene, request invalidation on each update.

## Input And Recovery

Use Pointer Events for mouse, pen, and touch. Keep pointer handlers small. Capture a pointer only during an active drag and reset state on pointer up, cancellation, and lost capture. Scope `touch-action` to the scene rather than disabling page scrolling globally.

Provide keyboard controls and visible DOM controls for any meaningful scene operation. Listen for WebGL context loss and show the static experience rather than leaving an empty black rectangle.

## Implementation Review

- Does the initial page work before the scene has loaded
- Is every nonessential asset lazy or intent loaded
- Can a constrained phone run the selected quality tier without sustained jank
- Is the scene idle when nobody is interacting with it
- Does any frame loop update React state or allocate objects
- Is there a static fallback for unavailable or lost graphics support
