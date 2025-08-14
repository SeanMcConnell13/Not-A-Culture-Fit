# SPDX-License-Identifier: MIT
# -*- coding: utf-8 -*-
"""
Not a Culture Fit — Polished GUI (Tkinter) with Sprite — Ollama-powered

Run (dev):
  pip install -r requirements.txt
  python src/nacf_ui_polished.py

Notes:
- Uses Tkinter + ttk with a clean chat layout, left panel card with sprite.
- Color palette derives from the sprite (charcoal, forest, leather brown, light gray).
- No packaging yet; later we can add a PyInstaller spec that bundles assets.
"""
from __future__ import annotations
import os
import random
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox
import textwrap
from typing import List, Dict, Any

import requests  # pip install requests
from PIL import Image, ImageTk  # pip install Pillow

# ---------- Config ----------
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434").rstrip("/")
MODEL_NAME = os.environ.get("NACF_MODEL", "llama3")
NUM_QUESTIONS_PER_INTERVIEW = 10

# ---------- Palette (from sprite) ----------
CHARCOAL = "#2f3b4a"   # frame bars, headings
FOREST   = "#2f5f3a"   # accents (buttons focus/active)
LEATHER  = "#a06b2a"   # subtle secondary
CANVAS   = "#f5f7fa"   # app background
CARD_BG  = "#ffffff"   # panels
INK      = "#1e2329"   # text
MUTED    = "#6b7785"

# ---------- Data ----------
ADJECTIVES = [
    "Synergistic","Quantum","Elastic","Ethical","Aggressively","Holistic",
    "Frictionless","Disruptive","Blockchain","Serverless","Omnichannel",
    "Ranch-Flavored","Ambient","Subprime","Eco-Competitive","Hypermobile",
    "Bleeding-Edge","Ceremonial","Chaotic Good","Militarized","Plausible"
]
NOUNS = [
    "Compliance","Insights","Dynamics","Optimizations","Enablement",
    "Monetization","Parabolas","Incentives","Liquidity","Pipelines",
    "Onboarding","KPIs","Clickthroughs","Entanglement","Arbitrage",
    "Synergies","Wrangling","Migrations","Intelligence","Silos"
]
SUFFIXES = ["LLC","& Sons","Group","Ltd.","PLC","AG","S.A.","LLP",
            "Holdings","Worldwide","International","Global","Capital"]
