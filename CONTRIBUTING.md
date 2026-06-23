# Contributing to Brand Skills

Brand Skills (`cofoundy/brand-skills`) is an open brand-genesis suite. Contributions — new skills,
better frameworks, more languages — are welcome.

## Ground rules

1. **Public-only dependencies.** Every skill must run for anyone with just an LLM key. Never add a
   dependency on a private API key, paid service credential, or proprietary infrastructure. Such
   integrations belong in a downstream private layer, not here.
2. **Brand genesis, not GTM.** v0 scope is creating a brand (naming → identity → voice → brand
   book). Go-to-market skills (ads, channels, growth) are out of scope for now — open an issue to
   discuss before adding.
3. **Skill shape.** Each skill is `skills/<name>/SKILL.md` with `name:` and `description:`
   frontmatter. Reference files live alongside it. Keep `SKILL.md` lean; push detail into
   references loaded on demand.
4. **Localization.** When adding examples, prefer covering both English and Spanish/LATAM. See
   `references/localization-es-latam.md`.
5. **Attribution.** If you adapt third-party MIT content, preserve its notice in `NOTICE`.

## Adding a language file

Language guides live in `skills/naming/languages/<code>.md` and are loaded on demand when a naming
brief targets that language. Use [`pl.md`](skills/naming/languages/pl.md) as the structural reference.

- **File name:** `<ISO 639-1 code>.md` (e.g. `de.md`, `ja.md`). Use a region code only when regional
  variation warrants separate files (e.g. `pt-PT.md` vs `pt-BR.md`).
- **Required sections:** phonosemantics, word formation, cultural conventions, anti-patterns, and
  cross-language pitfalls.
- **Register it:** add a row to the table in
  [`skills/naming/languages/INDEX.md`](skills/naming/languages/INDEX.md).

## Adding an industry file

Industry guides live in `skills/naming/industries/<industry>.md` and are loaded alongside the core
naming files (not instead of them).

- **File name:** lowercase, hyphenated industry slug (e.g. `fintech.md`, `health-tech.md`).
- **Required sections:** platform constraints, audience expectations, naming conventions, case
  studies, anti-patterns, and metaphor territories.
- **Register it:** add a row to the table in
  [`skills/naming/industries/INDEX.md`](skills/naming/industries/INDEX.md).

## Before opening a PR

```bash
bash scripts/validate-skills.sh
```

Add your skill to `.claude-plugin/marketplace.json` and the README skills table.
