-- phpMyAdmin SQL Dump
-- version 4.9.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Nov 01, 2021 at 07:20 AM
-- Server version: 8.0.18
-- PHP Version: 7.4.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `is212_project`
--

-- --------------------------------------------------------

--
-- Table structure for table `class`
--

DROP TABLE IF EXISTS `class`;
CREATE TABLE IF NOT EXISTS `class` (
  `classId` int(100) NOT NULL AUTO_INCREMENT,
  `courseId` int(100) NOT NULL,
  `courseName` varchar(100) NOT NULL,
  `trainerId` int(100) DEFAULT NULL,
  `startDateTime` datetime(6) NOT NULL,
  `endDateTime` datetime(6) NOT NULL,
  `capacity` int(100) NOT NULL,
  `slotsAvailable` int(100) NOT NULL,
  PRIMARY KEY (`classId`,`courseId`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `class`
--

INSERT INTO `class` (`classId`, `courseId`, `courseName`, `trainerId`, `startDateTime`, `endDateTime`, `capacity`, `slotsAvailable`) VALUES
(1, 1, 'Python Basics', 1, '2021-10-13 09:00:00.000000', '2021-10-27 21:00:00.000000', 40, 39),
(2, 1, 'Python Basics', 1, '2021-10-11 11:00:00.000000', '2021-10-25 18:00:00.000000', 13, 8),
(3, 1, 'Python Basics', 2, '2021-10-12 10:00:00.000000', '2021-10-26 19:00:00.000000', 14, 13),
(4, 2, 'Python Intermediate', 3, '2021-10-15 09:00:00.000000', '2021-10-29 16:00:00.000000', 30, 25),
(5, 3, 'Extreme Python', 2, '2021-10-19 00:00:00.000000', '2021-10-26 00:00:00.000000', 2, 1),
(6, 4, 'Data Management', 1, '2021-11-20 08:00:00.000000', '2021-11-30 17:00:00.000000', 10, 8),
(7, 5, 'Fire Python', 2, '2021-11-25 08:00:00.000000', '2021-12-15 23:59:00.000000', 10, 10),
(8, 5, 'Fire Python', 1, '2021-11-26 08:00:00.000000', '2021-12-16 23:59:00.000000', 10, 10);

-- --------------------------------------------------------

--
-- Table structure for table `course`
--

DROP TABLE IF EXISTS `course`;
CREATE TABLE IF NOT EXISTS `course` (
  `courseId` int(100) NOT NULL AUTO_INCREMENT,
  `courseName` varchar(100) NOT NULL,
  `preReq` int(100) DEFAULT NULL,
  `classes` int(100) NOT NULL,
  `startEnroll` datetime NOT NULL,
  `endEnroll` datetime NOT NULL,
  `open` tinyint(4) NOT NULL,
  `createdBy` varchar(100) NOT NULL,
  `updatedBy` varchar(100) DEFAULT NULL,
  `createdTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updateTime` timestamp NULL DEFAULT NULL,
  `isFull` tinyint(1) NOT NULL,
  PRIMARY KEY (`courseId`),
  KEY `createdBy` (`createdBy`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `course`
--

INSERT INTO `course` (`courseId`, `courseName`, `preReq`, `classes`, `startEnroll`, `endEnroll`, `open`, `createdBy`, `updatedBy`, `createdTime`, `updateTime`, `isFull`) VALUES
(1, 'Python Basics', NULL, 3, '2021-10-01 00:00:00', '2021-10-08 00:00:00', 0, 'hr1', NULL, '2021-10-13 14:28:29', NULL, 0),
(2, 'Python Intermediate', 1, 1, '2021-10-06 00:00:00', '2021-10-12 00:00:00', 0, 'hr1', NULL, '2021-10-13 14:28:29', NULL, 1),
(3, 'Extreme Python', 2, 1, '2021-10-13 00:00:00', '2021-10-17 00:00:00', 0, 'hr2', NULL, '2021-10-13 14:29:29', NULL, 0),
(4, 'Data Management', 1, 1, '2021-10-28 00:00:00', '2021-11-17 00:00:00', 1, 'hr2', NULL, '2021-10-13 14:29:29', NULL, 0),
(5, 'Fire Python', 3, 2, '2021-11-01 00:00:00', '2021-11-20 00:00:00', 1, 'hr1', NULL, '2021-10-13 14:29:29', NULL, 0);

-- --------------------------------------------------------

--
-- Table structure for table `coursematerials`
--

DROP TABLE IF EXISTS `coursematerials`;
CREATE TABLE IF NOT EXISTS `coursematerials` (
  `course_id` int(11) NOT NULL,
  `class_id` int(11) NOT NULL,
  `chapter_id` int(11) NOT NULL,
  `subchapter_id` varchar(100) NOT NULL,
  `chapter_name` varchar(100) NOT NULL,
  `content` varchar(100) NOT NULL,
  PRIMARY KEY (`course_id`,`class_id`,`chapter_id`,`subchapter_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `coursematerials`
--

INSERT INTO `coursematerials` (`course_id`, `class_id`, `chapter_id`, `subchapter_id`, `chapter_name`, `content`) VALUES
(1, 1, 1, '1a', 'Introduction to Python', 'slides'),
(1, 1, 1, '1b', 'Printing hello world', 'source code'),
(1, 1, 2, '2a', 'For Loop', 'slides'),
(1, 1, 2, '2b', 'Class Exercise', 'code'),
(1, 2, 1, '1a', 'I love Coffee', 'Coffee Beans'),
(1, 2, 1, '1b', 'I love Tea', 'Tea Leaves'),
(1, 2, 2, '2a', 'Baking Cake', 'Slides'),
(1, 2, 2, '2b', 'Cookies', 'Videos');

-- --------------------------------------------------------

--
-- Table structure for table `engineer`
--

DROP TABLE IF EXISTS `engineer`;
CREATE TABLE IF NOT EXISTS `engineer` (
  `engineerId` int(100) NOT NULL AUTO_INCREMENT,
  `engineerName` varchar(100) NOT NULL,
  `totalClasses` int(100) NOT NULL,
  `courseCompleted` int(100) DEFAULT NULL,
  `trainer` int(100) NOT NULL,
  `learner` int(100) NOT NULL,
  `learnerId` int(11) DEFAULT NULL,
  PRIMARY KEY (`engineerId`) USING BTREE,
  KEY `engineerId` (`engineerId`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `engineer`
--

INSERT INTO `engineer` (`engineerId`, `engineerName`, `totalClasses`, `courseCompleted`, `trainer`, `learner`, `learnerId`) VALUES
(1, 'Ling Li', 2, 1, 0, 1, 1),
(2, 'Trisha', 3, NULL, 0, 1, 2),
(3, 'Faith', 5, NULL, 0, 1, 3),
(4, 'Kal', 2, 3, 1, 0, NULL),
(5, 'Dora', 3, 4, 1, 1, 4);

-- --------------------------------------------------------

--
-- Table structure for table `ischapviewable`
--

DROP TABLE IF EXISTS `ischapviewable`;
CREATE TABLE IF NOT EXISTS `ischapviewable` (
  `learner_id` int(11) NOT NULL,
  `course_id` int(11) NOT NULL,
  `class_id` int(11) NOT NULL,
  `chapter_id` int(11) NOT NULL,
  `subchapter_id` varchar(100) NOT NULL,
  `chapter_viewable` tinyint(1) NOT NULL,
  `chapter_viewed` tinyint(1) NOT NULL,
  PRIMARY KEY (`learner_id`,`course_id`,`class_id`,`chapter_id`,`subchapter_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `ischapviewable`
--

INSERT INTO `ischapviewable` (`learner_id`, `course_id`, `class_id`, `chapter_id`, `subchapter_id`, `chapter_viewable`, `chapter_viewed`) VALUES
(1, 1, 1, 1, '1a', 1, 1),
(1, 1, 1, 1, '1b', 1, 1),
(1, 1, 1, 2, '2a', 0, 0),
(1, 1, 1, 2, '2b', 0, 0),
(2, 1, 2, 1, '1a', 1, 0),
(2, 1, 2, 1, '1b', 1, 0),
(2, 1, 2, 2, '2a', 0, 0),
(2, 1, 2, 2, '2b', 0, 0),
(4, 1, 1, 1, '1a', 1, 0),
(4, 1, 1, 1, '1b', 1, 0),
(4, 1, 1, 2, '2a', 0, 0),
(4, 1, 1, 2, '2b', 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `learner`
--

DROP TABLE IF EXISTS `learner`;
CREATE TABLE IF NOT EXISTS `learner` (
  `LearnerID` int(11) NOT NULL,
  `engineerId` int(100) NOT NULL,
  `LearnerName` varchar(100) NOT NULL,
  `CourseID` int(11) NOT NULL,
  `ClassID` int(11) NOT NULL,
  `assigned` tinyint(4) NOT NULL,
  `approved` tinyint(4) DEFAULT NULL,
  `courseCompleted` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`LearnerID`,`ClassID`,`CourseID`) USING BTREE,
  KEY `engineerId` (`engineerId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `learner`
--

INSERT INTO `learner` (`LearnerID`, `engineerId`, `LearnerName`, `CourseID`, `ClassID`, `assigned`, `approved`, `courseCompleted`) VALUES
(1, 1, 'Ling Li', 1, 1, 1, 1, 1),
(1, 1, 'Ling Li', 2, 4, 0, NULL, 1),
(1, 1, 'Ling Li', 4, 6, 0, 1, 0),
(2, 2, 'Trisha', 1, 1, 1, NULL, 1),
(2, 2, 'Trisha', 2, 4, 0, 1, 0);

-- --------------------------------------------------------

--
-- Table structure for table `questions`
--

DROP TABLE IF EXISTS `questions`;
CREATE TABLE IF NOT EXISTS `questions` (
  `question_id` int(11) NOT NULL AUTO_INCREMENT,
  `quiz_id` int(11) NOT NULL,
  `qn_type` varchar(100) NOT NULL,
  `question` mediumtext NOT NULL,
  `options` mediumtext,
  `answer` mediumtext NOT NULL,
  PRIMARY KEY (`question_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `questions`
--

INSERT INTO `questions` (`question_id`, `quiz_id`, `qn_type`, `question`, `options`, `answer`) VALUES
(1, 1, 'tf', 'Is SPM a good mod?', NULL, 'False'),
(2, 1, 'mcq', 'What to do tomorrow?', 'Work^Sleep^Nap^Eat', 'Eat'),
(3, 2, 'mcq', 'Dinner?', 'Macs^BK^KFC^Jollibee', 'Jollibee'),
(4, 2, 'tf', 'Is SIS fun?', NULL, 'False');

-- --------------------------------------------------------

--
-- Table structure for table `quiz`
--

DROP TABLE IF EXISTS `quiz`;
CREATE TABLE IF NOT EXISTS `quiz` (
  `quiz_id` int(11) NOT NULL AUTO_INCREMENT,
  `quiz_name` varchar(100) DEFAULT NULL,
  `course_id` int(11) NOT NULL,
  `class_id` int(11) NOT NULL,
  `chapter_id` int(11) NOT NULL,
  `isGraded` varchar(100) NOT NULL,
  `passing_grade` int(11) NOT NULL,
  `duration` int(11) NOT NULL,
  PRIMARY KEY (`quiz_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `quiz`
--

INSERT INTO `quiz` (`quiz_id`, `quiz_name`, `course_id`, `class_id`, `chapter_id`, `isGraded`, `passing_grade`, `duration`) VALUES
(1, 'Quiz 1', 1, 1, 1, 'Y', 3, 10),
(2, 'Quiz 2', 1, 1, 2, 'N', 5, 5),
(3, 'Quiz 3', 1, 1, 2, 'Y', 5, 10);

-- --------------------------------------------------------

--
-- Table structure for table `quiz_results`
--

DROP TABLE IF EXISTS `quiz_results`;
CREATE TABLE IF NOT EXISTS `quiz_results` (
  `learner_id` int(11) NOT NULL,
  `quiz_id` int(11) NOT NULL,
  `isViewable` int(11) NOT NULL,
  `score` int(11) NOT NULL,
  `quizPass` int(11) NOT NULL,
  `attempts` int(11) NOT NULL,
  PRIMARY KEY (`learner_id`,`quiz_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `quiz_results`
--

INSERT INTO `quiz_results` (`learner_id`, `quiz_id`, `isViewable`, `score`, `quizPass`, `attempts`) VALUES
(1, 1, 1, 3, 1, 1),
(2, 1, 3, 1, 1, 1),
(2, 2, 3, 1, 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `trainer`
--

DROP TABLE IF EXISTS `trainer`;
CREATE TABLE IF NOT EXISTS `trainer` (
  `trainerId` int(100) NOT NULL AUTO_INCREMENT,
  `engineerId` int(100) NOT NULL,
  `trainerName` varchar(100) NOT NULL,
  `courseAssigned` int(100) NOT NULL,
  `classAssigned` int(100) NOT NULL,
  PRIMARY KEY (`trainerId`,`engineerId`) USING BTREE,
  KEY `engineerId` (`engineerId`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `trainer`
--

INSERT INTO `trainer` (`trainerId`, `engineerId`, `trainerName`, `courseAssigned`, `classAssigned`) VALUES
(1, 4, 'Kal', 0, 0),
(2, 5, 'Dora', 0, 0);

DROP TABLE IF EXISTS `administrator`;
CREATE TABLE IF NOT EXISTS `administrator` (
  `adminID` int(100) NOT NULL AUTO_INCREMENT,
  `adminName` varchar(100) NOT NULL,
  PRIMARY KEY (`adminID`) USING BTREE,
  KEY `adminID` (`adminID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `administrator`
--

INSERT INTO `administrator` (`adminID`, `adminName`) VALUES
(1, 'Kai Ying'),
(2, 'Ling'),
(3, 'Li');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
