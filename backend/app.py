import atexit
import subprocess
from celery import Celery
from flask import Flask, request, jsonify, make_response, current_app, redirect, url_for
from config import Config
from database import db
from flask_cors import CORS
from flask_caching import Cache 
import bcrypt
import jwt
import os 
from datetime import datetime, timedelta, timezone


# File import
from controllers.admin.create import cre_level, cre_quiz, cre_subject, cre_chapter, create_quest
from controllers.admin.update import update_chapter, update_level, update_question, update_quiz, update_subject
from controllers.admin.read import Chapter_view, Que_length, Question_length, admin_dashboard_view, Level_view, Subject_view, ques_det, quiz_tit
from controllers.admin.delete import delete_chapter, delete_level, delete_question, delete_quiz, delete_subject
from controllers.admin.search import admin_search_result
from controllers.admin.user_control import block_user, find_usr, unblock_user
from controllers.admin.summary import get_admin_summary
from controllers.admin.auth import actual_otp, check_n_add_admin, find_admin, send_otp_for_admin


from controllers.user.auth import check_token_in_user, register_user, store_the_token, user_password
from controllers.user.user_choice import init_sub_list_of_user_sel_level, user_selected_level, user_selected_sub
from controllers.user.user_dashboard_start import use_dash_level_view
from controllers.user.user_dashboard import list_all_chapters_from_user_sel_sub, q1_list, q2_list, user_chap_pref, user_fav_sub_all_chap, user_selected_chap
from controllers.user.specific_chapter import chap_info
from controllers.user.user_quiz_start import get_quiz_data
from controllers.user.user_search import user_search_result
from controllers.user.user_summary import user_summary
from controllers.user.profile import delete_user, update_user_profile, user_prof

#scoring
from controllers.exam.store_answer import store_ans
from controllers.exam.quiz_summary import quiz_summ_info

# utility and Error
from middlewares.error_handlers import register_error_handlers
from utils.quiz_validator import verify_chapter, verify_level, verify_prev_question, verify_prev_quiz, verify_subject
from utils.user_validator import login_att, user_id_function, verify_login_user, verify_pre_user
from utils.uuid import generate_uuid





app = Flask(__name__)

app.config.from_object(Config)
db.init_app(app)
cache = Cache(app)

# ==========================================================
# === Load Celery with config ===
# ==========================================================
celery = Celery(app.name)
celery.conf.update(
    broker_url=app.config['CELERY_BROKER_URL'],
    result_backend=app.config['CELERY_RESULT_BACKEND'],
    imports=app.config['IMPORTS'],
    beat_schedule=app.config['BEAT_SCHEDULE']  
)



if app.config['CORS_ENABLED']:
    CORS(app, origins=app.config['CORS_ORIGINS'], supports_credentials=True)

register_error_handlers(app)

 

################## USER ROUTES #########################
@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if not username or not email or not password:
            return jsonify({"error": "Please provide all required fields"}), 400
            # verify_level(name)
            # if verify_level(name)==None:
        verify_pre_user(username, email)
        if verify_pre_user(username, email)==None:
            hashed_password = bcrypt.hashpw(
                password.encode('utf-8'), bcrypt.gensalt(app.config['BCRYPT_LOG_ROUNDS'])
            ).decode('utf-8')
            id = generate_uuid()
            # print(type(hashed_password.decode('utf-8')), hashed_password.decode('utf-8'))
            register_user(id, username, email, hashed_password)
            return jsonify({"message": "User registered successfully!"}), 200
        else:
            return jsonify({"message": "User Already Exist"}), 409
    return jsonify({"message": "Currently get meathod is disable"}), 400

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        identifier = request.form['identifier']
        password = request.form['password']

        # print(identifier, password, "Received form data")
        if not identifier or not password:
            return jsonify({"error": "Please provide all required fields"}), 400


        user = verify_login_user(identifier)
        if (user == True):

            user_id = user_id_function(identifier)
            user_passw = user_password(identifier)  
            check = bcrypt.checkpw(
                password.encode('utf-8'), user_passw.encode('utf-8')
            )
            if not check:
                return jsonify({"error": "Invalid credentials"}), 401
             
            payload = {
                'user_id': user_id,
                'exp': datetime.now(timezone.utc) + timedelta(days=4)
            }
            token = jwt.encode(
                payload, 
                app.config['SECRET_KEY'], 
                algorithm='HS256'
            )
            login_attempt = login_att(user_id)
            store_the_token(user_id, token)
            resp = make_response(jsonify({'message': 'Login successful', 
                                          'login_attempt': login_attempt, 
                                          'token': token}), 
                                          200)

            return resp

        else:
            return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({"message": "Currently get meathod is disable"}), 400

            # resp.set_cookie(
            #     'access_token',
            #     value=token,
            #     httponly=True,
            #     max_age=4*24*60*60,
            #     samesite='Lax',
            #     secure=False,
            #     path='/' 
            # )

