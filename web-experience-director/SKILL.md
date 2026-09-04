---
name: web-experience-director
description: Use when designing, building, reviewing, or improving a website or web interface where UI structure, UX, design systems, accessibility, responsive layout, typography, color, charts, icons, animation, cinematic presentation, 2.5D, interactive 3D, Three.js, React Three Fiber, WebGL, or stack-specific implementation changes the result. Do not use for backend-only, data-pipeline, CLI, infrastructure, legal, or nonvisual work.
---

# Web Experience Director

This skill combines searchable UI and UX design intelligence with visual direction for ordinary interfaces, cinematic pages, 2.5D compositions, and interactive 3D. Use the catalog for concrete choices and use the director layer to decide whether visual complexity is justified.

## Local Intelligence

The `data` directory contains the searchable catalog. It includes 88 visual styles with 79 searchable entries, 192 product profiles, 192 semantic palettes, 74 type pairings, 1934 licensed Google Font records, 105 curated icons plus 1512 upstream Phosphor icons, 119 UX guidelines, 17 motion recipes, 25 chart types, 22 stack catalogs, 51 website types, 44 design languages, and 35 layout structures.

The `scripts` directory contains the BM25 search engine, design-system generator, reasoning contract, taxonomy composition rules, catalog validators, refresh utilities, relevance evaluator, tests, and fixtures. Run `python3 scripts/validate_data.py` before trusting a catalog change. Run `python3 -m unittest discover -s scripts/tests -v` for the full regression suite.

## When To Apply

Use it for new pages, components, design systems, accessibility reviews, responsive layouts, typography, color, charts, icons, forms, navigation, dashboards, landing pages, portfolios, product viewers, motion, CSS 3D, canvas, WebGL, Three.js, React Three Fiber, and stack-specific interface implementation.

Skip it for backend logic, API or database design, data pipelines, infrastructure, DevOps, CLI scripts, legal pages, and nonvisual performance work unless the request changes how a user sees, reads, moves through, or operates an interface.

## Priority Order

Resolve higher priority constraints before visual preference.

| Priority | Area | Required Check |
| --- | --- | --- |
| 1 | Accessibility | Contrast, alternatives, keyboard, focus, names, roles, values, reduced motion |
| 2 | Touch and input | Usable tap targets, spacing, loading feedback, pointer and keyboard alternatives |
| 3 | Performance | Stable layout, responsive media, lazy loading, measured main-thread and GPU cost |
| 4 | Product fit | Product goal, audience, trust model, content priority, and primary action |
| 5 | Style and structure | One coherent visual language and a layout that fits the content behavior |
| 6 | Responsive layout | Mobile composition, reflow, zoom, safe areas, and no accidental horizontal scroll |
| 7 | Typography and color | Readable type roles, semantic tokens, contrast, and state that does not rely on hue alone |
| 8 | Motion | Motion has a job, a resting state, interruption behavior, and a reduced-motion path |
| 9 | Forms and feedback | Visible labels, local errors, focus management, status, and progressive disclosure |
| 10 | Navigation and data | Predictable routes, deep links, legends, labels, tooltips, and text alternatives |
| 11 | Spatial enhancement | A real reason for layers, camera, depth, video, canvas, or WebGL |

Read `references/quick-reference.md` for the full original UX rule set and `references/pro-rules.md` before final delivery.

## The Experience Decision

Start with semantic HTML, CSS, and the existing project stack. Select a more complex level only when the brief establishes a user or narrative need.

| Need | Experience Level | Default Implementation |
| --- | --- | --- |
| Scan data, complete forms, compare values, or work quickly | Routine UI | Semantic HTML, CSS, native controls, and accessible SVG or tables |
| Add editorial depth to text, images, or layout | Cinematic 2.5D | Layered DOM, CSS transforms, masks, clip paths, and focused sequencing |
| Show a fixed cinematic sequence | Pre-rendered motion | Responsive video or image sequence with poster and controls |
| Inspect, rotate, configure, or understand a spatial object or world | Interactive 3D | Three.js or React Three Fiber with WebGL and a useful static fallback |

