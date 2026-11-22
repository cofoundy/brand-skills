---
name: brand
description: Use when the user wants to create, name, define, audit or rebrand a brand — naming, strategy, identity, voice, positioning, messaging, story, audience, competitors, brand book, or a branded Claude Code spinner.
metadata:
  version: 1.0.0
---

# Brand

The main entry point to Brand Skills. The 16 specialist skills are available on request through
this router or by explicit invocation.

## How to run a brand skill

Read `../<skill>/SKILL.md` (a sibling of this skill's directory) and follow it as if it had been
invoked. Resolve relative resources against that specialist's directory. In Claude Code,
${CLAUDE_SKILL_DIR} refers to that directory. In Codex, use the path of the installed skill.
When a specialist hands off to another by name ("run `brand-context`"), load the sibling the same
way. Users can also invoke a specialist directly through their agent's skill picker.

Start every brand with `brand-init` (no `brand.yaml` yet), then `brand-context`. Everything else reads
that package.

## Routing

| Need | Skill |
|------|-------|
| New brand, no `brand.yaml` yet | `brand-init` |
| Capture or update brand DNA | `brand-context` |
| Name a product, brand, app or bot | `naming` |
| Check whether an existing name is free (trademark, domains, handles) | `naming` in `validar` mode |
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
