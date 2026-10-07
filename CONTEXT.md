# Nightshift — compressed context for the site chatbot

## What it is
Dark Factory by Team Nightshift: a three-seat AI software factory on the Band platform (band.ai).
One human message starts a run; the agent seats then handle every stage among themselves with no further human input.
Built for the WeAreDevelopers x BAND hackathon (Sep 26 – Oct 5, 2026). Team: Vibhor Tayal (product owner), Spark (program manager), Instinct (QA and release manager), Claude (platform engineer).

## The submitted run
Run 7, Oct 2 2026: built **Pocketful** (a kids' savings/pocket-money app) through **4 of 4 stages** in **2 h 27 min**,
with 4 BLOCK verdicts (all real faults the supplied checks had missed, all fixed in the room).
Supplied checks: 147/147, 35/35, 6/6, 5/5. Cost ~$59 at list price (covered by a Claude Max subscription, so no per-run bill).
Full chat export in room.json; repo: github.com/vibhortayal/nightshift-pocketful.

## The three seats
- **Architect** (claude-opus-5-5): reads the spec, writes the acceptance checklist, hands out work, accepts each stage, writes the final report. Never writes app code or overrules the Verifier.
- **Implementer** (claude-sonnet-5-5): builds each stage, writes its own tests, fixes findings. Never accepts its own work.
- **Verifier** (claude-opus-5-5): writes its own test list from the spec before seeing code, runs supplied + own checks, gives one verdict (PASS/BLOCK) per version. Never edits app code.

## How one stage runs (8 steps)
1. Architect turns the spec into an acceptance checklist. 2. Same brief goes to Implementer and Verifier.
3. Implementer builds while Verifier writes black-box tests from the spec. 4. Implementer self-tests, hands over one exact version.
5. Verifier tests that version independently. 6. One verdict to both: PASS, or BLOCK listing every problem with spec lines and reproductions.
7. Implementer fixes root causes; Verifier retests then regresses. 8. Architect accepts only on a valid PASS.
Five BLOCKs on one stage stops the run (stop the line). No seat may ask the human anything.

## Key design rules (10 commandments, condensed)
Split plan/build/check across three seats; strongest model judges, faster model builds; no waiting inside a turn,
background tasks off; mandates describe how to work, never what to build (same files built Tablekeeper's 4 stages in 1h37m too);
Verifier writes checks from the spec before seeing code; every check tied to a spec sentence; one verdict with all problems,
stop after five BLOCKs; never re-send the spec in fix rounds; small modules; commit the evidence.

## The journey
22 runs over six days (Sep 28 – Oct 3). Early runs failed on: background tasks dropping verdicts, the Architect waiting
inside a turn (34-min stall), unbounded verification (10 BLOCKs, stage never accepted), 15-min open probing (11h20m run).
Each failure became a rule. Run 6 hit 2h33m; Run 7 (submitted) 2h27m.

## Pocketful (the app built)
Kids' pocket-money/savings app: four stages from the hackathon spec (band-ai/dark-factory-wearedevs pocketful track).
Built entirely by the three seats from the spec, verified stage by stage.

## Links
Submission: lablab.ai (WeAreDevelopers hackathon, Nightshift entry). Repo: github.com/vibhortayal/nightshift-pocketful.
Project page: vibhortayal.github.io/nightshift/
