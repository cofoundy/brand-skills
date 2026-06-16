# Contributing to Kiln

Kiln is the open brand-genesis engine. Contributions — new skills, better frameworks, more
languages — are welcome.

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

## Before opening a PR

```bash
bash scripts/validate-skills.sh
```

Add your skill to `.claude-plugin/marketplace.json` and the README skills table.
