# SPDX-License-Identifier: MIT
# -*- coding: utf-8 -*-
"""
Not a Culture Fit — absurd AI interviewer (Windows-friendly, Ollama-powered)

Quick start (dev):
  1) Install Python 3.10+ on Windows
  2) pip install requests
  3) Install Ollama and pull a model (e.g. `ollama pull llama3`)
  4) Run: python src/not_a_culture_fit.py

Build .exe (one-file):
  py -m pip install --upgrade pip
  py -m pip install requests pyinstaller
  py -m PyInstaller --onefile --name NotACultureFit src/not_a_culture_fit.py
  → dist/NotACultureFit.exe (double-clickable)

Environment overrides (optional):
  OLLAMA_URL  (default: http://localhost:11434)
  NACF_MODEL  (default: llama3)

This app asks 10 ridiculous interview questions, critiques your answers in an
"unhinged corporate" voice, rejects you with flair, and offers to restart.
"""
from __future__ import annotations
import os
import random
import textwrap
import time
from typing import List, Dict, Any

import requests  # pip install requests

# --------------- Configuration ---------------
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434").rstrip("/")
MODEL_NAME = os.environ.get("NACF_MODEL", "llama3")  # e.g., llama3, llama3.1, mistral, etc.
NUM_QUESTIONS_PER_INTERVIEW = 10

# --------------- Data: Names, Companies, Questions, Reasons ---------------
ADJECTIVES = [
    "Synergistic", "Quantum", "Elastic", "Ethical", "Aggressively", "Holistic",
    "Frictionless", "Disruptive", "Blockchain", "Serverless", "Omnichannel",
    "Ranch-Flavored", "Ambient", "Subprime", "Eco-Competitive", "Hypermobile",
    "Bleeding-Edge", "Ceremonial", "Chaotic Good", "Militarized", "Plausible"
]
NOUNS = [
    "Compliance", "Insights", "Dynamics", "Optimizations", "Enablement",
    "Monetization", "Parabolas", "Incentives", "Liquidity", "Pipelines",
    "Onboarding", "KPIs", "Clickthroughs", "Entanglement", "Arbitrage",
    "Synergies", "Wrangling", "Migrations", "Intelligence", "Silos"
]
SUFFIXES = [
    "LLC", "& Sons", "Group", "Ltd.", "PLC", "AG", "S.A.", "LLP",
    "Holdings", "Worldwide", "International", "Global", "Capital"
]

MANAGER_FIRST = [
    "Gristle", "Nebula", "Chadwick", "Velvet", "Cabbage", "Stark", "Peony",
    "Vortex", "Crispin", "Zamboni", "Tarragon", "Gloria-7", "Kevlar",
    "Juniper", "Tungsten", "Paprika", "Mirth", "Drizzle", "Quantum", "Burlap"
]
MANAGER_LAST = [
    "Mcdagger", "FOMO", "Von Spreadsheet", "Gallowglass", "Afterparty",
    "Hardskill", "Dumpster", "Blunderbuss", "KPIson", "Debtforge",
    "Coldbrew", "Synergywolf", "Carbonara", "Quarterclose", "Powerpoint",
    "Benchmarker", "BrassTax", "Hedgefund", "Moonshot", "Stakeholder"
]

REJECTION_REASONS = [
    "We chose a candidate with more hands-on experience in interpretive dance-based standups.",
    "Your vibe didn’t align with our brand of cheerful despair.",
    "We needed someone who can forklift their own emotional baggage — with certification.",
    "Our algorithm confused your answer with a pizza coupon and auto-rejected it.",
    "You scored highly, but our culture fit requires a deep love of meetings without chairs.",
    "We pivoted to hiring a raccoon we found behind the office dumpster (series A mascot).",
    "Finance says your ROI on birthday cake consumption was negative YoY.",
    "We’re pursuing candidates who are fluent in both Kubernetes and Gregorian chant.",
    "Legal advised us to hire someone we can’t legally describe.",
    "We need a visionary who’s comfortable failing upward at scale.",
    "Our hiring freeze thawed, then refroze, then asked for PTO.",
    "You didn’t mention synergy enough; we require at least 12 synergies per response.",
    "Your answers were too correct for our experimental chaos environment.",
    "The role has been replaced by a spreadsheet with a knife.",
    "We require 8+ years experience in a framework announced yesterday.",
    "Our team voted and the snack bar lobbied against you.",
    "Astral HR determined your aura clashes with our brand palette.",
    "We promoted the role to Principal Intern and there can only be one.",
    "We’re optimizing for people who clap when planes land.",
    "We ran out of lanyards; please reapply after Q4 restock."
]

