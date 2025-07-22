from models.model import Level, Subject, User, Chapter, Quiz, UserAnswer, UserQuizAttempt, Question


def quiz_summ_info(quiz_id, user_id, attempt_number):
    quizDetails = {}
    name = Quiz.query.filter_by(uuid=quiz_id).first()
    quizDetails['title'] = name.title
    ch_name = Chapter.query.filter_by(uuid=name.chapter_uuid).first()
    quizDetails['chapter_name'] = ch_name.name
    quizDetails['max_score'] = name.max_score
    quizDetails['positive_marking'] = name.correct_score
    quizDetails['negative_marking'] = name.wrong_score




    score = {}
    userattempt = UserQuizAttempt.query.filter_by(quiz_uuid=quiz_id, user_uuid=user_id, attempt_number=attempt_number).first()
    score['total'] = name.max_score
    score['user_score'] = userattempt.score

    quest = []
    questions = Question.query.filter_by(quiz_uuid=quiz_id).all()
    for question in questions:
        quest.append({
            'question_id': question.uuid,
            'question': question.question_statement,
            'option1': question.option1,
            'option2': question.option2,
            'option3': question.option3,
            'option4': question.option4,
        })
    
    correct_ans = {}
    for q in questions:
        correct_ans[q.uuid] = q.correct_option
    
    user_ans = {}
    user_answers = UserAnswer.query.filter_by(quiz_uuid=quiz_id, user_uuid=user_id, attempt_no=attempt_number).all()
    for ans in user_answers:
        user_ans[ans.question_uuid] = ans.selected_option

    return quizDetails, score, correct_ans, quest,  user_ans