def check_token(token):
    # token = request.cookies.get('access_token')
    # if not token:
    #     return None, jsonify({"error": "Token is missing"}), 401

    try:
        # Optional: Check if token exists in database
        result = check_token_in_user(token)
        if result is None:
            return None, None, None #, jsonify({"error": "Token is not valid"}), 401

        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload, None, None
    except jwt.ExpiredSignatureError:
        return None, jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return None, jsonify({"error": "Invalid token"}), 401


####### start dashboard ########
@app.route('/api/level_info', methods=['GET'])
def level_info():
    info = use_dash_level_view()
    return jsonify({"message": "Welcome to the User Dashboard!", "info": info}), 200


@app.route('/api/start/select_level', methods=['POST'])
def select_level():
    if request.method == 'POST':
        token = request.args.get('token')
        if token == None:
            print("yoo")
            return jsonify({"message": "Something is Fishy"}), 404
        payload, error_response, status_code = check_token(token)
        data = request.get_json()
        if payload == None:
            return jsonify({"message": "token Not found"}), 403
        
        data_list = [uuid for uuid in data.values()]
        user_id = payload['user_id']
        user_selected_level(user_id, data_list)
        sub_list = init_sub_list_of_user_sel_level(data_list) 
        print(f"yeh hai -> {sub_list}")
        '''
        yeh hai -> [['HTML Programming', ['LsEDzDjimSjV', 'MAD 1', 'This is MAD -1 subject']], ['HTML Programming', ['LsEDzDjimSjV', 'MAD 1', 'This is MAD -1 subject']], [], ['Vue JS Programming', []], [], ['C Programming', []], [], ['Java Programming', []]]
        '''
        return jsonify({"message": "Level selected successfully", "subjects": sub_list}), 200
    return jsonify({"message": "Currently get meathod is disable"}), 400

@app.route('/api/start/select_sub', methods=['POST'])
def select_sub():
    if request.method == 'POST':
        token = request.args.get('token')
        if token == None:
            return jsonify({"message": "Something is Fishy"}), 404
        payload, error_response, status_code = check_token(token)
        data = request.get_json()
        if payload == None:
            return jsonify({"message": f"{error_response}"}), 403
        
        data_list = [uuid for uuid in data.values()]
        user_id = payload['user_id']
        user_selected_sub(user_id, data_list)
        # print(data_list, user_id)
        # send the level id to user's in as user.user_level 
        # recieve list of aall subejcts of that level
        # recieve the subject list 
        # sub_list = init_chap_list_of_user_sel_sub(data_list) 
        # print(f"yeh hai -> {sub_list}")
        '''
        yeh hai -> [['HTML Programming', ['LsEDzDjimSjV', 'MAD 1', 'This is MAD -1 subject']], ['HTML Programming', ['LsEDzDjimSjV', 'MAD 1', 'This is MAD -1 subject']], [], ['Vue JS Programming', []], [], ['C Programming', []], [], ['Java Programming', []]]
        '''
        return jsonify({"message": "sub selected successfully"}), 200
    return jsonify({"message": "Currently get meathod is disable"}), 400


###### Dashboard #########

@app.route('/dashboard/chapter_n_quiz', methods=['GET'])
def user_dashboard_chapter():
    token = request.args.get('token')
    print(token, "Token in user_dashboard_chapter")

    payload, error_response, status_code = check_token(token)
    if payload == None:
        return jsonify({"message": f"{error_response}"}), status_code
    user_id = payload['user_id']
    print("yes")
    # check if user has some bookmarkmarked chapter or not
    user_favorite_chapter = user_selected_chap(user_id)
    if user_favorite_chapter:
        quiz_list = q1_list(user_favorite_chapter, user_id)
        return jsonify({"message": "User has some bookmarked chapter", 
                        "chapters": user_favorite_chapter,
                        "quiz": quiz_list}), 200
    else:
        # collect all chapters from user selected subjects
        chapters_from_sub = list_all_chapters_from_user_sel_sub(user_id)

        print(chapters_from_sub, "Chapters from user selected subjects")
        quiz_list = q2_list(chapters_from_sub, user_id)
        print(quiz_list, "Quiz list from chapters")
        return jsonify({
            "message": "User has no bookmarked chapter, but here are all chapters from selected subjects",
            "chapters": chapters_from_sub,
            "quiz": quiz_list
        }), 200

