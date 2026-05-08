"""Flesch Reading Ease score to grade level conversion."""

import math


def flesch_to_grade(score) -> str:
    """Convert a Flesch Reading Ease score to a grade level string.

    Returns empty string for blank/NaN/None input (fixes the Google Sheets bug
    where blank scores were treated as 0 and returned '5th grade').
    """
    if score is None:
        return ""
    try:
        score = float(score)
    except (ValueError, TypeError):
        return ""
    if math.isnan(score):
        return ""

    if score >= 90:
        return "5th grade"
    if score >= 80:
        return "6th grade"
    if score >= 70:
        return "7th grade"
    if score >= 60:
        return "8th - 9th grade"
    if score >= 50:
        return "10th - 12th grade"
    if score >= 30:
        return "College"
    if score >= 10:
        return "College Graduate"
    if score >= 0:
        return "Professional"
    return "Invalid score"
