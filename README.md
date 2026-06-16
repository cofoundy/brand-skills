<div align="center">

# 🔥 Kiln

**The open brand-genesis engine — naming → identity → voice → brand book, from Claude Code.**

A from-zero brand creation suite for AI-native founders, agencies, and devs. Describe your
product; Kiln names it, decides its architecture, defines its identity and voice, briefs the
logo, and codifies a brand book — as Agent Skills that work in Claude Code, Cursor, Windsurf,
and any agent that supports the [Agent Skills spec](https://agentskills.io).

`npx skills add cofoundy/kiln`

[![License: MIT](https://img.shields.io/badge/License-MIT-black.svg)](./LICENSE)

</div>

---

## Why Kiln

A name is the first irreversible decision a startup makes — and most AI naming output is slop
(thesaurus mashups, `-ify` suffixes, dead metaphors). Kiln is **metaphor-driven**: it finds the
compressed story first, then the name. Then it carries that story through the entire identity —
architecture, voice, messaging, positioning, and a brand book — so the brand is coherent end to
end, not a logo glued to a tagline.

Built by [Cofoundy](https://cofoundy.dev). We use it to birth our own products; it's open so you
can birth yours.

## Install

```bash
# Any agent that supports the Agent Skills spec
npx skills add cofoundy/kiln

# Or as a Claude Code plugin marketplace
/plugin marketplace add cofoundy/kiln
```

## The pipeline

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
| **naming** | Metaphor-driven naming. 30–50 candidates → filtered → availability-checked → vetted finalists. Avoids AI slop. |
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

> **Scope:** Kiln v0 is brand *genesis* — it does not do go-to-market (ads, channels, growth).
> That's intentional; a brand should exist before it's marketed.

## Localization

Kiln ships first-class **Spanish / LATAM** support — Spanish phonosemantics, cultural-connotation
screening, and regional conventions — alongside English. See
[`references/localization-es-latam.md`](./references/localization-es-latam.md).

## Credits

Kiln stands on two excellent MIT-licensed projects, absorbed and extended here. See
[`NOTICE`](./NOTICE):

- Naming engine adapted from [**glacierphonk/naming**](https://github.com/glacierphonk/naming).
- Brand-genesis skills adapted from [**arnabbagxd/Brand-building-skills**](https://github.com/arnabbagxd/Brand-building-skills).

## License

[MIT](./LICENSE) © Cofoundy SAC. Upstream copyrights preserved in [`NOTICE`](./NOTICE).
