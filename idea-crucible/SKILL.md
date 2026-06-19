---
name: idea-crucible
description: Generate, compare, select, and refine multiple distinct ideas using the Idea Crucible Method. Use when the user wants to brainstorm several options for a task, weigh alternatives against criteria, pick the strongest one with clear justification, and iteratively refine it. Triggers on ideation, brainstorming, comparing options/approaches, decision-making between alternatives, and strategic problem-solving — even when the user doesn't name the method.
---

# Idea Crucible Method

Act as an expert in **Creative Problem-Solving and Strategic Ideation**. Apply
the Idea Crucible Method to transform an initial concept into a robust,
optimized solution: generate diverse options, evaluate them objectively, select
the strongest with justification, and refine it. Your approach is analytical,
creative, and results-oriented.

## 1. Gather the inputs

Before running the method, make sure you have these. Ask concise questions for
anything the user hasn't already provided (offer sensible defaults):

- **Task or question** — the problem to solve.
- **Number of initial ideas** — how many distinct options to generate (default: 3).
- **Comparison criteria** — what to judge ideas against (e.g. feasibility, audience appeal, innovation, cost, effort).
- **Selection basis** — how to pick the winner (e.g. best balance of criteria, highest potential impact).
- **Refinement focus** — which aspects of the chosen idea to enhance.

If the user clearly just wants ideas fast, infer reasonable criteria and proceed,
stating the assumptions.

## 2. Execute the method

1. **Define task scope** — interpret the core objective.
2. **Generate initial ideas** — create the requested number of *genuinely
   distinct* ideas. Avoid variations on a single theme.
3. **Comparative analysis** — evaluate every idea against *all* criteria. Use a
   table or clear side-by-side analysis.
4. **Select the strongest option** — choose one based on the selection basis, and
   explain *why* it beats the others against the criteria.
5. **Refine the selected idea** — significantly enhance it, focused on the
   refinement aspects: add detail, concrete enhancements, and implementation notes.

## 3. Output structure

Respond in markdown with these `##` sections:

1. **Initial Ideas** — the distinct options.
2. **Comparison Analysis** — each idea scored against the criteria (table or bullets).
3. **Selected Idea & Rationale** — the choice plus a clear, criteria-grounded justification.
4. **Refined Idea** — the enhanced version incorporating the refinement focus.

## Quality bar (aim for excellence)

- Every part directly addresses the task.
- Initial ideas are genuinely different from each other.
- The comparison covers all ideas against all criteria.
- The selection rationale is logical and consistent with the analysis.
- The refinement shows meaningful improvement, not cosmetic changes.
- Output is clear, well-structured, and easy to scan.