# this will return all chapters from all user selected subjects
@app.route('/dashboard/chapter_preference', methods=['GET'])
def user_dashboard_chapter_preference():
    if request.method == 'GET':
        token = request.args.get('token')
        if token == None:
            return jsonify({"message": "Something is Fishy"}), 404
        payload, error_response, status_code = check_token(token)
        if payload == None:
            return jsonify({"message": f"{error_response}"}), status_code
        print("List of all chapters from user selected subjects")

        user_id = payload['user_id']
        # collect the chapter names from backend and send the names to frontend
        list_all_chap_from_user_sel_sub = user_fav_sub_all_chap(user_id)
        return jsonify({
            "message": "User has some bookmarked chapter",
            "all_chapters": list_all_chap_from_user_sel_sub
        }), 200



        
        # return jsonify({"message": "User selected chapter stored successfully"}), 200
    return jsonify({"message": "Currently this meathod is disable"}), 400

# this will store the user selected chapter in user table
@app.route('/dashboard/user_chapter_preference', methods=['POST'])
def user_fix_his_preference():
    if request.method == 'POST':
        token = request.args.get('token')
        if token == None:
            return jsonify({"message": "Something is Fishy"}), 404
        payload, error_response, status_code = check_token(token)
        data = request.get_json()
        if payload == None:
            return jsonify({"message": f"{error_response}"}), status_code
        
        user_id = payload['user_id']
        print(data, "Data in user_fix_his_preference")


        set_user_chap_pref = user_chap_pref(user_id, data)

        
        return jsonify({"message": "User selected chapter stored successfully"}), 200
    return True



@app.route('/chapter/chapter_det_with_quiz/<chapter_id>', methods=['GET'])
def chapter_det_with_quiz(chapter_id):
    if request.method == 'GET':
        token = request.args.get('token')
        if token == None:
            return jsonify({"message": "Something is Fishy"}), 404
        payload, error_response, status_code = check_token(token)
        if payload == None:
            return jsonify({"message": f"{error_response}"}), status_code
        
        user_id = payload['user_id']
        # get the chapter details
        a = Chapter_view(chapter_id)
        # output is like : ['5Xa54fA8KFTx', 'HTML Coding Lession 1', 'This is HTML Coding Lession 1', [['homtjDOZggTv', 'HTML Coding Part 1', 'This is the First ever Quiz ', 40, 10.0, 5.0, datetime.datetime(2025, 6, 12, 0, 0), 10, 2, 2, 0]]]
        b = chap_info(chapter_id, user_id)
        chapter_info = [a[0], a[1], a[2], b]
        print(f"{chapter_info} +/n")
        print(f"a = {a}")
        # get the quiz details
        return jsonify({
            "message": "Chapter and Quiz details",
            "chapter_info": chapter_info,
        }), 200
    return jsonify({"message": "Currently this meathod is disable"}), 400
    

#################### QUIZ START #########################
@app.route('/quiz_info_start', methods=['GET'])
def quiz_info_start():
    if request.method == 'GET':
        token = request.args.get('token')
        if token == None:
            return jsonify({"message": "Something is Fishy"}), 404
        payload, error_response, status_code = check_token(token)
        if payload == None:
            return jsonify({"message": f"{error_response}"}), status_code
        
        user_id = payload['user_id']
        quiz_id = request.args.get('quiz_id')
        fdata = get_quiz_data(quiz_id)
        return jsonify({
            "quiz_data": fdata,
        }), 200
    return jsonify({"message": "Currently this meathod is disable"}), 400


@app.route('/quiz_submit/<quiz_id>/<attempt_number>', methods=['POST'])
def quiz_submit(quiz_id, attempt_number):
    if request.method == 'POST':
        token = request.args.get('token')
        if token == None:
            return jsonify({"message": "Something is Fishy"}), 404
        payload, error_response, status_code = check_token(token)
        if payload == None:
            return jsonify({"message": f"{error_response}"}), status_code
        user_id = payload['user_id']
            
        data = request.get_json()
        user_answers = data.get('userAnswers')
        store_ans(user_id, quiz_id, attempt_number, user_answers)

        return "yes"
    return jsonify({"message": "Currently this meathod is disable"}), 400


