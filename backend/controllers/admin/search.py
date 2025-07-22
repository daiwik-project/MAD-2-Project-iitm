# controllers/admin/search.py

from models.model import db, Quiz, Chapter, Subject, User, UserQuizAttempt
from datetime import datetime
from sqlalchemy import func

def admin_search_result(param, query):

    results = [] 

    if param == "quiz_title":
        quizzes = Quiz.query.filter(Quiz.title.ilike(f"%{query}%")).all()
        for quiz in quizzes:
            chapter = Chapter.query.get(quiz.chapter_uuid)
            subject = Subject.query.get(chapter.subject_uuid) if chapter else None
            user_count = db.session.query(func.count(func.distinct(UserQuizAttempt.user_uuid)))\
                .filter(UserQuizAttempt.quiz_uuid == quiz.uuid).scalar() or 0
            
            results.append({
                "Quiz Title": quiz.title,
                "Chapter Name": chapter.name if chapter else "N/A",
                "Subject Name": subject.name if subject else "N/A",
                "Scheduled Date": quiz.scheduled_date.strftime('%d-%m-%Y'),
                "Users Attempted": user_count
            })

    elif param == "chapter_name":
        chapters = Chapter.query.filter(Chapter.name.ilike(f"%{query}%")).all()
        for chapter in chapters:
            subject = Subject.query.get(chapter.subject_uuid)
            quizzes_in_chapter = Quiz.query.filter_by(chapter_uuid=chapter.uuid).all()
            for quiz in quizzes_in_chapter:
                user_count = db.session.query(func.count(func.distinct(UserQuizAttempt.user_uuid)))\
                    .filter(UserQuizAttempt.quiz_uuid == quiz.uuid).scalar() or 0
                
                results.append({
                    "Chapter Name": chapter.name,
                    "Subject Name": subject.name if subject else "N/A",
                    "Quiz Title": quiz.title,
                    "Scheduled Date": quiz.scheduled_date.strftime('%d-%m-%Y'),
                    "Users Attempted": user_count
                })
    
    elif param == "subject_name":
        subjects = Subject.query.filter(Subject.name.ilike(f"%{query}%")).all()
        for subject in subjects:
            chapters_in_subject = Chapter.query.filter_by(subject_uuid=subject.uuid).all()
            for chapter in chapters_in_subject:
                quizzes_in_chapter = Quiz.query.filter_by(chapter_uuid=chapter.uuid).all()
                for quiz in quizzes_in_chapter:
                    user_count = db.session.query(func.count(func.distinct(UserQuizAttempt.user_uuid)))\
                        .filter(UserQuizAttempt.quiz_uuid == quiz.uuid).scalar() or 0
                    
                    results.append({
                        "Subject Name": subject.name,
                        "Chapter Name": chapter.name,
                        "Quiz Title": quiz.title,
                        "Scheduled Date": quiz.scheduled_date.strftime('%d-%m-%Y'),
                        "Users Attempted": user_count
                    })

    elif param == "user_id":
        attempts = UserQuizAttempt.query.join(User, UserQuizAttempt.user_uuid == User.uuid)\
            .filter(User.uuid.ilike(f"%{query}%")).all()
        
        for attempt in attempts:
            user = User.query.get(attempt.user_uuid)
            quiz = Quiz.query.get(attempt.quiz_uuid)
            
            if user and quiz:
                results.append({
                    "User ID": user.uuid,
                    "Username": user.username,
                    "Quiz Title": quiz.title,
                    "Score": attempt.score,
                    "Attempted On": attempt.timestamp.strftime('%d-%m-%Y %H:%M')
                })
                
    elif param == "date":
        search_date = None
        try:
            search_date = datetime.strptime(query, '%d/%m/%Y').date()
        except ValueError:
            try:
                search_date = datetime.strptime(query, '%d-%m-%Y').date()
            except ValueError:
                return [] 

        if search_date:
            quizzes = Quiz.query.filter(func.date(Quiz.scheduled_date) == search_date).all()
            for quiz in quizzes:
                chapter = Chapter.query.get(quiz.chapter_uuid)
                subject = Subject.query.get(chapter.subject_uuid) if chapter else None
                user_count = db.session.query(func.count(func.distinct(UserQuizAttempt.user_uuid)))\
                    .filter(UserQuizAttempt.quiz_uuid == quiz.uuid).scalar() or 0
                
                results.append({
                    "Date": quiz.scheduled_date.strftime('%d-%m-%Y'),
                    "Quiz Title": quiz.title,
                    "Chapter Name": chapter.name if chapter else "N/A",
                    "Subject Name": subject.name if subject else "N/A",
                    "Users Attempted": user_count
                })

    return results