from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, or_
from flask_cors import CORS
import json
from os import environ

from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/is212_project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                           'pool_recycle': 280}

db = SQLAlchemy(app)

CORS(app)

class Learner(db.Model):
    __tablename__ = 'Learner'

    LearnerID = db.Column(db.Integer, primary_key=True)
    EngineerID = db.Column(db.Integer, nullable=False)
    LearnerName = db.Column(db.String(100), nullable=False)
    CourseID = db.Column(db.Integer, primary_key=True)
    ClassID = db.Column(db.Integer, primary_key=True)
    assigned = db.Column(db.Integer, nullable=False)
    approved = db.Column(db.Integer, nullable=True)
    CourseCompleted = db.Column(db.Integer, nullable=True) # 0/1 --> boolean

    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

class Course(db.Model):
    __tablename__ = 'Course'

    CourseID = db.Column(db.Integer, primary_key=True)
    CourseName = db.Column(db.String(100), nullable=False)
    PreReq = db.Column(db.Integer, nullable=True)
    Classes = db.Column(db.Integer, nullable=False)
    StartEnroll = db.Column(db.DateTime, nullable=False)
    EndEnroll = db.Column(db.DateTime, nullable=False)
    Open = db.Column(db.Integer, nullable=False)
    CreatedBy = db.Column(db.String(100), nullable=False)
    UpdatedBy = db.Column(db.String(100), nullable=True)
    CreatedTime = db.Column(db.DateTime, nullable=False, default=datetime.now)
    UpdateTime = db.Column(db.DateTime, nullable=True, default=datetime.now, onupdate=datetime.now)
    IsFull =  db.Column(db.Boolean, nullable=False)

    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

class CourseClass(db.Model):
    __tablename__ = 'Class'

    ClassId = db.Column(db.Integer, primary_key=True)
    CourseId = db.Column(db.Integer, primary_key=True)
    CourseName = db.Column(db.String(100), nullable=False)
    TrainerId = db.Column(db.Integer, nullable=True)
    StartDateTime = db.Column(db.DateTime, nullable=False,)
    EndDateTime = db.Column(db.DateTime, nullable=True,)
    Capacity = db.Column(db.Integer, nullable=False)
    SlotsAvailable = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

class CourseMaterials(db.Model):
    __tablename__ = 'CourseMaterials'

    course_id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, primary_key=True)
    subchapter_id = db.Column(db.String(100), primary_key=True)
    chapter_name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

class IsChapViewable(db.Model):
    __tablename__ = 'isChapViewable'

    learner_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, primary_key=True)
    subchapter_id = db.Column(db.String(100), primary_key=True)
    chapter_viewable = db.Column(db.Boolean, nullable=False)
    chapter_viewed = db.Column(db.Boolean, nullable=False)

    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

class Quiz(db.Model):
    __tablename__ = 'quiz'
    quiz_id = db.Column(db.Integer, primary_key=True, nullable=False)
    quiz_name = db.Column(db.String(65535), nullable=True)
    course_id = db.Column(db.Integer, primary_key=False, nullable=False)
    class_id = db.Column(db.Integer, primary_key=False, nullable=False)
    chapter_id = db.Column(db.Integer, primary_key=False, nullable=False)
    isGraded = db.Column(db.String(65535), nullable=False)
    passing_grade = db.Column(db.String(65535), nullable=False)
    duration = db.Column(db.Integer, nullable=False)

    def __init__(self, quiz_name, course_id, class_id, chapter_id, isGraded, passing_grade, duration):
        self.quiz_name = quiz_name
        self.course_id = course_id
        self.class_id = class_id
        self.chapter_id = chapter_id
        self.isGraded = isGraded
        self.passing_grade = passing_grade
        self.duration = duration

    def json(self):
        return {"quiz_id": self.quiz_id, "quiz_name": self.quiz_name, "course_id": self.course_id, "class_id": self.class_id, "chapter_id": self.chapter_id, "isGraded": self.isGraded, "passing_grade": self.passing_grade, "duration": self.duration}
    
    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

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
    
    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

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

