# Brand Skills — Branding, Naming & Brand Identity for AI Agents

**Open-source [Agent Skills](https://agentskills.io) for brand building: brand strategy, brand
naming, brand identity, voice, positioning, messaging, brand guidelines, and rebranding — from
Claude Code, Cursor, Windsurf, or any agent.**

```bash
npx skills add cofoundy/brand-skills
```

[![License: MIT](https://img.shields.io/badge/License-MIT-black.svg)](./LICENSE)

> **Brand genesis, end to end.** Describe your product; these skills name it, decide its brand
> architecture, define its identity and voice, brief the logo, and produce a brand book — as
> composable skills your AI agent loads on demand.

---

## Why these brand skills

A startup's name is its first irreversible decision, and most AI naming output is slop — thesaurus
mashups, `-ify` suffixes, dead metaphors. The **naming** skill here is metaphor-driven: it finds the
compressed story first, then the name, then carries that story through the whole identity —
architecture, voice, messaging, positioning, and a brand book — so the brand is coherent end to end,
not a logo glued to a tagline.

Maintained by [Cofoundy](https://cofoundy.dev). We use these skills to build our own products; they're
open so you can build yours.

## Install

```bash
# Any agent that supports the Agent Skills spec
npx skills add cofoundy/brand-skills

# Or as a Claude Code plugin marketplace
/plugin marketplace add cofoundy/brand-skills
```

## The brand-genesis pipeline

```
        ┌─────────────┐
        │brand-context│  ← foundation. Every skill reads this first.
        └──────┬──────┘
               │
   naming ─→ brand-architecture ─→ brand-identity ─┐
   (metaphor   (standalone vs       (logo brief,    │
    engine)     sub-brand vs         palette, type) │
                house-of-brands)                    ▼
   brand-strategy · brand-positioning · target-audience · competitor-branding
                                                    │
   brand-voice · brand-messaging · brand-story ─────┤
                                                    ▼
                                          brand-guidelines  (the brand book)
                                          brand-audit · rebranding
```

## Skills

| Skill | What it does |
|-------|--------------|
| **naming** | Metaphor-driven brand & product naming. 30–50 candidates → filtered → prior-art + availability checked → vetted finalists. Avoids AI slop. |
| **brand-context** | Foundation. Captures the brand DNA every other skill reads first. |
| **brand-strategy** | Brand heart, archetype, values — the full strategy report. |
| **brand-architecture** | Standalone vs sub-brand vs branded-house vs house-of-brands. Naming systems for product families. |
| **brand-positioning** | Competitive map, positioning territory + statement, proof points. |
| **target-audience** | ICP, personas, psychographics, audience language. |
| **competitor-branding** | How competitors brand themselves → gaps + differentiation. |
| **brand-identity** | Visual identity brief — logo direction, color, type, imagery (to brief a designer). |
| **brand-voice** | Verbal identity — tone, voice qualities, vocabulary, writing rules. |
| **brand-messaging** | Messaging hierarchy — taglines, value prop, key messages. |
| **brand-story** | Origin story + founder narrative (long / short / one-liner). |
| **brand-guidelines** | The brand book — logo usage, color, type, voice, application rules. |
| **brand-audit** | Brand health across 6 dimensions. |
| **rebranding** | Audit → reposition → relaunch an existing brand. |

> **Scope:** v0 is brand *genesis* — creating a brand. It does not do go-to-market (ads, channels,
> growth). That's intentional; a brand should exist before it's marketed.

## Spanish / LATAM localization

First-class **Spanish / LATAM** support — Spanish phonosemantics, cultural-connotation screening
across major markets, and regional conventions — alongside English. See
[`references/localization-es-latam.md`](./references/localization-es-latam.md).

## Credits

Built on two excellent MIT-licensed projects, absorbed and extended here (see [`NOTICE`](./NOTICE)):

- Naming engine adapted from [**glacierphonk/naming**](https://github.com/glacierphonk/naming).
- Brand-genesis skills adapted from [**arnabbagxd/Brand-building-skills**](https://github.com/arnabbagxd/Brand-building-skills).

## License

[MIT](./LICENSE) © Cofoundy SAC. Upstream copyrights preserved in [`NOTICE`](./NOTICE).

---

<sub>Keywords: brand skills · branding · brand strategy · brand naming · brand identity · brand
voice · brand positioning · brand guidelines · rebranding · agent skills · Claude Code · AI
branding · brand book generator.</sub>
