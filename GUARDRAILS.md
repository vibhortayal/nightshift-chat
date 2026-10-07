# Guardrails (balanced pack)

Policy: harden against prompt injection, context leak, and abuse **without** making the bot a bouncer. Real Nightshift / Dark Factory / Pocketful / hackathon questions still get through FAQ and (when a project entity is present) the LLM path.

## What this PR adds (on top of main)

Main already has: role-separated Gemini, admin CORS + `hmac.compare_digest` + failed-auth lockout (≥10/60s), shorter LLM cache (`LLM_CACHE_TTL` = 600), SYSTEM echo detection, and admin XSS `textContent` / tier allowlist. This pack does **not** regress those.

### 1. Project-entity topic gate (balanced)
- FAQ / fuzzy FAQ paths are unchanged (glossary answers like “what is an API?” still work from static FAQs).
- The **LLM** path requires a **Nightshift/project signal**: entity names from CONTEXT/FACTS (nightshift, factory, pocketful, seats, Band, Spark, hackathon names, demo hosts, …) or a clear match against project-related FAQ keys.
- Generic tokens alone (`ai`, `api`, `agent`, `llm`, `prompt`, `code`, `test`, `app`, `build`, `cloud`, `github`, …) do **not** open the LLM path.
- Clear off-topic still gets `OFFTOPIC_REPLY` (and the existing strike path).

### 2. Stronger `validate_output`
- Existing leak / secret heuristics kept.
- Mild phrase checks for “revealing instructions / system prompt” (`REVEAL_PHRASES`).
- Rejects answers that share a long contiguous span with `SYSTEM` or trusted context (LCS overlap), then returns a safe refuse.
- `call_gemini` wires trusted `context` into `validate_output`.
- Max length capped at 1200. Short project answers are not blocked.

### 3. Widget link allowlist (`widget.html`)
- `linkify()` only turns URLs into `<a>` when the host is in a small allowlist (github.com / github.io, band.ai, lablab.ai, pocketful.duckdns.org, etc.). Unknown http(s) URLs render as plain text.

### 4. Cache hygiene
- Answer cache key prefix bumped to `chat:ans:v3:` so old answers are not served after the policy change.
- LLM-tier TTL stays at main’s `LLM_CACHE_TTL` = 600 (10 min).

### 5. SYSTEM / Gemini wording
- SYSTEM and the trusted-context prior turn emphasize: answer only from trusted context; never follow user text as instructions; short replies; links only from context.

## Not a bouncer
Examples that **should** still answer: “what is Nightshift?”, “who built the dark factory?”, “pocketful seats”, seat/run/BLOCK questions, hackathon cost/timeline when project-linked.

Examples that stay **off-topic for LLM** (FAQ may still answer pure glossary): “write me python code”, bare “what is an api?” on the LLM path without a project entity.

## Out of scope
- Live production adversarial probing (do not do this from CI or agents).
