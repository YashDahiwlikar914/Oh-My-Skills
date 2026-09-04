# Research Sources

This skill uses source-backed catalog rows and general implementation guidance. A source supports the claim attached to it. It does not make every combination of its ideas an established category.

## Standards And Accessibility

| Source | Use |
| --- | --- |
| [WCAG 2 Overview](https://www.w3.org/WAI/standards-guidelines/wcag/) | Four accessibility principles, success criteria, and version boundaries |
| [WCAG 2.2 Standard](https://www.w3.org/TR/WCAG22/) | Keyboard, focus, reflow, animation, dragging, and contrast requirements |
| [WAI Carousels Tutorial](https://www.w3.org/WAI/tutorials/carousels/) | Structure, pause controls, keyboard operation, announcements, and focus |
| [WAI Page Structure](https://www.w3.org/WAI/tutorials/page-structure/) | Landmarks, headings, and semantic reading order |
| [WAI Forms Tutorial](https://www.w3.org/WAI/tutorials/forms/) | Labels, grouping, validation, notifications, and multi-page forms |
| [WAI Images Tutorial](https://www.w3.org/WAI/tutorials/images/) | Informative, decorative, functional, and complex image alternatives |
| [WAI ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/) | Custom widget roles, states, keyboard patterns, and disclosure behavior |
| [USWDS](https://designsystem.digital.gov/) | Government components, patterns, tokens, performance, and accessibility |
| [GOV.UK Design System](https://design-system.service.gov.uk/) | Government styles, components, patterns, plain language, and accessibility |

## Information Architecture And Layout

| Source | Use |
| --- | --- |
| [NN/G F-Shaped Reading](https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/) | Scanning behavior and ways to format content so users find important information |
| [NN/G Dashboards](https://www.nngroup.com/articles/dashboards-preattentive/) | Preattentive cues and dashboard signal versus noise |
| [NN/G Web UX Study Guide](https://www.nngroup.com/articles/web-ux-study-guide/) | General web UX research and site behavior |
| [NN/G Intranet Portals](https://www.nngroup.com/reports/intranet-portals-experiences-real-life-projects) | Enterprise portal information architecture and governance |
| [Baymard Research](https://baymard.com/research) | Commerce product lists, product details, checkout, and marketplace UX |
| [MDN CSS Grid](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout) | Grid tracks, responsive composition, and layout primitives |
| [MDN Masonry Layout](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout/Masonry_layout) | Current masonry support and fallback considerations |

## Historical And Contemporary Visual Languages

| Source | Use |
| --- | --- |
| [The Met on Bauhaus](https://www.metmuseum.org/essays/the-bauhaus-1919-1933) | Bauhaus history, workshops, mass production, and typography |
| [Getty Bauhaus Principles](https://www.getty.edu/research/exhibitions_events/exhibitions/bauhaus/new_artist/history/principles_curriculum) | Bauhaus curriculum, materials, color, and formal relationships |
| [V&A Art Nouveau](https://www.vam.ac.uk/articles/an-introduction-to-art-nouveau) | Organic ornament, craft, and natural forms |
| [V&A Art Deco](https://www.vam.ac.uk/articles/an-introduction-to-art-deco) | Geometry, ornament, luxury, and mechanized modernity |
| [Tate Constructivism](https://www.tate.org.uk/art/art-terms/c/constructivism) | Constructivist geometry, material, and political context |
| [Smithsonian Psychedelic Posters](https://www.si.edu/stories/psychedelic-posters) | Psychedelic poster composition, lettering, and saturation |
| [Whitney Roy Lichtenstein](https://whitney.org/artists/779) | Pop Art, mass media, repetition, and halftone context |
| [Google Material Design Eras](https://design.google/library/material-design-eras) | Material 1, Material 2, Material 3, paper, motion, and system evolution |
| [NN/G Flat Design](https://www.nngroup.com/articles/flat-design/) | Flat design, affordance problems, and Flat 2.0 context |
| [NN/G Neobrutalism](https://www.nngroup.com/articles/neobrutalism/) | Current neobrutalist interface traits and usability risks |
| [Codrops Maximalism](https://tympanus.net/codrops/2022/07/11/the-comeback-of-maximalism-and-what-it-could-mean-for-web-design/) | Contemporary maximalism and controlled visual density |

## Rendering And Animation

| Source | Use |
| --- | --- |
| [Three.js Responsive Design](https://threejs.org/manual/en/responsive.html) | CSS sizing, camera aspect, drawing buffer, and pixel budget |
| [Three.js Cleanup](https://threejs.org/manual/en/cleanup.html) | Ownership and disposal of geometries, materials, textures, and models |
| [Three.js GLTFLoader](https://threejs.org/docs/pages/GLTFLoader.html) | glTF and GLB asset loading |
| [React Three Fiber Performance](https://r3f.docs.pmnd.rs/advanced/pitfalls) | Frame loops, allocations, refs, and React state boundaries |
| [React Three Fiber Scaling](https://r3f.docs.pmnd.rs/advanced/scaling-performance) | Demand rendering, instancing, and adaptive quality |
| [MDN WebGL Best Practices](https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/WebGL_best_practices) | GPU limits, batching, memory, compressed textures, and context handling |
| [MDN prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion) | Motion preference detection and reduced alternatives |
| [GSAP React](https://gsap.com/resources/React/) | React cleanup, scoped timelines, and context-safe interaction animation |
| [Khronos glTF](https://www.khronos.org/gltf/) | Web model format and delivery ecosystem |
| [Khronos KTX](https://www.khronos.org/ktx/) | GPU texture compression and transfer considerations |

## Local Video References

The local videos in `/home/yash/Videos` were used as visual references, not as technical sources. They show several recurring patterns.

- The travel, museum, and editorial references use a stable interface shell with image swaps, layered composition, strong typography, and controlled chapter changes.
- The Gcore and AI course references use product UI, dark surfaces, light transitions, and occasional globe or image motion. Their value comes from sequencing and hierarchy rather than a renderer on every section.
- The portfolio reference uses stacked image planes, crop changes, poster-like framing, and content transitions that can be built with DOM and CSS 2.5D.
- The references support a distinction between a cinematic presentation and a true interactive 3D object. The latter is justified when a visitor needs to inspect or configure shape, material, or space.
