from app import app, db, Course
import json
import unittest
from app import CourseMaterials


from datetime import datetime

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

# Chia Ling Li (START)
class CourseMaterialsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

        with app.app_context():
            db.create_all()
            cm1 = CourseMaterials(course_id = 1,
                            class_id = 1,
                            chapter_id = 1,
                            subchapter_id = "1a",
                            chapter_name = "Introduction to Python",
                            content = "https://bingchilling.s3.ap-southeast-1.amazonaws.com/IS212+Week+1+-+Introduction.pdf")
            db.session.add(cm1)
            db.session.commit()
    
    def test_to_dict(self):
        m1 = CourseMaterials(course_id=1,class_id=1,
                          chapter_id=1, 
                          subchapter_id='1a',
                          chapter_name='Introduction to Python',
                          content='https://bingchilling.s3.ap-southeast-1.amazonaws.com/IS212+Week+1+-+Introduction.pdf')
        
        self.assertEqual(m1.to_dict(), {
            "course_id" : 1,
            "class_id" : 1,
            "chapter_id" : 1,
            "subchapter_id" : "1a",
            "chapter_name" : "Introduction to Python",
            "content" : "https://bingchilling.s3.ap-southeast-1.amazonaws.com/IS212+Week+1+-+Introduction.pdf"
            }
        )

    # Retrieve materials by chapter_id, class_id and course_id
    def test_find_by_chapter_id(self):
        res = self.app.get('/mono/chapterMaterial/1/1/1/1')
        self.assertEqual(res.status_code, 200)
        self.assertIn('1a', str(res.data))

    # Error in retrieving materials by chapter_id, class_id and course_id
    def test_find_by_chapter_id_404(self):
        res = self.app.get('/mono/chapterMaterial/1/1/1/3')
        self.assertEqual(res.status_code, 404)
        self.assertIn('3', str(res.data))

    # Retrieve all the chapters available for the class and course
    def test_get_chapIdBy_courseClass(self):
        res = self.app.get('/mono/allChaps/1/1')
        self.assertEqual(res.status_code, 200)
        self.assertIn('1', str(res.data))
    
    # This combination of classid, courseid and chapterid is valid
    def test_check_chapterValid(self):
        res = self.app.get('/mono/chapterValid/1/1/1')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Introduction to Python', str(res.data))

    # This combination of classid, courseid and chapterid is NOT valid
    def test_check_chapterValid_404(self):
        res = self.app.get('/mono/chapterValid/4/2/1')
        self.assertEqual(res.status_code, 404)
        self.assertIn('', str(res.data))

    def tearDown(self):
        db.session.remove()
        db.drop_all()
# Chia Ling Li (END)

# Trisha Olegario (START)
class CourseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        
        with app.app_context():
            db.create_all()
            c1 = Course(
                CourseID = 1,
                CourseName = 'Python Basics',
                PreReq = None,
                Classes = 3,
                StartEnroll = datetime(2021, 10, 1, 0,0,0),
                EndEnroll = datetime(2021,10, 8, 0,0,0),
                Open = 0,
                CreatedBy = 1,
                UpdatedBy = None,
                CreatedTime = datetime(2021, 10, 10, 22,28,29),
                UpdateTime = None,
                IsFull = 0
            )

            db.session.add(c1)
            db.session.commit()
    
    def test_to_dict(self):
        c1 = Course(
                CourseID = 1,
                CourseName = 'Python Basics',
                PreReq = None,
                Classes = 3,
                StartEnroll = datetime(2021, 10, 1, 0,0,0),
                EndEnroll = datetime(2021,10, 8, 0,0,0),
                Open = 0,
                CreatedBy = 1,
                UpdatedBy = None,
                CreatedTime = datetime(2021, 10, 10, 22,28,29),
                UpdateTime = None,
                IsFull = 0
            )
        self.assertEqual(c1.to_dict(), {
                'Classes': 3,
                'CourseID': 1,
                'CourseName': 'Python Basics',
                'CreatedBy': 1,
                'CreatedTime': datetime(2021, 10, 10, 22,28,29),
                'EndEnroll': datetime(2021,10, 8, 0,0,0),
                'IsFull': 0,
                'Open': 0,
                'PreReq': None,
                'StartEnroll': datetime(2021, 10, 1, 0,0,0),
                'UpdateTime': None,
                'UpdatedBy': None
        })
    
    def test_get_courses(self):
        res = self.app.get("/view_all_courses")
        self.assertEqual(res.status_code, 200)
        self.assertIn('Python Basics', str(res.data))
    
    def test_get_course_details(self):
        res = self.app.get("/get_course/1")
        self.assertEqual(res.status_code, 200)
        self.assertIn('Python Basics', str(res.data))
    
    def test_get_course_details_error(self):
        res = self.app.get("get_course/6")
        self.assertEqual(res.status_code, 404)

    def test_get_courses_by_admin(self):
        res = self.app.get("admin_courses/1")
        self.assertEqual(res.status_code, 200)
        self.assertIn('Python Basics', str(res.data))

    def test_get_courses_by_admin_error(self):
        res = self.app.get("admin_courses/3")
        self.assertEqual(res.status_code, 404)
    
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
# Trisha Olegario (END)

if __name__ == "__main__":
    unittest.main()