class Engineer(db.Model):
    __tablename__ = 'Engineer'

    EngineerID = db.Column(db.Integer, primary_key = True)
    EngineerName = db.Column(db.String(100), nullable = False)
    TotalClasses = db.Column(db.Integer, nullable = False)
    CourseCompleted = db.Column(db.Integer, nullable = False)
    Trainer = db.Column(db.Integer, nullable = False)
    Learner = db.Column(db.Integer, nullable = False)
    LearnerId = db.Column(db.Integer, nullable = False)

    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

db.create_all()

# Learner sign up for course - from trisha
@app.route("/course_signup/<string:LearnerID>/<string:CourseID>/<string:ClassID>", methods=['POST'])
def course_signup(LearnerID, CourseID, ClassID):
    LearnerID = LearnerID
    EngineerID =Engineer.query.filter_by(
            LearnerId=LearnerID).first().EngineerID
    LearnerName = request.json.get('LearnerName')
    CourseID = CourseID
    ClassID = ClassID
    assigned = 0
    approved = 0
    CourseCompleted = 0
    learner = Learner(LearnerID=LearnerID, EngineerID=EngineerID,LearnerName=LearnerName, CourseID=CourseID, ClassID=ClassID,
                    assigned=assigned, approved=approved, CourseCompleted=CourseCompleted)

    try:
        db.session.add(learner)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while signing up. " + str(e)
            }
        ), 500

    # added this function to add in rows to IsChapViewable
    # remove this and put in 1) assign learners to class 2) hr approve learner's enrollment
    addRowsToViewable(LearnerID, CourseID, ClassID)
    addRowsToQuizResults(LearnerID, CourseID, ClassID)

    return jsonify(
        {
            "code": 201,
            "message": "Successful sign up for course."
        }
    ), 201

# Get all the chaps available for the course and class
# Loop through and db.session.add()
# After the loop, db.session.commit()
def addRowsToViewable(LearnerID, CourseID, ClassID):
    MaterialsList = CourseMaterials.query.filter_by(
        course_id=CourseID).filter_by(class_id=ClassID).all()
    for material in MaterialsList:
        if (material.chapter_id == 1):
            learner_id = LearnerID
            course_id = material.course_id
            class_id = material.class_id
            chapter_id = material.chapter_id
            subchapter_id = material.subchapter_id
            chapter_viewable = 1
            chapter_viewed = 0

            row = IsChapViewable(learner_id=learner_id, course_id=course_id, class_id=class_id, chapter_id=chapter_id,
                                 subchapter_id=subchapter_id, chapter_viewable=chapter_viewable, chapter_viewed=chapter_viewed)
            db.session.add(row)
        else:
            learner_id = LearnerID
            course_id = material.course_id
            class_id = material.class_id
            chapter_id = material.chapter_id
            subchapter_id = material.subchapter_id
            chapter_viewable = 0
            chapter_viewed = 0

            row = IsChapViewable(learner_id=learner_id, course_id=course_id, class_id=class_id, chapter_id=chapter_id,
                                 subchapter_id=subchapter_id, chapter_viewable=chapter_viewable, chapter_viewed=chapter_viewed)
            db.session.add(row)

    try:
        db.session.commit()

    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while adding rows to isChapViewable Table. " + str(e)
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "message": "Successful added."
        }
    ), 201

def addRowsToQuizResults(LearnerID, CourseID, ClassID):
    QuizzesList = Quiz.query.filter_by(
        course_id=CourseID).filter_by(class_id=ClassID).all()
    for quiz in QuizzesList:
            learner_id = LearnerID
            quiz_id = quiz.quiz_id
            score = 0
            quizPass = 0
            isViewable = 0
            attempts = 0

            row = QuizResults(learner_id=learner_id, quiz_id=quiz_id, score=score, quizPass=quizPass,
                                 isViewable=isViewable, attempts=attempts)
            db.session.add(row)

    try:
        db.session.commit()

    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while adding rows to QuizResults Table. " + str(e)
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "message": "Successful added."
        }
    ), 201

