from logging import captureWarnings
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3308/is212_project'
                                        # '@localhost:3306/is212_example'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                           'pool_recycle': 280}

db = SQLAlchemy(app)

CORS(app)

# Learner 
class Learner(db.Model):
    __tablename__ = 'Learner'

    LearnerID = db.Column(db.Integer, primary_key=True)
    LearnerName = db.Column(db.String(100), nullable=False)
    CourseID = db.Column(db.Integer, primary_key=True)
    ClassID = db.Column(db.Integer, primary_key=True)
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

# Engineer
class Engineer(db.Model):
    __tablename__ = 'Engineer'

    EngineerID = db.Column(db.Integer, primary_key=True)
    EngineerName = db.Column(db.String(100), nullable=False)
    CourseID = db.Column(db.Integer, primary_key=True)
    ClassID = db.Column(db.Integer, primary_key=True)
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

# Course
class Course(db.Model):
    __tablename__ = 'Course'

    CourseID = db.Column(db.Integer, primary_key=True)
    CourseName = db.Column(db.String(100), nullable=False)
    PreReq = db.Column(db.Integer, nullable=True)
    Classes = db.Column(db.Integer, nullable=False)
    CreatedBy = db.Column(db.String(100), nullable=False)
    UpdatedBy = db.Column(db.String(100), nullable=True)
    CreatedTime = db.Column(db.DateTime, nullable=False, default=datetime.now)
    UpdateTime = db.Column(db.DateTime, nullable=True, default=datetime.now, onupdate=datetime.now)
    IsFull =  db.Column(db.Boolean, nullable=False)

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

# Class
class CourseClass(db.Model):
    __tablename__ = 'Class'

    ClassID = db.Column(db.Integer, primary_key=True)
    CourseID = db.Column(db.Integer, primary_key=True)
    CourseName = db.Column(db.String(100), nullable=False)
    TrainerID = db.Column(db.Integer, nullable=True)
    StartDateTime = db.Column(db.DateTime, nullable=False,)
    EndDateTime = db.Column(db.DateTime, nullable=True,)
    Materials = db.Column(db.String(100), nullable=False)
    Capacity = db.Column(db.Integer, nullable=False)
    SlotsAvailable = db.Column(db.Integer, nullable=False)

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

db.create_all()

# User story: View all courses --> OK
@app.route("/view_all_courses")
def get_all():
    courselist = Course.query.all()
    if len(courselist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "courses": [course.to_dict() for course in courselist]
                },
                 "message": "All courses are successfully returned."
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no courses."
        }
    ), 404

# get course by course id
@app.route("/get_course/<string:CourseID>")
def get_course_details(CourseID):
    course = Course.query.filter_by(CourseID=CourseID).first()
    if course:
        return jsonify({
            "code": 200,
            "data": {
                "course": course.to_dict()
            },
            "message": "Course details for Course ID {} successfully returned".format(CourseID)
        })

    return jsonify(
        {
            "code": 404,
            "data": {
                "CourseID": CourseID
            },
            "message": "Course with id: {} not found.".format(CourseID)
        }
    ), 404

# this url gets the learner's pre req course id 
# and then find the courses with that pre requisite and the classes under that course
@app.route("/learner_prereq/<string:LearnerID>")
def get_learner_prereq(LearnerID):
    learnerList = Learner.query.filter_by(LearnerID=LearnerID).all()
    if len(learnerList):
        for learner in learnerList:
            print(learner.CourseCompleted)
            course_id = learner.CourseID

            if (learner.CourseCompleted == 1):
                # if CourseCompleted = 1 then call function, if not, don't allow function call
                return find_by_pre_req(course_id, LearnerID)

            # if pre-requisite course is not completed, do not show courses   
            return jsonify({
                "code": 500,
                "data": {
                    "CourseID": course_id
                },
                "message": "Learner found. Course is not completed. Unable to show courses with pre-requisite"
                
            })

    else:
        return jsonify(
            {
                "code": 404,
               "message": "Learner not found"
            }
        )

# CourseID = 1 --> returns courses with pre requisite = 1
@app.route("/course_prereq/<string:CourseID>")
def find_by_pre_req(CourseID, LearnerID):
    # classList = get_class_details(CourseID) # gets classes of courses (that have the pre requisite)
    courselist = Course.query.filter_by(PreReq=CourseID).all()

    if len(courselist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "Learner ID": LearnerID,
                    "courses": [course.to_dict() for course in courselist],
                    # "classes": [courseclass.to_dict() for courseclass in classList]
                },
                "message": "Courses with pre-requisite courseid: {} successfully returned.".format(CourseID)
            },
              
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "CourseID": CourseID
            },
            "message": "Courses with pre-requisite courseid: {} not found.".format(CourseID)
        }
    ), 404

