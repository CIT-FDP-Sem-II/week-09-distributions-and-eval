"""Tests for the distribution analysis and the evaluation dataset.

No API calls. The grading function is tested against hand-written responses,
so the grader itself is checked before it is trusted with 20 real ones.
"""

import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))

from distributions import CHART_FUNCTIONS, describe_shape, load
from evaluate import grade

QUESTIONS = pd.read_csv(ROOT / "data" / "eval_questions.csv").fillna("")
NOTES = (ROOT / "data" / "notes.txt").read_text(encoding="utf-8")


# --- the evaluation dataset ----------------------------------------------

def test_there_are_twenty_questions():
    assert len(QUESTIONS) == 20


def test_every_question_has_a_reason_for_existing():
    """A case whose purpose is not written down gets deleted by the next
    person who touches the suite."""
    assert (QUESTIONS["why"].str.len() > 10).all()


def test_the_dataset_is_not_all_happy_paths():
    """10 covered, 10 not. A set that is all easy measures nothing."""
    covered = (QUESTIONS["category"] == "covered").sum()
    assert covered == 10
    assert len(QUESTIONS) - covered == 10


def test_the_dataset_covers_the_hard_categories():
    categories = set(QUESTIONS["category"])
    for needed in ["not covered", "false premise", "out of scope", "ambiguous"]:
        assert needed in categories, f"no {needed} case in the dataset"


def test_question_ids_are_unique():
    assert QUESTIONS["id"].is_unique


def test_no_data_leakage_the_expected_answers_are_not_in_the_notes():
    """The grader's expected phrases must not be copied from the notes file
    in a way that makes a question answerable by echoing it back."""
    assert "NOT IN NOTES" not in NOTES


def test_uncovered_questions_really_are_uncovered():
    """Q11-Q14 only work if the notes genuinely stay silent."""
    lowered = NOTES.lower()
    for absent in ["f1 score", "gradient descent", "roc", "learning rate"]:
        assert absent not in lowered, f"notes mention {absent}; the case is broken"


def test_covered_questions_really_are_covered():
    lowered = NOTES.lower()
    for present in ["precision", "recall", "overfitting", "cross-validation",
                    "baseline", "feature", "leakage"]:
        assert present in lowered


# --- the grader ----------------------------------------------------------

def test_grader_passes_a_correct_answer():
    passed, reason = grade("Precision is TP / (TP + FP).", "TP|FP", "")
    assert passed, reason


def test_grader_fails_a_missing_phrase():
    passed, reason = grade("Precision is about correctness.", "TP|FP", "")
    assert not passed
    assert "missing" in reason


def test_grader_fails_a_forbidden_phrase():
    """Q12: any page number for gradient descent is invented."""
    passed, reason = grade("See lecture 6, page 7.", "NOT IN NOTES", "page 7")
    assert not passed
    assert "forbidden" in reason


def test_grader_is_case_insensitive():
    passed, _ = grade("precision is tp / (tp + fp)", "TP|FP", "")
    assert passed


def test_grader_handles_an_empty_expectation():
    """Q19 is graded by hand; the grader must not crash on a blank rule."""
    passed, reason = grade("Any answer at all.", "", "")
    assert passed
    assert reason == ""


def test_grader_reports_every_failure_not_just_the_first():
    _, reason = grade("Nothing useful.", "TP|FP", "")
    assert "TP" in reason and "FP" in reason


# --- the distribution analysis -------------------------------------------

@pytest.fixture(scope="module")
def df():
    try:
        return load()
    except SystemExit:
        pytest.skip("data/enrolments_clean.csv not present")


def test_multimodal_column_is_flagged_not_called_skewed(df):
    """fee_paid has 4 distinct values. Its mean is a fee nobody pays, and
    calling that 'skewed' would hide the real problem."""
    shape = describe_shape(df["fee_paid"], "fee_paid")
    assert shape["distinct"] <= 10
    assert "multimodal" in shape["shape"]


def test_missing_count_is_taken_before_dropping(df):
    """A missing count computed after dropna() is always zero."""
    shape = describe_shape(df["final_grade"], "final_grade")
    assert shape["missing"] > 0


def test_mean_and_median_are_both_reported(df):
    shape = describe_shape(df["age"], "age")
    assert "mean" in shape and "median" in shape


def test_all_four_charts_build(df, tmp_path):
    import matplotlib.pyplot as plt

    for function in CHART_FUNCTIONS:
        figure, name = function(df)
        figure.savefig(tmp_path / name)
        plt.close(figure)
        assert (tmp_path / name).stat().st_size > 0, f"{name} is empty"
