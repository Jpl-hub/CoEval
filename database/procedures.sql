USE course_evaluation_system;

-- 存储过程1：计算课程平均评分
DELIMITER //
CREATE PROCEDURE CalculateAverageScore(IN class_id INT, OUT avg_score FLOAT)
BEGIN
  SELECT AVG(Score) INTO avg_score
  FROM Evaluation
  WHERE ClassID = class_id;
END //
DELIMITER ;

-- 存储过程2：查询教师所授课程及评价
DELIMITER //
CREATE PROCEDURE GetTeacherClassesWithEvaluation(IN teacher_id VARCHAR(10))
BEGIN
  SELECT c.ClassID, co.Name AS CourseName, c.Semester, 
         COUNT(e.EvaluationID) AS EvaluationCount,
         IFNULL(AVG(e.Score), 0) AS AverageScore
  FROM Class c
  JOIN Course co ON c.CourseID = co.CourseID
  LEFT JOIN Evaluation e ON c.ClassID = e.ClassID
  WHERE c.TeacherID = teacher_id
  GROUP BY c.ClassID, co.Name, c.Semester;
END //
DELIMITER ;

-- 存储过程3：获取学生未评价课程列表
DELIMITER //
CREATE PROCEDURE GetStudentUnevaluatedClasses(IN student_id VARCHAR(10))
BEGIN
  SELECT c.ClassID, co.Name AS CourseName, t.Name AS TeacherName, 
         c.Semester, c.TimeLocation
  FROM StudentClass sc
  JOIN Class c ON sc.ClassID = c.ClassID
  JOIN Course co ON c.CourseID = co.CourseID
  JOIN Teacher t ON c.TeacherID = t.TeacherID
  LEFT JOIN Evaluation e ON sc.StudentID = e.StudentID AND sc.ClassID = e.ClassID
  WHERE sc.StudentID = student_id AND e.EvaluationID IS NULL;
END //
DELIMITER ;

-- 存储过程4：获取学生已评价课程列表
DELIMITER //
CREATE PROCEDURE GetStudentEvaluatedClasses(IN student_id VARCHAR(10))
BEGIN
  SELECT c.ClassID, co.Name AS CourseName, t.Name AS TeacherName, 
         c.Semester, c.TimeLocation, e.Score, e.Comment, e.EvaluationTime
  FROM StudentClass sc
  JOIN Class c ON sc.ClassID = c.ClassID
  JOIN Course co ON c.CourseID = co.CourseID
  JOIN Teacher t ON c.TeacherID = t.TeacherID
  JOIN Evaluation e ON sc.StudentID = e.StudentID AND sc.ClassID = e.ClassID
  WHERE sc.StudentID = student_id;
END //
DELIMITER ;

-- 存储过程5：添加课程评价
DELIMITER //
CREATE PROCEDURE AddEvaluation(
  IN student_id VARCHAR(10),
  IN class_id INT,
  IN score INT,
  IN comment TEXT,
  OUT success BOOLEAN
)
BEGIN
  DECLARE student_exists INT DEFAULT 0;
  DECLARE already_evaluated INT DEFAULT 0;
  
  -- 检查学生是否选了这门课
  SELECT COUNT(*) INTO student_exists
  FROM StudentClass
  WHERE StudentID = student_id AND ClassID = class_id;
  
  -- 检查是否已经评价过
  SELECT COUNT(*) INTO already_evaluated
  FROM Evaluation
  WHERE StudentID = student_id AND ClassID = class_id;
  
  -- 如果学生选了这门课并且还没有评价过，则添加评价
  IF student_exists > 0 AND already_evaluated = 0 THEN
    INSERT INTO Evaluation (StudentID, ClassID, Score, Comment, EvaluationTime)
    VALUES (student_id, class_id, score, comment, NOW());
    SET success = TRUE;
  ELSE
    SET success = FALSE;
  END IF;
END //
DELIMITER ;

-- 存储过程6：获取教学班评价详情
DELIMITER //
CREATE PROCEDURE GetClassEvaluationDetails(IN class_id INT)
BEGIN
  SELECT e.EvaluationID, e.Score, e.Comment, e.EvaluationTime,
         s.StudentID, s.Name AS StudentName, s.Major
  FROM Evaluation e
  JOIN Student s ON e.StudentID = s.StudentID
  WHERE e.ClassID = class_id
  ORDER BY e.EvaluationTime DESC;
END //
DELIMITER ;

-- 存储过程7：获取学生选课记录
DELIMITER //
CREATE PROCEDURE GetStudentEnrollments()
BEGIN
  SELECT sc.StudentID, s.Name AS StudentName, 
         sc.ClassID, c.CourseID, co.Name AS CourseName, 
         sc.SelectTime,
         (SELECT COUNT(*) FROM Evaluation e 
          WHERE e.StudentID = sc.StudentID AND e.ClassID = sc.ClassID) > 0 AS HasEvaluated
  FROM StudentClass sc
  JOIN Student s ON sc.StudentID = s.StudentID
  JOIN Class c ON sc.ClassID = c.ClassID
  JOIN Course co ON c.CourseID = co.CourseID
  ORDER BY sc.SelectTime DESC;
END //
DELIMITER ; 