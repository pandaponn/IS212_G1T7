from datetime import datetime
from app import app, db
import json
import unittest
from app import CourseMaterials, Learner, CourseClass

# Lim Zhi Hao (START)
class QuestionsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
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
# Lim Zhi Hao (END)


# Kaldora Ng Kai Ying (START)
class ClassesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        with app.app_context():
            db.create_all()
            l1 = Learner(LearnerID = 1,
                        EngineerID = 1,
                        LearnerName = "LingLi",
                        CourseID = 1,
                        ClassID = 1,
                        assigned = 1,
                        approved = 1,
                        CourseCompleted = 0)
            
            l2 = Learner(LearnerID = 2,
                        EngineerID = 1,
                        LearnerName = "Kaldora",
                        CourseID = 1,
                        ClassID = 1,
                        assigned = 0,
                        approved = None,
                        CourseCompleted = 0)

            class1 = CourseClass(ClassId = 1,
                        CourseId = 1,
                        CourseName = "Python Basics",
                        TrainerId = 1,
                        StartDateTime = datetime(2021, 6, 14, 8, 15, 0),
                        EndDateTime = datetime(2021, 12, 14, 8, 15, 0),
                        Capacity = 40,
                        SlotsAvailable = 35)

            db.session.add(l1)
            db.session.add(l2)
            db.session.add(class1)
            db.session.commit()

    def test_to_dict_learner(self):
        l1 = Learner(LearnerID = 1,
                        EngineerID = 1,
                        LearnerName = "LingLi",
                        CourseID = 1,
                        ClassID = 1,
                        assigned = 1,
                        approved = 1,
                        CourseCompleted = 0)
                        
        self.assertEqual(l1.to_dict(), {
            "LearnerID" : 1,
            "EngineerID" : 1,
            "LearnerName" : "LingLi",
            "CourseID" : 1,
            "ClassID" : 1,
            "assigned" : 1,
            "approved" : 1,
            "CourseCompleted": 0
            }
        )

    # Get specific learner details
    def test_learner_details(self):
        res = self.app.get('/view_learner_details/1')
        self.assertEqual(res.status_code, 200)
        self.assertIn('1', str(res.data))

    # Get learners class list for specific course and class list
    def test_class_list(self):
        res = self.app.get('/view_class_list/1/1/1')
        self.assertEqual(res.status_code, 200)
        self.assertIn('1', str(res.data))

    # Get Learner with pending and not assigned to any course 
    def test_pending_courses(self):
        res = self.app.get('/pending_courses')
        self.assertEqual(res.status_code, 200)
        self.assertIn('2', str(res.data))

    # Get all classes under a specific course
    def test_class(self):
        res = self.app.get('/class_details/1')
        self.assertEqual(res.status_code, 200)
        self.assertIn('1', str(res.data))

    # check if content returned is application/json
    def test_class_content(self):
        tester = app.test_client(self)
        response = tester.get("/class_details/1")
        self.assertEqual(response.content_type, "application/json")

    # check for class data returned
    def test_class_data(self):
        tester = app.test_client(self)
        response = tester.get("/class_details/1")
        self.assertTrue(b'data' in response.data)

    # def test_assign_trainer(self):
    #     class1 = CourseClass(ClassId = 1,
    #                     CourseId = 1,
    #                     CourseName = "Python Basics",
    #                     TrainerId = 1,
    #                     StartDateTime = datetime(2021, 6, 14, 8, 15, 0),
    #                     EndDateTime = datetime(2021, 12, 14, 8, 15, 0),
    #                     Capacity = 40,
    #                     SlotsAvailable = 35)

    #     res = self.app.put('/assign_engineer/1/1/1', data=json.dumps(dict(class1)), content_type='application/json')
    #     self.assertEqual(res.status_code, 201)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
# Kaldora Ng Kai Ying (END)

if __name__ == "__main__":
    unittest.main()