# User Story: Withdraw from self-enrolled class
# Show a list of classes that are still in enrollment period
# get all enrolled classes -> filter_by leaner_id and assigned = 0
# return the classes that are still in the enrollment period
@app.route("/mono/withdrawableClasses/<string:learner_id>")
def get_withdrawableClasses(learner_id):
    CurrentDate = datetime.now()
    print(CurrentDate)

    # only can withdraw from self-enrolled class, provided if its still in enrollment period
    ClassList = Learner.query.filter_by(LearnerID=learner_id).filter_by(assigned=0).all()

    withdrawable_list= []

    for i in range(len(ClassList)):
        courseInfo =  Course.query.filter_by(CourseID=ClassList[i].CourseID).first()
        StartEnroll = courseInfo.StartEnroll
        EndEnroll = courseInfo.EndEnroll
        
        if (CurrentDate >= StartEnroll and CurrentDate <= EndEnroll):
            result = CourseClass.query.filter_by(CourseId=ClassList[i].CourseID).filter_by(ClassId=ClassList[i].ClassID).first()
            withdrawable_list.append(result)

    if len(withdrawable_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "withdrawable_list": [course.to_dict() for course in withdrawable_list]
                },
                "message": "Withdrawable classes for learner_id {} has successfully returned.".format(learner_id)
            },

        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "learner_id": learner_id
            },
            "message": "No withdrawable classes found."
        }
    ), 404

# Delete from Learner, IsChapViewable, QuizResults
@app.route("/mono/withdraw/<string:learner_id>/<string:class_id>/<string:course_id>", methods=['POST'])
def withdraw_class(learner_id,class_id,course_id):
    # delete row from learner
    Learner.query.filter_by(LearnerID=learner_id).filter_by(ClassID=class_id).filter_by(CourseID=course_id).delete()
    
    # delete rows from IsChapViewable
    IsChapViewable.query.filter_by(learner_id=learner_id).filter_by(class_id=class_id).filter_by(course_id=course_id).delete()
    
    # delete rows from QuizResults
    QuizzesList = Quiz.query.filter_by(class_id=class_id).filter_by(course_id=course_id).all()
    for quiz in QuizzesList:
            quiz_id = quiz.quiz_id
            QuizResults.query.filter_by(learner_id=learner_id).filter_by(quiz_id=quiz_id).delete()
    try:
        db.session.commit()

    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while withdrawing. " + str(e)
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "message": "Successful withdrawn from the class."
        }
    ), 201

# User Story: View all enrolled courses
# Get all enrolled courses by LearnerID from Learner
# Get the start and end DATETIME by CourseId and ClassId from CourseClass
# + User Story: Learner is only allowed to view course materials when enrollment is approved -> filter_by(approved=1)
@app.route("/mono/enrolledCourses/<string:LearnerID>")
def get_enrolled_courses(LearnerID):
    EnrolledList = Learner.query.filter_by(LearnerID=LearnerID).filter_by(approved=1).all()

    CourseDetails = []

    for enroll in EnrolledList:
        result = CourseClass.query.filter_by(CourseId=enroll.CourseID).filter_by(ClassId=enroll.ClassID).first()
        CourseDetails.append(result)

    CourseDetails = [course.to_dict() for course in CourseDetails]
    CourseDetails = sorted(CourseDetails, key = lambda k:k["StartDateTime"])

    if len(CourseDetails):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "CourseDetails": CourseDetails
                },
                "message": "Enrolled courses for LearnerID {} has successfully returned.".format(LearnerID)
            },

        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "LearnerID": LearnerID
            },
            "message": "Enrolled courses not found."
        }
    ), 404

# User Story: View course materials by the different chapters
# Get all the chapters by LearnerID, classId and course_id from CourseMaterial
@app.route("/mono/allMaterial/<string:learner_id>/<string:class_id>/<string:course_id>")
def find_by_course_class(learner_id, class_id, course_id):
    ViewableList = IsChapViewable.query.filter_by(learner_id=learner_id).filter_by(
        class_id=class_id).filter_by(course_id=course_id).all()

    CourseName = Course.query.filter_by(CourseID=course_id).first().CourseName

    UniqueChapIds = []
    ChapterViewable = {}

    for view in ViewableList:
        if view.chapter_id not in UniqueChapIds:
            UniqueChapIds.append(view.chapter_id)
            print(str(view.chapter_id)+"," + str(view.chapter_viewable))
            ChapterViewable[view.chapter_id] = view.chapter_viewable

    if len(ViewableList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "UniqueChapIds": UniqueChapIds,
                    "ChapterViewable": ChapterViewable,
                    "CourseName": CourseName
                },
                "message": "Course Materials with ClassId {} has successfully returned.".format(class_id)
            },

        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "class_id": class_id,
                "course_id": course_id
            },
            "message": "Course material not found."
        }
    ), 404

