from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, or_
from flask_cors import CORS
import json
from app import app
import unittest

class QuestionsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.question = {
                            "quiz_id" : 1,
                            "question" : "A",
                            "qn_type" : "tf",
                            "options" : "null",
                            "answer" : "A"
                        }

    def test_question_creation(self):
        res = self.app.post('/quiz/createQuestion', data=json.dumps(dict(self.question)), content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertIn('A', str(res.data))

    # def tearDown(self):
    #     with self.app.app_context():
    #         # drop all tables
    #         db.session.remove()
    #         db.drop_all()


if __name__ == "__main__":
    unittest.main()