################### QUIZ SUMMARY #########################
@app.route('/quiz_summary_info/<quiz_id>/<attempt_number>', methods=['GET'])
def quiz_summary_info(quiz_id, attempt_number):
    if request.method == 'GET':
        token = request.args.get('token')
        if token == None:
            return jsonify({"message": "Something is Fishy"}), 404
        payload, error_response, status_code = check_token(token)
        if payload == None:
            return jsonify({"message": f"{error_response}"}), status_code
        user_id = payload['user_id']
        quizdet, score, correct_answer, questions,  useranswer  = quiz_summ_info(quiz_id, user_id, attempt_number) 
        print(quizdet, score, correct_answer, questions,  useranswer)
        return jsonify({
            "quiz_details": quizdet,
            "score": score,
            "questions": questions,
            "user_answer": useranswer,
            "correct_answer": correct_answer
        }), 200


    return jsonify({"message": "Currently this meathod is disable"}), 400



################# summary page #########################
@app.route('/u_summary_page', methods=['GET'])
def user_summary_page():
    if request.method == 'GET':
        token = request.args.get('token')
        if token == None:
            return jsonify({"message": "Something is Fishy"}), 404
        payload, error_response, status_code = check_token(token)
        if payload == None:
            return jsonify({"message": f"{error_response}"}), status_code
        
        user_id = payload['user_id']

        summary = user_summary(user_id)
        return jsonify({
            "message": "User summary",
            "summary": summary
        }), 200
    return jsonify({"message": "Currently this meathod is disable"}), 400



############### search page #########################



@app.route('/u/search', methods=['POST'])
def user_search():
    if request.method == 'POST':
        
        token = request.args.get('token')
        print("hi")
        if token == None:
            return jsonify({"message": "Something is Fishy"}), 404
        payload, error_response, status_code = check_token(token)
        if payload == None:
            return jsonify({"message": f"{error_response}"}), status_code
        user_id = payload['user_id']
        # take form data 
        parameter = request.form['parameter']
        querry = request.form['querry']
        search_dict = user_search_result(user_id, parameter, querry)
        print(search_dict)
        return jsonify({
            "message": "Search result",
            "search_result": search_dict
        }), 200
    return jsonify({"message": "Currently this meathod is disable"}), 400
    

############### Profile page ######################

@app.route('/u/profile', methods=['GET'])
def user_profile():
    if request.method == 'GET':
        token = request.args.get('token')
        if token == None:
            return jsonify({"message": "Something is Fishy"}), 404
        payload, error_response, status_code = check_token(token)
        if payload == None:
            return jsonify({"message": f"{error_response}"}), status_code
        
        user_id = payload['user_id']
        user_data = user_prof(user_id)
        print(user_data)
        return jsonify({
            "message": "User profile data",
            "user_data": user_data
        }), 200
    return jsonify({"message": "Currently this method is disabled"}), 400


@app.route('/u/profile/edit', methods=['POST'])
def user_profile_edit():
    if request.method == 'POST':
        token = request.args.get('token')
        if token == None:
            return jsonify({"message": "Something is Fishy"}), 404
        payload, error_response, status_code = check_token(token)
        if payload == None:
            return jsonify({"message": f"{error_response}"}), status_code
        
        user_id = payload['user_id']
        # take form data 

        uuid_from_form = request.form['id']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if uuid_from_form != user_id:
            return jsonify({"message": "Something is Fishy"}), 404


        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt(app.config['BCRYPT_LOG_ROUNDS'])
        ).decode('utf-8')
        update_user_profile(user_id, username,email, hashed_password) 
        return jsonify({
            "message": "User profile updated successfully"
        }), 200
        
        
@app.route('/u/profile/delete', methods=['POST'])
def user_profile_delete():
    if request.method == 'POST':
        token = request.args.get('token')
    if token == None:
        return jsonify({"message": "Something is Fishy"}), 404
    payload, error_response, status_code = check_token(token)
    if payload == None:
        return jsonify({"message": f"{error_response}"}), status_code
        
    user_id = payload['user_id']

    delete_user(user_id)
    return jsonify({
        "message": "User profile deleted successfully"
    }), 200








# Admin Routes
################## CREATE ROUTES #########################
@app.route('/admin_dashboard/create/level', methods=['GET', 'POST'])
def create_level():
    if request.method == 'POST':
        name = request.form['level_name']
        description = request.form['level_description']
        if name and description:
            verify_level(name)
            if verify_level(name)==None:
                id = generate_uuid()
                cre_level(id, name, description)
                cache.clear()
                return jsonify({
                    "message": "Level is Created Susscessfully N",
                    "level_id": id}), 200
            else:
                return jsonify({"error": " Level Already Exist"}), 409
        else:
            return jsonify({"error": "Please Provide level name and descriptions"}), 400
    return jsonify({"message": "Currently get meathod is disable"}), 415

