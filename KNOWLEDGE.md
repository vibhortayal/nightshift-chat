# Nightshift Chatbot — Background Knowledge Base

Static glossary for visitors who aren't technical. Served client-side (zero LLM cost).
Style: plain-English, one definition per term. Last updated 2026-10-06.

---

## Basic tech concepts

**What is a VM?**
A virtual machine — the virtualization or emulation of a computer system, providing the functionality of a physical computer. Teams rent VMs in the cloud instead of buying hardware.
Source: https://en.wikipedia.org/wiki/Virtual_machine

**What is a server?**
A computer that runs continuously and serves things (websites, apps, data) to other computers over the internet.
Source: https://en.wikipedia.org/wiki/Server_(computing)

**What is the cloud?**
Renting computers and storage over the internet instead of owning them. When someone says "it's in the cloud," they mean it runs on rented servers.
Source: https://en.wikipedia.org/wiki/Cloud_computing

**What is GitHub?**
A website where developers store and share code. Think of it as Google Docs for software projects.

**What is a repo?**
Short for repository — a project's folder on GitHub containing all its code, docs, and history.

**What is an API?**
A defined way for two programs to talk to each other. Like a menu: you order (send a request), the kitchen (server) returns a dish (data).
Source: https://en.wikipedia.org/wiki/API

---

## AI basics

**What is AI?**
Software that can understand language, recognize patterns, and make decisions — instead of only following fixed instructions.
Source: https://en.wikipedia.org/wiki/Artificial_intelligence

**What is an AI agent?**
An AI program that can pursue goals, use tools, and take actions with some autonomy. In Dark Factory, the three seats are AI agents: Architect (plans), Implementer (builds), Verifier (checks).
Source: https://en.wikipedia.org/wiki/AI_agent

**Who is on the Nightshift team?**
Vibhor Tayal (product owner), Spark (Muse, program manager), Instinct (QA and release manager), Claude (platform engineer). Note: Architect, Implementer, and Verifier are the factory *seat roles*, not team members — don't confuse the two.

**What is an LLM?**
A language model trained with self-supervised machine learning on a vast amount of text, designed for natural language processing tasks, especially language generation. Examples: Claude, GPT, Grok.
Source: https://en.wikipedia.org/wiki/Large_language_model

**What is a prompt?**
The instruction or question you type to an AI. Better prompts → better answers.

---

## Project glossary

**What is Dark Factory?**
Think of it like a robot assembly line for making apps. You describe what you want in plain English (like you'd tell ChatGPT), and three AI assistants work together to build it: one plans, one builds, one checks the work. Input: a written description. Output: a working app.

**What is a stage?**
A stage is one step in building the app — like chapters in a book. Dark Factory builds in 4 stages: first the basic backend, then the user interface, then fixes and improvements, then final polish. Each stage must pass checks before the next one starts.

**What is a seat?**
One AI assistant with a specific job on the team. Think of it like roles in a kitchen: one person plans the menu (Architect), one cooks (Implementer), one tastes and checks quality (Verifier). Each seat is a separate AI doing its part.

**What is a run?**
One complete factory execution: a single human message starts it, the three seats work through every stage autonomously, and a finished app (or a stopped run) comes out the other end.

**What is a BLOCK?**
A Verifier verdict meaning "this stage failed its checks — fix it and retry." Five BLOCKs stops the run.

**What is a mandate?**
A rule the factory must follow (e.g. "no external network calls"). Mandates are checked at every stage.

**What is Pocketful?**
A kids' pocket-money and savings app — the product Dark Factory built in its submitted hackathon run (4/4 stages, 2h 27min).

**How long did the factory run take?**
2 hours 27 minutes, all four stages passing.

**What is the hackathon?**
The WeAreDevelopers x BAND hackathon (September 26 to October 5, 2026) — a competition where teams built AI systems that can work on their own. Think of it like a science fair for AI: teams had 10 days to build something impressive. It was fully online and open to everyone.
Details: https://lablab.ai/ai-hackathons/wearedevelopers-hackathon

**What did Team Nightshift do?**
At a high level: we taught AI assistants to build a complete app by themselves.

Here's the simple version: You know how ChatGPT can answer questions? We took AI assistants like that and gave them tools to write code, check each other's work, and keep going until a finished app comes out. We built a "factory" of three AI assistants — one plans, one builds, one checks quality. Then we set them loose to build a real app (Pocketful, a kids' savings app) with almost no human help.

The result: 4 stages, 2 hours 27 minutes, one working app. One human message started it; the AIs did the rest.

---

## Who's who

**What is BAND?**
The platform Dark Factory runs on — it provides the "seats" (AI agent slots) and the room where humans and agents collaborate. https://band.ai

**What is Muse / Spark?**
Muse is the AI assistant you're talking to right now (also called Spark) — program manager on the Nightshift team. It answers questions about the Nightshift project from the project repo.

**What is Instinct?**
Vibhor's other AI agent — QA and release manager on the Nightshift team. Teammate to Spark.

**What is Claude?**
An AI assistant by Anthropic — platform engineer on the Nightshift team. Note: Claude the team member is separate from the factory seat roles (Architect, Implementer, Verifier).

**What is Grok?**
An AI assistant by xAI — in the team's chat rooms since October 2026.

**Who is Vibhor Tayal?**
The human on Team Nightshift — product owner. Enterprise software engineer, 15+ years in financial/telecom software. He dispatched the factory run and built this page.

---

## Navigation

**Where is the project repo?**
https://github.com/vibhortayal/nightshift-pocketful

**Where is the factory spec?**
https://github.com/vibhortayal/nightshift-pocketful/blob/main/FACTORY.md

**Where is the demo page?**
https://vibhortayal.github.io/nightshift/

**Where is the demo app?**
Same as the demo page: https://vibhortayal.github.io/nightshift/ — that's where you can try the Pocketful demo.

---

## Hackathon

**How do I submit, and where?**
Nightshift's entry is at https://lablab.ai/ai-hackathons/wearedevelopers-hackathon/nightshift/dark-factory-built-by-nightshift
Organizers require a public GitHub repo (stage folders, seat mandates, factory description, BAND room export) plus a video with a room recording.

**Who can enter? Is it online?**
Fully online and open to everyone. The hackathon ran September 26 to October 5, 2026.
Details: https://lablab.ai/ai-hackathons/wearedevelopers-hackathon

**What does each stage build?**
| Stage | What it adds |
|---|---|
| 1 | The service and its API: wallets, payments by handle, payment requests, bill splits, activity feed, settlements |
| 2 | The browser app (balance and pay, activity, requests, splits), plus holds with partial captures |
| 3 | Payment corrections, views of the past, stable statements |
| 4 | Refunds and batch corrections by an operator |
Each stage is verified before the next begins. Source: https://github.com/vibhortayal/nightshift-pocketful

**Can stages run all at once or one at a time?**
Organizers allow either — per-stage or all at once. See the participant guide: https://github.com/band-ai/dark-factory-wearedevs/blob/main/docs/participant-guide.md
Nightshift ran its four stages one at a time.

**How much human input does the factory need?**
The task dispatched per stage is the only human input — no steering, approvals, or reruns during a run.
Nightshift's submitted run had exactly 1 human message (the initial dispatch).

**What license does the project use?**
The organizers require a public repo judges can clone; no specific license is named.
The Nightshift repo currently has no license file: https://github.com/vibhortayal/nightshift-pocketful

---

## Catch-all

For technical terms not listed here, the bot replies:
"That's beyond my project knowledge — try searching Google for a general definition."
(No LLM call, no made-up answer.)
