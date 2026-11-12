# Validate an Existing Name — `validar <name> <industry> <country>`

Use this mode when the name **already exists** (the founder chose it, the company trades under it,
a client brought it) and the question is only: *can we keep it?* You do NOT generate candidates,
explore metaphors, or interview. You run the Step 5 availability gate on ONE name, add the
registry checks of the target country, and write a verdict with evidence.

Output: `validacion-nombre.md` (template at the end), written where the caller asks — never inside
someone else's product repo unless told to.

---

## Inputs

| Input | Required | Where it comes from |
| ----- | -------- | ------------------- |
| `name` | yes | The exact spelling as used in market (keep articles: "El X" is checked as "El X" AND "X") |
| `industry` | yes | Free text ("podcast / digital media platform"). You map it to Nice classes below |
| `country` | yes | ISO country or name. Drives registry, ccTLD and handle priorities |
| Brief doc | no | A product-intent doc (`INTENCION-PRODUCTO.md`, `brief.yaml`, a filled `templates/naming-brief.md`) — read it for platforms that matter and what the product does; do not ask what it already answers |

If the industry is too vague to pick Nice classes, pick the 2–4 most likely ones, say which you
picked and why, and continue. Never stop to ask.

---

## Procedure (run every row; a row you could not run is reported, not skipped)

### 1. Variants to test

Build the search set before searching:
- Exact name, with and without the article (`El Foo`, `Foo`), with and without spaces (`elfoo`).
- **Phonetic twins across languages.** A Spanish spelling of an English word (or vice versa) is a
  homonym to the ear even if the letters differ. Write the word it *sounds like* and test it too.
  Example: a Spanish-phonetic spelling of an English media word collides with the English brand.
- Plural/possessive forms registries often hold (`Foo's`, `Foos`).

### 2. Trademark registry of the country (the gate that matters most)

**Nice classes by industry** (pick the ones the business actually sells in):

| Industry | Classes to check |
| -------- | ---------------- |
| Podcast, streaming, digital media, publishing | 9 (downloadable media/apps), 38 (transmission/streaming), 41 (entertainment, production, publishing), 35 (advertising — media sells ads) |
| SaaS / software | 9, 42 (+35 if it sells marketing/business services) |
| E-commerce / retail | 35 + the class of the goods sold |
| Food & drink | 29, 30, 32, 43 (restaurants) |
| Fintech | 36, 9, 42 |
| Education | 41, 9 |
| Health / wellness | 44, 5, 10 |

**Peru — INDECOPI.**
1. Official free search: **BuscaTuMarca** — `https://enlinea.indecopi.gob.pe/buscatumarca/`
   (no login). Search the name and its variants, note results in the chosen classes.
   *Known limit:* its firewall can block automated/datacenter clients ("Web Page Blocked!" page or
   connection closed). If blocked, record it as **not verified** with the date and the error, and
   use the fallback.
2. Fallback: **WIPO Global Brand Database** — `https://branddb.wipo.int/en/similarname` — it
   carries INDECOPI data (`(PE) INDECOPI` in the IP office / designation filter). Steps:
   brand name → strategy *Embedded* for the exact term (and *Phonetic* for the twin) → Filters →
   IP office / designation **(PE)** → Nice classes from the table. Switch layout to *List* if
   rows seem missing (the default view virtualizes long lists). Record every row: mark, owner,
   class, status (registered / pending / expired), number.
