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

    courseID = db.Column(db.String(100), primary_key=True)
    courseName = db.Column(db.String(100), nullable=False)
    preReq = db.Column(db.Integer, nullable=False)
    classes = db.Column(db.Integer, nullable=False)
    createdBy = db.Column(db.String(100), nullable=False)
    updatedBy = db.Column(db.String(100), nullable=False)
    createdTime = db.Column(db.String(100), nullable=False)
    updateTime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    engineerAssigned = db.Column(db.Boolean, nullable=False)

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
    TrainerID = db.Column(db.Integer, nullable=True)
    StartDateTime = db.Column(db.DateTime, nullable=False,)
    EndDateTime = db.Column(db.DateTime, nullable=True,)
    Materials = db.Column(db.String(100), nullable=False)
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

db.create_all()

# User Story: Assign Engineers to sections
# Get all the courses that are assigned to a trainer by assignedEngineer
@app.route("/mono/allCourses/<string:engineerAssigned>")
def view_assigned_courses(engineerAssigned):
    AssignedCourseList = Course.query.filter_by(
        engineerAssigned=engineerAssigned).all()
    if AssignedCourseList:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "Assigned Courses": [assigned_courses.to_dict() for assigned_courses in AssignedCourseList]
                },
                "message": "All Assigned Courses have successfully returned."
            },
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "engineerAssigned": engineerAssigned
            },
            "message": "Assigned courses not found."
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