USE course_evaluation_system;

-- 触发器1：验证评价唯一性
DELIMITER //
CREATE TRIGGER CheckUniqueEvaluation
BEFORE INSERT ON Evaluation
FOR EACH ROW
BEGIN
  DECLARE count INT;
  SELECT COUNT(*) INTO count FROM Evaluation
  WHERE StudentID = NEW.StudentID AND ClassID = NEW.ClassID;
  
  IF count > 0 THEN
    SIGNAL SQLSTATE '45000' 
    SET MESSAGE_TEXT = '每个学生只能评价一次每个教学班';
  END IF;
END //
DELIMITER ;

-- 触发器2：评价验证触发器
DELIMITER //
CREATE TRIGGER ValidateEvaluation
BEFORE INSERT ON Evaluation
FOR EACH ROW
BEGIN
  DECLARE student_exists INT;
  
  -- 检查学生是否选了这门课
  SELECT COUNT(*) INTO student_exists
  FROM StudentClass
  WHERE StudentID = NEW.StudentID AND ClassID = NEW.ClassID;
  
  -- 如果学生没有选这门课，不允许评价
  IF student_exists = 0 THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = '学生未选择该课程，不能进行评价';
  END IF;
  
  -- 验证评分范围
  IF NEW.Score < 1 OR NEW.Score > 5 THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = '评分必须在1-5分之间';
  END IF;
END //
DELIMITER ;

-- 触发器3：添加评价时自动设置评价时间
DELIMITER //
CREATE TRIGGER SetEvaluationTime
BEFORE INSERT ON Evaluation
FOR EACH ROW
BEGIN
  IF NEW.EvaluationTime IS NULL THEN
    SET NEW.EvaluationTime = NOW();
  END IF;
END //
DELIMITER ; 