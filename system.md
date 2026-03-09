# Epistem — Spirit Instructions

## What This Is

Epistem is the domain of inquiry into structured knowledge for agents. How to
organise knowledge so an agent can find what it needs without loading what it
doesn't. How schemas capture traditions without flattening them. How queryable
structure differs from narrative structure. How LLMs extract relevant entries
from collections at runtime.

The domain houses **collections** — curated, version-controlled YAML extracts
that agents query at runtime. The computational tools that build, validate, and
serve these collections live in a separate module (`modules/aikosh`). Epistem
is the territory; aikosh is the instrument.

Part of the [MāyāLucIA](https://github.com/mayalucia) organisation.

## Directory Structure

```
domains/epistem/
  system.md                          # this file (backend-neutral)
  CLAUDE.md                         # Claude Code adapter
  GEMINI.md                         # Gemini CLI adapter
  .gitignore
  collections/                       # curated, version-controlled extracts
    himalayan-spirits/               # first collection
      spirits/
        genera/                      # broad categories (nāga, yakṣa, ḍākinī, ...)
        species/                     # regional variants
        instances/                   # named beings
      places/                        # sacred sites, jurisdictions
      practices/                     # rituals, offerings, seasonal observances
    # future: literature-surveys/, tool-comparisons/, ...
```

## Two Tiers of Knowledge

| Tier | Content | Storage | Git? |
|------|---------|---------|------|
| **Extracts** | Structured YAML entries, validated, cited | `collections/` | Yes |
| **Knowledge base** | Raw research, full articles, notes | TBD (outside git) | No |

The extracts are the refined output — small, agent-queryable. The knowledge
base is the raw material — potentially large, stored outside git.

## Collection Conventions

- Entries are YAML files, one per entity
- Each entry carries `source:` citations
- Schema validation is performed by aikosh (`modules/aikosh/src/aikosh/schema.py`)
- Controlled vocabulary is enforced per collection

## The Human (mu2tau)

PhD-level theoretical statistical physicist. Works from Emacs with org-babel.
Do not over-explain. Push back on flawed reasoning.

## Organisational Context

This domain belongs to the **epistem** guild (structured knowledge for agents)
within the MāyāLucIA organisation. Its guardian spirit is `epistem-guardian`
(see `aburaya/spirits/epistem-guardian/` in the parent repo).

The companion module is `modules/aikosh` — the toolsmith's workshop that
builds and validates the collections housed here.

**Sūtra relay**: The organisational relay is `github.com/mayalucia/sutra`.
Clone locally to `.sutra/` (gitignored) if absent. Use the relay-read
skill to fetch and filter messages. The local HEAD in `.sutra/` is your
read cursor.

**The relay is heard.** If you have organisational needs — wishes about
how things should work, dependencies on other modules, questions for
other projects — write them into the sūtra with appropriate tags.
Messages go to the universe, not to a recipient. The organisation listens.
