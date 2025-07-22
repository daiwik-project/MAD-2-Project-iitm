from models.model import Level, Subject, User, Chapter, Quiz, UserQuizAttempt
import json
from database import db


def user_summary(user_id):
    user = User.query.filter_by(uuid=user_id).first()
    # If the user doesn't exist, we can't do anything.
    if not user:
        return None

    # This is the dictionary we will fill with all our results.
    summary = {
        "total_quiz_attempts": 0,
        "avg_percentage": 0,
        "subject_wise_quiz_attempts": {},
        "highest_score_quiz_wise": {},
        "month_wise_quiz_attempts": {},
        "average_score_per_subject": {},
        "quizzes_attempted_per_chapter": {},
        "best_score_in_each_subject": {},
        "number_of_attempts_per_quiz": {},
    }
    all_attempts = UserQuizAttempt.query.filter_by(user_uuid=user_id).all()
    summary["total_quiz_attempts"] = len(all_attempts)

    month_counts = {}
    attempts_per_quiz_counts = {}
    total_percentage_sum = 0

    for attempt in all_attempts:
        # For month-wise counts
        month_str = attempt.timestamp.strftime("%Y-%m")
        if month_str in month_counts:
            month_counts[month_str] += 1
        else:
            month_counts[month_str] = 1
        
        # We need to get the quiz object to find its title.
        quiz = Quiz.query.get(attempt.quiz_uuid)
        if quiz:
            if quiz.title in attempts_per_quiz_counts:
                attempts_per_quiz_counts[quiz.title] += 1
            else:
                attempts_per_quiz_counts[quiz.title] = 1
            
            # We also add up all the percentages to calculate the overall average later.
            if quiz.max_score > 0:
                percentage = (attempt.score * 100) / quiz.max_score
                total_percentage_sum += percentage

    summary["month_wise_quiz_attempts"] = month_counts
    summary["number_of_attempts_per_quiz"] = attempts_per_quiz_counts

        # Calculate the overall average percentage
    if summary['total_quiz_attempts'] > 0:
        summary['avg_percentage'] = round(total_percentage_sum / summary['total_quiz_attempts'], 2)


    # We will use the `attempts_per_quiz_counts` dictionary we just made.
    highest_score_quiz_wise = {}
    for quiz_title in attempts_per_quiz_counts.keys():
        quiz = Quiz.query.filter_by(title=quiz_title).first()
        if not quiz:
            continue

        # Get all scores for this specific quiz for this user
        user_scores_for_quiz = [
            att.score for att in all_attempts if att.quiz_uuid == quiz.uuid
        ]
        
        # Find the highest score in that list (BUG FIX)
        if user_scores_for_quiz and quiz.max_score > 0:
            max_score = max(user_scores_for_quiz)
            percentage = (max_score * 100) / quiz.max_score
            highest_score_quiz_wise[quiz.title] = round(percentage, 2)
            
    summary["highest_score_quiz_wise"] = highest_score_quiz_wise

    # --- 3. Calculate Subject and Chapter-based stats ---
    # We need to loop through the subjects the user has selected.
    
    subject_ids = json.loads(user.user_selected_subject) if user.user_selected_subject else []

    for subject_id in subject_ids:
        subject = Subject.query.get(subject_id)
        if not subject:
            continue

        subject_attempt_count = 0
        subject_total_percentage = 0
        subject_best_percentage = 0
        
        chapters = Chapter.query.filter_by(subject_uuid=subject.uuid).all()
        for chapter in chapters:
            quizzes_attempted_in_chapter = 0
            quizzes_in_chapter = Quiz.query.filter_by(chapter_uuid=chapter.uuid).all()
            
            for quiz in quizzes_in_chapter:
                # Find all attempts for this specific quiz
                attempts_for_this_quiz = [
                    att for att in all_attempts if att.quiz_uuid == quiz.uuid
                ]

                if attempts_for_this_quiz:
                    # This quiz was attempted, so we count it for the chapter.
                    quizzes_attempted_in_chapter += 1
                    
                    # Add this quiz's attempt count to the subject's total.
                    subject_attempt_count += len(attempts_for_this_quiz)

                    # Find the best score for this quiz to calculate the subject's best score
                    if quiz.max_score > 0:
                        best_score_for_quiz = max([att.score for att in attempts_for_this_quiz])
                        best_percentage_for_quiz = (best_score_for_quiz * 100) / quiz.max_score
                        # Update the subject's best score if this one is higher
                        if best_percentage_for_quiz > subject_best_percentage:
                            subject_best_percentage = best_percentage_for_quiz

                    # Add up percentages for the subject's average (BUG FIX)
                    for attempt in attempts_for_this_quiz:
                        if quiz.max_score > 0:
                            subject_total_percentage += (attempt.score * 100) / quiz.max_score

            summary["quizzes_attempted_per_chapter"][chapter.name] = quizzes_attempted_in_chapter

        # Now we can finalize the stats for this subject
        summary["subject_wise_quiz_attempts"][subject.name] = subject_attempt_count
        summary["best_score_in_each_subject"][subject.name] = round(subject_best_percentage, 2)
        
        if subject_attempt_count > 0:
            average_for_subject = subject_total_percentage / subject_attempt_count
            summary["average_score_per_subject"][subject.name] = round(average_for_subject, 2)
        else:
            summary["average_score_per_subject"][subject.name] = 0
    print(summary)
    return summary

















