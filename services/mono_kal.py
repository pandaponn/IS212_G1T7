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

    CourseID = db.Column(db.String(100), primary_key=True)
    CourseName = db.Column(db.String(100), nullable=False)
    PreReq = db.Column(db.Integer, nullable=False)
    Classes = db.Column(db.Integer, nullable=False)
    CreatedBy = db.Column(db.String(100), nullable=False)
    UpdatedBy = db.Column(db.String(100), nullable=False)
    CreatedTime = db.Column(db.String(100), nullable=False)
    UpdateTime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    IsFull = db.Column(db.Boolean, nullable=False)

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

    ClassID = db.Column(db.Integer, primary_key=True)
    CourseID = db.Column(db.Integer, primary_key=True)
    CourseName = db.Column(db.String(100), nullable=False)
    TrainerID = db.Column(db.Integer, nullable=True)
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

    TrainerID = db.Column(db.Integer, primary_key = True)
    EngineerID = db.Column(db.Integer, primary_key = True)
    TrainerName = db.Column(db.String(100), nullable = False)
    CourseAssigned = db.Column(db.Integer, nullable = False)
    ClassAssigned = db.Column(db.Integer, nullable = False)

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
    classList = CourseClass.query.filter_by(CourseID=CourseID).all()
    if len(classList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "courseclasses": [courseclass.to_dict() for courseclass in classList]
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

# View all available engineers
@app.route("/view_all_engineers/<int:Learner>")
def view_available_engineers(Learner):
    EngineerList = Engineer.query.filter_by(Learner=Learner).all()
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

# User Story: View Assigned Courses by Trainer
@app.route("/classdetails/<int:TrainerID>")
def view_trainer_classes(TrainerID):
    AssignedClassList = CourseClass.query.filter_by(
        TrainerID=TrainerID).all()
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


if __name__ == '__main__':
    app.run(port=5100, debug=True)