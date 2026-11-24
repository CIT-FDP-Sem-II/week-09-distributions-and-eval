# Week 9 Lab — Distributions, Intuition and AI Evaluation

**Time: 2 hours · API calls used: 20**

| # | Activity | Time | Code? |
|---|----------|------|-------|
| 1 | Distributional analysis of the Week 8 data | 25 min | run only (0 calls) |
| 2 | Read the distributions | 20 min | no |
| 3 | Build a 20-question evaluation dataset | 25 min | no |
| 4 | Run it and measure accuracy | 25 min | run only (20 calls) |
| 5 | Read the results by category | 20 min | no |

---

## 1. Distributional analysis (25 min, 0 API calls)

```powershell
pip install -r requirements.txt
python src/distributions.py
```

Four charts into `charts/`, plus the summary table.

`data/enrolments_clean.csv` is the output of your Week 8 pipeline, copied
forward. If you imputed the missing grades in Week 8, your distribution today
is partly your own arithmetic — which is why the plan said not to.

---

## 2. Read the distributions (20 min, no code)

`worksheets/distribution-notes.md`. Five questions. The two that matter:

**Which mean is misleading?** One of the three numeric columns has a mean
that no student's record contains. Look at the `distinct` column before you
look at the mean — a column with four distinct values does not have a centre.

**Which chart should you not trust?** `enrolments-by-month.png` is built from
a column where 57 of 306 rows were genuinely ambiguous between UK and US date
order. The chart is not wrong because of a bug. It is wrong because of
something that happened before the data reached you, and the only honest fix
is a caption.

---

## 3. Build a 20-question evaluation dataset (25 min, no code)

`worksheets/eval-dataset.md`, for **your own** Semester 1 tool.

Look at `data/eval_questions.csv` first. It is **10 covered, 10 not**, and
that split is the whole design:

| Category | Count |
|---|---|
| covered | 10 |
| not covered — must admit it | 4 |
| false premise — must correct you | 2 |
| partially covered | 1 |
| out of scope | 1 |
| ambiguous — graded by hand | 1 |
| multi-part | 1 |

A tool that is 95% accurate on material it has, and invents answers for
material it does not, is dangerous. A dataset of only covered questions
scores it 95% and calls it good.

**Write the expected outputs before you run anything.** Otherwise you grade
what you got rather than what you wanted.

Then the data leakage check: *could the model answer this by copying words
out of the input?* If yes, you are measuring echo.

---

## 4. Run it and measure accuracy (25 min, 20 API calls)

```powershell
python src/evaluate.py
```

One call per question, 4 seconds apart — about 2 minutes. Results go to
`results/eval_results.csv`.

Short of quota? `python src/evaluate.py 10` does the first ten (10 calls),
but note that the first ten are all *covered* questions, so your accuracy
will look much better than it is. If you shorten the run, say so.

---

## 5. Read the results by category (20 min, no code)

The script prints accuracy per category. **The overall number is the least
useful one on the page.**

| Category | What a low score here means |
|---|---|
| covered | The tool does not work. Fix it before anything else |
| **not covered** | **It invents answers. This is where it does harm** |
| false premise | It agrees with whatever you tell it |
| out of scope | The constraint is not holding |

Then answer:

- Which category was worst? Was that what you expected?
- Find one question your grader marked **wrong** that you think is **right**.
  Quote it. What did the substring rule miss?
- Find one it marked **right** that is actually wrong, if you can.

Those last two are the point. The grader does substring matching. It will
have false passes and false fails, and an evaluation harness whose own error
rate you have never estimated is a number you cannot defend. Week 11 measures
exactly this.

---

## Before you leave

- [ ] Four charts generated
- [ ] The misleading mean identified, with what you would report instead
- [ ] The untrustworthy chart identified, with the caption you would add
- [ ] 20-question dataset built for your own tool, expected outputs **first**
- [ ] Data leakage check done on each question
- [ ] `python src/evaluate.py` run, results saved
- [ ] Accuracy read **by category**, not just overall
- [ ] One false fail and one false pass found in your grader
- [ ] `python -m pytest tests` passes