# get class details of a specific course
@app.route("/classdetails/<string:CourseID>")
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

# get details of a specific class
@app.route("/courseclassdetails/<string:ClassID>")
def get_courseclass_details(ClassID):
    courseclass = CourseClass.query.filter_by(ClassID=ClassID).first()
    if courseclass:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "courseclass": courseclass.to_dict()
                },
                "message": "Class with id: {} successfully returned.".format(ClassID)
            },
              
        )
        # return classList
    return jsonify(
        {
            "code": 404,
            "data": {
                "ClassID": ClassID
            },
            "message": "Class with id: {} not found.".format(ClassID)
        }
    ), 404


# sign up for class
# check if prerequisite for course is met --> OK
# check if slots are available --> OK
# check if course has NOT been taken before --> OK (duplicate entry will give error)
@app.route("/course_signup/<string:LearnerID>/<string:CourseID>/<string:ClassID>", methods=['POST'])
def validate_prereq(CourseID, LearnerID, ClassID):
    learner = Learner.query.filter_by(LearnerID=LearnerID).all()
    course = Course.query.filter_by(CourseID=CourseID).first()
    # print(course.CourseID)
    print(course)
    print(learner)
    coursePreReq = course.PreReq
    print('prerequisite: ', coursePreReq)

    for each in learner:
        learnerPreReq = each.CourseID
        learnerComplete = each.CourseCompleted
        print('learner prerequisite: ', learnerPreReq, 'completed: ', learnerComplete)

        if coursePreReq == None:
            # course has no pre-requisite
            # return jsonify(
            #     {
            #         "code": 200,
            #         "CourseID": CourseID,
            #         "message": "Able to sign up"
            #     }
            # ), 200
            return course_signup(LearnerID, CourseID, ClassID)
        
        # if there is a pre-requisite, check if the course pre-req == learner course id
        if learnerPreReq == coursePreReq:
            print('learnerPreReq: ', learnerPreReq, ', coursePreReq: ', coursePreReq)
            if learnerComplete == 1:
                # return jsonify(
                #     {
                #         "code": 200,
                #         "message": "Learner has completed course pre-requisite"
                #     }
                # ), 200
                return course_signup(LearnerID, CourseID, ClassID)
            else: # learner did not complete course
                print(learnerComplete)
                return jsonify(
                    {
                        "code": 503,
                        "message": "Learner did not complete course pre-requisite"
                    }
                ), 500
        else: # learner is not taking pre-requisite
            print('learnerPreReq: ', learnerPreReq, ', coursePreReq: ', coursePreReq)
            return jsonify(
                {
                    "code": 502,
                    "message": "Learner is not taking pre-requisite "
                }
            ), 500
        # return course_signup(LearnerID, CourseID,ClassID)



def course_signup(LearnerID, CourseID, ClassID):
    LearnerID = LearnerID
    # LearnerName = request.json.get('LearnerName')
    LearnerName = 'Trisha'
    CourseID = CourseID
    ClassID = ClassID
    CourseCompleted = 0
    learner = Learner(LearnerID=LearnerID, LearnerName=LearnerName, CourseID=CourseID, ClassID=ClassID, 
                        CourseCompleted=CourseCompleted)
    
    courseclass = CourseClass.query.filter_by(ClassID=ClassID).first() 
    print(courseclass)
    SlotsAvailable = courseclass.SlotsAvailable
    CourseName = courseclass.CourseName
    # print(slotsAvailable)
    

    # if there are no available slots, do not allow sign up
    if SlotsAvailable <= 0:
        return jsonify(
                {
                    "code": 500,
                    "data": {
                        "CourseID": CourseID,
                        "CourseName": CourseName,
                        "ClassID": ClassID,
                        "Slots Available": SlotsAvailable
                    },
                    "message": "No more available slots. Please try different class. "
                }
            ), 500
    else: # slots available --> allow sign up
        try:
            data = SlotsAvailable -1
            # print(data)
            courseclass.SlotsAvailable = data

            db.session.add(learner)
            db.session.commit()
        except Exception as e:
            return jsonify(
                {
                    "code": 501,
                    "message": "An error occurred while signing up. " + str(e)
                }
            ), 501

        return jsonify(
            {
                "code": 201,
                "message": "Successful sign up for course."
            }
        ), 201


if __name__ == '__main__':
    app.run(port=5100, debug=True)