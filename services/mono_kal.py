from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3308/is212_project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                           'pool_recycle': 280}

db = SQLAlchemy(app)

CORS(app)

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

class Trainer(db.Model):
    __tablename__ = 'Trainer'

    TrainerId = db.Column(db.Integer, primary_key = True)
    EngineerID = db.Column(db.Integer, primary_key = True)
    TrainerName = db.Column(db.String(100), nullable = False)
    CourseId = db.Column(db.Integer, nullable = False)
    ClassId = db.Column(db.Integer, nullable = False)

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

class Engineer(db.Model):
    __tablename__ = 'Engineer'

    EngineerID = db.Column(db.Integer, primary_key = True)
    EngineerName = db.Column(db.String(100), nullable = False)
    TotalClasses = db.Column(db.Integer, nullable = False)
    CourseCompleted = db.Column(db.Integer, nullable = False)
    Trainer = db.Column(db.Integer, nullable = False)
    Learner = db.Column(db.Integer, nullable = False)
    LearnerId = db.Column(db.Integer, nullable = False)
    TrainerId = db.Column(db.Integer, nullable = False)


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

    # __mapper_args__ = {
    #     'polymorphic_identity': 'person'
    # }

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

    def __init__(self, quiz_name, course_id, class_id, chapter_id, isGraded, passing_grade):
        self.quiz_name = quiz_name
        self.course_id = course_id
        self.class_id = class_id
        self.chapter_id = chapter_id
        self.isGraded = isGraded
        self.passing_grade = passing_grade

    def json(self):
        return {"quiz_id": self.quiz_id, "quiz_name": self.quiz_name, "course_id": self.course_id, "class_id": self.class_id, "chapter_id": self.chapter_id, "isGraded": self.isGraded, "passing_grade": self.passing_grade}
    
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


db.create_all()

# User Story: Assign Engineers to sections
# Get all the courses that are assigned to a trainer by assignedEngineer
@app.route("/view_all_courses/<int:IsFull>")
def view_assigned_courses(IsFull):
    AssignedCourseList = Course.query.filter_by(
        IsFull=IsFull).all()
    if AssignedCourseList:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "AssignedCourses": [assigned_courses.to_dict() for assigned_courses in AssignedCourseList]
                },
                "message": "All Assigned Courses have successfully returned."
            },
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "classAssigned": IsFull
            },
            "message": "Assigned courses not found."
        }
    ), 404

# get class details of a specific course
@app.route("/class_details/<string:CourseID>")
def get_class_details(CourseID):
    classList = CourseClass.query.filter_by(CourseId=CourseID).all()
    if len(classList):
      classlist = [courseclass.to_dict() for courseclass in classList]
      classlist = sorted(classlist, key=lambda k:k["StartDateTime"], reverse=True)
      return jsonify(
            {
                "code": 200,
                "data": {
                    "courseclasses": classlist
                },
                "message": "Classes for course with courseid: {} successfully returned.".format(CourseID)
            },
              
        )
        # return classList
    return jsonify(
        {
            "code": 404,
            "data": {
                "CourseID": CourseID
            },
            "message": "Classes for courses with courseid: {} not found.".format(CourseID)
        }
    ), 404


# Get details for specific learner through Engineer ID
@app.route("/view_learner_details/<int:EngineerID>")
def view_specific_learner(EngineerID):
    LearnerList = Learner.query.filter_by(EngineerID=EngineerID).all()
    if LearnerList:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "AvailableLearners": [available_learner.to_dict() for available_learner in LearnerList]
                },
                "message": "Learner have successfully returned."
            },
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "AvailableLearners": EngineerID
            },
            "message": "Learner not found."
        }
    ), 404

# Assigning and updating db for trainers
@app.route("/assign_trainer/<string:TrainerID>/<string:CourseID>/<string:ClassID>", methods=['PUT'])
def assign_trainer(TrainerID, CourseID, ClassID):
    classInfo = CourseClass.query.filter_by(
            CourseId=CourseID).filter_by(ClassId=ClassID).first()

    classInfo.TrainerId = TrainerID

    try:
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while assigning engineer. " + str(e)
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "message": "Successfully assigned engineer to course."
        }
    ), 201

