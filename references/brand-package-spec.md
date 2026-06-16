# Brand Package & Registry Spec

This is the persistence layer. A brand is not ephemeral chat output — it is a **structured,
versioned, queryable package** on disk, indexed by a **registry**. Think `package.json` +
`node_modules`, for a brand.

Every skill reads the package *first* and writes its output *into* the package, so a brand
accumulates coherently across sessions instead of being regenerated from scratch each time.

---

## 1. The brand package

A brand lives in one folder:

```
<brand>/                 # ./brand/ (in-situ) · brands/<slug>/ (portfolio) · <product>/brand/ (in a product repo)
  brand.yaml             # ← manifest: the queryable HEAD (name, one-liner, status, paths)
  context.md             # brand DNA — identity, audience, positioning, values, voice (was .agents/brand-context.md)
  naming.md              # naming rationale + finalists + chosen name
  strategy.md
  architecture.md        # brand architecture (standalone / sub-brand / branded-house / house-of-brands)
  identity.md            # visual identity brief
  voice.md
  messaging.md
  positioning.md
  story.md
  guidelines.md          # the brand book
  audit.md
  assets/                # logo, palette, type, exports
```

Skills create only the files they produce; the package grows over time. `brand.yaml` is always present.

### `brand.yaml` schema

```yaml
schema_version: 1
slug: cofoundy                 # kebab-case id (unique in a registry)
name: Cofoundy                 # display name
one_liner: One sentence on what it is.   # the recall headline
tagline: ""                    # market-facing line (optional until messaging runs)
archetype: ""                  # primary brand archetype (optional until strategy runs)
status: draft                  # draft | active | archived
stage: ""                      # pre-launch | early | growth | established
industry: ""
languages: [en]                # e.g. [es, en] for LATAM brands
links:
  domain: ""
  repo: ""
created: 2026-06-16            # YYYY-MM-DD (pass in; scripts never read the clock)
updated: 2026-06-16
version: 1
artifacts:                     # which package files exist (skills update this as they write)
  context: false
  naming: false
  strategy: false
  architecture: false
  identity: false
  voice: false
  messaging: false
  positioning: false
  story: false
  guidelines: false
  audit: false
```

---

## 2. The registry (the portfolio brain)

When you manage more than one brand, a registry indexes them so any agent can answer
"what brands exist / where do they live / what's the one-liner" without opening each package.

`brands/registry.yaml`:

```yaml
schema_version: 1
brands:
  - slug: cofoundy
    name: Cofoundy
    one_liner: One sentence on what it is.
    path: brands/cofoundy        # relative to the registry file
    status: active
    created: 2026-06-16
```

**The registry is a SSOT file, NOT agent memory.** Locations + one-liners are *data*: they belong in
this file (git-tracked, shareable across machines and teammates), never in an LLM's per-machine
auto-memory. A file is more "brain" than memory: durable, queryable, diffable.

---

## 3. Discovery contract (how every skill finds the brand)

Before doing any work, a skill loads the brand package:

1. Look for `brand.yaml` in: `./`, then `./brand/`, then `brands/<slug>/` (if a slug is known/asked).
2. Found → read `brand.yaml` (+ `context.md` and any sibling `*.md` relevant to the task). Use it; do
   not re-ask for what's already captured.
3. Not found → this is a new brand. Run `brand-init` (or `brand-context`) to create the package first.
4. Legacy fallback: a bare `.agents/brand-context.md` from older runs — read it, and offer to migrate
   it into a package via `brand-init`.

After producing output, a skill writes its file into the package and flips the matching
`artifacts.<x>: true` flag in `brand.yaml` (and refreshes `updated`).

---

## 4. Tooling

`skills/brand-init/scripts/brand.sh` is dependency-free (pure bash, no YAML lib):

```bash
brand.sh init  --name "Cofoundy" [--slug cofoundy] [--one-liner "…"] [--out DIR] [--date YYYY-MM-DD] [--register brands/registry.yaml]
brand.sh list  [--registry brands/registry.yaml]      # slug · name · one-liner · path · status
brand.sh set   --package DIR --key one_liner --value "…"   # update a brand.yaml scalar
```

`init` scaffolds the package + `brand.yaml` + `assets/` and (optionally) upserts the registry.
Scripts never read the system clock — pass `--date` (keeps runs deterministic/reproducible).
