from models.model import Level, Subject, User, Chapter, Quiz, UserQuizAttempt, Question
import json
from database import db




def get_quiz_data(quiz_id):
    data = []
    quiz = Quiz.query.filter_by(uuid=quiz_id).first()
    data.append(quiz.title)
    data.append(quiz.duration_minutes)
    data.append(quiz.max_score)
    data.append(quiz.correct_score)
    data.append(quiz.wrong_score)
    chap = Chapter.query.filter_by(uuid=quiz.chapter_uuid).first()
    data.append(chap.name)
    question_data = {}
    quest = Question.query.filter_by(quiz_uuid= quiz_id).all()
    data.append(len(quest))
    for q in range(len(quest)):
        question_data[q] = [quest[q].uuid, quest[q].question_statement, quest[q].option1, quest[q].option2, quest[q].option3, quest[q].option4]
    data.append(question_data)
    print(data)

    return data