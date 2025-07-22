from models.model import  Level, Subject, Chapter, Quiz, Question

def verify_subject(name, level_id):
    sub = Subject.query.filter_by(name=name, level_uuid=level_id).first()
    if sub:
        return False
    return None

def verify_chapter(name, subject_id):
    ch = Chapter.query.filter_by(name=name, subject_uuid=subject_id).first()
    if ch:
        return False
    return None 

def verify_level(name):
    lev = Level.query.filter_by(name=name).first()
    if lev:
        return False
    return None

def verify_prev_quiz(title, chapter_id):
    quiz = Quiz.query.filter_by(title=title, chapter_uuid=chapter_id).first()
    if quiz:
        return False
    return None

def verify_prev_question(question, quiz_id):
    ques = Question.query.filter_by(question_statement=question, quiz_uuid=quiz_id).first()
    if ques:
        return False
    return None