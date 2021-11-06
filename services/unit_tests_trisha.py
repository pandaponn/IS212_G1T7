import unittest

from mono_trisha import Course

class TestCourse(unittest.TestCase):
    def test_to_dict(self):
        c1 = Course(
            CourseID=1,
            CourseName='Python Basics',
            PreReq=None,
            Classes=3,
            StartEnroll="Fri, 01 Oct 2021 00:00:00 GMT",
            EndEnroll="Fri, 08 Oct 2021 00:00:00 GMT",
            Open=0,
            CreatedBy=1,
            UpdatedBy=None,
            CreatedTime="Wed, 13 Oct 2021 22:28:29 GMT",
            UpdateTime=None,
            IsFull=False
        )
        self.assertEqual(c1.to_dict(), {
        "Classes": 3, 
        "CourseID": 1, 
        "CourseName": "Python Basics", 
        "CreatedBy": 1, 
        "CreatedTime": "Wed, 13 Oct 2021 22:28:29 GMT", 
        "EndEnroll": "Fri, 08 Oct 2021 00:00:00 GMT", 
        "IsFull": False, 
        "Open": 0, 
        "PreReq": None, 
        "StartEnroll": "Fri, 01 Oct 2021 00:00:00 GMT", 
        "UpdateTime": None, 
        "UpdatedBy": None
            }
        )
    
    def test_is_open(self):
        c1 = Course(
            CourseID=1,
            CourseName='Python Basics',
            PreReq=None,
            Classes=3,
            StartEnroll="Fri, 01 Oct 2021 00:00:00 GMT",
            EndEnroll="Fri, 08 Oct 2021 00:00:00 GMT",
            Open=0,
            CreatedBy=1,
            UpdatedBy=None,
            CreatedTime="Wed, 13 Oct 2021 22:28:29 GMT",
            UpdateTime=None,
            IsFull=False
        )
        self.assertEqual(c1.Open, 0)

    def test_has_prereq(self):
        c1 = Course(
            CourseID=1,
            CourseName='Python Basics',
            PreReq=None,
            Classes=3,
            StartEnroll="Fri, 01 Oct 2021 00:00:00 GMT",
            EndEnroll="Fri, 08 Oct 2021 00:00:00 GMT",
            Open=0,
            CreatedBy=1,
            UpdatedBy=None,
            CreatedTime="Wed, 13 Oct 2021 22:28:29 GMT",
            UpdateTime=None,
            IsFull=False
        )
        self.assertEqual(c1.PreReq, )
        