QUESTION_BANK: List[str] = [
    "How would you explain the internet to a medieval blacksmith using only bread metaphors?",
    "Estimate how many pigeons it would take to move a Honda Civic one meter and justify the math.",
    "Describe a time you had to refactor your personality for Q3.",
    "If our roadmap were a casserole, what ingredient are you removing and why?",
    "Design a scrum ceremony for procrastination and outline the deliverables.",
    "Teach me Kubernetes using three spoons and a haunting memory.",
    "Our core value is ‘respectfully unhinged.’ Tell me about a time you were both.",
    "How many tabs should a high performer have open, minimum?",
    "You have 30 seconds to unionize a swarm of bees. Go.",
    "Pitch a new metric that will ruin morale but look great on slides.",
    "What’s your favorite exception to swallow silently and why?",
    "Write a brief postmortem for a meeting that never happened.",
    "What shade of beige best represents enterprise alignment?",
    "Draft an apology to a printer you’ve wronged.",
    "Explain CAP theorem to my dog who only understands vibes.",
    "If you were a microservice, which one would constantly restart and why?",
    "Tell me about a time you scaled empathy horizontally.",
    "How would you migrate our feelings to the cloud?",
    "Create an OKR for taking shorter walks to the fridge.",
    "How do you handle feedback delivered exclusively via vibes and tambourine?",
    "Invent a governance policy for office succulents.",
    "Why are we still using JIRA? Give three spiritual reasons.",
    "Design a dark pattern that convinces me to hydrate.",
    "What is the ethical number of monitors? Defend your position.",
    "How would you deprecate lunch?",
    "Choose: tabs, spaces, or fire. Explain.",
    "Write a migration plan from hope to resignation with zero downtime.",
    "Tell me about a time you Tetris’d a budget into existence.",
    "Draft an RFC for replacing chairs with large exercise balls.",
    "How would you normalize chaos in third normal form?",
    "Convince me that the coffee is fine (it isn’t).",
    "If the build breaks in the forest and no one hears it, who’s on call?",
    "Design a feature no one asked for but everyone will be forced to use.",
    "How many microservices is too many? Use only farm animals in your proof.",
    "Pitch a startup that sells silence as a subscription.",
    "Tell me about conflict you escalated to the moon for brand reasons.",
    "Estimate our NPS among ghosts.",
    "Write a 2-sentence SLA for hugs.",
    "What’s the minimum viable ritual to summon a deploy that works?",
    "Refactor this sentence: ‘We value family’ into something concerning.",
    "Describe your personal caching strategy for grudges.",
    "How would you shard the concept of trust?",
    "Name a hill you refused to die on and why it was the parking lot.",
    "Design a captcha humans consistently fail but bots love.",
    "Tell me a secret about Excel that scares you.",
    "Draft a zero-trust architecture for snacks.",
    "What makes a meeting truly mandatory in your heart?",
    "How would you handle a teammate who only communicates via forwardable emails?",
    "Define ‘senior’ without using the words ‘tired’ or ‘seen things.’",
    "Write release notes for a nap.",
    "Explain your approach to load balancing friendships at work.",
    "What KPI would you use to measure joy?",
    "Create a risk register for office birthdays.",
    "How many story points is an existential crisis?",
    "Walk me through your incident response for vibes being off.",
    "Suggest a reorg that increases morale for exactly 11 minutes.",
    "When should we pivot to selling hoodies?",
    "Design a security policy for the office microwave.",
    "Write a 1-line regex that ruins your week.",
    "How would you compress a scream to fit in a status update?",
    "Draft a memo convincing us to adopt tabs ironically.",
    "What is your philosophy on staplers?",
    "Build a decision tree for bringing up The Cloud.",
    "Tell me about a time your calendar became sentient.",
    "Propose a feature that adds value by removing joy.",
    "What is the acceptable RTO (Return To Office) for a soul?",
    "How do you sunset a coworker’s novelty mug collection?",
    "Compare our roadmap to a haunted carnival ride.",
    "Write a performance review for caffeine.",
    "How would you monetize eye contact?",
    "Create an escalation path for printer jams that ends in therapy.",
    "What’s your personal SLA for replying to ‘quick question’?",
    "Describe a migration from Slack to interpretive dance.",
    "Explain monorepos to a raccoon with a MBA.",
    "How do you ensure backwards compatibility with past mistakes?",
    "Propose a feature flag for hope.",
    "What is the ethical way to A/B test birthdays?",
    "Draft a 3-point plan to de-bureaucratize bureaucracy.",
    "How many meetings until we call it a festival?",
    "What’s your disaster recovery plan for weekends?",
    "Write a PR description for changing nothing but sounding brave.",
    "Design an org chart inspired by spaghetti.",
    "Map our tech stack to kitchen appliances and identify the cursed blender.",
    "When is it okay to paginate an apology?",
    "Explain observability using soap operas.",
    "What is your policy on feral requirements?",
    "Draft a compliance checklist for vibes-based hiring.",
    "How would you improve our latency to joy?",
    "Write a migration guide from optimism to realism.",
    "What should our 404 page apologize for?",
    "Estimate the blast radius of a spicy Slack emoji.",
    "Invent a new agile ceremony called ‘Feelings Triage.’",
    "How do you version-control promises?",
    "When does a backlog become folklore?",
    "Give a blameless postmortem for a snack theft you committed.",
    "What’s the SSO (Single Snack Onboarding) process?",
    "How would you sandbox an executive idea safely?",
    "Write a Helm chart for regret.",
    "Explain your approach to debugging people.",
    "Propose a dress code for Zoom squares.",
    "What is our core competency if not emails?",
    "Create a performance rubric for vibes.",
    "If budgets were seasons, which one just ghosted us?",
    "What’s your policy on saving face vs. saving the repo?",
    "How would you hotfix a friendship?",
    "What’s the minimum number of dashboards to feel alive?",
    "Write a termination email for a sticky note."
]

