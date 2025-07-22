from models.model import Level, Subject, User, Chapter, Quiz, UserAnswer, UserQuizAttempt, Question
import json
from database import db
from utils.uuid import generate_uuid


def store_ans(user_id, quiz_id, attempt_nuber, data):
    # if user is already done the 1st attempt
    usr_attempt = UserQuizAttempt.query.filter_by(
        user_uuid=user_id, quiz_uuid=quiz_id, attempt_number=attempt_nuber
    ).first()
    if usr_attempt:
        print("User has already attempt this quiz with same no of attepmt")
        return False
    
    score = 0
    correct_score = 0
    wrong_score = 0

    scores = Quiz.query.filter_by(uuid=quiz_id).first()
    correct_score = scores.correct_score
    wrong_score = scores.wrong_score
    for d in data:
        # finding the answer of the question in db
        ans = Question.query.filter_by(uuid = d).first()
        # print(ans, "Answer in store_ans")
        if data[d] == ans.correct_option:
            score += correct_score
            uuid = generate_uuid()
            # saving each answer in user tabel
            new_answer = UserAnswer(
                uuid=uuid,
                user_uuid = user_id,
                attempt_no = attempt_nuber,
                quiz_uuid = quiz_id,
                question_uuid = d,
                selected_option = data[d],
                is_correct = 1,
            )
            db.session.add(new_answer)
            db.session.commit()

        else:
            score -= wrong_score
            uuid = generate_uuid()
            new_answer = UserAnswer(
                uuid=uuid,
                user_uuid = user_id,
                attempt_no = attempt_nuber,
                quiz_uuid = quiz_id,
                question_uuid = d,
                selected_option = data[d],
                is_correct = 0,
            )
            db.session.add(new_answer)
            db.session.commit()

    print(score, "Score in store_ans")

    # saving the user quiz attempt
    n_id = generate_uuid()
    user_quiz_attempt = UserQuizAttempt(
        uuid=n_id,
        user_uuid=user_id,
        quiz_uuid=quiz_id,
        score=score,
        attempt_number=attempt_nuber
    )
    db.session.add(user_quiz_attempt)
    db.session.commit()
    return True
