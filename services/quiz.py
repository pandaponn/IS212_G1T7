from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, or_
from flask_cors import CORS
import json
from os import environ


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:8889/spm'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)

db = SQLAlchemy(app)  

class Questions(db.Model):
    __tablename__ = 'questions'
    question_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quiz_id = db.Column(db.Integer, nullable=False)
    qn_type = db.Column(db.String(65535), nullable=False)
    question = db.Column(db.String(65535), nullable=False)
    options = db.Column(db.String(65535), nullable=True)
    answer = db.Column(db.String(65535), nullable=False)

    def __init__(self, quiz_id, qn_type, question, options, answer):
        self.quiz_id = quiz_id
        self.qn_type = qn_type
        self.question = question
        self.options = options
        self.answer = answer

    def json(self):
        return {"question_id": self.question_id, "quiz_id": self.quiz_id, "qn_type": self.qn_type, "question": self.question, "options": self.options, "answer": self.answer}


# Create Quiz Question
@app.route("/quiz/createQuestion", methods=['POST'])
def create_question():

    data = request.get_json()
    app = Questions(**data)
    try: 
        db.session.add(app)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the question."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": {
                'question_id' : app.question_id,
                'quiz_id' : app.quiz_id,
                'qn_type' : app.qn_type,
                'question' : app.question,
                'options' : app.options,
                'answer' : app.answer
            }
        }
    ), 201
    
# Retrieve all questions for specific quiz on create_quiz.html
@app.route("/quiz/retrieveAllQuestions", methods=['POST'])
def retrieveAllQuestions():
    data = request.get_json()
    quiz_id = data['quiz_id']
    # quiz_id = 1

    qn_list = Questions.query.filter_by(quiz_id=quiz_id)
    allQuestions = []
    for qn in qn_list:

        output = {
            'question_id' : qn.question_id,
            'quiz_id' : qn.quiz_id,
            'qn_type' : qn.qn_type,
            'question' : qn.question,
            'options' : qn.options,
            'answer' :  qn.answer
        }

        allQuestions.append(output)
        
    if allQuestions:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "questions": allQuestions
                }
            }
        )
    print(allQuestions)

    return jsonify(
        {
            "code": 404,
            "message": "Questions not found."
        }
    ), 404

# Retrieve all questions for specific quiz on create_quiz.html
@app.route("/quiz/retrieveQuestion", methods=['POST'])
def retrieveQuestion():
    data = request.get_json()
    question_id = data['question_id']

    qn_list = Questions.query.filter_by(question_id=question_id)
    for qn in qn_list:

        output = {
            'question_id' : qn.question_id,
            'quiz_id' : qn.quiz_id,
            'qn_type' : qn.qn_type,
            'question' : qn.question,
            'options' : qn.options,
            'answer' :  qn.answer
        }

    if output:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "questions": output
                }
            }
        )

    return jsonify(
        {
            "code": 404,
            "message": "Questions not found."
        }
    ), 404


class Quiz(db.Model):
    __tablename__ = 'quiz'
    quiz_id = db.Column(db.Integer, primary_key=True, nullable=False)
    quiz_name = db.Column(db.String(65535), nullable=True)
    course_id = db.Column(db.Integer, primary_key=False, nullable=False)
    class_id = db.Column(db.Integer, primary_key=False, nullable=False)
    chapter_id = db.Column(db.Integer, primary_key=False, nullable=False)
    isGraded = db.Column(db.String(65535), nullable=False)
    passing_grade = db.Column(db.String(65535), nullable=False)

    def __init__(self, quiz_name, course_id, class_id, chapter_id, isGraded, passing_grade):
        self.quiz_name = quiz_name
        self.course_id = course_id
        self.class_id = class_id
        self.chapter_id = chapter_id
        self.isGraded = isGraded
        self.passing_grade = passing_grade

    def json(self):
        return {"quiz_id": self.quiz_id, "quiz_name": self.quiz_name, "course_id": self.course_id, "class_id": self.class_id, "chapter_id": self.chapter_id, "isGraded": self.isGraded, "passing_grade": self.passing_grade}

