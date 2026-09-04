# Design Doc Template

Copy this skeleton when writing the architectural spec to
`.agents/superpowers/specs/YYYY-MM-DD-<topic>-design.md`. Fill every section.
The plan executor reads this doc directly, so each field must be concrete and
free of placeholders. The field names mirror the `writing-plans` plan header so
the handoff is lossless.

# <Feature Name> Design

**Status:** Draft | Approved
**Date:** YYYY-MM-DD
**Author:** <agent> + <human partner>

## Overview

One to three sentences on what this builds and why now.

## Goals

- Do: <what success looks like, with a signal you hit it>
- Do: <>

## Non-Goals

- Don't: <explicitly out of scope>
- Don't: <>

## Requirements

### Functional

- <requirement stated so a test could pass or fail>
- <>

### Success Criteria

- <measurable definition of done>
- <>

### Constraints

- <stack, platform, budget, deadline, compatibility>

## Tech Stack

- <key technologies/libraries with version floors>

## Global Constraints

- <project-wide rules copied verbatim: version floors, dependency limits,
  naming and copy rules, platform requirements — one line each>

## Architecture

2-5 sentences on the approach and how the pieces fit together.

## Components And Interfaces

| Component | Responsibility | Consumes | Produces |
|---|---|---|---|
| | | | |

For each interface, name the exact signature, parameter types, and return
shape the executor needs. A task implementer sees only their own task, so the
names and types here are how neighboring tasks learn what to call.

## Data Flow

Step by step, trace a request or action through the system.

## Error Handling

List the failure modes and the response to each, including the edge cases the
design must survive.

## Testing Approach

How each requirement is verified: unit, integration, and manual checks. Link to
the test harness if one exists.

## Open Questions

- <question still unresolved, with the decision needed>

## Out Of Scope

- <deferred work a later spec should cover>
