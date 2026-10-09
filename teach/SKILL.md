---
name: teach
description: Teach the user a new skill or concept, within this workspace.
disable-model-invocation: true
argument-hint: "What would you like to learn about?"
---

The user wants you to teach them something. They intend to learn the topic over multiple sessions, so you track state between sessions.

## Teaching Workspace

Each time the user invokes `/teach`, create a Title Case folder inside the current directory, named after the topic, such as `Rust-Basics/`. If that folder already exists, reuse it. This folder is the teaching workspace. Put everything you create inside it, and nothing outside it.

Name every file and subfolder you create in Title Case or in full caps. Use hyphens instead of spaces. Full caps suits the top-level documents like `MISSION.md`. Title Case suits everything else, such as `Lessons/1-Intro-To-Loops.html`.

Workspace paths such as `./Lessons/` resolve from the topic folder. Only the `*-FORMAT.md` links resolve from this skill's folder. These files hold the state of their learning.

- `MISSION.md` captures the _reason_ the user is interested in the topic. Ground all teaching in it. Follow [MISSION-FORMAT.md](./MISSION-FORMAT.md).
- `./Reference/*.html` holds reference materials. These compress the learnings from the lessons into cheat sheets, reference algorithms, syntax, yoga poses, and glossaries. They are the raw units of learning. Make them beautiful, print-friendly, and quick to scan.
- `RESOURCES.md` lists resources that ground your teaching in context or supply knowledge and wisdom. Follow [RESOURCES-FORMAT.md](./RESOURCES-FORMAT.md).
- `./Learning-Records/*.md` holds learning records of what the user has learned. They work like architectural decision records in software development. They capture non-obvious lessons and key insights that you may need to revise later or that should drive future sessions. Use them to calculate the zone of proximal development. Title them `1-<Title-Case-Name>.md` and increment the number each time. Follow [LEARNING-RECORD-FORMAT.md](./LEARNING-RECORD-FORMAT.md).
- `./Lessons/*.html` holds lessons. A **lesson** is a single, self-contained HTML output that teaches one tightly scoped thing tied to the mission. It is the primary unit of teaching in this workspace.
- `./Assets/*` holds reusable **components** shared across lessons. See [Assets](#assets).
- `NOTES.md` is your scratchpad for user preferences and working notes.

## Philosophy

Deep learning needs three things.

- **Knowledge**, captured from high-quality, high-trust resources
- **Skills**, acquired through relevant interactive lessons you devise from the knowledge
- **Wisdom**, which comes from interacting with other learners and practitioners

Until `RESOURCES.md` is well populated, focus on finding high-quality resources that help the user acquire knowledge. Don't trust your parametric knowledge.

Some topics need more skills than knowledge. Theoretical physics leans toward knowledge. Yoga leans toward skills.

### Fluency vs Storage Strength

Keep two types of learning apart.

- **Fluency strength** is in-the-moment retrieval of knowledge.
- **Storage strength** is long-term retention of knowledge.

Fluency gives the user an illusory sense of mastery. Storage strength is the real goal. Design lessons that build long-term retention through desirable difficulty.

- Retrieval practice, which means recall from memory
- Spacing, which means distributing practice over time
- Interleaving, which means mixing different but related topics in practice. Use it for skills practice only.

## Lessons

The lesson is the main thing you produce. It carries knowledge and skills to the user. Each lesson is one self-contained HTML file, saved to `./Lessons/` and titled `1-<Title-Case-Name>.html`, with the number incrementing each time.

Make each lesson **beautiful**, with clean, readable typography and layout, since the user will return to it to review. Think Tufte.

Keep the lesson short enough to finish quickly. Learners have small working memory, and the lesson must fit inside it. Give the user a single tangible win to build on. Tie the lesson directly to the mission and keep it inside the user's zone of proximal development.

If possible, open the lesson file for the user with a CLI command.

Link each lesson to other lessons and reference documents with HTML anchors.

Recommend one primary source in each lesson for the user to read or watch. Pick the highest-quality, highest-trust resource you found on the topic.

Add a reminder in each lesson to ask the agent followup questions. The agent is their teacher and can help with anything unclear.

## Typography and Writing

Lessons and reference documents use **Urbanist** for titles and headings, and **Outfit** for all other content. Load both from Google Fonts in the shared stylesheet, with a sans-serif fallback. Set them there once and don't override them in individual lessons.

Invoke the `stop-slop` skill before writing prose for the teaching material. That covers lessons, reference documents, and quiz text.

## Hard-Word Definitions

The user should never have to leave a lesson to look up a word. Whenever lesson or reference text uses a hard word, show its meaning in a pop-up when the user hovers over it.

The reader is Indian and English is their third language. Judge hard words by that, not by what a native speaker would find hard. A hard word is one a fluent but non-native reader is unlikely to know. Cover rare or formal vocabulary, idioms and phrasal verbs, words with several meanings, Latin or French loanwords, jargon, and technical terms the lesson hasn't taught yet. When unsure, mark the word. A needless pop-up costs less than a lost reader. Skip everyday words, and skip terms the lesson itself defines in the surrounding sentence. Mark each word the first time it appears on a page, plus any later spot far enough from the first that the reader may have forgotten it.

- Build one reusable component for this in `./Assets/` the first time you need it. A small script plus styles that show a tooltip is enough. Link it from every lesson and reference document, and don't inline it.
- Mark words in HTML with a `<span class="define" tabindex="0" data-definition="...">word</span>` pattern or an equivalent. Underline marked words with a dotted line so the user can see which ones are hoverable.
- The pop-up opens on hover and on keyboard focus, and on tap for touch screens. It closes when the pointer or focus leaves. It must stay inside the viewport and never cover the word itself.
- Write each definition in plain English, in one or two short sentences. Define the word as it is used in this lesson. Use no word harder than the one being defined, and prefer short, common words and simple sentence structure. Avoid idioms inside definitions. Where a concrete example makes the meaning clearer, add one short example sentence.
- Invoke the `stop-slop` skill before writing the definitions, exactly as for the rest of the prose. Definitions get the same scrutiny as lesson text. No filler openers like "refers to" or "a term used to describe". State the meaning directly.
- Keep definitions consistent with `GLOSSARY.md` and the glossary reference if either exists. A glossary term needs no separate pop-up wording that contradicts it.

## Assets

Build lessons from reusable **components** stored in `./Assets/`. These include stylesheets, quiz widgets, simulators, diagram helpers, and anything a second lesson could reuse.

Default to reuse. Read `./Assets/` before authoring a lesson and build from the components already there. When a lesson needs something new and reusable, write it as a component in `./Assets/` and link to it. Don't inline code that a future lesson would duplicate.

A shared stylesheet is the first component each workspace earns. Each lesson links it, so the lessons look like one consistent course instead of a pile of one-offs. The component library should grow with the workspace.

## The Mission

Tie each lesson into the mission, the reason the user is interested in the topic.

If the user is unclear about the mission, or `MISSION.md` is empty, start by asking why they want to learn this.

Without the mission, knowledge acquisition floats free of real-world goals. Lessons feel too abstract, and you can't judge what the user should do next.

Missions may change as the user builds skills and knowledge. That is normal. Update `MISSION.md` and add a learning record to capture the change. Confirm with the user before changing the mission.

## Zone of Proximal Development

Challenge the user just enough in each lesson.

The user may name an exact thing to learn. If they don't, find their zone of proximal development in three steps.

- Read their `Learning-Records`.
- Work out the right thing to teach from their mission.
- Teach the most relevant thing that fits in their zone of proximal development.

## Knowledge

Design lessons around a skill the user will learn. Include only the knowledge that skill requires. Teach the knowledge first, then have the user practice the skill through an interactive feedback loop.

Gather knowledge from trusted resources first, and track them in `RESOURCES.md`. Fill lessons with citations, meaning links to external resources that back up each claim. Citations make the lesson more trustworthy.

Difficulty hurts knowledge acquisition because it eats the working memory the user needs for understanding.

## Skills

Knowledge is about acquisition. Skills are about durability and flexibility, so make the knowledge stick.

Difficulty helps skill acquisition. Effortful retrieval builds storage strength. Teach skills through interactive lessons, using these tools.

- Interactive lessons with quizzes and light in-browser tasks
- Lessons that guide the user through a list of real-world steps, such as yoga poses

Base each of these on a **feedback loop** where the user receives feedback on their performance. Keep the loop as tight as possible, with immediate and ideally automatic feedback.

In quizzes, give each answer the same number of words, and the same number of characters where possible. Vary the position of the correct answer across questions. Give the user no clues about the answer through formatting or order.

## Acquiring Wisdom

Wisdom comes from real-world interaction, which means testing skills outside the learning environment.

When the user asks a question that seems to need wisdom, attempt an answer by default, then hand them to a **community**.

A community is a place, online or offline, where the user can test their skills in the real world. It might be a forum, a subreddit, a real-world class if the budget allows, or a local interest group.

Look for high-reputation communities the user can join. If the user says they don't want to join a community, respect that.

## Reference Documents

Create reference documents while you create lessons. Lessons can link to them. They track the raw units of knowledge that matter across lessons.

The user will rarely revisit lessons but will revisit reference documents. Make them the compressed essence of the lesson, in a format built for quick reference.

Some learning topics lend themselves to reference.

- Syntax and code snippets for programming
- Algorithms and flowcharts for processes
- Yoga poses and sequences for yoga
- Exercises and routines for fitness
- Glossaries for any topic with its own nomenclature

Glossaries are an essential reference. Once you create one, follow it in each lesson.

## `NOTES.md`

The user will sometimes express preferences about how they want to be taught, or things for you to keep in mind. Record those preferences here so you can refer back to them when you design lessons or work with the user.
