from logging import captureWarnings
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/is212_project'
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
    EngineerID = db.Column(db.Integer,nullable=False )
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

# Engineer
class Engineer(db.Model):
    __tablename__ = 'Engineer'

    EngineerID = db.Column(db.Integer, primary_key = True)
    EngineerName = db.Column(db.String(100), nullable = False)
    TotalClasses = db.Column(db.Integer, nullable = False)
    CourseCompleted = db.Column(db.Integer, nullable = False)
    Trainer = db.Column(db.Integer, nullable = False)
    Learner = db.Column(db.Integer, nullable = False)
    LearnerId = db.Column(db.Integer, nullable=True)


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
    StartEnroll = db.Column(db.DateTime, nullable=False)
    EndEnroll = db.Column(db.DateTime, nullable=False)
    Open = db.Column(db.Integer, nullable=False)
    CreatedBy = db.Column(db.Integer, nullable=False)
    UpdatedBy = db.Column(db.Integer, nullable=True)
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

# Class
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
@app.route("/learner_prereq/<int:LearnerID>")
def get_learner_prereq(LearnerID):
    learnerList = Learner.query.filter_by(LearnerID=LearnerID, CourseCompleted=1).all()
    if len(learnerList):
        for learner in learnerList:
            course_id = learner.CourseID
        
            return find_by_pre_req(course_id, LearnerID)
            
            # return jsonify({
            #     "code": 200,
            #     "message": "Courses found"
            # }), 200

    return jsonify({
        "code": 500,
        "message": "Learner found. Unable to show courses with pre-requisite"
        
    })


# CourseID = 1 --> returns courses with pre requisite = 1
@app.route("/course_prereq/<int:CourseID>")
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
    classList = CourseClass.query.filter_by(CourseId=CourseID).all()
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
    courseclass = CourseClass.query.filter_by(ClassId=ClassID).first()
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
    duplicate = Learner.query.filter_by(LearnerID=LearnerID).filter_by(
        CourseID=CourseID).first()
    learner = Learner.query.filter_by(LearnerID=LearnerID).filter_by(
        CourseCompleted=1).all()

    course = Course.query.filter_by(CourseID=CourseID).first()
    coursePreReq = course.PreReq
    isCourseEnrollOpen = course.Open

    courseclass = CourseClass.query.filter_by(ClassId=ClassID).first() 
    SlotsAvailable = courseclass.SlotsAvailable

    # check if learner has taken/is taking/applied the course
    if duplicate:
        return jsonify(
                {
                    "code": 501,
                    "message": "Duplicate course. Already enrolled / applied for this course."
                }
            ), 501

    # check if course has prereq
    if course.PreReq == None:
        # no prereq and enrollment is open
        if isCourseEnrollOpen == 1:
            if SlotsAvailable <= 0:
                 return jsonify(
                    {
                        "code": 500,
                        "message": "No more available slots. Please try different class."
                    }
                ), 500
            else:
                course_signup(LearnerID, CourseID, ClassID)
                return jsonify({
                    "code": "200",
                    "message": "Course has no prerequisite. Processing sign up."
                }), 200
        # no prereq but enrollment is closed
        return jsonify({
            "code": "502",
            "message": "Enrollment for course is closed"
        }), 502
    
    # if course has prereq
    else:
        # learner did not complete any course before
        if not learner:
            print('no learner')
            return jsonify({
                "code": "404",
                "message": "no prequisites of learner"
            }), 404
        else:
            # learner completed some courses before
            # loop through them to check if learner completed the prereq course
            # print(learner[::-1])
            # learner = learner[::-1]
            for each in learner:
                if each.CourseID == coursePreReq:
                    # Prereq taken by learner and enrollment is open
                    if isCourseEnrollOpen == 1:
                        if SlotsAvailable <= 0:
                            return jsonify(
                                {
                                    "code": 500,
                                    "message": "No more available slots. Please try different class."
                                }
                            ), 500
                        else:
                            course_signup(LearnerID, CourseID, ClassID)
                            return jsonify({
                                "code": "200",
                                "message": "Learner completed prereq course. Processing sign up"
                            })
                    # Prereq taken by learner but enrollment is closed
                    else:
                        return jsonify({
                            "code": "502",
                            "message": "Enrollment for course is closed"
                        }),502
                # learner did not take the prereq before
                return jsonify({
                    "code": "404",
                    "message": "learner does not have pre requisite"
                }), 404

                