# Create Subject
@app.route('/admin_dashboard/<level_id>/create/subject', methods=['GET', 'POST'])
def create_subject(level_id):
    if request.method == 'POST':
        name = request.form['subject_name']
        description = request.form['subject_description']
        if name and description:
            verify_subject(name, level_id)
            if verify_subject(name, level_id)==None:
                id = generate_uuid()
                cre_subject(id, name, description, level_id)
                cache.clear()
                return jsonify({
                    "message": "Subject is Created Susscessfully",
                    "level_id": level_id,
                    "subject_id": id}), 200
            else:

                return jsonify({"error": " Subject Already Exist"}), 409
        else:
            return jsonify({"error": "Please Provide subject name and descriptions"}), 400
    return jsonify({"message": "Currently get meathod is disable"}), 415

# create Chapter
@app.route('/admin_dashboard/<level_id>/level/<subject_id>/subject/create/chapter', methods=['POST'])
def create_chapter(level_id, subject_id):
    if request.method == 'POST':
        name = request.form['chapter_name']
        description = request.form['chapter_description']
        if name and description:
            verify_chapter(name, subject_id)
            if verify_chapter(name, subject_id)==None:
                uuid = generate_uuid()
                print(uuid, name, description, subject_id)
                cre_chapter(uuid, name, description, subject_id)
                cache.clear()
                return jsonify({"message": "Chapter is Created Susscessfully", "level_id": level_id, "subject_id": subject_id, "chapter_id": uuid}), 200
            else:
                return jsonify({"error": " Chapter Already Exist"}), 409
        else:
            return jsonify({"error": "Please Provide subject name and descriptions"}), 400
    return jsonify({"message": "Chapter is Created Susscessfully"}), 200

@app.route('/admin_dashboard/<level_id>/level/<subject_id>/subject/<chapter_id>/chapter/create/quiz', methods=['POST'])
def create_quiz(level_id, subject_id, chapter_id):
    if request.method == 'POST':
            title = request.form['quizTitle']
            description = request.form['quizDescription']
            max_marks = request.form['quizMaxMarks']
            correct_marks = request.form['quizcorrectscore']
            negative_marks = request.form['quizwrongscore']
            scheduled_date = request.form['quizScheduledDate']
            max_time = request.form['quizMaxTime']
            total_questions = request.form['quiztotalquestion']
            if title and description:
                if verify_prev_quiz(title, chapter_id) is None:
                    uuid = generate_uuid()
                    cre_quiz(
                        uuid, title, description, max_marks, 
                        correct_marks, negative_marks, chapter_id,
                        scheduled_date, max_time, total_questions
                    )
                    cache.clear()
                    return jsonify({
                        "message": "Quiz is Created Susscessfully",
                        "level_id": level_id,
                        "subject_id": subject_id,
                        "chapter_id": chapter_id,
                        "quiz_id": uuid}), 200
                else:
                    return jsonify({"error": "Quiz Already Exist"}), 409
            else:
                return jsonify({"error": "Please Provide quiz title and descriptions"}), 400
       
            # Create the quiz in the database
    return jsonify({"message": "Currently get meathod is disable"}), 415

@app.route('/api/admin_dashboard/<level_id>/level/<subject_id>/subject/<chapter_id>/chapter/<quiz_id>/quiz/create/question', methods=['POST'])
def create_question(level_id, subject_id, chapter_id, quiz_id):
    que_len = Question_length(quiz_id)
    if request.method == 'POST':
        data = request.get_json()
        print(data, "Data in create_question")
        for key, question_data in data.items():
            print(question_data, f"Processing data for {key}")

            if not question_data:
                print(f"Skipping empty data for {key}")
                continue  # skip if the question data is missing

            question = question_data.get('statement')
            options = question_data.get('options') 
            answer = question_data.get('correct')

            # Check if all required data is present
            if not all([question, options, answer]) or len(options) < 4:
                print(f"Skipping incomplete question: {question}")
                continue

            option_a = options[0]
            option_b = options[1]
            option_c = options[2]
            option_d = options[3]

            if verify_prev_question(question, quiz_id) is None:
                uuid = generate_uuid()
                create_quest(
                    uuid, quiz_id, question, option_a, option_b, option_c, option_d, answer
                )
                cache.clear()
                print("Question created successfully:", question)
            else:
                print(f"Question '{question}' already exists. Skipping.")
                # If  want to stop everything,   keep the return statement:
                # return jsonify({"error": f"Question '{question}' already exists"}), 409

        return jsonify({
            "message": "Questions created successfully",
            "level_id": level_id,
            "subject_id": subject_id,
            "chapter_id": chapter_id,
            "quiz_id": quiz_id
        }), 200

    return jsonify({"message": "Currently, GET method is disabled"}), 415

