# controllers\admin\create.py
from models.model import Level, Subject, Chapter, Quiz, Question, db
from datetime import datetime


def cre_level(id, name, description):
    new_level = Level(uuid=id, name=name, description=description)
    db.session.add(new_level)
    db.session.commit()
    return True

def cre_subject(id, name, description, level_id):
    new_subject = Subject(uuid=id, name=name, description=description, level_uuid=level_id)
    db.session.add(new_subject)
    db.session.commit()
    return True

def cre_chapter(id, name, description, subject_id):
    new_chapter = Chapter(uuid=id, name=name, description=description, subject_uuid=subject_id)
    db.session.add(new_chapter)
    db.session.commit()
    return True


    
def cre_quiz(uuid, title, description, max_marks, correct_marks, negative_marks, chapter_id, scheduled_date, max_time, total_questions):
    scheduled_datetime = datetime.strptime(scheduled_date, '%Y-%m-%d')
    max_marks_int = int(max_marks)
    correct_marks_float = float(correct_marks)
    negative_marks_float = float(negative_marks)
    max_time_int = int(max_time)
    total_questions_int = int(total_questions)
    
    new_quiz = Quiz(
        uuid=uuid,
        title=title,
        description=description,
        max_score=max_marks_int,
        correct_score=correct_marks_float,
        wrong_score=negative_marks_float,
        chapter_uuid=chapter_id,
        scheduled_date=scheduled_datetime,
        duration_minutes=max_time_int,
        total_questions=total_questions_int
    )
    
    db.session.add(new_quiz)
    db.session.commit()
    return True

def create_quest(uuid, quiz_id, question, option1, option2, option3, option4, correct_option):
    new_question = Question(
        uuid=uuid,
        quiz_uuid=quiz_id,
        question_statement=str(question),
        option1=str(option1),
        option2=str(option2),
        option3=str(option3),
        option4=str(option4),
        correct_option=str(correct_option)
    )
    
    db.session.add(new_question)
    db.session.commit()
    return True