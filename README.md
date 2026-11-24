# Week 9 — Distributions, Intuition and AI Evaluation

**CIT AI-Native Engineering Program · Year 1 · Semester 2 · Module M3**

Two halves that turn out to be the same thing: reading the shape of real data,
and building a test set that tells you the truth about an AI system.

**Lab time: 2 hours. API calls: 20.** See [LAB.md](LAB.md).

## Contents

| Path | What it is |
|---|---|
| `src/distributions.py` | Four charts and the summary table. No API calls |
| `data/enrolments_clean.csv` | The Week 8 pipeline's output, carried forward |
| `data/notes.txt` | The lecture notes the evaluation questions are asked against |
| `data/eval_questions.csv` | **20 questions with expected outputs** — 10 covered, 10 not |
| `src/evaluate.py` | Runs the dataset, grades it, reports accuracy by category |
| `src/gemini_client.py` | Copied forward from Week 2, unchanged |
| `worksheets/distribution-notes.md` | Reading the charts |
| `worksheets/eval-dataset.md` | Building your own 20 |
| `tests/` | 18 tests. No API key needed. |

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1          # mac/linux: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env                 # mac/linux: cp .env.example .env
```

## Running

```powershell
python src/distributions.py   # 4 charts + summary - no API calls
python -m pytest tests -v     # 18 tests - no API calls

python src/evaluate.py        # 20 API calls, ~2 minutes
python src/evaluate.py 10     # first 10 only
```

> **Not verified in this repo:** `evaluate.py` needs a live key and has not
> been run here. `distributions.py` and the whole test suite run offline and
> are verified — all four charts build and are non-empty.

## The mean nobody pays

```
column        n  missing  distinct      mean   median   shape
final_grade 284       22       224     67.60     71.1   roughly symmetric
age         300        6        28     30.52     30.0   roughly symmetric
fee_paid    305        1         4  40400.00  48000.0   multimodal - only 4
                                                        distinct values; the
                                                        mean is not a real one
```

`fee_paid` has **four** distinct values: 25000, 32000, 48000, 55000. Its mean
is 40,400 — a fee **no student pays**. It is not a centre; it is an artefact
of averaging four price bands.

This is why `describe()` is not enough. The `distinct` column catches it; the
mean, median and standard deviation all look perfectly reasonable.

## The chart with a caption problem

`charts/enrolments-by-month.png` shows enrolments per month. It is built from
a column where **70 of 306 rows** had dates genuinely ambiguous between UK and
US order — `03/04/2025` is 3 April or 4 March and nothing in the data says
which.

No bug produced this. No better parser fixes it. The chart needs a caption
saying 23% of rows may be in the wrong month, and that caption is the finding.

## The evaluation dataset: 10 covered, 10 not

| Category | Count | What it catches |
|---|---|---|
| covered | 10 | Does it work at all? |
| **not covered** | 4 | **Does it admit it, or invent?** |
| false premise | 2 | Does it correct you, or agree? |
| partially covered | 1 | Does it answer the half it can? |
| out of scope | 1 | Does the constraint hold? |
| ambiguous | 1 | Graded by hand |
| multi-part | 1 | Completeness under length pressure |

A tutoring tool that is 95% accurate on material it has and invents answers
for material it does not is a **dangerous** tool. A test set of only covered
questions scores it 95% and calls it good.

`evaluate.py` reports accuracy **by category** for this reason. The overall
percentage is the least useful number it prints.

## The grader's own error rate

`grade()` does case-insensitive substring matching. It is crude on purpose,
and it is wrong in two directions:

- **False fail** — a correct answer phrased in different words
- **False pass** — a wrong answer that happens to contain the right substring

Both are real. The lab asks you to find one of each. **An evaluation harness
whose own error rate you have never estimated is a number you cannot defend** —
and Week 11 is where you measure it.

---

## Set B (non-IT background)

**`src/distributions.py`**
- `load()` — reads the cleaned CSV from Week 8.
- `describe_shape(series, name)` — for one column, works out how many values
  are missing, how many are distinct, the mean, median, spread and quartiles,
  and then decides what shape it is. It checks the number of distinct values
  **first**, because a column with only four of them does not have a middle.
- `chart_grade_histogram`, `chart_age_distribution`, `chart_grade_by_course`,
  `chart_enrolments_over_time` — one function per chart. Each builds the
  figure and returns it with its filename.
- `main()` — loads, prints the summary, saves all four charts.

**`src/evaluate.py`**
- `SYSTEM` — the instructions sent with every question, telling the model to
  answer only from the notes and to say `NOT IN NOTES` when it cannot.
- `grade(response, must_contain, must_not_contain)` — checks whether the
  required phrases appear and the forbidden ones do not. Returns pass/fail
  plus the reason.
- `main()` — reads the 20 questions, sends each one, grades the reply, saves
  every row to a CSV, and prints accuracy per category.

### What Set B may simplify

- **15 questions instead of 20**, keeping the same mix — at least 3 must be
  "not covered" cases.
- Full distributional analysis is **not required**. For each chart, write
  **2–3 sentences on what the shape means**. That is the Set B requirement.
- Adversarial inputs are not required.

### What Set B may **not** simplify

- Expected outputs written **before** the run.
- The dataset must include questions the material does **not** cover.
- Accuracy read per category, not as one number.
