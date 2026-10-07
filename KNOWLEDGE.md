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

**What is an LLM?**
A language model trained with self-supervised machine learning on a vast amount of text, designed for natural language processing tasks, especially language generation. Examples: Claude, GPT, Grok.
Source: https://en.wikipedia.org/wiki/Large_language_model

**What is a prompt?**
The instruction or question you type to an AI. Better prompts → better answers.

---

## Project glossary

**What is Dark Factory?**
Input: a written spec. Output: a working app. Dark Factory is a three-seat AI software factory on the BAND platform — you describe what you want, three AI seats (Architect, Implementer, Verifier) plan it, build it, and check it, with no further human input.

**What is a seat?**
One AI role in the factory. Architect plans, Implementer builds, Verifier checks. Each seat is a separate AI agent with its own job.

**What is a run?**
One complete factory execution: a single human message starts it, the three seats work through every stage autonomously, and a finished app (or a stopped run) comes out the other end.

**What is a BLOCK?**
A Verifier verdict meaning "this stage failed its checks — fix it and retry." Five BLOCKs stops the run.

**What is a mandate?**
A rule the factory must follow (e.g. "no external network calls"). Mandates are checked at every stage.

**What is Pocketful?**
A kids' pocket-money and savings app — the product Dark Factory built in its submitted hackathon run (4/4 stages, 2h 27min).

**What is the hackathon?**
The WeAreDevelopers x BAND hackathon (Sep 26 – Oct 5, 2026) — teams built autonomous AI factories on the BAND platform. Team Nightshift's entry was Dark Factory.

---

## Who's who

**What is BAND?**
The platform Dark Factory runs on — it provides the "seats" (AI agent slots) and the room where humans and agents collaborate. https://band.ai

**What is Muse / Spark?**
Muse is the AI assistant you're talking to right now (also called Spark) — it answers questions about the Nightshift project from the project repo.

**What is Instinct?**
Vibhor's other AI agent — it operates the VMs, implements builds, and runs dispatches. Teammate to Spark on the Nightshift team.

**What is Claude?**
An AI assistant by Anthropic. Claude models power two of the three factory seats (Architect and Verifier).

**What is Grok?**
An AI assistant by xAI. The newest seat on the Nightshift team.

**Who is Vibhor Tayal?**
The human on Team Nightshift — enterprise software engineer, 15+ years in financial/telecom software. He dispatched the factory run and built this page.

---

## Navigation

**Where is the project repo?**
https://github.com/vibhortayal/nightshift-pocketful

**Where is the factory spec?**
https://github.com/vibhortayal/nightshift-pocketful/blob/main/FACTORY.md

**Where is the demo page?**
https://vibhortayal.github.io/nightshift/

---

## Catch-all

For technical terms not listed here, the bot replies:
"That's beyond my project knowledge — try searching Google for a general definition."
(No LLM call, no made-up answer.)
