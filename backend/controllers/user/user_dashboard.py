from models.model import Level, Subject, User, Chapter, Quiz, UserQuizAttempt
import json
from database import db


def user_selected_chap(user_id):
    user = User.query.filter_by(uuid=user_id).first()
    if user.user_selected_chapter is not None:
        user_selected_chapter = json.loads(user.user_selected_chapter)
        result = []
        for chapter_uuid in user_selected_chapter:
            chapter = Chapter.query.filter_by(uuid=chapter_uuid).first()
            sub = Subject.query.with_entities(Subject.name).filter_by(uuid=chapter.subject_uuid).first()
            result.append([chapter.uuid, chapter.name, chapter.description, sub[0]])
        # return result
        if result != []:
            return result
        else:
            return None

    
def list_all_chapters_from_user_sel_sub(user_id):
    user = User.query.filter_by(uuid=user_id).first()
    print(f'user_selected_subject: {user.user_selected_subject}')
    if user.user_selected_subject is None:
        return []
    
    user_selected_subject = json.loads(user.user_selected_subject)
    result = []

    for subject_uuid in user_selected_subject:
        print(f'subject_uuid: {subject_uuid}')
        chapters = Chapter.query.filter_by(subject_uuid=subject_uuid).all()
        if chapters  != []:
            
            for chapter in chapters:
                sub = Subject.query.with_entities(Subject.name).filter_by(uuid=chapter.subject_uuid).first()
                result.append([chapter.uuid, chapter.name, chapter.description, sub[0]])

    return result
    


def q1_list(user_favorite_chapter, user_id):
    result = []
    for ch in user_favorite_chapter:
        quizzes = Quiz.query.filter_by(chapter_uuid=ch[0]).all()
        
        if quizzes != []:
            for quiz in quizzes:
                user_attempt = UserQuizAttempt.query.with_entities(UserQuizAttempt.attempt_number).filter_by(quiz_uuid=quiz.uuid, user_uuid= user_id ).order_by(UserQuizAttempt.attempt_number.desc()).first()
                if user_attempt is None:
                    result.append([quiz.uuid, quiz.title, quiz.description, quiz.max_score, quiz.correct_score, quiz.wrong_score, quiz.scheduled_date, quiz.duration_minutes, quiz.total_questions, 0])
                else:
                    result.append([quiz.uuid, quiz.title, quiz.description, quiz.max_score, quiz.correct_score, quiz.wrong_score, quiz.scheduled_date, quiz.duration_minutes, quiz.total_questions, user_attempt[0]])    
    return result


def q2_list(chapters_from_sub, user_id):
    result = []
    for ch in chapters_from_sub:
        quizzes = Quiz.query.filter_by(chapter_uuid=ch[0]).all()
        
        if quizzes != []:
            for quiz in quizzes:
                user_attempt = UserQuizAttempt.query.with_entities(UserQuizAttempt.attempt_number).filter_by(quiz_uuid=quiz.uuid, user_uuid= user_id ).order_by(UserQuizAttempt.attempt_number.desc()).first()
                if user_attempt is None:
                    result.append([quiz.uuid, quiz.title, quiz.description, quiz.max_score, quiz.correct_score, quiz.wrong_score, quiz.scheduled_date, quiz.duration_minutes, quiz.total_questions, 0])
                else:
                    result.append([quiz.uuid, quiz.title, quiz.description, quiz.max_score, quiz.correct_score, quiz.wrong_score, quiz.scheduled_date, quiz.duration_minutes, quiz.total_questions, user_attempt[0]])

    return result

def user_fav_sub_all_chap(user_id):
    user = User.query.filter_by(uuid=user_id).first()
    user_selected_subject = json.loads(user.user_selected_subject)
    result = []
    for subject_uuid in user_selected_subject:
        chapters = Chapter.query.filter_by(subject_uuid=subject_uuid).all()
        for chapter in chapters:
            result.append([chapter.uuid, chapter.name])
    return result



def user_chap_pref(user_id, data):
    user = User.query.filter_by(uuid=user_id).first()
    ids = []
    for chapter_id in data.values():
        ids.append(chapter_id)

    print(f'ids: {ids}')

    user.user_selected_chapter = json.dumps(ids)
    db.session.commit()
    
    return True