############# READ/VIEW RoUTE ###########
@app.route('/api/admin_dashboard')
@cache.cached(timeout=300)
def admin_dashboard():
    info = admin_dashboard_view()
    return jsonify({"message": "Welcome to the Admin Dashboard!", "info": info}), 200

@app.route('/api/admin_dashboard/level/<level_id>', methods=['GET'])
@cache.cached(timeout=300)
def view_level(level_id):
    info = Level_view(level_id)
    return jsonify({"message": "Now You can view Level details", "info": info}), 200

@app.route('/api/admin_dashboard/subject/<subject_id>', methods=['GET'])
@cache.cached(timeout=300)
def view_subject(subject_id):
    info  = Subject_view(subject_id)
    return jsonify({"message": "Now You can view Subject details", "info": info}), 200

@app.route('/api/admin_dashboard/<level_id>/level/<subject_id>/subject/<chapter_id>', methods=['GET'])
@cache.cached(timeout=300)
def view_chapter(level_id, subject_id, chapter_id):
    info = Chapter_view(chapter_id)
    return jsonify({"message": "Now You can view Chapter details", "info": info}), 200

@app.route('/api/admin_dashboard/<level_id>/level/<subject_id>/subject/<chapter_id>/chapter/<quiz_id>/quiz/que_length', methods=['GET'])
@cache.cached(timeout=300)
def get_quiz_que_length(level_id, subject_id, chapter_id, quiz_id):
    quiz_title = quiz_tit(quiz_id)
    info = [Que_length(quiz_id), quiz_title.title, Chapter_view(chapter_id)[1], Subject_view(subject_id)[1]]
    return jsonify({"message": "Now You can view Quiz details", "info": info,}), 200

@app.route('/api/admin_dashboard/<level_id>/level/<subject_id>/subject/<chapter_id>/chapter/<quiz_id>/quiz/get_questions', methods=['GET'])
@cache.cached(timeout=300)
def get_question(level_id, subject_id, chapter_id, quiz_id):

    ques = ques_det(quiz_id)
    info = [Question_length(quiz_id), ques]
    return jsonify({"message": "Now You can view Quiz details", "info": info,}), 200

############ UPDATE/EDIT ROUTE ############
@app.route('/admin_dashboard/<level_id>/update/level', methods=['POST'])
def update_level_det(level_id):
    if request.method == 'POST':
        name = request.form['level_name']
        description = request.form['level_description']
        print(name, description)
        update_level(level_id, name, description)
        cache.clear()
        return jsonify({"message": "Level is Updated Susscessfully", }), 200
    return jsonify({"message": "There are some Errors in your request"}), 400

@app.route('/admin_dashboard/<level_id>/level/<subject_id>/update/subject', methods=['POST'])
def update_subject_det(level_id, subject_id):
    if request.method == 'POST':
        title = request.form['subject_name']
        description = request.form['subject_description']
        
        print(title, description, "Received form data")
        update_subject(subject_id, title, description)
        cache.clear()
        return jsonify({"message": "Subject is Updated Susscessfully", }), 200
    return jsonify({"message": "There are some Errors in your request"}), 400

@app.route('/admin_dashboard/<level_id>/level/<subject_id>/subject/<chapter_id>/update/chapter', methods=['POST'])
def update_chap_det(level_id, subject_id, chapter_id):
    if request.method == 'POST':
        title = request.form['chapter_name']
        description = request.form['chapter_description']
        print(title, description, "Received form data")
        update_chapter(chapter_id, title, description)
        cache.clear()
        return jsonify({"message": "Chapter is Updated Susscessfully", }), 200
    return jsonify({"message": "There are some Errors in your request"}), 400

