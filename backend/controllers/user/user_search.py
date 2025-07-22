from models.model import Level, Subject, User, Chapter, Quiz, UserQuizAttempt
import json


from datetime import datetime
from models.model import Subject, Chapter, Quiz, UserQuizAttempt

def user_search_result(user_id, parameter, query):
    """
    Searches a user's quiz attempts.
    This code is written to be very simple and repetitive for teaching purposes.
    Each 'if' block is a complete, separate process.
    """
    # This is the final list we will return. We will add a dictionary to it for each result.
    results_list = []

    # --- Search by Quiz Title ---
    if parameter == "quiz_title":
        print("Searching by Quiz Title...")
        # 1. First, find all quizzes in the database that match the search title.
        all_matching_quizzes = Quiz.query.filter(Quiz.title.ilike(f"%{query}%")).all()

        # 2. Now, loop through each quiz we found.
        for quiz in all_matching_quizzes:
            # 3. For each quiz, find all the attempts made by OUR specific user.
            user_attempts = UserQuizAttempt.query.filter_by(user_uuid=user_id, quiz_uuid=quiz.uuid).all()

            # 4. A user might have tried a quiz many times. We loop through each attempt.
            for attempt in user_attempts:
                # 5. For this single attempt, we gather all the other information we need.
                chapter = Chapter.query.get(quiz.chapter_uuid)
                subject = Subject.query.get(chapter.subject_uuid)
                
                # 6. Calculate the percentage for this one attempt.
                percentage = 0
                if quiz.max_score > 0:
                    percentage = round((attempt.score * 100) / quiz.max_score, 2)

                # 7. Create a dictionary (one "row" for our table) with all the info.
                row = {
                    "quiz_id": quiz.uuid,
                    "quiz_title": quiz.title,
                    "chapter_name": chapter.name,
                    "subject_name": subject.name,
                    "date": quiz.scheduled_date.strftime('%d/%m/%Y'),
                    "max_marks": quiz.max_score,
                    "your_score": attempt.score,
                    "percentage": percentage,
                    "attempt_number": attempt.attempt_number
                }
                # 8. Add this row to our final list of results.
                results_list.append(row)

    # --- Search by Chapter Name ---
    elif parameter == "chapter_name":
        print("Searching by Chapter Name...")
        # 1. First, find all chapters that match the search name.
        all_matching_chapters = Chapter.query.filter(Chapter.name.ilike(f"%{query}%")).all()

        # 2. Now, loop through each chapter we found.
        for chapter in all_matching_chapters:
            # 3. For each chapter, find all the quizzes inside it.
            quizzes_in_chapter = Quiz.query.filter_by(chapter_uuid=chapter.uuid).all()
            
            # 4. Now we have a list of quizzes. We loop through them.
            for quiz in quizzes_in_chapter:
                # 5. For each quiz, find all the attempts made by OUR specific user.
                user_attempts = UserQuizAttempt.query.filter_by(user_uuid=user_id, quiz_uuid=quiz.uuid).all()

                # 6. Loop through each of those attempts.
                for attempt in user_attempts:
                    # 7. For this single attempt, gather all the info.
                    subject = Subject.query.get(chapter.subject_uuid)
                    percentage = 0
                    if quiz.max_score > 0:
                        percentage = round((attempt.score * 100) / quiz.max_score, 2)

                    # 8. Create the dictionary "row".
                    row = {
                        "quiz_id": quiz.uuid,
                        "quiz_title": quiz.title,
                        "chapter_name": chapter.name,
                        "subject_name": subject.name,
                        "date": quiz.scheduled_date.strftime('%d/%m/%Y'),
                        "max_marks": quiz.max_score,
                        "your_score": attempt.score,
                        "percentage": percentage,
                        "attempt_number": attempt.attempt_number
                    }
                    # 9. Add the row to our final list.
                    results_list.append(row)

    # --- Search by Subject Name ---
    elif parameter == "subject_name":
        print("Searching by Subject Name...")
        # This process is the same, just with one more loop.
        all_matching_subjects = Subject.query.filter(Subject.name.ilike(f"%{query}%")).all()
        for subject in all_matching_subjects:
            chapters_in_subject = Chapter.query.filter_by(subject_uuid=subject.uuid).all()
            for chapter in chapters_in_subject:
                quizzes_in_chapter = Quiz.query.filter_by(chapter_uuid=chapter.uuid).all()
                for quiz in quizzes_in_chapter:
                    user_attempts = UserQuizAttempt.query.filter_by(user_uuid=user_id, quiz_uuid=quiz.uuid).all()
                    for attempt in user_attempts:
                        percentage = 0
                        if quiz.max_score > 0:
                            percentage = round((attempt.score * 100) / quiz.max_score, 2)
                        row = {
                            "quiz_id": quiz.uuid,
                            "quiz_title": quiz.title,
                            "chapter_name": chapter.name,
                            "subject_name": subject.name,
                            "date": quiz.scheduled_date.strftime('%d/%m/%Y'),
                            "max_marks": quiz.max_score,
                            "your_score": attempt.score,
                            "percentage": percentage,
                            "attempt_number": attempt.attempt_number
                        }
                        results_list.append(row)

    # --- Search by Score ---
    elif parameter == "score":
        print("Searching by Score...")
        try:
            # The score from the form is text, so we must change it to a number.
            score_to_find = int(query)
            
            # 1. Find all attempts by our user that have exactly this score.
            matching_attempts = UserQuizAttempt.query.filter_by(user_uuid=user_id, score=score_to_find).all()

            # 2. Loop through each attempt we found.
            for attempt in matching_attempts:
                # 3. For each attempt, we need to find the quiz, chapter, and subject info.
                quiz = Quiz.query.get(attempt.quiz_uuid)
                chapter = Chapter.query.get(quiz.chapter_uuid)
                subject = Subject.query.get(chapter.subject_uuid)
                
                percentage = 0
                if quiz.max_score > 0:
                    percentage = round((attempt.score * 100) / quiz.max_score, 2)

                # 4. Create the dictionary "row".
                row = {
                    "quiz_id": quiz.uuid,
                    "quiz_title": quiz.title,
                    "chapter_name": chapter.name,
                    "subject_name": subject.name,
                    "date": quiz.scheduled_date.strftime('%d/%m/%Y'),
                    "max_marks": quiz.max_score,
                    "your_score": attempt.score,
                    "percentage": percentage,
                    "attempt_number": attempt.attempt_number
                }
                # 5. Add the row to our final list.
                results_list.append(row)
        except ValueError:
            # If the user typed something that is not a number (like "abc"), we do nothing.
            print("Error: Score search query was not a valid number.")

    # --- Search by Date ---
    elif parameter == "date":
        print("Searching by Date...")
        try:
            # We expect the date in 'YYYY-MM-DD' format.
            search_date = datetime.strptime(query, '%Y-%m-%d').date()
            
            # 1. Find all quizzes that were scheduled on that specific day.
            all_quizzes_on_date = Quiz.query.filter(Quiz.scheduled_date.like(f"{search_date}%")).all()
            
            # From here, the logic is the same as the "quiz_title" search.
            for quiz in all_quizzes_on_date:
                user_attempts = UserQuizAttempt.query.filter_by(user_uuid=user_id, quiz_uuid=quiz.uuid).all()
                for attempt in user_attempts:
                    chapter = Chapter.query.get(quiz.chapter_uuid)
                    subject = Subject.query.get(chapter.subject_uuid)
                    percentage = 0
                    if quiz.max_score > 0:
                        percentage = round((attempt.score * 100) / quiz.max_score, 2)
                    row = {
                        "quiz_id": quiz.uuid,
                        "quiz_title": quiz.title,
                        "chapter_name": chapter.name,
                        "subject_name": subject.name,
                        "date": quiz.scheduled_date.strftime('%d/%m/%Y'),
                        "max_marks": quiz.max_score,
                        "your_score": attempt.score,
                        "percentage": percentage,
                        "attempt_number": attempt.attempt_number
                    }
                    results_list.append(row)
        except ValueError:
            # If the user typed a date in the wrong format, we do nothing.
            print("Error: Date search query was not in YYYY-MM-DD format.")

    # After the correct 'if' block has run, we return the final list.
    return results_list

