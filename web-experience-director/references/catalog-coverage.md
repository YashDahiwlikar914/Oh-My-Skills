# Catalog Coverage

The catalog separates three different decisions. Website type describes the job people come to do. Design language describes the visual and material grammar. Layout structure describes how content and controls are arranged. A page can combine one entry from each set.

## Coverage Model

The original catalogs remain the source for common product patterns, palettes, typography, UX rules, icons, charts, motion presets, and stack guidance. The extended catalogs add verified anchors for broader website and design work.

| Catalog | Search Domain | Current Coverage | Use It For |
| --- | --- | ---: | --- |
| Product patterns | `product` | 192 | Product intent and audience context |
| Visual styles | `style` | 88 total, 79 searchable | Existing UI style selection and compatibility |
| Website types | `website-types` | 51 | Site purpose, page inventory, trust model, and content fit |
| Design languages | `design-languages` | 44 total, 43 active | Historical and contemporary visual grammar |
| Layout structures | `layout-structures` | 35 | Composition, responsive behavior, and reading order |
| Color systems | `color` | 192 | Semantic color roles and contrast-aware palettes |
| Typography | `typography` and `google-fonts` | 74 pairings and 1934 families | Type roles, mood, scripts, and licensed web fonts |
| UX guidance | `ux` and `web` | 119 plus app-interface rules | Accessibility, interaction, forms, navigation, and feedback |
| Motion | `gsap` | 17 | DOM timeline and motion recipes |
| Charts | `chart` | 25 | Data shape, chart selection, and alternatives |
| Icons | `icons` | 105 curated plus 1512 upstream | Semantic icon selection and imports |
| Stack guidance | `--stack` | 22 stacks and 1260 rows | Framework-specific implementation and freshness |

## Website Types

The website type catalog covers public marketing, commerce, publishing, support, public service, community, education, software, media, events, finance, healthcare, discovery, and niche archive work. Use `website-types` when the request names a site purpose or asks what pages and flows it needs.

The catalog distinguishes site purpose from a feature. A marketplace is not the same as an e-commerce store. A course marketplace is not the same as an LMS. A public information portal is not the same as a government eligibility service. A 3D asset marketplace is still a commerce and discovery problem with an optional spatial preview.

For an uncovered niche, select the closest verified type, state the mismatch, and synthesize only the missing constraints. Do not invent a new industry benchmark or claim that the niche has a canonical UX pattern.

## Design Languages

The design-language catalog includes modernist systems, decorative movements, counterculture print languages, tactile interface languages, product design systems, nostalgia styles, atmospheric digital treatments, editorial languages, motion-led work, and spatial material directions.

Historical names identify a source-backed visual grammar. They do not authorize copying a museum object, typeface, logo, poster, or living artist. Translate the grammar into current semantics, content, licensing, and accessibility requirements.

Use a style as a complete system only when its type, color, surface, density, and motion agree. A style can be a campaign layer or a small accent instead of a product-wide skin. Mark a combination as generated when the catalog contains its ingredients but not the combination itself.

## Layout Structures

The layout catalog covers linear reading, scanning patterns, grids, collections, data displays, application shells, editorial compositions, navigation, workflows, continuous feeds, maps, spatial workspaces, and 3D viewers.

Choose layout from content behavior, not from visual popularity. A bento grid is useful when tile size communicates feature priority. A table is useful when exact relationships matter. A masonry wall is useful when variable image height is part of browsing. A dashboard grid is useful when people monitor and act on metrics. These are not interchangeable skins.

Every spatial or unusual layout needs a mobile composition and a source order that still makes sense without its visual arrangement. Overlap, sticky rails, carousels, maps, and canvases need explicit alternatives.

## Verified And Generated

An active row is a verified ingredient. Its row includes a source list, a verification date, responsive guidance, accessibility guidance, and anti-patterns.

The combination of a website type, design language, layout, motion level, and stack is usually generated. The composition output must list its verified ingredients and use `status: generated`. It must not create a historical name, citation, palette standard, statistic, browser guarantee, or performance result.

Candidate rows are retained for review but excluded from default search. Deprecated rows are not returned as recommendations. A zero-result query is a signal to retry or synthesize with an explicit fallback label.

## Query Examples

```bash
python3 scripts/search.py "government benefits eligibility" --domain website-types
python3 scripts/search.py "Bauhaus Swiss typography" --domain design-languages
python3 scripts/search.py "editorial masonry" --domain layout-structures
python3 scripts/search.py "luxury watch product viewer" --experience
python3 scripts/search.py "cybersecurity SaaS" --design-system --motion 4 --density 5
```

Use separate searches when the intent differs. Search `website-types` for the site's job. Search `design-languages` for visual grammar. Search `layout-structures` for composition. Search `ux`, `web`, or `chart` for a concrete interaction or accessibility outcome. Search the detected stack last.
