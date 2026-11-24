# Worksheet — Building an Evaluation Dataset

(20 minutes, no API calls)

## What makes a good test set

| Property | What it means | What goes wrong without it |
|---|---|---|
| **Coverage** | Every capability is tested | A feature nobody tests is a feature nobody checks |
| **Balance** | Not all happy paths | 100% accuracy that means nothing |
| **Expected outputs** | Written down **before** running | You grade what you got, not what you wanted |
| **No leakage** | Answers not visible in the input | You measure echo, not understanding |

The dataset in `data/eval_questions.csv` is **10 covered, 10 not**. That split
is the design, not an accident: a tutoring tool that is 95% accurate on
material it has and invents answers for material it does not is a dangerous
tool, and a dataset of only covered questions would score it 95% and call it
good.

## Build your own 20 for your Semester 1 tool

| # | Question | Expected output | Category | Why this case |
|---|----------|-----------------|----------|---------------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |

*(continue to 20 — Set B: 15)*

Aim for this mix:

| Category | How many |
|---|---|
| covered / happy path | 8–10 |
| not covered — must admit it | 3–4 |
| false premise — must correct you | 2 |
| out of scope | 1–2 |
| ambiguous — graded by hand | 1 |
| multi-part | 1–2 |

## Data leakage check

Before you finish, check each question:

> Could the model answer this correctly **by copying words out of the input**
> without understanding anything?

If yes, it is not testing what you think. The commonest form is an expected
answer phrased in exactly the words the source material uses.

## The limits of your grader

The grader in `src/evaluate.py` does substring matching. Write down two
specific ways it will be wrong:

1. **False fail:** a correct answer it will mark wrong because…

2. **False pass:** a wrong answer it will mark right because…

> Both exist. Week 11 measures how often. An evaluation harness whose own
> error rate you have never estimated is a number you cannot defend.
