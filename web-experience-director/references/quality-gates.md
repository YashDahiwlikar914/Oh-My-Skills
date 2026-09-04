# Quality Gates

## Accessibility Is Part Of The Experience

Essential content, navigation, and actions must exist in semantic DOM. Canvas can enhance an experience but cannot be the only way to read content, operate controls, learn status, or complete a task.

Give meaningful visual content a useful text alternative, caption, or adjacent explanation that matches its purpose. Custom scene controls need an accessible name, role, current state, and keyboard operation. Use native controls where they fit.

| Area | Required Check |
| --- | --- |
| Keyboard | All controls work in a logical order with visible, unobscured focus |
| Touch and pointer | Meaningful actions have a click or tap path that does not require dragging |
| Motion | `prefers-reduced-motion` keeps meaning and function while removing nonessential travel and looping |
| Contrast | Text and controls meet WCAG 2.2 AA contrast requirements over every image, video, and scene state |
| Text alternatives | Visual information has suitable alternative text, captions, or adjacent explanation |
| Custom controls | Scene controls expose a name, role, state, value where relevant, and keyboard operation |
| Canvas | A useful static or DOM fallback exists for load failure, context loss, and unsupported graphics |
| Loading | A poster, skeleton, or stable first state prevents empty or shifting content |

## Responsive And Device Review

Test the actual experience, not only a desktop screenshot.

| Test | Evidence |
| --- | --- |
| Narrow mobile | Content order, tap targets, safe areas, and scene gestures work without horizontal overflow |
| Touch device | Page scrolling remains available and controls work without hover |
| Keyboard | A complete primary journey works with focus visible at every point |
| Reduced motion | The page remains intentional and usable without camera travel, parallax, or loops |
| No WebGL | Product content and primary action remain available |
| Slow network | The first useful content appears before optional assets finish |
| Constrained hardware | Rendering quality degrades gracefully without continuous heat or input lag |

## Performance Review

Measure on a target mobile profile with browser performance tooling. Inspect long tasks, layout work during animation, frame pacing, memory growth across navigation, and input response. Do not use a desktop GPU as proof that a scene is ready.

Keep a written quality tier for scenes that need one. State the model detail, texture policy, render scale, post-processing, animation policy, and fallback. Make the lower tier look intentional instead of merely broken.

## Final Review

Before delivery, verify all of these points.

- The visual premise is specific and visible in the finished work.
- The primary user task is faster to understand than the visual effect.
- Every animation has a named job and a resting state.
- The selected technology is the smallest useful level of complexity.
- The mobile composition is deliberate.
- The no-motion and no-WebGL paths preserve the experience purpose.
- The production build has been checked for console errors, failed assets, and layout shifts.
- Known limitations are stated plainly.

## Research Sources

Use these primary references when a decision needs current technical detail.

| Topic | Source |
| --- | --- |
| Responsive canvas sizing and cleanup | Three.js Manual Responsive Design and Cleanup |
| Model loading | Three.js GLTFLoader and Khronos glTF 2.0 guidance |
| React scene performance | React Three Fiber Advanced Pitfalls and Scaling Performance |
| GPU limits and resource management | MDN WebGL Best Practices |
| Motion preference | MDN prefers-reduced-motion |
| Keyboard and drag alternatives | W3C WCAG 2.2 Keyboard and Dragging Movements |
| React animation cleanup | GSAP React documentation |
| Asset compression | Khronos KTX and Basis Universal documentation |