3D is not a premium default. A finance dashboard, checkout form, government service, or documentation page usually needs speed and clarity. A product viewer, spatial map, museum object, or game may justify live rendering. A portfolio or editorial page often needs 2.5D rather than WebGL.

## Experience Brief

Before implementation, record this short brief in the response or project notes.

| Decision | Required Detail |
| --- | --- |
| Product purpose | User goal, audience, primary action, trust needs, and content that cannot be hidden behind effects |
| Visual premise | One concrete world, material, cultural reference, or tension that guides type, color, imagery, surface, and movement |
| Hierarchy | What users notice first, next, and only on demand |
| Experience level | Routine UI, cinematic 2.5D, pre-rendered motion, or interactive 3D, with a reason a simpler level would not meet the need |
| Structure | Website type, page pattern, layout structure, reading order, and mobile composition |
| Spatial plan | Flat, layered, or live scene. For spatial work include subject, depth hierarchy, camera range, preset views, reset path, and stable content rail |
| Motion script | What moves, trigger, job, duration range, easing, rest state, interruption behavior, and reduced-motion variant |
| Interaction paths | Pointer, touch, keyboard, screen reader, and single-pointer alternatives for every meaningful action |
| Delivery budget | Target device, asset limits, rendering scale, loading plan, quality tier, fallback, and evidence required |
| Source status | Verified catalog entries, generated combinations, assumptions, and unresolved questions |

Reject a direction described only as premium, modern, futuristic, immersive, or award winning. Turn the label into concrete decisions tied to the product.

## Workflow

### 1. Analyze Requirements

Extract the product type, target audience, usage context, style words, content priority, device limits, and detected stack.

Use the repository rather than guessing the stack. Check `package.json` for React, Next.js, Vue, Svelte, Nuxt, Angular, or related packages. Check `pubspec.yaml`, `Package.swift`, `*.xcodeproj`, `composer.json`, and `app.json` when relevant. If stack-specific guidance changes the result and no stack is detectable, ask one focused question.

Classify the site with `website-types` and the composition with `layout-structures` when those domains matter. Use `design-languages` for historical or contemporary visual language. Use the original `product` domain for product patterns and the original `style` domain for UI styles.

### 2. Select The Experience Level

Ask whether the requested visual treatment helps people understand, inspect, navigate, decide, or remember something. If not, use routine UI. If a real object or environment needs arbitrary inspection, use interactive 3D. If the work is an editorial sequence, use 2.5D. If the motion is fixed, use media.

Build the semantic and responsive path first. Canvas is an enhancement and never the only place for essential text, navigation, prices, forms, status, or product actions.

### 3. Generate A Design System

For a new page or project, use the design-system mode. The generator aggregates product, style, color, landing, and typography results and applies the product reasoning rules.

```bash
python3 ~/.agents/skills/web-experience-director/scripts/search.py "<product> <industry> <keywords>" --design-system --project-name "<Project Name>"
```

It returns a pattern, style, palette, typography pairing, semantic color tokens, effects, anti-patterns, source identities, and an experience recommendation. Treat search output as a recommendation, not as permission to override repository rules or the brief.

### 3a. Persist The Design System

Use Master plus page overrides when decisions must survive across sessions. Always pass the project root explicitly.

```bash
python3 ~/.agents/skills/web-experience-director/scripts/search.py "<query>" --design-system --persist --project-name "<Project Name>" --output-dir "<project-root>"
```

This writes `design-system/<project-slug>/MASTER.md`. Add `--page "dashboard"` to write `pages/dashboard.md`. Read the existing Master and page override before regenerating. A present file is protected by default. Use `--force` only with explicit authorization.

When building a page, check its override first. The override changes only that page. The Master remains the global source of truth.

### 3b. Tune The Design Dials