# def user_summary(user_id):
#     user = User.query.filter_by(uuid=user_id).first()
#     if not user:
#         return None
#     summary = {
#         "total_quiz_attempts": 0,
#         "avg_percentage":0,
#         "subject_wise_quiz_attempts": {},
#         "highest_score_quiz_wise": {},
#         "month_wise_quiz_attempts": {},
#         "average_score_per_subject": {},
#         "quizzes_attempted_per_chapter": {},
#         "best_score_in_each_subject": {},
#         "number_of_attempts_per_quiz": {},
#     }
#     summary["total_quiz_attempts"] = UserQuizAttempt.query.filter_by(user_uuid=user_id).count()
    
#     subjects = json.loads(user.user_selected_subject) if user.user_selected_subject else []
#     for subject in subjects:
#         attempt_count = 0
#         chapters = Chapter.query.filter_by(subject_uuid=subject.uuid).all()
#         for chapter in chapters:
#             quizzes = Quiz.query.filter_by(chapter_uuid=chapter.uuid).all()
#             for quiz in quizzes:
#                 attempts = UserQuizAttempt.query.filter_by(user_uuid=user_id, quiz_uuid=quiz.uuid).count()
#                 attempt_count += attempts  # Add the count directly
#         summary["subject_wise_quiz_attempts"][subject.name] = attempt_count
    
#     quizzes = Quiz.query.all()
#     for quiz in quizzes:
#         user_score = (UserQuizAttempt.query
#                     .with_entities(UserQuizAttempt.score)
#                     .filter_by(user_uuid=user_id, quiz_uuid=quiz.uuid)  # Corrected line
#                     .all())
#         if user_score:
#             max_poss_score = quiz.max_score
#             percentage = (user_score[0][0] *100) / max_poss_score
#             summary["highest_score_quiz_wise"][quiz.title] = percentage

    
#     all_attempts = UserQuizAttempt.query.filter_by(user_uuid=user_id).all()
#     month_counts = {}
#     for attempt in all_attempts:
#         if attempt.timestamp: 
#            month_str = attempt.timestamp.strftime("%Y-%m")  
#            if month_str in month_counts:
#                month_counts[month_str] += 1
#            else:
#                month_counts[month_str] = 1
#     summary["month_wise_quiz_attempts"] = month_counts

#     subjects = json.loads(user.user_selected_subject) if user.user_selected_subject else []
#     for subject in subjects:
#         total_possible_score = 0
#         total_achieved_score = 0
#         chapters = Chapter.query.filter_by(subject_uuid=subject.uuid).all()
#         for chapter in chapters:
#             quizzes = Quiz.query.filter_by(chapter_uuid=chapter.uuid).all()
#             for quiz in quizzes:
#                 attempts = UserQuizAttempt.query.filter_by(user_uuid=user_id, quiz_uuid=quiz.uuid).all()
#                 if attempts:
#                     total_possible_score += quiz.max_score  
#                     for attempt in attempts:
#                         if attempt.score is not None:
#                             total_achieved_score += attempt.score
#         if (total_possible_score> 0):
#             avg_score_percentage = (total_achieved_score / total_possible_score) * 100
#             summary["average_score_per_subject"][subject.name] = avg_score_percentage

#     subjects = json.loads(user.user_selected_subject)
#     for subject in subjects:
#         best_score_subject = 0  
#         chapters = Chapter.query.filter_by(subject_uuid=subject.uuid).all()
#         for chapter in chapters:
#             quizzes_attempted_count = 0
#             quizzes = Quiz.query.filter_by(chapter_uuid=chapter.uuid).all()
#             for quiz in quizzes:
#                 user_attempts_quiz = UserQuizAttempt.query.filter_by(user_uuid=user_id, quiz_uuid=quiz.uuid).all()
#                 if user_attempts_quiz:
#                     quizzes_attempted_count += 1  
#                     for attempt in user_attempts_quiz:
#                         if attempt.score is not None: 
#                            score_percentage = (attempt.score * 100) / quiz.max_score
#                            best_score_subject = max(best_score_subject, score_percentage)  

#             summary["quizzes_attempted_per_chapter"][chapter.name] = quizzes_attempted_count  

#         summary["best_score_in_each_subject"][subject.name] = best_score_subject 

#     user_attempts = UserQuizAttempt.query.filter_by(user_uuid=user_id).all()
#     attempts_per_quiz = {}
#     for attempt in user_attempts:
#         quiz = Quiz.query.get(attempt.quiz_uuid)  
#         if quiz:
#             attempts_per_quiz[quiz.title] = attempt.attempt_number 

#     summary["number_of_attempts_per_quiz"] = attempts_per_quiz

#     return summary
