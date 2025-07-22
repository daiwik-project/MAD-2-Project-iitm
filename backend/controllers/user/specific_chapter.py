from models.model import Level, Subject, User, Chapter, Quiz, UserQuizAttempt
import json
from database import db


def chap_info(chap_id, user_id):
    result = []
    quizezz = Quiz.query.filter_by(chapter_uuid=chap_id).all()
    if quizezz != []:
        for quiz in quizezz:
            user_attempt = UserQuizAttempt.query.with_entities(UserQuizAttempt.attempt_number).filter_by(quiz_uuid=quiz.uuid, user_uuid= user_id ).first()
            if user_attempt is None:
                result.append([quiz.uuid, quiz.title, quiz.description, quiz.max_score, quiz.correct_score, quiz.wrong_score, quiz.scheduled_date, quiz.duration_minutes, quiz.total_questions, 0])
            else:
                result.append([quiz.uuid, quiz.title, quiz.description, quiz.max_score, quiz.correct_score, quiz.wrong_score, quiz.scheduled_date, quiz.duration_minutes, quiz.total_questions, user_attempt[0]])    



    return result