MANAGER_FIRST = [
    "Gristle","Nebula","Chadwick","Velvet","Cabbage","Stark","Peony",
    "Vortex","Crispin","Zamboni","Tarragon","Gloria-7","Kevlar",
    "Juniper","Tungsten","Paprika","Mirth","Drizzle","Quantum","Burlap"
]
MANAGER_LAST = [
    "Mcdagger","FOMO","Von Spreadsheet","Gallowglass","Afterparty",
    "Hardskill","Dumpster","Blunderbuss","KPIson","Debtforge",
    "Coldbrew","Synergywolf","Carbonara","Quarterclose","Powerpoint",
    "Benchmarker","BrassTax","Hedgefund","Moonshot","Stakeholder"
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
if len(QUESTION_BANK) < 100:
    base = "Give an unreasonably detailed answer to: why meetings breed more meetings?"
    QUESTION_BANK.extend([f"{base} (variant {i+1})" for i in range(100 - len(QUESTION_BANK))])

# ---------- Helpers ----------
def gen_company_name() -> str:
    return random.choice([
        f"{random.choice(ADJECTIVES)} {random.choice(NOUNS)} {random.choice(SUFFIXES)}",
        f"{random.choice(ADJECTIVES)} {random.choice(NOUNS)} & Associates",
        f"{random.choice(NOUNS)} of {random.choice(ADJECTIVES)} {random.choice(SUFFIXES)}",
        f"{random.choice(ADJECTIVES)}-{random.choice(NOUNS)} {random.choice(SUFFIXES)}",
    ])

def gen_manager_name() -> str:
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

def ollama_generate(prompt: str, *, model: str, url: str) -> str:
    endpoint = f"{url}/api/generate"
    payload: Dict[str, Any] = {"model": model, "prompt": prompt, "stream": False,
                               "options": {"temperature": 0.9, "top_p": 0.95, "repeat_penalty": 1.1, "num_predict": 160}}
    resp = requests.post(endpoint, json=payload, timeout=120)
    resp.raise_for_status()
    data = resp.json()
    return (data.get("response") or "").strip()

# ---------- UI ----------
class NACFApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Not a Culture Fit — Absurd Interviewer")
        self.geometry("980x720")
        self.configure(bg=CANVAS)

        # State
        self.company = ""
        self.manager = ""
        self.questions: List[str] = []
        self.idx = 0
        self.model = MODEL_NAME
        self.url = OLLAMA_URL

        # Styles
        style = ttk.Style(self)
        if "vista" in style.theme_names():
            style.theme_use("vista")
        style.configure("TLabel", background=CANVAS, foreground=INK)
        style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"), background=CANVAS, foreground=CHARCOAL)
        style.configure("Card.TFrame", background=CARD_BG, relief="ridge", borderwidth=1)
        style.configure("Header.TFrame", background=CHARCOAL)
        style.configure("Header.TLabel", background=CHARCOAL, foreground="#ffffff", font=("Segoe UI", 12, "bold"))
        style.configure("TButton", padding=6)
        style.map("TButton",
                  background=[("active", FOREST)],
                  foreground=[("active", "#ffffff")])

        # Header
        header = ttk.Frame(self, style="Header.TFrame")
        header.pack(fill="x", side="top")
        ttk.Label(header, text="Not a Culture Fit — Interview Console", style="Header.TLabel").pack(side="left", padx=12, pady=8)
        self.model_var = tk.StringVar(value=self.model)
        self.url_var = tk.StringVar(value=self.url)
        right = ttk.Frame(header, style="Header.TFrame")
        right.pack(side="right", padx=8, pady=6)
        ttk.Label(right, text="Model:", style="Header.TLabel").pack(side="left", padx=(0,4))
        ttk.Entry(right, textvariable=self.model_var, width=14).pack(side="left", padx=(0,10))
        ttk.Label(right, text="Ollama:", style="Header.TLabel").pack(side="left", padx=(0,4))
        ttk.Entry(right, textvariable=self.url_var, width=24).pack(side="left", padx=(0,10))
        ttk.Button(right, text="New Interview", command=self.new_interview).pack(side="left")

        # Body: left panel (sprite card) + chat card
        body = ttk.Frame(self, style="Card.TFrame")
        body.pack(fill="both", expand=True, padx=12, pady=12)

        self.left = ttk.Frame(body, style="Card.TFrame")
        self.left.pack(side="left", fill="y", padx=10, pady=10)
        self._build_left_card(self.left)

        self.right = ttk.Frame(body, style="Card.TFrame")
        self.right.pack(side="left", fill="both", expand=True, padx=(0,10), pady=10)
        self._build_chat_card(self.right)

        self._set_welcome()

    # Left card with sprite and details
    def _build_left_card(self, parent):
        # load sprite
        sprite_path = os.path.join(os.path.dirname(__file__), "..", "assets", "manager_sprite.png")
        try:
            img = Image.open(sprite_path)
            # scale to fit nicely (~220px tall) using NEAREST for pixel crispness
            h_target = 220
            scale = h_target / img.height
            w = int(img.width * scale)
            h = int(img.height * scale)
            img = img.resize((w, h), Image.NEAREST)
            self.sprite = ImageTk.PhotoImage(img)
        except Exception as e:
            self.sprite = None

        frame = ttk.Frame(parent, style="Card.TFrame")
        frame.pack(fill="y", padx=8, pady=8)
        ttk.Label(frame, text="Hiring Manager", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=12, pady=(12,4))
        if self.sprite:
            lbl = ttk.Label(frame, image=self.sprite)
            lbl.image = self.sprite
            lbl.pack(padx=12, pady=(4,8))
        self.name_label = ttk.Label(frame, text="—", font=("Segoe UI", 11))
        self.name_label.pack(anchor="w", padx=12, pady=(4,8))
        ttk.Separator(frame, orient="horizontal").pack(fill="x", padx=12, pady=8)
        ttk.Label(frame, text="Company", font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=12)
        self.company_label = ttk.Label(frame, text="—")
        self.company_label.pack(anchor="w", padx=12, pady=(2,12))
        ttk.Label(frame, text="Status", font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=12)
        self.status_label = ttk.Label(frame, text="Waiting to start…", foreground=MUTED)
        self.status_label.pack(anchor="w", padx=12, pady=(2,12))

    # Chat card (chat area + input box)
    def _build_chat_card(self, parent):
        top = ttk.Frame(parent, style="Card.TFrame")
        top.pack(fill="both", expand=True, padx=8, pady=8)

        # progress
        self.progress_var = tk.StringVar(value="0/10")
        self.progress = ttk.Progressbar(top, maximum=NUM_QUESTIONS_PER_INTERVIEW, value=0)
        self.progress.pack(fill="x", padx=10, pady=(10,6))
        self.progress_label = ttk.Label(top, textvariable=self.progress_var)
        self.progress_label.pack(anchor="e", padx=12, pady=(0,4))

        # chat area
        self.chat = scrolledtext.ScrolledText(top, wrap="word", height=20, bg=CARD_BG, relief="flat")
        self.chat.pack(fill="both", expand=True, padx=10, pady=6)
        self.chat.configure(state="disabled")
        # tags
        self.chat.tag_configure("system", foreground=MUTED, spacing1=4, spacing3=6, lmargin1=4, lmargin2=4)
        self.chat.tag_configure("manager", foreground=INK, spacing1=6, spacing3=8, lmargin1=4, lmargin2=4, background="#eef3f6")
        self.chat.tag_configure("user", foreground=INK, spacing1=6, spacing3=8, lmargin1=40, lmargin2=40, background="#fff7e8")

        # input row
        row = ttk.Frame(top)
        row.pack(fill="x", padx=10, pady=(6,10))
        self.entry = tk.Text(row, height=3, wrap="word")
        self.entry.pack(side="left", fill="x", expand=True)
        self.entry.bind("<Return>", self._on_enter)
        self.entry.bind("<Shift-Return>", lambda e: None)
        ttk.Button(row, text="Send ▶", command=self.send_current).pack(side="left", padx=(8,0))

    def _set_welcome(self):
        self.company = gen_company_name()
        self.manager = gen_manager_name()
        self.name_label.config(text=self.manager)
        self.company_label.config(text=self.company)
        self.status_label.config(text="Ready")
        self._chat_system(f"Welcome to Not a Culture Fit.\nModel: {self.model}  •  Server: {self.url}")
        self._chat_manager(f"Thank you for your time today. You’re being considered for a position at {self.company}. I’m the Hiring Manager, {self.manager}. Click 'New Interview' when ready.")

    def new_interview(self):
        self.model = (self.model_var.get().strip() or "llama3")
        self.url = (self.url_var.get().strip() or "http://localhost:11434")
        self.company = gen_company_name()
        self.manager = gen_manager_name()
        self.name_label.config(text=self.manager)
        self.company_label.config(text=self.company)
        self.questions = random.sample(QUESTION_BANK, NUM_QUESTIONS_PER_INTERVIEW)
        self.idx = 0
        self.progress["value"] = 0
        self.progress_var.set(f"0/{NUM_QUESTIONS_PER_INTERVIEW}")
        self.chat.configure(state="normal"); self.chat.delete("1.0","end"); self.chat.configure(state="disabled")
        self._chat_manager(f"Welcome back. Fresh requisition from {self.company}. I’m {self.manager}. Let's begin.")
        self._ask_next_question()

    # Chat helpers
    def _chat_insert(self, text: str, tag: str):
        self.chat.configure(state="normal")
        self.chat.insert("end", text + "\n", (tag,))
        self.chat.see("end")
        self.chat.configure(state="disabled")

    def _chat_system(self, text: str):
        self._chat_insert(text, "system")

    def _chat_manager(self, text: str):
        self._chat_insert("🧑‍💼 " + text, "manager")

    def _chat_user(self, text: str):
        self._chat_insert("🙋 " + text, "user")

    # Q&A flow
    def _ask_next_question(self):
        if self.idx >= NUM_QUESTIONS_PER_INTERVIEW:
            self._decision()
            return
        q = self.questions[self.idx]
        self._chat_manager(f"Q{self.idx+1}: {q}")
        self.status_label.config(text=f"Awaiting answer to Q{self.idx+1}")
        self.entry.focus_set()

    def _on_enter(self, event):
        # Shift+Enter for newline, plain Enter sends
        if event.state & 0x0001:  # Shift
            return
        self.send_current()
        return "break"

    def send_current(self):
        user_ans = self.entry.get("1.0","end").strip()
        if not user_ans:
            return
        self.entry.delete("1.0","end")
        self._chat_user(user_ans)
        self.status_label.config(text="Scoring answer…")
        prompt = build_critique_prompt(self.company, self.manager, self.questions[self.idx], user_ans)

        def worker():
            try:
                critique = ollama_generate(prompt, model=self.model, url=self.url)
            except Exception as e:
                critique = f"[Ollama error: {e}]"
            self.after(0, lambda: self._handle_critique(critique))

        threading.Thread(target=worker, daemon=True).start()

    def _handle_critique(self, critique: str):
        if not critique:
            critique = "I’ve seen stronger convictions in a lukewarm decaf. Next."
        self._chat_manager(critique)
        self.idx += 1
        self.progress["value"] = self.idx
        self.progress_var.set(f"{self.idx}/{NUM_QUESTIONS_PER_INTERVIEW}")
        if self.idx < NUM_QUESTIONS_PER_INTERVIEW:
            self._ask_next_question()
        else:
            self._decision()

    def _decision(self):
        self.status_label.config(text="Final decision rendered.")
        self._chat_manager("Decision: " + random.choice(REJECTION_REASONS))
        self._chat_system("Interview again? Use the 'New Interview' button in the header.")

def main():
    app = NACFApp()
    app.mainloop()

if __name__ == "__main__":
    main()