# Get materials by chapter_id, class_id and course_id from CourseMaterial
@app.route("/mono/chapterMaterial/<string:learner_id>/<string:class_id>/<string:course_id>/<string:chapter_id>")
def find_by_chapter_id(learner_id, class_id, course_id, chapter_id):
    MaterialsList = CourseMaterials.query.filter_by(class_id=class_id).filter_by(
        course_id=course_id).filter_by(chapter_id=chapter_id).all()
    print(MaterialsList)
    if len(MaterialsList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "Materials": [Materials.to_dict() for Materials in MaterialsList],
                    "Learner_id": learner_id
                },
                "message": "Course Material with ChapterId {} has successfully returned.".format(chapter_id)
            },

        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "learner_id": learner_id,
                "class_id": class_id,
                "course_id": course_id,
                "chapter_id": chapter_id
            },
            "message": "Course material not found."
        }
    ), 404

# Mark chapter as viewed
# Get all materials of a chapter and check if all materials for that chapter (eg. Chapter 1 - 1a and 1b have been viewed)
# If all viewed, mark quiz as viewable, mark next chapter as viewable
@app.route("/mono/markChapterMaterial/<string:learner_id>/<string:class_id>/<string:course_id>/<string:chapter_id>/<string:subchapter_id>")
def mark_chapter(learner_id, class_id, course_id, chapter_id, subchapter_id):
    subMaterials = mark_as_viewed(
        learner_id, class_id, course_id, subchapter_id)
    ChapMaterials = find_materials_chapter_id(
        learner_id, class_id, course_id, chapter_id)

    viewed = []
    for m in ChapMaterials:
        if m.chapter_viewed == True:
            viewed.append(m)

    if len(viewed) == len(ChapMaterials):
        Quiz_viewable = mark_quiz_as_viewable(
            learner_id, class_id, course_id, chapter_id)
        print(Quiz_viewable)

        return {
            "Quiz": [Quiz_viewable.to_dict()],
            "Materials": [subMaterials.to_dict()]
        }
    return {
        "Materials": subMaterials.to_dict()
    }


def mark_as_viewed(learner_id, class_id, course_id, subchapter_id):
    try:
        Materials = IsChapViewable.query.filter_by(learner_id=learner_id).filter_by(class_id=class_id).filter_by(
            course_id=course_id).filter_by(subchapter_id=subchapter_id).first()
        print(Materials)
        if not Materials:
            return []

        print(Materials.chapter_viewed)
        if Materials.chapter_viewed == False:
            Materials.chapter_viewed = True
            print(Materials.chapter_viewed)
        else:
            return Materials
        db.session.commit()
        return Materials
    except Exception as e:
        return []


def find_materials_chapter_id(learner_id, class_id, course_id, chapter_id):
    MaterialsList = IsChapViewable.query.filter_by(learner_id=learner_id).filter_by(class_id=class_id).filter_by(
        course_id=course_id).filter_by(chapter_id=chapter_id).all()
    print('Print Material List')
    print(MaterialsList)
    print('Done with material list')
    if len(MaterialsList):
        return MaterialsList
    return []


def mark_quiz_as_viewable(learner_id, ClassId, CourseId, ChapterId):
    try:
        quiz_id =  Quiz.query.filter_by(class_id=ClassId).filter_by(
            course_id=CourseId).filter_by(chapter_id=ChapterId).first().quiz_id
        result = QuizResults.query.filter_by(learner_id=learner_id).filter_by(
            quiz_id=quiz_id).first()
        print(result)
        if not result:
            return []

        print(result.isViewable)
        if result.isViewable == False:
            result.isViewable = True
            print(result.isViewable)
        else:
            return result
        db.session.commit()
        return result
    except Exception as e:
        return []