# create Quiz Entry inside quiz table (quiz_id=auto_increment, isGraded="N", passing_grade=0)
@app.route("/quiz/createQuizInfo", methods=['POST'])
def create_quiz_info():
    data = request.get_json()
    app = Quiz(**data)
    try: 
        db.session.add(app)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the quiz."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": {
                'quiz_id' : app.quiz_id,
                'isGraded' : app.isGraded,
                'passing_grade' : app.passing_grade
            }
        }
    ), 201

# update Passing Grade & Graded 
@app.route("/quiz/updateQuizGrading", methods=['PUT'])
def update_quiz_grading():
    data = request.get_json()
    quiz = Quiz.query.filter_by(quiz_id=data['quiz_id']).first()
    if quiz: 
        quiz.isGraded = data['isGraded']
        quiz.passing_grade = data['passing_grade']
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data":  {
                    'quiz_id' : data['quiz_id'],
                    'isGraded' : data['isGraded'],
                    'passing_grade' : data['passing_grade']
                }
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            
            "message": "Quiz not found."
        }
    ), 404

# retrieve Quiz Information
@app.route("/quiz/retrieveQuizInfo", methods=['POST'])
def retrieveQuizInfo():
    data = request.get_json()
    quiz_id = data['quiz_id']

    quiz = Quiz.query.filter_by(quiz_id=quiz_id)
    for q in quiz:
        output = {
            'quiz_name' : q.quiz_name,
            'course_id' : q.course_id,
            'class_id' : q.class_id,
            'chapter_id' : q.chapter_id,
            'passing_grade' : q.passing_grade,
            'isGraded' : q.isGraded
        }

    if output:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "quiz": output
                }
            }
        )

    return jsonify(
        {
            "code": 404,
            "message": "Quiz not found."
        }
    ), 404

# update Quiz Name
@app.route("/quiz/updateQuizName", methods=['PUT'])
def update_quiz_name():
    data = request.get_json()
    quiz = Quiz.query.filter_by(quiz_id=data['quiz_id']).first()
    if quiz: 
        quiz.quiz_name = data['quiz_name']
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data":  {
                    'quiz_id' : data['quiz_id'],
                    'quiz_name' : data['quiz_name']
                }
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            
            "message": "Quiz not found."
        }
    ), 404

class QuizResults(db.Model):
    __tablename__ = 'quiz_results'
    learner_id = db.Column(db.Integer, primary_key=True, nullable=False)
    quiz_id = db.Column(db.Integer, primary_key=True, nullable=False)
    score = db.Column(db.Integer, primary_key=False, nullable=False)
    quizPass = db.Column(db.Integer, primary_key=False, nullable=False)
    isViewable = db.Column(db.Integer, primary_key=False, nullable=False)
    attempts = db.Column(db.Integer, primary_key=False, nullable=False)

    def __init__(self, learner_id, quiz_id, score, quizPass, isViewable, attempts):
        self.learner_id = learner_id
        self.quiz_id = quiz_id
        self.score = score
        self.quizPass = quizPass
        self.isViewable = isViewable
        self.attempts = attempts

    def json(self):
        return {"learner_id": self.learner_id, "quiz_id": self.quiz_id, "score": self.score, "quizPass": self.quizPass, "isViewable": self.isViewable, "attempts": self.attempts}

# update score & quizPass
@app.route("/quiz/updateQuizResults", methods=['PUT'])
def update_quiz_results():
    data = request.get_json()
    quiz = QuizResults.query.filter_by(quiz_id=data['quiz_id']).first()
    if quiz: 
        if data['score'] > quiz.score:
            quiz.score = data['score']
            quiz.quizPass = data['quizPass']
            quiz.attempts = quiz.attempts + 1
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data":  {
                        'quiz_id' : data['quiz_id'],
                        'score' : data['score'],
                        'quizPass' : data['quizPass']
                    }
                }
            ), 200
        else:
            quiz.attempts = quiz.attempts + 1
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data":  {
                        'quiz_id' : data['quiz_id'],
                        'score' : data['score'],
                        'quizPass' : data['quizPass']
                    },
                    "message": "Quiz score not updated as previous result is better."
                }
            ), 200
    return jsonify(
        {
            "code": 404,
            
            "message": "Quiz not found."
        }
    ), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
