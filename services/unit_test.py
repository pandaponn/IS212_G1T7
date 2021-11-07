from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, or_
from flask_cors import CORS
import json
from app import app, db
import unittest

class QuestionsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:8889/spm_test'
        db.create_all()
        self.question_tf = {
                            "quiz_id" : 1,
                            "question" : "A",
                            "qn_type" : "tf",
                            "options" : "null",
                            "answer" : "A"
                        }
        self.question_mcq = {
                                "quiz_id" : 1,
                                "question" : "What to do tomorrow?",
                                "qn_type" : "mcq",
                                "options" : "Work^Sleep^Nap^Eat",
                                "answer" : "Eat"
                            }
        self.retrieve_all = {
                                "quiz_id" : 1
                            }
        self.retrieve_question = {
                                    "question_id" : 1
                                }

    # Create a True/False question in a quiz
    def test_question_creation_tf(self):
        res = self.app.post('/quiz/createQuestion', data=json.dumps(dict(self.question_tf)), content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertIn('A', str(res.data))

    # Create an MCQ question in a quiz
    def test_question_creation_mcq(self):
        res = self.app.post('/quiz/createQuestion', data=json.dumps(dict(self.question_mcq)), content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertIn('Eat', str(res.data))

    # Retrieve all questions for specific quiz on create_quiz.html
    def test_retrieve_all_questions(self):
        self.app.post('/quiz/createQuestion', data=json.dumps(dict(self.question_tf)), content_type='application/json')
        res = self.app.post('/quiz/retrieveAllQuestions', data=json.dumps(dict(self.retrieve_all)), content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertIn('A', str(res.data))

    # Retrieve specific question for specific quiz on create_quiz.html
    def test_retrieve_question(self):
        self.app.post('/quiz/createQuestion', data=json.dumps(dict(self.question_mcq)), content_type='application/json')
        res = self.app.post('/quiz/retrieveQuestion', data=json.dumps(dict(self.retrieve_question)), content_type='application/json')
        self.assertEqual(res.status_code, 201)

    def tearDown(self):
        db.session.remove()
        db.drop_all()


if __name__ == "__main__":
    unittest.main()