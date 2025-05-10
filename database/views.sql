USE course_evaluation_system;

-- 视图1：课程评价统计视图
CREATE VIEW CourseEvaluationStats AS
SELECT c.ClassID, co.CourseID, co.Name AS CourseName, 
       t.Name AS TeacherName, c.Semester,
       COUNT(e.EvaluationID) AS EvaluationCount,
       IFNULL(AVG(e.Score), 0) AS AverageScore
FROM Class c
JOIN Course co ON c.CourseID = co.CourseID
JOIN Teacher t ON c.TeacherID = t.TeacherID
LEFT JOIN Evaluation e ON c.ClassID = e.ClassID
GROUP BY c.ClassID, co.CourseID, co.Name, t.Name, c.Semester;

-- 视图2：学生选课与评价视图
CREATE VIEW StudentClassEvaluation AS
SELECT sc.StudentID, s.Name AS StudentName,
       c.ClassID, co.Name AS CourseName, t.Name AS TeacherName,
       c.Semester, e.Score, e.Comment, e.EvaluationTime
FROM StudentClass sc
JOIN Student s ON sc.StudentID = s.StudentID
JOIN Class c ON sc.ClassID = c.ClassID
JOIN Course co ON c.CourseID = co.CourseID
JOIN Teacher t ON c.TeacherID = t.TeacherID
LEFT JOIN Evaluation e ON sc.StudentID = e.StudentID AND sc.ClassID = e.ClassID;

-- 视图3：教师课程评价详情视图
CREATE VIEW TeacherClassEvaluationDetails AS
SELECT t.TeacherID, t.Name AS TeacherName, 
       c.ClassID, co.Name AS CourseName, c.Semester,
       COUNT(e.EvaluationID) AS EvaluationCount,
       IFNULL(AVG(e.Score), 0) AS AverageScore,
       COUNT(CASE WHEN e.Score = 5 THEN 1 END) AS Score5Count,
       COUNT(CASE WHEN e.Score = 4 THEN 1 END) AS Score4Count,
       COUNT(CASE WHEN e.Score = 3 THEN 1 END) AS Score3Count,
       COUNT(CASE WHEN e.Score = 2 THEN 1 END) AS Score2Count,
       COUNT(CASE WHEN e.Score = 1 THEN 1 END) AS Score1Count
FROM Teacher t
JOIN Class c ON t.TeacherID = c.TeacherID
JOIN Course co ON c.CourseID = co.CourseID
LEFT JOIN Evaluation e ON c.ClassID = e.ClassID
GROUP BY t.TeacherID, t.Name, c.ClassID, co.Name, c.Semester; 