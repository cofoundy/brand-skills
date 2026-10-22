---
name: brand
description: Use when the user wants to create, name, define, audit or rebrand a brand — naming, strategy, identity, voice, positioning, messaging, story, audience, competitors, brand book, or a branded Claude Code spinner.
metadata:
  version: 1.0.0
---

# Brand

The single entry point to Brand Skills. The other 16 skills are hidden from the agent's skill list
(`disable-model-invocation: true`) so they cost no context until needed; this skill routes to them.

## How to run a brand skill

Read `../<skill>/SKILL.md` (a sibling of this skill's directory) and follow it as if it had been
invoked. In that file, `${CLAUDE_SKILL_DIR}` means its own directory. When a skill hands off to
another by name ("run `brand-context`"), load that one the same way — never through the Skill tool.
The user can still call any of them directly as `/<skill>`.

Start every brand with `brand-init` (no `brand.yaml` yet), then `brand-context`. Everything else reads
that package.

## Routing

| Need | Skill |
|------|-------|
| New brand, no `brand.yaml` yet | `brand-init` |
| Capture or update brand DNA | `brand-context` |
| Name a product, brand, app or bot | `naming` |
| Full strategy report (heart, archetype, values) | `brand-strategy` |
| Standalone vs sub-brand vs house of brands | `brand-architecture` |
| Competitive map and positioning statement | `brand-positioning` |
| ICP, personas, audience language | `target-audience` |
| How competitors brand themselves | `competitor-branding` |
| Logo direction, color, type, imagery brief | `brand-identity` |
| Tone, voice, vocabulary, writing rules | `brand-voice` |
| Taglines, value prop, key messages | `brand-messaging` |
| Origin and founder story | `brand-story` |
| The brand book | `brand-guidelines` |
| Brand health check | `brand-audit` |
| Reposition and relaunch an existing brand | `rebranding` |
| The brand inside Claude Code (spinner) | `brand-mod` |

Several needs at once → run them in pipeline order: context → naming → architecture → identity →
strategy/positioning/audience/competitors → voice/messaging/story → guidelines.