3. The formal **búsqueda de antecedentes** (paid, per class, via INDECOPI's online services) is
   the legal answer. This mode does not replace it: say so in the report when the verdict will
   be used to commit money to the name.

**Other LatAm registries** (same method; WIPO GBD covers most of them as a fallback):

| Country | Registry | Public search |
| ------- | -------- | ------------- |
| Mexico | IMPI | MARCia — `https://marcia.impi.gob.mx/` |
| Colombia | SIC | `https://sipi.sic.gov.co/` |
| Chile | INAPI | `https://www.inapi.cl/` (búsqueda de marcas) |
| Argentina | INPI | `https://portaltramites.inpi.gob.ar/` |
| Brazil | INPI | `https://busca.inpi.gov.br/pePI/` |
| Other / unsure | — | WIPO GBD filtered by the office code |

These were not all exercised by this skill's authors; if one fails, report it as not verified.

**Reading results:**
- Same or confusingly similar mark, **registered or pending**, in a class the business uses → **tomado** (or **riesgo** if only similar, not identical).
- Same mark only in unrelated classes → note it; not a block.
- **Expired / ended** marks → not a block, but list them (someone used it; could refile).

### 3. Domains

```bash
TLDS="com <cctld> com.<cctld>" bash ${CLAUDE_SKILL_DIR}/scripts/check-availability.sh <name-no-spaces> domain
```
Peru: `TLDS="com pe com.pe"`. Test the variants without the article too (`foo.com`). A domain
that is taken: open it (`curl -sI`, or a browser) — parked/for sale vs a live business in the same
industry are very different findings.

*Known registry quirk:* NIC.pe's whois echoes `Domain Name:` back even for unregistered names and
puts the verdict in `Domain Status: No Object Found`. The script handles it; if you whois by hand,
read the status line.

### 4. Social handles (priority by industry and country)

For media and consumer brands in LatAm: Instagram, TikTok, YouTube, X, Facebook, Spotify/Apple
Podcasts (shows with the name). A plain HTTP status is NOT evidence for most networks — they
return 200 for everything or block bots. What actually worked when this mode was built:

| Network | Reliable probe | Unreliable |
| ------- | -------------- | ---------- |
| YouTube | `curl` → 404 on `youtube.com/@handle` = free | — |
| TikTok | Browser (agent-browser / Playwright): the profile page shows handle, followers, bio when taken | `curl` status (always 200) |
| Instagram | Browser while logged in | Logged-out browser shows "Profile isn't available" for both free and some existing profiles → **unclear** |
| X | Browser while logged in | `curl` and logged-out browser get 403/404 inconsistently → **unclear** |
| Telegram | `t.me/handle` page with a `tgme_page_title` element = taken | `og:title` is "Contact @handle" either way |
| Apple Podcasts | `podcasts.apple.com/<cc>/search?term=<name>` in a browser | — |

Report each handle as **libre / tomado (by whom, if visible) / no verificado (why)**.

### 5. Homonyms in the industry

- Web search: `"<name>"`, `"<name>" <industry>`, `"<name>" <country>`, and the phonetic twin + industry.
- Industry directories: podcast apps for media; app stores for apps; GitHub for dev tools.
- Search engines may serve a captcha to automated clients; record it and use another engine.
- A famous brand that is the **phonetic twin in another language** in the same industry is a
  finding even if it has no registration in the country: it costs search visibility and can draw
  an opposition if that owner registers locally.

---

## Verdict rules

| Verdict | When |
| ------- | ---- |
| **tomado** | Identical/confusing mark registered or pending in a class the business needs, OR a direct competitor already trades under it in the same country |
| **riesgo** | No blocking mark, but any of: similar mark in a needed class; a famous phonetic twin in the same industry; the main domain or the key handle is taken by a third party; the registry check could not be run (only the fallback) |
| **libre** | Registry checked (official or fallback) with no conflict in the needed classes, main domain(s) free or owned by the business, key handles free, no relevant homonym |

When the registry was checked only through a fallback, the best possible verdict is **riesgo** —
unless the caller accepts the fallback, which you note.

Every claim carries its URL (or command) and the date you checked it. Something you could not
verify goes in its own section, never silently into "libre".

---

## Template — `validacion-nombre.md`

```markdown
# Validación de nombre: <Nombre>

- Rubro: <rubro> · País: <país> · Clases Niza revisadas: <n, n, n> (por qué)
- Fecha de verificación: <YYYY-MM-DD>
- Brief usado: <ruta o "ninguno">

## Veredicto: <libre | riesgo | tomado>
<2–3 líneas: el porqué, con la evidencia que lo decide.>

## Evidencia por fuente
| Fuente | Qué se buscó | Resultado | URL / comando | Fecha |
| ------ | ------------ | --------- | ------------- | ----- |
| Registro de marcas (oficial) | ... | ... | ... | ... |
| Registro de marcas (respaldo WIPO GBD) | ... | ... | ... | ... |
| Dominio .com / ccTLD | ... | ... | ... | ... |
| Instagram / TikTok / YouTube / X / ... | ... | ... | ... | ... |
| Homónimos en el rubro | ... | ... | ... | ... |

## Marcas encontradas
<mark · owner · class · status · number, one per line; expired ones included>

## No verificado
<cada fuente que no se pudo abrir: qué se intentó, error literal, qué haría falta (login, navegador, pago)>

## Qué haría falta para pasar a "libre"
<p. ej. búsqueda de antecedentes oficial en clases X; comprar dominio; reclamar handle>
```