The optional dials bias existing search results. They do not replace the product fit decision.

```bash
python3 ~/.agents/skills/web-experience-director/scripts/search.py "<query>" --design-system --variance 8 --motion 6 --density 4
```

| Dial | Low | Mid | High |
| --- | --- | --- | --- |
| `--variance` | Centered and minimal | Balanced and modern | Bold and asymmetric |
| `--motion` | Subtle feedback | Standard sequencing | Complex choreography |
| `--density` | Spacious | Standard | Dense and dashboard-oriented |

Do not use a high motion dial to justify motion that has no job. Do not use a high variance dial to break reading order or accessibility.

### 4. Search The Smallest Useful Domain

Use one dominant intent per query with two to five meaningful terms and a useful constraint such as product, platform, or interaction. Verify the returned domain, identity, status, and fit before applying it.

| Need | Domain or Command |
| --- | --- |
| Existing interface style | `--domain style` |
| Historical or contemporary design language | `--domain design-languages` |
| Product type and page inventory | `--domain website-types` or `--domain product` |
| Layout and composition | `--domain layout-structures` or `--domain landing` |
| Palette and semantic colors | `--domain color` |
| Type pairing | `--domain typography` |
| Licensed individual font | `--domain google-fonts` |
| UX or accessibility outcome | `--domain ux` |
| Web and native interface behavior | `--domain web` |
| Chart choice | `--domain chart` |
| Icon choice | `--domain icons` |
| DOM and SVG motion | `--domain gsap` |
| React rendering guidance | `--domain react` |
| Framework implementation | `--stack <stack>` |
| Verified ingredients plus generated experience | `--experience` |

Useful searches include `"error summary validation" --domain ux`, `"focus not obscured" --domain ux`, `"decorative icon aria hidden" --domain icons`, `"stop animation offscreen" --domain gsap`, `"keyboard accessible chart" --domain chart`, and `"3d viewer fallback" --domain layout-structures`.

The three taxonomy domains are independent. Search the website type for the site's job, the design language for visual grammar, and the layout structure for composition. A generated combination must name its verified ingredients.

### 5. Handle Search Failure

If a search returns zero results, retry once with a narrower or clearer query or an explicit domain. If it remains empty, label any general guidance as fallback guidance. Never present an empty result as a database match.

Candidate taxonomy rows are excluded from default search. Deprecated style rows resolve to their active parent or explicit replacement. Do not promote an unverified candidate because its name sounds plausible.

### 6. Apply Stack Guidance

Use the detected stack and its current guidance. The catalog includes React, Next.js, Vue, Svelte, Astro, Nuxt, Angular, Tailwind, shadcn, Three.js, Laravel, SwiftUI, React Native, Flutter, Jetpack Compose, JavaFX, WPF, WinUI, Avalonia, Uno, and UWP.

```bash
python3 ~/.agents/skills/web-experience-director/scripts/search.py "<implementation concern>" --stack <stack>
```

Keep framework guidance separate from visual direction. Do not assume a stack and do not combine current and legacy guidance without an explicit migration need.

## Visual Direction

Read `references/visual-systems.md` when choosing or reviewing type, color, surface, hierarchy, layout, or a visual language. Read `references/catalog-coverage.md` when combining website type, design language, and structure.

Use one visual premise. A watch viewer can be a watchmaker inspection bench. A fashion archive can be a printed catalogue on a workshop table. A security product can use an incident report becoming an action plan. These premises create decisions. A dark gradient, glowing orb, glass cards, grain, giant sans heading, and cursor follower do not.

Use real copy, real names, real images, real data, loading states, empty states, and error states early. A layout that only works with short placeholder text is not ready.

## Motion And Spatial Direction

Read `references/motion-and-spatial-design.md` for motion roles, 2.5D, camera planning, scene composition, scroll, input, and reduced motion.

Motion can orient, explain, confirm, connect, or create atmosphere. Name the job before choosing a library. Every sequence needs a resting state and interruption behavior.

