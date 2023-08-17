from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import Question
from .helper import (
    DUMMY_QUESTIONS,
    WEATHER_DATA,
    get_count_of_exams,
    get_user_score,
    get_ledarboard,
)

main = Blueprint("main", __name__)


@main.route("/")
def index():
    total_score_of_user = 0
    exam_count = 0

    if current_user.is_authenticated:
        total_score_of_user = get_user_score()
        exam_count = get_count_of_exams()

    leaderboard = get_ledarboard()

    return render_template(
        "index.html",
        current_user=current_user,
        total_score_of_user=total_score_of_user,
        exam_count=exam_count,
        weather=WEATHER_DATA,
        leaderboard=leaderboard,
    )


@main.route("/upload-initial-dummy-data")
def upload_dummy():
    try:
        # Create dummy questions
        for q in DUMMY_QUESTIONS:
            question = Question(
                question=q["question"],
                answer=q["answer"],
                choice1=q["choice1"],
                choice2=q["choice2"],
                choice3=q["choice3"],
                choice4=q["choice4"],
            )
            db.session.add(question)
        db.session.commit()
        print("SUCCESSFULLY LOADED!")
    except Exception as e:
        print("ERROR: ", e)

    return redirect(url_for("main.index"))


@main.route("/delete-all-questions")
def delete_all_questions():
    try:
        Question.query.delete()
        db.session.commit()
        print("SUCCESSFULLY DELETED!")
    except Exception as e:
        print("ERROR: ", e)

    return redirect(url_for("main.index"))
