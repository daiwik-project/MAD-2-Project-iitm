
from models.model import Level, Subject, Chapter, Quiz, Question, db
from datetime import datetime


def update_level(level_id, name, description):
    level = Level.query.filter_by(uuid=level_id).first()
    if level:
        level.name = name
        level.description = description
        db.session.commit()
        return True
    return False

def update_subject(subject_id, title, description):
    subject = Subject.query.filter_by(uuid=subject_id).first()
    if subject:
        subject.name = title
        subject.description = description
        db.session.commit()
        return True
    return False

def update_chapter(chapter_id, title, description):
    chapter = Chapter.query.filter_by(uuid=chapter_id).first()
    if chapter:
        chapter.name = title
        chapter.description = description
        db.session.commit()
        return True
    return False

def update_quiz(quiz_id, title, description, max_marks, correct_marks, negative_marks, scheduled_date, max_time, total_questions):
    quiz = Quiz.query.filter_by(uuid=quiz_id).first()
    if quiz:
        scheduled_date = datetime.strptime(scheduled_date, '%Y-%m-%d')

        quiz.title = title
        quiz.description = description
        quiz.max_score = max_marks
        quiz.correct_score = correct_marks
        quiz.wrong_score = negative_marks
        quiz.scheduled_date = scheduled_date
        quiz.duration_minutes = max_time
        quiz.total_questions = total_questions
        db.session.commit()
        return True
    return False

def update_question(question_id, question, option_a, option_b, option_c, option_d, answer):
    question_obj = Question.query.filter_by(uuid=question_id).first()
    if question_obj:
        question_obj.question_statement = question
        question_obj.option1 = option_a
        question_obj.option2 = option_b
        question_obj.option3 = option_c
        question_obj.option4 = option_d
        question_obj.correct_option = answer
        db.session.commit()
        return True
    return False

