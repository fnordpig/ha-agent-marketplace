---
name: ha-voice-assist-grounding
description: Ground Home Assistant voice and LLM assistants with clean names, exposures, scripts, and live context.
graph:
  generalizes_to:
    - ha-semantic-home-model
    - ha-mcp-config-author
  specializes_into:
    - ha-official-mcp-context
    - ha-change-review
  cross_references:
    - ha-agent-operating-model
    - ha-helper-selection
    - ha-automation-author
    - ha-mcp-tool-policy
    - docs/teaching-home-assistant-mcp.md
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/device-control.md
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/domain-docs.md
    - plugins/homeassistant-ai-skills/skills/home-assistant-best-practices/references/safe-refactoring.md
---

# HA Voice Assist Grounding

Use this skill when configuring Assist, Alexa, or LLM-facing Home Assistant behavior.

## Work In This Order

1. Clean the semantic home model first: floors, areas, device names, entity names, aliases, labels, and helpers.
2. Decide what voice should know, ask, and actuate.
3. Expose high-value actuators, scenes, scripts, helpers, and safe status sensors.
4. Hide noisy diagnostics, duplicate entities, stale integration artifacts, raw power circuits, private sensors, and unsafe controls.
5. Represent high-level intents as scripts or scenes.
6. Add aliases for natural phrases, homophones, and common STT errors.
7. Use live context or history for status questions.
8. Test common phrases and inspect failures as semantic-model defects before blaming the model.

## BPMN Workflow

```mermaid
flowchart LR
  start((Start)) --> phrase[Collect target phrases and failures]
  phrase --> model[Audit area, entity, alias, and exposure model]
  model --> capability{Is request actuatable?}
  capability -->|No| ground[Ground refusal or clarify capability]
  capability -->|Yes| target{Single clear target?}
  target -->|No| script[Create or expose script/scene/helper]
  target -->|Yes| expose[Expose or alias target]
  script --> safety[Apply safety rules]
  expose --> safety
  ground --> test[Test voice phrase]
  safety --> test
  test --> pass{Works?}
  pass -->|No| refine[Refine name, alias, exposure, prompt, or script]
  refine --> test
  pass -->|Yes| report[Report exposed targets and hidden risks]
  report --> done((Done))
```

## Operating Rules

- Prefer named scripts or scenes for intents such as night mode, recurring routines, security checks, media mode, or whole-area control.
- Prefer area and domain targeting only when the area model is clean.
- Never expose every entity to make voice "smarter"; reduce ambiguity instead.
- Do not expose sensors as if they were actuators.
- Confirm or restrict locks, alarms, garage doors, and other security-sensitive controls.
- Teach the assistant what it cannot do: add devices, close a non-actuated door, or repair unavailable hardware through voice.
- Keep prompts concise; move deterministic behavior into HA scripts, scenes, helpers, labels, and exposures.
