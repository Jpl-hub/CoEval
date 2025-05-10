-- 创建数据库
DROP DATABASE IF EXISTS course_evaluation_system;
CREATE DATABASE course_evaluation_system;
USE course_evaluation_system;

-- 创建角色表
CREATE TABLE Role (
    RoleID INT PRIMARY KEY,
    RoleName VARCHAR(20) NOT NULL,
    Description VARCHAR(100)
);

-- 创建学生表
CREATE TABLE Student (
    StudentID VARCHAR(10) PRIMARY KEY,
    Name VARCHAR(50) NOT NULL,
    Major VARCHAR(50),
    Password VARCHAR(50) NOT NULL,
    RoleID INT NOT NULL,
    FOREIGN KEY (RoleID) REFERENCES Role(RoleID)
);

-- 创建教师表
CREATE TABLE Teacher (
    TeacherID VARCHAR(10) PRIMARY KEY,
    Name VARCHAR(50) NOT NULL,
    Title VARCHAR(20),
    Password VARCHAR(50) NOT NULL,
    RoleID INT NOT NULL,
    FOREIGN KEY (RoleID) REFERENCES Role(RoleID)
);

-- 创建课程表
CREATE TABLE Course (
    CourseID VARCHAR(10) PRIMARY KEY,
    Name VARCHAR(50) NOT NULL,
    Credit FLOAT NOT NULL
);

-- 创建教学班表
CREATE TABLE Class (
    ClassID INT AUTO_INCREMENT PRIMARY KEY,
    CourseID VARCHAR(10) NOT NULL,
    TeacherID VARCHAR(10) NOT NULL,
    Semester VARCHAR(20) NOT NULL,
    TimeLocation VARCHAR(100),
    FOREIGN KEY (CourseID) REFERENCES Course(CourseID),
    FOREIGN KEY (TeacherID) REFERENCES Teacher(TeacherID)
);

-- 创建学生选课表
CREATE TABLE StudentClass (
    StudentID VARCHAR(10) NOT NULL,
    ClassID INT NOT NULL,
    SelectTime DATETIME NOT NULL,
    PRIMARY KEY (StudentID, ClassID),
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID),
    FOREIGN KEY (ClassID) REFERENCES Class(ClassID)
);

-- 创建评价表
CREATE TABLE Evaluation (
    EvaluationID INT AUTO_INCREMENT PRIMARY KEY,
    StudentID VARCHAR(10) NOT NULL,
    ClassID INT NOT NULL,
    Score INT NOT NULL,
    Comment TEXT,
    EvaluationTime DATETIME NOT NULL,
    UNIQUE KEY (StudentID, ClassID),
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID),
    FOREIGN KEY (ClassID) REFERENCES Class(ClassID)
);

-- 插入角色数据
INSERT INTO Role (RoleID, RoleName, Description) VALUES
(1, '学生', '可以评价所修课程'),
(2, '教师', '可以查看所授课程的评价'),
(3, '管理员', '可以管理系统数据');

-- 插入学生数据
INSERT INTO Student (StudentID, Name, Major, Password, RoleID) VALUES
('S001', '张三', '计算机科学', '123456', 1),
('S002', '李四', '软件工程', '123456', 1),
('S003', '王五', '人工智能', '123456', 1),
('S004', '赵六', '数据科学', '123456', 1),
('S005', '钱七', '网络工程', '123456', 1);

-- 插入教师数据
INSERT INTO Teacher (TeacherID, Name, Title, Password, RoleID) VALUES
('T001', '刘教授', '教授', '123456', 2),
('T002', '陈副教授', '副教授', '123456', 2),
('T003', '杨讲师', '讲师', '123456', 2);

-- 插入管理员数据 (假设管理员信息存储在教师表中)
INSERT INTO Teacher (TeacherID, Name, Title, Password, RoleID) VALUES
('A001', '管理员', '管理员', 'admin123', 3);

-- 插入课程数据
INSERT INTO Course (CourseID, Name, Credit) VALUES
('C001', '数据库原理', 4.0),
('C002', '操作系统', 3.5),
('C003', '计算机网络', 3.0);

-- 插入教学班数据
INSERT INTO Class (ClassID, CourseID, TeacherID, Semester, TimeLocation) VALUES
(1, 'C001', 'T001', '2023-秋', '周一3-4节 主楼301'),
(2, 'C001', 'T002', '2023-秋', '周三5-6节 主楼302'),
(3, 'C002', 'T003', '2023-秋', '周二1-2节 主楼201'),
(4, 'C003', 'T001', '2023-秋', '周四7-8节 主楼401');

-- 插入学生选课数据
INSERT INTO StudentClass (StudentID, ClassID, SelectTime) VALUES
('S001', 1, '2023-08-01 10:00:00'),
('S001', 3, '2023-08-01 10:05:00'),
('S002', 1, '2023-08-01 11:00:00'),
('S002', 4, '2023-08-01 11:05:00'),
('S003', 2, '2023-08-02 09:00:00'),
('S003', 3, '2023-08-02 09:05:00'),
('S004', 2, '2023-08-02 10:00:00'),
('S004', 4, '2023-08-02 10:05:00'),
('S005', 1, '2023-08-03 14:00:00'),
('S005', 3, '2023-08-03 14:05:00');

-- 插入评价数据
INSERT INTO Evaluation (EvaluationID, StudentID, ClassID, Score, Comment, EvaluationTime) VALUES
(1, 'S001', 1, 5, '课程内容丰富，教师讲解清晰', '2023-12-20 15:30:00'),
(2, 'S002', 1, 4, '整体不错，希望增加实践环节', '2023-12-21 10:20:00'),
(3, 'S003', 2, 5, '教师教学认真负责，课程内容实用', '2023-12-22 16:45:00'),
(4, 'S004', 2, 3, '课程内容较多，建议调整教学进度', '2023-12-23 09:15:00'),
(5, 'S005', 1, 4, '教学质量很好，希望增加交流环节', '2023-12-24 14:30:00'); 