Use CSS layers before a renderer for editorial depth. Use live 3D when the user must inspect, rotate, configure, or understand a spatial subject. Keep the content rail, labels, controls, and primary action in semantic DOM.

Do not hijack document scrolling. Do not make dragging, hover, a cursor follower, camera travel, or precise scroll position the only route to information or action.

## Implementation Direction

Read `references/implementation.md` before adding a scene, timeline, media sequence, or renderer. It covers CSS, GSAP, video, Three.js, React Three Fiber, glTF and GLB, KTX2, asset ownership, quality tiers, input, context loss, and demand rendering.

Keep ownership clear.

- React owns infrequent application state and semantic UI.
- CSS owns simple presentational transitions and layout.
- GSAP owns deliberate DOM or scene timelines and cleans them up.
- A renderer or frame loop owns per-frame object and camera transforms.

Do not update React state, allocate vectors, create materials, or perform layout reads inside a high-frequency frame loop. Render continuously only while something moves. Reuse resources, instance repeated meshes, cap internal resolution, and dispose of owned GPU resources.

## Accessibility And Quality

Read `references/quality-gates.md` and `references/pro-rules.md` before delivery.

- Keep essential content and actions in semantic DOM.
- Give informative visual content useful alternative text, captions, or adjacent explanation.
- Give custom controls an accessible name, role, state, and value where relevant.
- Keep keyboard order and visual order understandable.
- Provide a click or tap alternative for every dragging action.
- Respect `prefers-reduced-motion` without removing meaning or function.
- Keep contrast valid over every image, video, canvas, and scene state.
- Provide a static or DOM fallback for failed media, unsupported WebGL, and lost context.
- Recompose for narrow screens instead of shrinking a desktop scene until it fails.
- Test slow network, zoom, touch, keyboard, reduced motion, no WebGL, and constrained hardware.

## Output Contract

When giving a design recommendation, return these parts in order.

1. Experience level and reason
2. Product type, visual language, and layout structure
3. Content hierarchy and primary action
4. Visual premise and design system sources
5. Motion or spatial script when selected
6. Implementation stack and asset plan
7. Responsive, keyboard, touch, reduced-motion, and fallback behavior
8. Performance budget and verification evidence
9. Verified, generated, fallback, and unresolved decisions

Do not call a generated combination a canonical style. Do not invent proof, metrics, source citations, browser support, asset budgets, or performance results.

## References

- `references/quick-reference.md` contains the original searchable ten-category UX guidance.
- `references/pro-rules.md` contains the original pre-delivery checklist.
- `references/catalog-coverage.md` explains website types, design languages, layout structures, and verified versus generated coverage.
- `references/research-sources.md` contains the research bibliography and local video observations.
- `references/visual-systems.md` covers hierarchy, premise, typography, color, surfaces, and responsive composition.
- `references/motion-and-spatial-design.md` covers motion jobs, 2.5D, real-time scenes, camera, scroll, and input.
- `references/implementation.md` covers CSS, GSAP, media, Three.js, React Three Fiber, assets, performance, and recovery.
- `references/quality-gates.md` covers accessibility, device testing, performance evidence, fallbacks, and sources.

## Search Tool

The local search tool is in this skill directory. Invoke it by its full path.

```bash
python3 ~/.agents/skills/web-experience-director/scripts/search.py "<query>" --domain <domain>
python3 ~/.agents/skills/web-experience-director/scripts/search.py "<query>" --stack <stack>
python3 ~/.agents/skills/web-experience-director/scripts/search.py "<query>" --experience
python3 ~/.agents/skills/web-experience-director/scripts/search.py "<query>" --experience --website-type "<type>" --design-language "<language>" --layout-structure "<structure>"
```

The tool supports `--design-system`, `--persist`, `--output-dir`, `--page`, `--force`, `--variance`, `--motion`, `--density`, `--json`, and `--full`. Use `--help` for the complete current argument list.