# User Story: Take the quizzes for the classes
# Get all the quizzes by learner_id, classId and CourseID
@app.route("/mono/allQuizzes/<string:learner_id>/<string:ClassId>/<string:CourseID>")
def find_by_course_id(learner_id, ClassId, CourseID):
    resultList = Quiz.query.filter_by(class_id=ClassId).filter_by(course_id=CourseID).all()
    CourseName = Course.query.filter_by(CourseID=CourseID).first().CourseName

    QuizNameList = []
    QuizList = []
    for result in resultList:
        QuizNameList.append(result.quiz_name)
        QuizList.append(QuizResults.query.filter_by(learner_id=learner_id).filter_by(
            quiz_id=result.quiz_id).first())
    if QuizList:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "Quizzes": [quiz.to_dict() for quiz in QuizList],
                    "QuizNameList": QuizNameList,
                    "CourseName": CourseName
                },
                "message": "Quizzes with ClassId {} has successfully returned.".format(ClassId)
            },

        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "ClassId": ClassId,
                "CourseId": CourseID
            },
            "message": "Quiz not found."
        }
    ), 404

# User Story: Engineer view quiz results
# return only the quiz that has been attempted
@app.route("/mono/allResults/<string:learner_id>/<string:ClassId>/<string:CourseId>")
def get_all_results(learner_id, ClassId, CourseId):
    Quiz_info = Quiz.query.filter_by(class_id=ClassId).filter_by(course_id=CourseId).all()
    CourseName = Course.query.filter_by(CourseID=CourseId).first().CourseName

    QuizNameList = []
    quizResultsList = []
    for quiz in Quiz_info:
        QuizNameList.append(quiz.quiz_name)
        quizResultsList.append(QuizResults.query.filter_by(learner_id=learner_id).filter_by(
            quiz_id=quiz.quiz_id).first())

    ResultList = []
    for r in range(len(quizResultsList)):
        if quizResultsList[r].attempts != 0:
            ResultList.append(quizResultsList[r])

    stats = []
    for r in range(len(ResultList)):
        quiz_id = ResultList[r].quiz_id
        stats.append(get_stats(quiz_id))

    if ResultList:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "quizResults": [Result.to_dict() for Result in ResultList],
                    "stats": stats,
                    "QuizNameList": QuizNameList,
                    "CourseName": CourseName
                },
                "message": "Results with ClassId {} has successfully returned.".format(ClassId)
            },

        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "learner_id": learner_id,
                "ClassId": ClassId,
                "CourseId": CourseId
            },
            "message": "Results not found."
        }
    ), 404

# get all the quiz results by QuizId and CourseId
# compute the average, min and max of the cohort (taking the same course)
def get_stats(quiz_id):
    allResultList = QuizResults.query.filter_by(quiz_id=quiz_id).all()
    scoreList = []
    statList = {}
    statList[quiz_id] = {}
    
    if len(allResultList) == 1:
        return scoreList
        
    for a in range(len(allResultList)):
        if allResultList[a].attempts != 0:
            scoreList.append(allResultList[a].score)

    avgScore = round(sum(scoreList)/len(scoreList), 2)
    statList[quiz_id]['avgScore'] = avgScore

    minScore = min(scoreList)
    statList[quiz_id]['minScore'] = minScore

    maxScore = max(scoreList)
    statList[quiz_id]['maxScore'] = maxScore

    return statList

# User Story: Trainer view quiz results of a class
# Use TrainerId to get the courses and classes the trainer is teaching
# UI part - make drop down for courseId, classId and quizId
@app.route("/mono/trackResults/allClasses/<string:TrainerId>")
def get_all_classes(TrainerId):
    ClassList = CourseClass.query.filter_by(TrainerId=TrainerId).all()
    print(ClassList)

    classIdList = []
    courseIdList = []
    uniqueCourseIdList = []

    for c in ClassList:
        courseIdList.append(c.CourseId)
        if c.ClassId not in classIdList:
            classIdList.append(c.ClassId)
        if c.CourseId not in uniqueCourseIdList:
            uniqueCourseIdList.append(c.CourseId)

    print(classIdList)
    print(courseIdList)

    if ClassList:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "classIdList": classIdList,
                    "courseIdList": uniqueCourseIdList
                },
                "message": "Classes taughts by TrainerId {} has successfully returned.".format(TrainerId)
            },

        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "TrainerId": TrainerId
            },
            "message": "Classes taught by trainer not found."
        }
    ), 404

