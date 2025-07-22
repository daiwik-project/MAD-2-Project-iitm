# controllers/jobs/celery_tasks.py

from app import celery, app
from flask import render_template
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from models.model import Chapter, Quiz, Subject, User, UserQuizAttempt, db



##################### TASK - 1 #####################
@celery.task
def send_email_to_user(user_id, quiz_id):
    """Sends a single email to a single user about new quiz with a single quiz link."""
    with app.app_context():
        try:
            user = User.query.get(user_id)
            quiz = Quiz.query.get(quiz_id)
            chapter = Chapter.query.get(quiz.chapter_uuid)

            if not all([user, quiz, chapter]):
                print("ERROR: User, Quiz, or Chapter not found. Aborting email.")
                return

            msg = MIMEMultipart()
            msg['From'] = app.config['MAIL_USERNAME']
            msg['To'] = user.email
            msg['Subject'] = f'New Quiz Available: {quiz.title}'

            html_body = render_template(
                'new_quiz.html',
                chapter_name=chapter.name,
                quiz_url=f"http://localhost:8080/dashboard/attempt/{quiz.uuid}/attempt_=1",
                username=user.username,
                current_time=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
            )
            msg.attach(MIMEText(html_body, 'html'))

            print(f"Connecting to Gmail to send email to {user.email}...")
            with smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT']) as server:
                server.starttls()
                server.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
                server.send_message(msg)

            print(f"SUCCESS: Email sent successfully to {user.email}!")
            return "Email sent successfully!"

        except Exception as e:
            print(f"ERROR: Could not send email. Reason: {e}")
            return f"Email failed: {str(e)}"



# This is your scheduled task.
@celery.task
def check_new_created_quiz_24_hrs_ago():
    """
    Scheduled task to find new quizzes and notify relevant users.
    """
    with app.app_context():
        print("SCHEDULED TASK: Checking for new quizzes...")
        twenty_four_hours_ago = datetime.utcnow() - timedelta(hours=24)
        latest_quizzes = Quiz.query.filter(Quiz.created_at >= twenty_four_hours_ago).all()

        if not latest_quizzes:
            print("No new quizzes found in the last 24 hours.")
            return

        print(f"Found {len(latest_quizzes)} new quizzes. Processing...")
        for quiz in latest_quizzes:
            
            search_term = f"%{quiz.chapter_uuid}%"
            relevant_users = User.query.filter(User.user_selected_chapter.like(search_term)).all()

            if not relevant_users:
                print(f"No users have bookmarked the chapter for quiz '{quiz.title}'.")
                continue # Move to the next quiz

            for user in relevant_users:
                attempt = UserQuizAttempt.query.filter_by(
                    user_uuid=user.uuid,
                    quiz_uuid=quiz.uuid
                ).first()

                if not attempt:
                    print(f"User {user.username} has not attempted quiz {quiz.title}. Sending notification.")
                    send_email_to_user.delay(user.uuid, quiz.uuid)
                else:
                    print(f"User {user.username} has already attempted quiz '{quiz.title}'. Skipping.")



