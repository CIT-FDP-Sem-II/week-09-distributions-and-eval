# Worksheet — Reading the Distributions

Run `python src/distributions.py`, then answer these from the charts and the
summary table. (20 minutes)

## 1. The misleading mean

One of the three numeric columns has a mean that is **actively misleading** —
a number no student's record contains.

> Which column:
>
> What its mean is:
>
> Why that number is meaningless:
>
> What you would report instead:

Hint: look at the `distinct` column in the summary table before you look at
the mean.

## 2. Mean vs median

| Column | mean | median | What the gap tells you |
|---|---|---|---|
| final_grade | | | |
| age | | | |
| fee_paid | | | |

When mean and median agree, the distribution is roughly symmetric and the
mean is a fair summary. When they disagree, the mean is reporting the tail.

## 3. The shape of the grades

Look at `charts/grades-histogram.png`.

> Is it one hump or more than one? If more, what might the second one be —
> a different course, a different campus, a resit cohort?
>
> Check it: does `charts/grade-by-course.png` explain it?

## 4. The chart you should not trust

`charts/enrolments-by-month.png` is built from the `enrolled_on` column.

> From Week 8: how many rows had dates that were **genuinely ambiguous**
> between UK and US format?
>
> What fraction of the dataset is that?
>
> What would you write under this chart before showing it to anyone?

This is the most important question on the sheet. The chart is not wrong
because of a bug. It is wrong because of something that happened before the
data reached you, and the only honest fix is a caption.

## 5. Missing data

| Column | How many missing | Does that change the chart? |
|---|---|---|
| final_grade | | |
| age | | |

> 22 grades are missing. Were those students excluded from the histogram?
> If the missing grades are not random — say, students who dropped out — what
> does that do to the mean grade you are reporting?

This is survivorship bias, and it is invisible in every chart on the page.
