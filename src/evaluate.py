"""Run the evaluation dataset against the model and measure accuracy.

    python src/evaluate.py            # all 20 questions = 20 API calls
    python src/evaluate.py 5          # first 5           =  5 API calls

Reuses GeminiClient from Week 2, unchanged.

Writes results/eval_results.csv - one row per question, with the response,
the verdict and which check failed. Accuracy is printed by category, because
a single accuracy number over a mixed dataset hides the thing you need to
know: this model is usually fine on covered material and unreliable on
material the notes do not contain.
"""

import sys
import time
from pathlib import Path

import pandas as pd

from gemini_client import GeminiClient, MissingKeyError

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data"
RESULTS = ROOT / "results"
PAUSE_SECONDS = 4

SYSTEM = """You are a subject tutor answering a first-year undergraduate's
question about their lecture notes.

Rules:
- Answer only from the notes supplied.
- If the notes do not cover something, say exactly: NOT IN NOTES
- Never invent a lecture or page number.
- If the question contains a statement that the notes contradict, correct it.
- Keep the answer under 120 words."""


def grade(response, must_contain, must_not_contain):
    """Score one response. Returns (passed, reason).

    Deliberately crude: substring matching, case-insensitive. It cannot judge
    whether an answer is well written, and it will mark a correct answer wrong
    if it uses different words. That is a real limitation, not a bug, and
    Week 11 is where you measure how often it happens.
    """
    text = response.lower()
    reasons = []

    for phrase in [p for p in str(must_contain).split("|") if p.strip()]:
        if phrase.strip().lower() not in text:
            reasons.append(f"missing '{phrase.strip()}'")

    for phrase in [p for p in str(must_not_contain).split("|") if p.strip()]:
        if phrase.strip().lower() in text:
            reasons.append(f"contains forbidden '{phrase.strip()}'")

    return (not reasons), "; ".join(reasons)


def main():
    questions = pd.read_csv(DATA / "eval_questions.csv").fillna("")
    notes = (DATA / "notes.txt").read_text(encoding="utf-8")

    if len(sys.argv) > 1:
        questions = questions.head(int(sys.argv[1]))

    try:
        client = GeminiClient()
    except MissingKeyError as exc:
        print(f"STOPPED: {exc}")
        return 1

    RESULTS.mkdir(exist_ok=True)
    print(f"{len(questions)} questions = {len(questions)} API calls\n")

    rows = []
    for _, question in questions.iterrows():
        message = f"{question['question']}\n\nNOTES:\n{notes}"
        try:
            response = client.ask(message, system=SYSTEM)
            error = ""
        except Exception as exc:
            response, error = "", f"{type(exc).__name__}: {exc}"

        if error:
            passed, reason = False, error
        else:
            passed, reason = grade(
                response, question["must_contain"], question["must_not_contain"]
            )

        rows.append({
            "id": question["id"],
            "category": question["category"],
            "question": question["question"],
            "response": response,
            "passed": passed,
            "reason": reason,
        })
        print(f"  {question['id']}  {'pass' if passed else 'FAIL'}  {reason}")
        time.sleep(PAUSE_SECONDS)

    results = pd.DataFrame(rows)
    results.to_csv(RESULTS / "eval_results.csv", index=False)

    print("\nACCURACY BY CATEGORY")
    print("=" * 52)
    by_category = results.groupby("category")["passed"].agg(["sum", "count"])
    for category, row in by_category.iterrows():
        print(f"  {category:<22}{int(row['sum'])}/{int(row['count'])}")
    overall = results["passed"].sum()
    print(f"  {'OVERALL':<22}{overall}/{len(results)}  "
          f"({100 * overall / len(results):.0f}%)")

    print(f"\nWritten to {RESULTS / 'eval_results.csv'}")
    print(
        "\nThe overall number is the least useful one here. Look at the "
        "'not covered' row - that is where a tutoring tool does harm."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
