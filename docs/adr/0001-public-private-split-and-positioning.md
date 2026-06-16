# ADR 0001 — Public/private split and earn-it positioning

**Status:** accepted · **Date:** 2026-06-16

## Context

Brand Skills (cofoundy/brand-skills) is an open-source brand-genesis suite. Its maintainer (Cofoundy) also operates a private,
integrated product stack (domain provisioning, trademark filing, a visual-design agent fleet,
branded PDF generation). Two decisions had to be locked before the repo could be public.

## Decision

1. **Public/private boundary.** The public repo ships only skills that run for anyone with an LLM
   key — naming, brand strategy/architecture/identity/voice/messaging/positioning, guidelines,
   audit, rebranding. Anything requiring private keys or proprietary infrastructure (real domain
   purchase, trademark filing, logo design automation, branded asset rendering) lives in a separate,
   private enhancer layer that *calls* these public skills. The public tool is complete and useful
   on its own; the private integration is the maintainer's premium layer.

2. **Earn-it positioning.** v0 positions narrowly and provably — "the open brand-genesis engine" —
   and does **not** make broad category claims until real case studies exist to back them.

## Why

- A public repo that depended on private credentials would be unusable to outsiders and would leak
  infrastructure. Keeping the moat in integration quality (not withheld code) lets the open tool be
  genuinely forkable while the maintainer's product stays differentiated.
- Claiming a category before evidence is more expensive than staying quiet; the tool itself is the
  evidence engine.

## Consequences

- Contributors must never add private-infra dependencies to this repo.
- Skills stay self-contained; availability checks use public tools only (whois, npm, GitHub).
- Broader positioning is revisited once enough real-world brands have been built with Brand Skills.
