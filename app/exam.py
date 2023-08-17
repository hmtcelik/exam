from sqlalchemy.sql import func
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from .models import Exam, Question
from . import db
from .helper import get_count_of_exams, get_user_score

exam = Blueprint("exam", __name__)


@login_required
@exam.route("/exam", methods=["GET", "POST"])
def exam_():
    questions = Question.query.order_by(func.random()).limit(5)

    if request.method == "POST":
        score = 0
        for q in questions:
            if q.answer == request.form.get(f"answer{str(q.id)}"):
                score += 1

        exam = Exam(
            score=score,
            user_id=current_user.id,
        )

        db.session.add(exam)
        db.session.commit()

        return render_template(
            "exam_result.html",
            score=score,
            total_score_of_user=get_user_score(),
            exam_count=get_count_of_exams(),
        )

    return render_template(
        "exam.html",
        questions=questions,
        questionIds=[q.id for q in questions],
        total_score_of_user=get_user_score(),
        exam_count=get_count_of_exams(),
    )