# Ensure we truly have 100 questions (pad if needed)
if len(QUESTION_BANK) < 100:
    base = "Give an unreasonably detailed answer to: why meetings breed more meetings?"
    needed = 100 - len(QUESTION_BANK)
    QUESTION_BANK.extend([f"{base} (variant {i+1})" for i in range(needed)])

# --------------- Helpers ---------------
def gen_company_name() -> str:
    import random
    adj = random.choice(ADJECTIVES)
    noun = random.choice(NOUNS)
    suf = random.choice(SUFFIXES)
    forms = [
        f"{adj} {noun} {suf}",
        f"{adj} {noun} & Associates",
        f"{noun} of {adj} {suf}",
        f"{adj}-{noun} {suf}",
    ]
    return random.choice(forms)


def gen_manager_name() -> str:
    import random
    return f"{random.choice(MANAGER_FIRST)} {random.choice(MANAGER_LAST)}"


def build_critique_prompt(company: str, manager: str, question: str, answer: str) -> str:
    persona = f"""
You are {manager}, the unapologetically chaotic Hiring Manager at {company}.
Your style is razor-witty, corporate-feral, and a little unhinged, but not hateful or discriminatory.
Speak like a jaded executive life coach who lives inside a slide deck.
Keep responses SHORT: 1–3 punchy sentences max. Address the candidate directly.
""".strip()
    task = f"""
QUESTION: {question}
CANDIDATE_ANSWER: {answer}
TASK: Deliver a bespoke critique of the candidate's answer in the context of the question.
- Be funny, specific, and cutting, like performance feedback written on a sticky note at 2am.
- Avoid slurs or anything targeting protected classes.
- No markdown, no lists, just prose (1–3 sentences).
""".strip()
    return persona + "\n\n" + task


def ollama_generate(prompt: str, *, model: str = MODEL_NAME, url: str = OLLAMA_URL, options: Dict[str, Any] | None = None) -> str:
    import requests
    endpoint = f"{url}/api/generate"
    payload: Dict[str, Any] = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }
    if options is None:
        options = {"temperature": 0.9, "top_p": 0.95, "repeat_penalty": 1.1, "num_predict": 160}
    payload["options"] = options
    resp = requests.post(endpoint, json=payload, timeout=120)
    resp.raise_for_status()
    data = resp.json()
    return (data.get("response") or "").strip()


def pick_questions(n: int) -> List[str]:
    import random
    return random.sample(QUESTION_BANK, n)


def banner():
    print("=" * 68)
    print(" Not a Culture Fit — tiny AI interviewer (Ollama) ")
    print("=" * 68)


def interview_once():
    company = gen_company_name()
    manager = gen_manager_name()
    print()
    print(
        textwrap.fill(
            f"Thank you for your time today. You’re being considered for a position at {company}. "
            f"I’m the Hiring Manager, {manager}.", width=80
        )
    )
    print()

    questions = pick_questions(NUM_QUESTIONS_PER_INTERVIEW)
    for idx, q in enumerate(questions, start=1):
        print(f"Q{idx}: {q}")
        try:
            ans = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n[Session ended]")
            return
        if not ans:
            ans = "[Candidate stares into middle distance]"

        prompt = build_critique_prompt(company, manager, q, ans)
        try:
            critique = ollama_generate(prompt)
        except Exception as e:
            critique = f"[Ollama error: {e}]"
        if not critique:
            critique = "I’ve seen stronger convictions in a lukewarm decaf. Next."
        print(f"\n{manager}: {critique}\n")
        time.sleep(0.2)

    print("-" * 68)
    print("Decision:")
    print(random.choice(REJECTION_REASONS))
    print("-" * 68)


def main():
    import random
    random.seed()
    banner()
    while True:
        interview_once()
        try:
            again = input("Interview again? (Y/N): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            return
        if again not in {"y", "yes"}:
            print("Understood. We’ll circle back never. Have a compliant day.")
            return
        print("\nRebooting the hiring machine…\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("[!] Unexpected error:", e)
        raise
