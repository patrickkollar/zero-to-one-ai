# zero-to-one-ai

A hands-on exploration of building useful AI systems from real problems.

This repository documents the journey from experimenting with conversational AI to building working AI applications — starting with a problem I was personally trying to solve:

**How do I find the jobs that are actually worth my time?**

---

# Zero → 1 → N

## Building useful AI from a real problem

Everyone kept saying AI was the next big thing.

I thought, *okay... but what do you actually do with it?*

I didn't know how to build an AI application. I wasn't trying to become a machine-learning engineer. I was an experienced operator with a problem to solve.

I was looking for my next job.

So I started talking to an AI.

At first, it was just a conversation:

> Find me jobs that might be a good fit.

The results weren't great.

So I started teaching it what "good" meant.

Too junior.

Wrong kind of work.

Not actually remote.

I've already seen that one.

That's interesting, even though it isn't an obvious match.

Don't show me that again.

Over time, those conversations became something more.

They became **constraints, preferences, scoring, decision logic and feedback loops.**

Eventually, the conversation became a workflow.

Then the workflow became repeatable.

Then it became an application.

**I had gone from using AI to building with AI.**

This repository documents that journey.

The goal isn't to demonstrate the fanciest AI architecture possible.

It's to demonstrate a more practical skill:

> **Taking something new and ambiguous, figuring out how to make it useful, building the first working version and then turning what works into a system that can scale.**

That's the journey from **0 → 1 → N.**

---

# The first project: Job Needle Finder

Job Needle Finder is an AI-powered job intelligence application.

It evaluates job opportunities against a candidate profile, scores them across multiple dimensions, filters poor fits and presents the results in a decision-oriented dashboard.

The system uses an LLM for reasoning, while the scoring engine applies the defined weighting model separately.

That distinction matters.

**The LLM provides judgment.  
The system provides the decision framework.**

---

## What it does today

### Initial evaluation

Each opportunity is evaluated against:

- Actual work
- Seniority and scope
- Transferability
- Compensation
- Work model

The system produces:

- An overall score
- A fit assessment
- Strengths
- Concerns
- Dimension-level scores

### Decision dashboard

The Streamlit interface is designed around the questions that actually matter:

**Is this a good fit?**

**Why?**

**Where doesn't it fit?**

**Is it worth pursuing?**

### Deep Dive

For opportunities that deserve more attention, the user can request a second-stage LLM analysis.

The Deep Dive examines:

- Why the opportunity fits
- Where it doesn't fit
- What should be investigated
- The bottom line

This is intentionally separate from the initial evaluation.

The first pass is designed to be fast and decision-oriented.

The second pass goes deeper only when it's useful.

---

# How it evolved

### 0 — The problem

> "I need to find a job."

### 1 — The experiment

> "Let's see if AI can help."

### 2 — The learning loop

> "That's not a good fit. Here's why."

### 3 — The decision framework

Those corrections became structured criteria.

### 4 — The system

Reasoning + scoring + workflow + interface.

### 5 — The next step

The current application is the first working version.

The next evolution is to give the system a much richer understanding of the person behind the resume — their experience, capabilities, career goals and preferences.

---

# What this demonstrates

- Human-in-the-loop AI
- LLM-powered reasoning
- Structured outputs
- Deterministic scoring
- Decision frameworks
- Workflow orchestration
- Streamlit application development
- Iterative system design
- Learning by building

Most importantly:

**The system was built by solving a real problem, not by starting with a technology demo.**

---

# What's next

Job Needle Finder is the first experiment.

The next system will explore an AI professional experience guide — a system that can represent an individual's actual experience, capabilities, accomplishments and career goals, then use that context to answer questions about fit and transferability without inventing experience.

Longer term, that becomes part of a broader idea:

**An AI operating partner for the individual operator.**

A system that can understand:

- What you're trying to accomplish
- What you've actually done
- What you're good at
- Where your experience transfers
- What you're learning
- What you've accomplished
- What you should be thinking about next

The long-term idea is simple:

> **Build systems that help people get better at the work they do.**

This is my journey from **0 → 1 → N.**