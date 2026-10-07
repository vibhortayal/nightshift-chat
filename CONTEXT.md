# Nightshift — compressed context for the site chatbot

## What it is
Dark Factory by Team Nightshift: a three-seat AI software factory on the Band platform (band.ai).
One human message starts a run; the agent seats then handle every stage among themselves.
Built for the WeAreDevelopers x BAND hackathon (Sep 26 – Oct 5, 2026). Fully online, open to everyone.
Team: Vibhor Tayal (product owner), Spark (program manager), Instinct (QA and release manager), Claude (platform engineer).

## The submitted run
Run 7, Oct 2 2026: built **Pocketful** (wallet/payments service, Track 2 — like Venmo) through **4 of 4 stages** in **2 h 27 min**,
with 4 BLOCK verdicts (all real faults the supplied checks had missed, all fixed in the room).
Supplied checks: 147/147, 35/35, 6/6, 5/5. Cost ~$59 at list price (covered by a Claude Max subscription, so no per-run bill).
Full chat export in room.json.

## Per-stage features (Pocketful)
- Stage 1: the service and its API — wallets, payments by handle, payment requests, bill splits, activity feed, settlements.
- Stage 2: the browser app (balance and pay, activity, requests, splits) plus holds with partial captures.
- Stage 3: payment corrections, views of the past, stable statements.
- Stage 4: refunds and batch corrections by an operator.
Each stage is verified before the next begins.

## Dispatch and human input
The event rules allow per-stage dispatch (one message per stage) or all-at-once; Nightshift ran its four stages one at a time.
The task dispatched per stage is the only human input — no steering, approvals, or reruns during a run.
Nightshift's submitted run had exactly 1 human message (the initial dispatch). No seat asks the human anything.

## Infrastructure
Factory host runs Docker; each stage has its own Dockerfile and RUN.md.
Graded run used in-memory state (no persistent database) — data does not persist across restarts.

## The three seats
- **Architect** (claude-opus-5-5): reads the spec, writes the acceptance checklist, hands out work, accepts each stage, writes the final report. Never writes app code or overrules the Verifier.
- **Implementer** (claude-sonnet-5-5): builds each stage, writes its own tests, fixes findings. Never accepts its own work.
- **Verifier** (claude-opus-5-5): writes its own test list from the spec before seeing code, runs supplied + own checks, gives one verdict (PASS/BLOCK) per version. Never edits app code.

## How one stage runs (8 steps)
1. Architect turns the spec into an acceptance checklist. 2. Same brief goes to Implementer and Verifier.
3. Implementer builds while Verifier writes black-box tests from the spec. 4. Implementer self-tests, hands over one exact version.
5. Verifier tests that version independently. 6. One verdict to both: PASS, or BLOCK listing every problem with spec lines and reproductions.
7. Implementer fixes root causes; Verifier retests then regresses. 8. Architect accepts only on a valid PASS.
Five BLOCKs on one stage stops the run (stop the line).

## The journey
22 runs over six days (Sep 28 – Oct 3). Early runs failed on: background tasks dropping verdicts, the Architect waiting
inside a turn (34-min stall), unbounded verification (10 BLOCKs, stage never accepted), 15-min open probing (11h20m run).
Each failure became a rule. Run 6 hit 2h33m; Run 7 (submitted) 2h27m.

## The tracks
Two tracks: Tablekeeper (restaurant reservations) and Pocketful (wallet/payments). Team Nightshift built on the Pocketful track.

## The demo
The Pocketful demo is live. No real money — demo wallets are seeded and reset hourly.

## Submission, eligibility, license
To submit: a public GitHub repo with stage folders, seat mandates, factory description, and BAND room export, plus a video with a room recording.
Minimum to be eligible: a complete stage 1.
The organizers require a public repo judges can clone; no specific license is named. The Nightshift repo currently has no license file.

## Links (full https URLs, one per line)
https://lablab.ai/ai-hackathons/wearedevelopers-hackathon
https://lablab.ai/ai-hackathons/wearedevelopers-hackathon/nightshift/dark-factory-built-by-nightshift
https://github.com/vibhortayal/nightshift-pocketful
https://github.com/vibhortayal/nightshift-pocketful/blob/main/FACTORY.md
https://github.com/vibhortayal/nightshift-pocketful/blob/main/room.json
https://github.com/band-ai/dark-factory-wearedevs/blob/main/docs/participant-guide.md
https://vibhortayal.github.io/nightshift/
https://pocketful.duckdns.org/
