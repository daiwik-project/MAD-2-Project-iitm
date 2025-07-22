# controllers\admin\create.py
from models.model import  Level, Subject, Chapter, Quiz, Question, db



def admin_dashboard_view():
    level_info = Level.query.with_entities(Level.name, Level.description, Level.uuid).all()

    subjects_info = Subject.query.with_entities(Subject.name, Subject.level_uuid).all()


    result = []

    for level in level_info:
        level_data = [level.name, level.description, level.uuid, []]
        for subject in subjects_info:
            if subject.level_uuid == level.uuid:
                level_data[3].append(subject.name)  
        result.append(level_data)
    return result


def Level_view(level_id):
    level = Level.query.filter_by(uuid=level_id).first()
    subject = Subject.query.filter_by(level_uuid=level_id).all()
    result = [level.uuid, level.name, level.description, []]
    if subject:
        for sub in subject:
            subject_data = [sub.uuid, sub.name, sub.description]
            result[3].append(subject_data)
    return result



def Subject_view(subject_id):
    subject = Subject.query.filter_by(uuid=subject_id).first()
    chapter = Chapter.query.filter_by(subject_uuid=subject_id).all()
    result = [subject.uuid, subject.name, subject.description, []]
    if chapter:
        for chap in chapter:
            chapter_data = [chap.uuid, chap.name, chap.description]
            result[3].append(chapter_data)
    return result


def Chapter_view(chapter_id):
    chapter = Chapter.query.filter_by(uuid=chapter_id).first()
    quiz = Quiz.query.filter_by(chapter_uuid=chapter_id).all()
    result = [chapter.uuid, chapter.name, chapter.description, []]
    if quiz:
        for q in quiz:
            current_cre_total_questions = Question.query.filter_by(quiz_uuid=q.uuid).count()
            remaining_questions = q.total_questions - current_cre_total_questions
            quiz_data = [q.uuid, q.title, q.description, q.max_score, q.correct_score, q.wrong_score, q.scheduled_date, q.duration_minutes, q.total_questions, current_cre_total_questions, remaining_questions]
            result[3].append(quiz_data)
    return result

def quiz_tit(quiz_id):
    quiz_title = Quiz.query.filter_by(uuid=quiz_id).first()
    return quiz_title


def Que_length(quiz_id):
    quiz = Quiz.query.filter_by(uuid=quiz_id).first()
    if quiz:
        current_cre_total_questions = Question.query.filter_by(quiz_uuid=quiz.uuid).count()
        remaining_questions = quiz.total_questions - current_cre_total_questions
        return remaining_questions
    return None

def Question_length(quiz_id):
    quiz = Quiz.query.filter_by(uuid=quiz_id).first()
    if quiz:
        return quiz.total_questions
    return None


def ques_det(quiz_id):
    ques_details = Question.query.filter_by(quiz_uuid=quiz_id).all()
    
    result = []
    for q in ques_details:
        question_data = {
            'uuid': q.uuid,
            'question': q.question_statement,
            'option1': q.option1,
            'option2': q.option2,
            'option3': q.option3,
            'option4': q.option4,
            'correct_option': q.correct_option
        }
        result.append(question_data)
    
    return result