################### TASK - 2 #################
@celery.task
def send_email_report():
    """
    Scheduled task to send a monthly performance report to all active users.
    """
    with app.app_context():
        print("Starting monthly report job...")
        
        # Time setup
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=30)
        month_name = start_date.strftime('%B %Y')

        # Get active users
        all_users = User.query.filter_by(is_active=True).all()
        
        if not all_users:
            print("No active users found. Stopping job.")
            return

        print(f"Found {len(all_users)} users to send reports to.")

        for user in all_users:
            try:
                print(f"\n--- Processing report for user: {user.username} ---")

                # Get user's attempts from last month
                attempts_this_month = UserQuizAttempt.query.filter(
                    UserQuizAttempt.user_uuid == user.uuid,
                    UserQuizAttempt.timestamp.between(start_date, end_date)
                ).all()

                if not attempts_this_month:
                    print(f"User {user.username} has no quizzes this month. Skipping.")
                    continue

                # Initialize data structures
                all_percentage_scores = []
                subject_scores = {}
                quizzes_by_id = {}
                highest_score_info = {'score': -1, 'quiz_name': 'N/A'}

                # Process each attempt
                for attempt in attempts_this_month:
                    quiz = Quiz.query.get(attempt.quiz_uuid)
                    if not quiz or quiz.max_score == 0:
                        continue
                    
                    # Calculate percentage score
                    percentage = round((attempt.score / quiz.max_score) * 100)
                    all_percentage_scores.append(percentage)
                    
                    # Track highest score
                    if percentage > highest_score_info['score']:
                        highest_score_info = {
                            'score': percentage,
                            'quiz_name': quiz.title
                        }
                    
                    # Group attempts by quiz
                    if attempt.quiz_uuid not in quizzes_by_id:
                        quizzes_by_id[attempt.quiz_uuid] = []
                    quizzes_by_id[attempt.quiz_uuid].append(attempt)
                    
                    # Track subject scores
                    chapter = Chapter.query.get(quiz.chapter_uuid)
                    if chapter:
                        subject = Subject.query.get(chapter.subject_uuid)
                        if subject:
                            subject_name = subject.name
                            if subject_name not in subject_scores:
                                subject_scores[subject_name] = {'scores': [], 'count': 0}
                            subject_scores[subject_name]['scores'].append(percentage)
                            subject_scores[subject_name]['count'] += 1

                # Calculate overall average score
                average_score = round(sum(all_percentage_scores) / len(all_percentage_scores)) if all_percentage_scores else 0

                # Prepare quiz breakdown
                quiz_breakdown_list = []
                for quiz_id, attempts in quizzes_by_id.items():
                    quiz = Quiz.query.get(quiz_id)
                    if not quiz:
                        continue
                    
                    # Find best attempt for this quiz
                    best_score = max(attempt.score for attempt in attempts)
                    best_percentage = round((best_score / quiz.max_score) * 100)
                    best_attempt = next(attempt.attempt_number for attempt in attempts if attempt.score == best_score)
                    
                    # Get subject name
                    chapter = Chapter.query.get(quiz.chapter_uuid)
                    subject_name = "Unknown"
                    if chapter:
                        subject = Subject.query.get(chapter.subject_uuid)
                        if subject:
                            subject_name = subject.name
                    
                    quiz_breakdown_list.append({
                        'title': quiz.title,
                        'subject': subject_name,
                        'best_score_percentage': best_percentage,
                        'best_attempt_number': best_attempt,
                        'total_attempts': len(attempts),
                    })

                # Find strongest/weakest subjects
                strongest_subject = {'name': 'N/A', 'avg_score': 0}
                weakest_subject = {'name': 'N/A', 'avg_score': 100}
                
                for subject_name, data in subject_scores.items():
                    if data['scores']:
                        avg_score = round(sum(data['scores']) / len(data['scores']))
                        # Update strongest subject
                        if avg_score > strongest_subject['avg_score']:
                            strongest_subject = {
                                'name': subject_name,
                                'avg_score': avg_score
                            }
                        # Update weakest subject
                        if avg_score < weakest_subject['avg_score']:
                            weakest_subject = {
                                'name': subject_name,
                                'avg_score': avg_score
                            }

                # Prepare data for email
                summary_stats = {
                    'quizzes_taken': len(quizzes_by_id),
                    'average_score': average_score,
                    'highest_score': highest_score_info,
                    'best_subject': strongest_subject['name']
                }
                
                performance_insights = {
                    'strongest_subject': strongest_subject,
                    'improvement_area': weakest_subject
                }

                # Render and send email
                html_body = render_template(
                    'monthly_email.html',
                    username=user.username,
                    month_name=month_name,
                    summary_stats=summary_stats,
                    quiz_attempts=quiz_breakdown_list,
                    performance_insights=performance_insights,
                    dashboard_url="http://localhost:8080/summary" 
                )
                
                msg = MIMEMultipart()
                msg['From'] = app.config['MAIL_USERNAME']
                msg['To'] = user.email
                msg['Subject'] = f'Your {month_name} Performance Report'
                msg.attach(MIMEText(html_body, 'html'))
                
                with smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT']) as server:
                    server.starttls()
                    server.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
                    server.send_message(msg)
                
                print(f"SUCCESS: Report sent to {user.email}")

            except Exception as e:
                print(f"ERROR: Failed to send report to {user.username}. Reason: {e}")
        
        print("\nMonthly report job finished.")
        return "Monthly reports process completed."