# Assigning and updating db
@app.route("/assign_engineer/<string:LearnerID>/<string:CourseID>/<string:ClassID>/<string:LearnerName>", methods=['POST'])
def assign_engineer(LearnerID, CourseID, ClassID, LearnerName):
    LearnerID = LearnerID
    EngineerID = Engineer.query.filter_by(
            LearnerId=LearnerID).first().EngineerID
    LearnerName = LearnerName
    CourseID = CourseID
    ClassID = ClassID
    assigned = 1
    approved = 1
    CourseCompleted = 0
    learner = Learner(LearnerID=LearnerID, EngineerID=EngineerID, LearnerName=LearnerName, CourseID=CourseID, ClassID=ClassID, assigned=assigned, approved=approved,
                      CourseCompleted=CourseCompleted)

    try:
        db.session.add(learner)

        classInfo = CourseClass.query.filter_by(
            CourseId=CourseID).filter_by(ClassId=ClassID).first()
        classInfo.SlotsAvailable -= 1

        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while assigning engineer. " + str(e)
            }
        ), 500

    # added this function to add in rows to IsChapViewable
    addRowsToViewable(LearnerID, CourseID, ClassID)
    addRowsToQuizResults(LearnerID, CourseID, ClassID)

    return jsonify(
        {
            "code": 201,
            "message": "Successfully assigned engineer to course."
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

# View all available engineers
@app.route("/view_all_engineers/<int:isLearner>/<int:CourseID>")
def view_available_engineers(isLearner, CourseID):
    EngineerList = Engineer.query.filter_by(Learner=isLearner).all()
    print(EngineerList)

    AvailableList = []
    for i in range(len(EngineerList)):
        print(EngineerList[i].LearnerId)
        result = Learner.query.filter_by(LearnerID=EngineerList[i].LearnerId).filter_by(CourseID=CourseID).first()
        if result:
            continue
        else:
            AvailableList.append(EngineerList[i])

    if EngineerList:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "AvailableEngineers": [available_engineers.to_dict() for available_engineers in EngineerList]
                },
                "message": "All Assigned Courses have successfully returned."
            },
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "AvailableEngineers": Learner
            },
            "message": "Engineers not found."
        }
    ), 404

# View all available trainers
@app.route("/view_all_trainers/<int:isTrainer>/<int:CourseID>")
def view_available_trainers(isTrainer, CourseID):
    EngineerList = Engineer.query.filter_by(Trainer=isTrainer).all()
    # print(EngineerList)

    AvailableList = []
    for i in range(len(EngineerList)):
        print(EngineerList[i].TrainerId)
        result = Trainer.query.filter_by(TrainerId=EngineerList[i].TrainerId).filter_by(CourseId=CourseID).first()
        if result:
            continue
        else:
            AvailableList.append(EngineerList[i])
    if EngineerList:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "AvailableTrainers": [available_trainers.to_dict() for available_trainers in AvailableList]
                },
                "message": "All available trainers have successfully returned."
            },
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "AvailableTrainers": Trainer
            },
            "message": "Engineers not found."
        }
    ), 404

# User Story: View Assigned Courses by Trainer
@app.route("/classdetails/<int:TrainerId>")
def view_trainer_classes(TrainerID):
    AssignedClassList = CourseClass.query.filter_by(
        TrainerId=TrainerID).all()
    if AssignedClassList:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "AssignedClasses": [assigned_classes.to_dict() for assigned_classes in AssignedClassList]
                },
                "message": "All assigned classes with trainer ID {} has successfully returned.".format(TrainerID)
            },
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "trainerID": TrainerID
            },
            "message": "Trainer not found."
        }
    ), 404

# Get Class List
@app.route("/view_class_list/<int:approved>/<int:CourseID>/<int:ClassID>")
def view_class_list(approved, CourseID, ClassID):
    ClassList = Learner.query.filter_by(approved=approved).filter_by(CourseID=CourseID).filter_by(ClassID=ClassID).all()
    if ClassList:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "ClassList": [class_list.to_dict() for class_list in ClassList]
                },
                "message": "Learner have successfully returned."
            },
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "courseID": CourseID
            },
            "message": "Learner not found."
        }
    ), 404

if __name__ == '__main__':
    app.run(port=5100, debug=True)