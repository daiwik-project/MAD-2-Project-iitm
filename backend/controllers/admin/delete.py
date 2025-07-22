import json
from models.model import Level, Subject, Chapter, Quiz, Question, User, db

def delete_question(question_id):
    question = Question.query.filter_by(uuid=question_id).first()
    db.session.delete(question)
    db.session.commit()
    return True

def delete_quiz(quiz_id):
    questions = Question.query.filter_by(quiz_uuid=quiz_id).all()
    for question in questions:
        db.session.delete(question)
    
    quiz = Quiz.query.filter_by(uuid=quiz_id).first()
    db.session.delete(quiz)
    db.session.commit()
    return True

def delete_chapter(chapter_id):

    print(f"Updating users to remove chapter ID: {chapter_id}")
    all_users = User.query.all()
    for user in all_users:
        if user.user_selected_chapter:
            selected_chapters = json.loads(user.user_selected_chapter)
            
            chapters_to_keep = []
            for c_id in selected_chapters:
                if c_id != chapter_id:
                    chapters_to_keep.append(c_id)
            
            user.user_selected_chapter = json.dumps(chapters_to_keep)

    print(f"Finding all quizzes for chapter ID: {chapter_id}")
    quizzes_to_delete = Quiz.query.filter_by(chapter_uuid=chapter_id).all()
    for quiz in quizzes_to_delete:
        print(f"  - Deleting questions for quiz: {quiz.title}")
        questions_to_delete = Question.query.filter_by(quiz_uuid=quiz.uuid).all()
        for question in questions_to_delete:
            db.session.delete(question)
        
        print(f"  - Deleting quiz: {quiz.title}")
        db.session.delete(quiz)

    print(f"Deleting the main chapter object...")
    chapter = Chapter.query.filter_by(uuid=chapter_id).first()
    db.session.delete(chapter)

    print("Committing all changes.")
    db.session.commit()
    return True


def delete_subject(subject_id):

    chapters_to_delete = Chapter.query.filter_by(subject_uuid=subject_id).all()
    chapter_ids_to_delete = []
    for chapter in chapters_to_delete:
        chapter_ids_to_delete.append(chapter.uuid)

    all_users = User.query.all()
    for user in all_users:
        if user.user_selected_subject:
            selected_subjects = json.loads(user.user_selected_subject)
            subjects_to_keep = []
            for s_id in selected_subjects:
                if s_id != subject_id:
                    subjects_to_keep.append(s_id)
            user.user_selected_subject = json.dumps(subjects_to_keep)

        if user.user_selected_chapter:
            selected_chapters = json.loads(user.user_selected_chapter)
            chapters_to_keep = []
            for c_id in selected_chapters:
                if c_id not in chapter_ids_to_delete:
                    chapters_to_keep.append(c_id)
            user.user_selected_chapter = json.dumps(chapters_to_keep)  
        
    for chapter in chapters_to_delete:
        quizzes_to_delete = Quiz.query.filter_by(chapter_uuid=chapter.uuid).all()
        for quiz in quizzes_to_delete:
            questions_to_delete = Question.query.filter_by(quiz_uuid=quiz.uuid).all()
            for question in questions_to_delete:
                db.session.delete(question)
            db.session.delete(quiz)
        db.session.delete(chapter)

    subject = Subject.query.filter_by(uuid=subject_id).first()
    db.session.delete(subject)

    db.session.commit()
    return True


def delete_level(level_id):

    print(f"Finding everything inside Level ID: {level_id}")
    subjects_to_delete = Subject.query.filter_by(level_uuid=level_id).all()
    
    subject_ids_to_delete = []
    for subject in subjects_to_delete:
        subject_ids_to_delete.append(subject.uuid)
    
    chapter_ids_to_delete = []
    for subject in subjects_to_delete:
        chapters = Chapter.query.filter_by(subject_uuid=subject.uuid).all()
        for chapter in chapters:
            chapter_ids_to_delete.append(chapter.uuid)

    print("Updating all users to remove the subjects and chapters from this level...")
    all_users = User.query.all()
    for user in all_users:
        if user.user_selected_subject:
            selected_subjects = json.loads(user.user_selected_subject)
            subjects_to_keep = []
            for s_id in selected_subjects:
                if s_id not in subject_ids_to_delete:
                    subjects_to_keep.append(s_id)
            user.user_selected_subject = json.dumps(subjects_to_keep)

        if user.user_selected_chapter:
            selected_chapters = json.loads(user.user_selected_chapter)
            chapters_to_keep = []
            for c_id in selected_chapters:
                if c_id not in chapter_ids_to_delete:
                    chapters_to_keep.append(c_id)
            user.user_selected_chapter = json.dumps(chapters_to_keep)

    print("Starting to delete all objects in the level...")
    for subject in subjects_to_delete:
        chapters = Chapter.query.filter_by(subject_uuid=subject.uuid).all()
        for chapter in chapters:
            quizzes = Quiz.query.filter_by(chapter_uuid=chapter.uuid).all()
            for quiz in quizzes:
                questions = Question.query.filter_by(quiz_uuid=quiz.uuid).all()
                for question in questions:
                    db.session.delete(question)
                db.session.delete(quiz)
            db.session.delete(chapter)
        db.session.delete(subject)

    print("Deleting the main level object...")
    level = Level.query.filter_by(uuid=level_id).first()
    db.session.delete(level)

    print("Committing all changes.")
    db.session.commit()
    return True