@app.route('/admin_dashboard/<level_id>/level/<subject_id>/subject/<chapter_id>/chapter/<quiz_id>/update/quiz', methods=['POST'])
def update_quiz_det(level_id, subject_id, chapter_id, quiz_id):
    if request.method == 'POST':
        title = request.form['quizTitle']
        description = request.form['quizDescription']
        max_marks = int(request.form['quizMaxMarks'])
        correct_marks = float(request.form['quizcorrectscore'])
        negative_marks = float(request.form['quizwrongscore'])
        scheduled_date = request.form['quizScheduledDate']
        max_time = int(request.form['quizMaxTime'])
        total_questions = int(request.form['quiztotalquestion'])
        # print(scheduled_date)
        update_quiz(quiz_id, title, description, max_marks, correct_marks, negative_marks, scheduled_date, max_time, total_questions)
        cache.clear()
        return jsonify({"message": "Quiz is Updated Susscessfully", }), 200
    return jsonify({"message": "There are some Errors in your request"}), 400

@app.route('/admin_dashboard/<level_id>/level/<subject_id>/subject/<chapter_id>/chapter/<quiz_id>/quiz/<question_id>/update/question', methods=['POST'])
def update_question_det(level_id, subject_id, chapter_id, quiz_id, question_id):
    if request.method == 'POST':
        question = request.form['question']
        option_a = request.form['option1']
        option_b = request.form['option2']
        option_c = request.form['option3']
        option_d = request.form['option4']
        answer = request.form['correct_option']

        update_question(question_id, question, option_a, option_b, option_c, option_d, answer)
        cache.clear()
        return jsonify({"message": "Question is Updated Susscessfully", }), 200
    return jsonify({"message": "There are some Errors in your request"}), 400

############### DELETE/REMOVE ROUTE ###############
@app.route('/admin_dashboard/<level_id>/level/<subject_id>/subject/<chapter_id>/chapter/<quiz_id>/quiz/<question_id>/delete/question', methods=['DELETE'])
def delete_question_det(level_id, subject_id, chapter_id, quiz_id, question_id):
    if request.method == 'DELETE':
        try:
            delete_question(question_id)
            cache.clear()

            return jsonify({"message": "Question is Deleted Susscessfully", }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"message": "There are some Errors in your request"}), 400

@app.route('/admin_dashboard/<level_id>/level/<subject_id>/subject/<chapter_id>/chapter/<quiz_id>/delete/quiz', methods=['DELETE'])
def delete_quiz_det(level_id, subject_id, chapter_id, quiz_id):
    if request.method == 'DELETE':
        try:
            delete_quiz(quiz_id)
            cache.clear()

            return jsonify({"message": "Quiz is Deleted Susscessfully", }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"message": "There are some Errors in your request"}), 400

@app.route('/admin_dashboard/<level_id>/level/<subject_id>/subject/<chapter_id>/delete/chapter', methods=['DELETE'])
def delete_chapter_det(level_id, subject_id, chapter_id):
    if request.method == 'DELETE':
        try:
            delete_chapter(chapter_id)
            cache.clear()

            return jsonify({"message": "Chapter is Deleted Susscessfully", }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"message": "There are some Errors in your request"}), 400

@app.route('/admin_dashboard/<level_id>/level/<subject_id>/delete/subject', methods=['DELETE'])
def delete_subject_det(level_id, subject_id):
    if request.method == 'DELETE':
        try:
            delete_subject(subject_id)
            cache.clear()

            return jsonify({"message": "Subject is Deleted Susscessfully", }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"message": "There are some Errors in your request"}), 400

@app.route('/admin_dashboard/<level_id>/delete/level', methods=['DELETE'])
def delete_level_det(level_id):
    if request.method == 'DELETE':
        try:
            delete_level(level_id)
            cache.clear()

            return jsonify({"message": "Level is Deleted Susscessfully", }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"message": "There are some Errors in your request"}), 400



############## SEARCH ROUTE ##################
@app.route('/api/admin/search', methods=['GET', 'POST'])
def admin_search_api():
    if request.method == 'POST':
        param = request.form['parameter']
        query = request.form['query']
        if not param or not query:
            return jsonify({"error": "Missing 'parameter' or 'query'"}), 400

        results = admin_search_result(param, query)

        if not results:
            return jsonify({"results": [], "message": "No results found."}), 200

        return jsonify({"results": results}), 200


############ USER CNTRL ###################
@app.route('/api/admin/find_users', methods=['GET'])
def find_users_api():
    if request.method == 'GET':
        query_str = request.args.get('query')
        print(f"fall fvjf{query_str}")
        if query_str:
            search_pattern = f"%{query_str}%"
            find_users = find_usr(query_str)
            return jsonify({"users": find_users}), 200

@app.route('/api/admin/block_user', methods=['POST'])
def block_users_api():
    if request.method == 'POST':
        user_id = request.json.get('user_id')
        print(user_id)
        block_user(user_id)
        return jsonify({"message": "User blocked successfully"}), 200
    return jsonify({"message": "There are some Errors in your request"}), 400

