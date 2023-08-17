from sqlalchemy.sql import func
from flask_login import current_user
from .models import Exam, User
from . import db
from datetime import datetime, timedelta


def get_ledarboard():
    results = (
        db.session.query(Exam.user_id, func.sum(Exam.score).label("total_score"))
        .group_by(Exam.user_id)
        .order_by(func.sum(Exam.score).desc())
        .all()
    )

    leaderboard = []
    for result in results:
        user = User.query.filter_by(id=result.user_id).first()
        leaderboard.append({"user": user, "score": result.total_score})

    return leaderboard


def get_user_score():
    total_score = (
        db.session.query(func.sum(Exam.score))
        .filter(Exam.user_id == current_user.id)
        .scalar()
    )
    if total_score is None:
        total_score = 0
    return total_score


def get_count_of_exams():
    exam_count = len(Exam.query.filter_by(user_id=current_user.id).all())
    return exam_count * 5


DAYS_TR = {
    "Monday": "Pazartesi",
    "Tuesday": "Salı",
    "Wednesday": "Çarşamba",
    "Thursday": "Perşembe",
    "Friday": "Cuma",
    "Saturday": "Cumartesi",
    "Sunday": "Pazar",
}

WEATHER_DATA = {
    "Ankara": [
        {
            "date": datetime.today().strftime("%d.%m.%Y"),
            "night": 21,
            "day": 26,
            "tr": DAYS_TR[datetime.today().strftime("%A")],
        },
        {
            "date": (datetime.today() + timedelta(days=1)).strftime("%d.%m.%Y"),
            "night": 23,
            "day": 33,
            "tr": DAYS_TR[(datetime.today() + timedelta(days=1)).strftime("%A")],
        },
        {
            "date": (datetime.today() + timedelta(days=2)).strftime("%d.%m.%Y"),
            "night": 18,
            "day": 36,
            "tr": DAYS_TR[(datetime.today() + timedelta(days=2)).strftime("%A")],
        },
    ],
    "Istanbul": [
        {
            "date": datetime.today().strftime("%d.%m.%Y"),
            "night": 22,
            "day": 28,
            "tr": DAYS_TR[datetime.today().strftime("%A")],
        },
        {
            "date": (datetime.today() + timedelta(days=1)).strftime("%d.%m.%Y"),
            "night": 21,
            "day": 31,
            "tr": DAYS_TR[(datetime.today() + timedelta(days=1)).strftime("%A")],
        },
        {
            "date": (datetime.today() + timedelta(days=2)).strftime("%d.%m.%Y"),
            "night": 18,
            "day": 32,
            "tr": DAYS_TR[(datetime.today() + timedelta(days=2)).strftime("%A")],
        },
    ],
}


DUMMY_QUESTIONS = [
    {
        "id": 1,
        "question": "Aşağıdaki operatörlerden hangisi kalanı bulma (mod alma, örn: 7’nin 3 ile bölümünden kalanı bulma) ifadesinin karşılığıdır?",
        "answer": "%",
        "choice1": "%",
        "choice2": "<>",
        "choice3": "**",
        "choice4": "//",
    },
    {
        "id": 2,
        "question": "Python kodlama dilinde kullanıcıdan veri alınması gereken durumlarda kullanılması gereken kod aşağıdakilerden hangisi?",
        "answer": "input()",
        "choice1": "len()",
        "choice2": "input()",
        "choice3": "print()",
        "choice4": "exit()",
    },
    {
        "id": 3,
        "question": "Metinsel bir ifadeyi sayısal bir ifadeye çevirmek için aşağıdaki komutlardan hangisi kullanılmaktadır?",
        "answer": "int()",
        "choice1": "char()",
        "choice2": "num()",
        "choice3": "str()",
        "choice4": "int()",
    },
    {
        "id": 4,
        "question": "Aşağıdaki karşılaştırma operatörlerinden hangisi “eşitse” ifadesinin karşılığıdır?",
        "answer": "==",
        "choice1": "=",
        "choice2": "<>",
        "choice3": "==",
        "choice4": "!=",
    },
    {
        "id": 5,
        "question": "Bir listenin uzunluğunu bulmak için hangi fonksiyonu kullanırız?",
        "answer": "len()",
        "choice1": "input()",
        "choice2": "num()",
        "choice3": "str()",
        "choice4": "len()",
    },
    {
        "id": 6,
        "question": "Listenin ilk elemanını hangi şık doğru seçer?",
        "answer": "liste[0]",
        "choice1": "liste[1]",
        "choice2": "liste[2]",
        "choice3": "liste[0]",
        "choice4": "liste[-1]",
    },
    {
        "id": 7,
        "question": "Hangisi bir liste oluşturmak için kullanılan doğru komuttur?",
        "answer": "benim_listem = []",
        "choice1": "benim_listem = {}",
        "choice2": "benim_listem = ()",
        "choice3": "benim_listem = create_list()",
        "choice4": "benim_listem = None",
    },
]