def course_signup(LearnerID, CourseID, ClassID):
    LearnerID = LearnerID
    # include the engineerid (update class learner and engineer)

    # LearnerName = request.json.get('LearnerName')
    LearnerName = 'Ling Li'
    EngineerID = Engineer.query.filter_by(LearnerId=LearnerID).first().EngineerID
    CourseID = CourseID
    ClassID = ClassID
    Assigned = 0
    Approved = None
    CourseCompleted = 0
    learner = Learner(LearnerID=LearnerID, LearnerName=LearnerName, EngineerID=EngineerID, CourseID=CourseID, ClassID=ClassID, 
                        assigned=Assigned, approved=Approved, CourseCompleted=CourseCompleted)
    
    courseclass = CourseClass.query.filter_by(ClassId=ClassID).first() 
    print(courseclass)
    # SlotsAvailable = courseclass.SlotsAvailable
    # CourseName = courseclass.CourseName
 
    try:
        # data = SlotsAvailable -1
        # print(data)
        # courseclass.SlotsAvailable = data

        # slots available will reduce only if enrollment is approved? 
        # yes

        db.session.add(learner)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 501,
                "message": "An error occurred while signing up. " + str(e) # duplicate
            }
        ), 501

    return jsonify(
        {
            "code": 201,
            "message": "Successful sign up for course."
        }
    ), 201

# gets courses created by an admin
@app.route("/admin_courses/<string:CreatedBy>")
def get_courses_by_admin(CreatedBy):
    admin = CreatedBy
    print(admin)
    courseList = Course.query.filter_by(CreatedBy=CreatedBy).all()
    if len(courseList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "courses": [course.to_dict() for course in courseList]
                },
                "message": "Courses created by admin {} successfully returned.".format(admin)
            },
              
        )
        # return classList
    return jsonify(
        {
            "code": 404,
            "message": "Can't find courses created by admin {}.".format(admin)
        }
    ), 404

# get pending approval enrollment
@app.route("/pending_courses")
def get_pending_courses():
    courseList = Learner.query.filter_by(assigned=0).filter_by(approved=None).all()
    if len(courseList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "pending": [course.to_dict() for course in courseList],
                    "Number of courses": len(courseList)
                },
                "message": "Courses pending approval successfully returned."
            },
              
        )
        # return classList
    return jsonify(
        {
            "code": 404,
            "message": "All courses have been vetted"
        }
    ), 404

# set self-enrollment period of a course
@app.route("/set_enrollment_period/<int:CourseID>", methods=["PUT"])
def set_enrollment_period(CourseID):
    course = Course.query.filter_by(CourseID=CourseID).first()
    if not course:
        return jsonify({
            "code": 404,
            "message": "Course not found"
        }), 404
    else:
        start = course.StartEnroll
        end = course.EndEnroll
        print(start, end)
        data = request.get_json()
        print(data)
        if "Start Date" in data:
            course.StartEnroll = data["Start Date"]
        if "End Date" in data:
            course.EndEnroll = data["End Date"]
        
        course.Open = 1
        
        db.session.commit()
        
        return jsonify({
            "code": 200,
            "data": {
                "course start of enrollment": course.StartEnroll,
                "course end of enrollment": course.EndEnroll
            },
            "message": "enrollment period successfully set"
        }), 200

# approve/reject self-enrollment
@app.route("/vet_self_enroll/<int:LearnerID>", methods=["PUT"])
def vet_self_enroll(LearnerID):
    # assigned = 0, approved = null (pending)
    Current = datetime.now()
    print(Current)
    learner = Learner.query.filter_by(LearnerID=LearnerID).filter_by(assigned=0).filter_by(approved=None).first()
    if not learner:
        return jsonify({
            "code": "404",
            "message": "Learner has not self-enrolled in any class."
        }), 404
    else:
        print(learner)
        courseToApprove = learner.CourseID
        classToApprove = learner.ClassID
        courseDetails = Course.query.filter_by(CourseID=courseToApprove).first()
        classDetails = CourseClass.query.filter_by(ClassId=classToApprove).first()
        print('enrollment period: ',courseDetails.StartEnroll, ' to ', courseDetails.EndEnroll)
        CourseStart = courseDetails.StartEnroll
        # CourseEnd = courseDetails.EndEnroll
        ClassStart = classDetails.StartDateTime
        # slotsAvailable = classDetails.SlotsAvailable


        data = request.get_json()
        print(data)

        # 
        if (Current >= CourseStart and Current < ClassStart):
            print('able to approve or reject enrollment')
        
            if data["Approved"] == "approved":
                learner.approved = 1
                classDetails.SlotsAvailable -= 1
            if data["Approved"] == "rejected":
                learner.approved = 0

            db.session.commit()

            return jsonify({
                "code": "200",
                "data": {
                    "learner pending course": learner.to_dict(),
                },
                "message": "Enrollment has been " + data['Approved']
            }), 200
        else:
            return jsonify({
                "code": "500",
                "message": "Enrollment cannot be approved or rejected."
            }), 500
            
                


if __name__ == '__main__':
    app.run(port=5100, debug=True)