@app.route('/api/admin/unblock_user', methods=['POST'])
def unblock_users_api():
    if request.method == 'POST':
        user_id = request.json.get('user_id')
        unblock_user(user_id)
        return jsonify({"message": "User unblocked successfully"}), 200
    return jsonify({"message": "There are some Errors in your request"}), 400


############ ADMIN OTP #################

@app.route('/', methods=['GET'])
@cache.cached(timeout=300)
def index():
    if request.method == 'GET':
        check_n_add_admin()
        return jsonify({"message": "Admin Check sussfully"})
    return jsonify({"error": "Invalid request method"}), 405


@app.route('/api/request_otp', methods=['POST'])
def request_admin_otp():
    if request.method == 'POST':
        email = request.form['email']
        print(email)
        if not email:
            return jsonify({"error": "Email is required"}), 400

        # Find the admin using your existing function
        admin = find_admin(email)
        if not admin:
            return jsonify({"error": "Admin account not found"}), 404

        # Call the function DIRECTLY.
        # The user's request will now WAIT for the email to be sent.
        success = send_otp_for_admin(admin)

        if success:
            return jsonify({"message": "OTP has been sent to the admin email address."}), 200
        else:
            return jsonify({"error": "Failed to send OTP email. Please try again later."}), 500

    return jsonify({"error": "Invalid request method"}), 405


@app.route('/api/verify_otp', methods=['POST'])
def verify_otp():
    if request.method == 'POST':
        email = request.form['email']
        user_otp = request.form['otp']

        if not email or not user_otp:
            return jsonify({"error": "Email and OTP are required"}), 400

        # Check if the provided OTP matches the one we stored
        correct_otp = actual_otp(email)
        if correct_otp and correct_otp == user_otp:
            payload = {
                'admin_email': email,
            }
            token = jwt.encode(
                payload, 
                app.config['SECRET_KEY'], 
                algorithm='HS256'
            )

            return jsonify({"message": "OTP verified successfully", "admin_token": token}), 200
        else:
            # The frontend will catch this error and ask again.
            return jsonify({"error": "Invalid OTP"}), 401
    return jsonify({"error": "Invalid request method"}), 405

    

################### ADMIN SUMMARY #####################
@app.route('/admin_dashboard/summary', methods=['GET'])
def admin_summary():
    # 1. Get the complete summary data from the helper function.
    # This dictionary already has almost everything we need.
    summary_data = get_admin_summary()
    return jsonify(summary_data), 200
    


processes = []

def start_background_services():
    """A helper function to start the Celery services."""
    print("--- Starting Background Services (Main Process Only) ---")

    # Command to start the Celery Worker.
    # '--pool=solo' is crucial for Windows compatibility.
    worker_cmd = ["celery", "-A", "app.celery", "worker", "--pool=solo", "--loglevel=info"]
    worker_p = subprocess.Popen(worker_cmd)
    processes.append(worker_p)
    print(f"Celery Worker started with PID: {worker_p.pid}")

    # Command to start the Celery Beat (the scheduler)
    beat_cmd = ["celery", "-A", "app.celery", "beat", "--loglevel=info"]
    beat_p = subprocess.Popen(beat_cmd)
    processes.append(beat_p)
    print(f"Celery Beat started with PID: {beat_p.pid}")


def stop_background_services():
    """A helper function to stop the services when press CTRL+C."""
    print("\n--- Stopping all background services... ---")
    for p in processes:
        p.terminate()  # Ask the process to stop
    print("--- Shutdown complete. ---")




# This is the main entry point of our script.
if __name__ == '__main__':

    # THE CRUCIAL CHECK:
    # We only start Celery if we are in the MAIN process.
    # If 'WERKZEUG_RUN_MAIN' is 'true', we are in the child (reloaded) process, so we skip starting Celery.
    if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        with app.app_context():
            print("--- Checking and creating database tables... ---")
            # This line is the key: it creates the .sqlite3 file and all your tables.
            db.create_all()
            print("--- Database is ready. ---")
        # 1. Start the Celery Worker and Beat in the background.
        start_background_services()

        # 2. Register cleanup to run ONLY when the main process exits (CTRL+C).
        atexit.register(stop_background_services)

    # 3. Start the Flask web server.
    print("--- Starting Flask Web Server (Reloader Active) ---")
    print(f"Visit http://127.0.0.1:5000 or on port 5000 in your browser.")

    # We keep debug=True (which enables the reloader by default)
    app.run(debug=True, port=5000)