@app.route("/mono/trackResults/quizByCourseClass/<string:class_id>/<string:course_id>")
def get_quizIdBy_courseClass(class_id, course_id):
    QuizList = Quiz.query.filter_by(
        class_id=class_id).filter_by(course_id=course_id).all()
    print(QuizList)

    quizIdList = []
    for quiz in QuizList:
        if quiz.quiz_id not in quizIdList:
            quizIdList.append(quiz.quiz_id)

    print(quizIdList)
    if quizIdList:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "quizIdList": quizIdList
                }
            }
        )

# Use courseId, classId and quizId to get all the quizResults for that particular quiz, class and course
@app.route("/mono/ClassQuizResults/<string:quiz_id>")
def get_all_classResults(quiz_id):
    quizName = Quiz.query.filter_by(quiz_id=quiz_id).first().quiz_name

    quizResults = QuizResults.query.filter_by(quiz_id=quiz_id).all()

    learnerList = []
    for result in quizResults:
        learnerList.append(result.learner_id)

    nameList = get_learner_name(learnerList)

    if quizResults:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "quizResults": [result.to_dict() for result in quizResults],
                    "nameList": nameList,
                    "quizName": quizName
                },
                "message": "Results for quiz_id {} has successfully returned.".format(quiz_id)
            },

        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "quiz_id": quiz_id
            },
            "message": "Classes taught by trainer not found."
        }
    ), 404

# Getting engineer names
def get_learner_name(learnerList):
    nameList = []
    for LearnerID in learnerList:
        result = Learner.query.filter_by(LearnerID=LearnerID).first()
        nameList.append(result.LearnerName)
    return nameList

# FROM QUIZ.PY
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
            'isGraded' : q.isGraded,
            'duration' : q.duration
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

# update score & quizPass
@app.route("/quiz/updateQuizResults", methods=['PUT'])
def update_quiz_results():
    data = request.get_json()
    learner_id=data['learner_id']
    quiz_id=data['quiz_id']
    isGraded = data['isGraded']
    quiz = QuizResults.query.filter_by(learner_id=learner_id).filter_by(quiz_id=quiz_id).first()

    quiz_info = Quiz.query.filter_by(quiz_id=quiz_id).first()
    class_id = quiz_info.class_id
    course_id = quiz_info.course_id
    next_chapId = quiz_info.chapter_id+1

    # mark next chap as viewable
    mark_chap_as_viewable(learner_id, class_id, course_id, next_chapId)
    
    # check if quiz is graded and if pass, update course as completed
    if(isGraded=='Y' and data['quizPass']==1):
        mark_course_completed(learner_id, class_id, course_id)

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
                        'learner_id' : data['learner_id'],
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
                        'learner_id': data['learner_id'],
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

def mark_chap_as_viewable(learner_id, class_id, course_id, next_chapId):
    try:
        Chap_result = IsChapViewable.query.filter_by(learner_id=learner_id).filter_by(class_id=class_id).filter_by(
            course_id=course_id).filter_by(chapter_id=next_chapId).all()
        print(Chap_result)
        if not Chap_result:
            return []

        for C in Chap_result:
            print(C.chapter_viewable)
            if C.chapter_viewable == False:
                C.chapter_viewable = True
                print(C.chapter_viewable)
            else:
                return Chap_result
        db.session.commit()
        return Chap_result
    except Exception as e:
        return []

 # update course as completed
def mark_course_completed(learner_id, CourseId, ClassId):
    try:
        learnerCourse = Learner.query.filter_by(LearnerID=learner_id).filter_by(ClassID=ClassId).filter_by(
            CourseID=CourseId).first()
        print(learnerCourse)

        if learnerCourse.CourseCompleted == False:
            learnerCourse.CourseCompleted = True
            print(learnerCourse.CourseCompleted)

        db.session.commit()

    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while updating CourseCompleted. " + str(e)
            }
        ), 500
    return jsonify(
        {
            "code": 201,
            "message": "Successfully updated CourseCompleted to True."
        }
    ), 201

if __name__ == '__main__':
    app.run(port=5100, debug=True)