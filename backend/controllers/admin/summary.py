from models.model import Chapter, Level, Quiz, Subject, UserQuizAttempt, User, db, UserQuizAttempt
from sqlalchemy import func, desc


def get_admin_summary():
    """Generate comprehensive admin summary with new Level-based structure"""
    summary = {
        "total_levels": 0,
        "subjects_per_level": {},
        "quizzes_per_subject": {},
        "quiz_max_attempts": {},
        "level_top_scorer": {},
        "quiz_wise_top_scorer": {},
        "student_with_most_attempts": {}
    }

    summary["total_levels"] = Level.query.count()

    level_subjects = db.session.query(
        Level.name,
        func.count(Subject.uuid)
    ).join(Subject, Level.uuid == Subject.level_uuid
    ).group_by(Level.name).all()
    
    summary["subjects_per_level"] = {level: count for level, count in level_subjects}

    subject_quizzes = db.session.query(
        Subject.name,
        func.count(Quiz.uuid)
    ).join(Chapter, Subject.uuid == Chapter.subject_uuid
    ).join(Quiz, Chapter.uuid == Quiz.chapter_uuid
    ).group_by(Subject.name).all()
    
    summary["quizzes_per_subject"] = {subject: count for subject, count in subject_quizzes}

    quiz_attempts = db.session.query(
        Quiz.title,
        func.max(UserQuizAttempt.attempt_number)).outerjoin(UserQuizAttempt, Quiz.uuid == UserQuizAttempt.quiz_uuid
    ).group_by(Quiz.title).all()
    
    summary["quiz_max_attempts"] = {quiz: attempts or 0 for quiz, attempts in quiz_attempts}

    level_top_scores = {}
    for level in Level.query.all():
        top_attempt = (db.session.query(UserQuizAttempt, User)
            .join(User, UserQuizAttempt.user_uuid == User.uuid)
            .join(Quiz, UserQuizAttempt.quiz_uuid == Quiz.uuid)
            .join(Chapter, Quiz.chapter_uuid == Chapter.uuid)
            .join(Subject, Chapter.subject_uuid == Subject.uuid)
            .filter(Subject.level_uuid == level.uuid)
            .order_by(UserQuizAttempt.score.desc())
            .first())
        
        if top_attempt:
            attempt, user = top_attempt
            level_top_scores[level.name] = {
                'student_name': user.username,
                'score': attempt.score,
                'quiz_title': Quiz.query.get(attempt.quiz_uuid).title
            }
        else:
            level_top_scores[level.name] = {'student_name': None, 'score': 0, 'quiz_title': None}
    
    summary["level_top_scorer"] = level_top_scores

    quiz_top_scorers = {}
    for quiz in Quiz.query.all():
        top_attempt = (db.session.query(UserQuizAttempt, User)
            .join(User, UserQuizAttempt.user_uuid == User.uuid)
            .filter(UserQuizAttempt.quiz_uuid == quiz.uuid)
            .order_by(UserQuizAttempt.score.desc())
            .first())
        
        if top_attempt:
            attempt, user = top_attempt
            quiz_top_scorers[quiz.title] = {
                'student_name': user.username,
                'score': attempt.score
            }
        else:
            quiz_top_scorers[quiz.title] = {'student_name': None, 'score': 0}
    
    summary["quiz_wise_top_scorer"] = quiz_top_scorers

    active_student = db.session.query(
        User.username,
        func.count(UserQuizAttempt.uuid)
    ).join(UserQuizAttempt, User.uuid == UserQuizAttempt.user_uuid
    ).group_by(User.uuid
    ).order_by(desc(func.count(UserQuizAttempt.uuid))
    ).first()
    
    if active_student:
        summary["student_with_most_attempts"] = {
            'student_name': active_student[0],
            'total_attempts': active_student[1]
        }
    else:
        summary["student_with_most_attempts"] = {'student_name': None, 'total_attempts': 0}
    print(summary)
    return summary




