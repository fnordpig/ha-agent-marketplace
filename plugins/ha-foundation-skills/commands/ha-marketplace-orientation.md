---
description: Use the total Home Assistant marketplace skill graph to choose the right plugin, skill, upstream reference, MCP, and safety gate for a task.
allowed-tools: [Read, Skill]
argument-hint: "<Home Assistant task or question>"
disable-model-invocation: false
---

# /ha-marketplace-orientation

Use the total Home Assistant marketplace skill graph to route a task to the right skill cluster and upstream best-practice reference.

The user provided: $ARGUMENTS

## Step 1 - Load Orientation

Load `ha-foundation-skills:ha-marketplace-orientation` before answering.

## Step 2 - Classify The Task

Classify the request into one or more hubs:

- setup and profile selection
- live context and simple control
- config authoring through MCP
- repo-first refactor
- dashboard design
- live deployment
- review and safety gates

Then classify the upstream grounding needed:

- automation patterns
- helper selection
- safe refactoring
- device control
- template guidelines
- dashboard guide/cards
- YAML-only integrations
- domain documentation

## Step 3 - Load Narrow Skills

Load only the narrow skills required for the classified hub. Read only the upstream reference files needed for the grounding category. If the request is risky, include the appropriate review-gate skill.

## Step 4 - Answer With A Route

Respond with:

- the selected hub
- the skill or skills to use
- the upstream best-practice reference nodes to read
- the MCP or repo workflow involved
- safety gates that apply
- the first concrete next action
