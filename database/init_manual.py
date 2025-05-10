#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import traceback
import mysql.connector
from mysql.connector import Error

# 数据库连接配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'abc123'
}

# 数据库名称
DB_NAME = 'course_evaluation_system'

def execute_sql_file(connection, cursor, file_path):
    """执行SQL文件中的语句"""
    print(f"执行SQL文件: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            sql_script = file.read()
            
        # 分割SQL语句
        statements = sql_script.split(';')
        
        # 执行每条SQL语句
        for statement in statements:
            statement = statement.strip()
            if statement:
                try:
                    cursor.execute(statement)
                    connection.commit()
                except Error as e:
                    print(f"SQL执行错误: {e}")
                    
        print(f"SQL文件 {file_path} 执行完成")
    except Error as e:
        print(f"读取或执行SQL文件错误: {e}")
    except FileNotFoundError:
        print(f"文件未找到: {file_path}")

def create_database(connection, cursor, db_name):
    """创建数据库"""
    try:
        print(f"正在创建数据库 {db_name}...")
        cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
        cursor.execute(f"CREATE DATABASE {db_name} DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        connection.commit()
        print(f"数据库 {db_name} 创建成功")
        
        # 切换到新创建的数据库
        connection.database = db_name
        print(f"已切换到数据库: {db_name}")
    except Error as e:
        print(f"创建数据库错误: {e}")
        raise

def create_tables(connection, cursor):
    """创建表结构"""
    print("开始创建表结构...")
    try:
        # 创建角色表
        print("创建角色表...")
        cursor.execute("""
        CREATE TABLE Role (
            RoleID INT PRIMARY KEY,
            RoleName VARCHAR(20) NOT NULL,
            Description VARCHAR(100)
        )
        """)
        
        # 创建学生表
        print("创建学生表...")
        cursor.execute("""
        CREATE TABLE Student (
            StudentID VARCHAR(10) PRIMARY KEY,
            Name VARCHAR(50) NOT NULL,
            Major VARCHAR(50),
            Password VARCHAR(50) NOT NULL,
            RoleID INT NOT NULL,
            FOREIGN KEY (RoleID) REFERENCES Role(RoleID)
        )
        """)
        
        # 创建教师表
        print("创建教师表...")
        cursor.execute("""
        CREATE TABLE Teacher (
            TeacherID VARCHAR(10) PRIMARY KEY,
            Name VARCHAR(50) NOT NULL,
            Title VARCHAR(20),
            Password VARCHAR(50) NOT NULL,
            RoleID INT NOT NULL,
            FOREIGN KEY (RoleID) REFERENCES Role(RoleID)
        )
        """)
        
        # 创建课程表
        print("创建课程表...")
        cursor.execute("""
        CREATE TABLE Course (
            CourseID VARCHAR(10) PRIMARY KEY,
            Name VARCHAR(50) NOT NULL,
            Credit FLOAT NOT NULL
        )
        """)
        
        # 创建教学班表
        print("创建教学班表...")
        cursor.execute("""
        CREATE TABLE Class (
            ClassID INT AUTO_INCREMENT PRIMARY KEY,
            CourseID VARCHAR(10) NOT NULL,
            TeacherID VARCHAR(10) NOT NULL,
            Semester VARCHAR(20) NOT NULL,
            TimeLocation VARCHAR(100),
            FOREIGN KEY (CourseID) REFERENCES Course(CourseID),
            FOREIGN KEY (TeacherID) REFERENCES Teacher(TeacherID)
        )
        """)
        
        # 创建学生选课表
        print("创建学生选课表...")
        cursor.execute("""
        CREATE TABLE StudentClass (
            StudentID VARCHAR(10) NOT NULL,
            ClassID INT NOT NULL,
            SelectTime DATETIME NOT NULL,
            PRIMARY KEY (StudentID, ClassID),
            FOREIGN KEY (StudentID) REFERENCES Student(StudentID),
            FOREIGN KEY (ClassID) REFERENCES Class(ClassID)
        )
        """)
        
        # 创建评价表
        print("创建评价表...")
        cursor.execute("""
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
        )
        """)
        
        connection.commit()
        print("所有表结构创建成功")
    except Error as e:
        print(f"创建表结构错误: {e}")
        raise

def insert_initial_data(connection, cursor):
    """插入初始数据"""
    print("开始插入初始数据...")
    try:
        # 插入角色数据
        print("插入角色数据...")
        cursor.execute("""
        INSERT INTO Role (RoleID, RoleName, Description) VALUES
        (1, '学生', '可以评价所修课程'),
        (2, '教师', '可以查看所授课程的评价'),
        (3, '管理员', '可以管理系统数据')
        """)
        
        # 插入学生数据
        print("插入学生数据...")
        cursor.execute("""
        INSERT INTO Student (StudentID, Name, Major, Password, RoleID) VALUES
        ('S001', '张三', '计算机科学', '123456', 1),
        ('S002', '李四', '软件工程', '123456', 1),
        ('S003', '王五', '人工智能', '123456', 1),
        ('S004', '赵六', '数据科学', '123456', 1),
        ('S005', '钱七', '网络工程', '123456', 1)
        """)
        
        # 插入教师数据
        print("插入教师数据...")
        cursor.execute("""
        INSERT INTO Teacher (TeacherID, Name, Title, Password, RoleID) VALUES
        ('T001', '刘教授', '教授', '123456', 2),
        ('T002', '陈副教授', '副教授', '123456', 2),
        ('T003', '杨讲师', '讲师', '123456', 2)
        """)
        
        # 插入管理员数据
        print("插入管理员数据...")
        cursor.execute("""
        INSERT INTO Teacher (TeacherID, Name, Title, Password, RoleID) VALUES
        ('A001', '管理员', '管理员', 'admin123', 3)
        """)
        
        # 插入课程数据
        print("插入课程数据...")
        cursor.execute("""
        INSERT INTO Course (CourseID, Name, Credit) VALUES
        ('C001', '数据库原理', 4.0),
        ('C002', '操作系统', 3.5),
        ('C003', '计算机网络', 3.0)
        """)
        
        # 插入教学班数据
        print("插入教学班数据...")
        cursor.execute("""
        INSERT INTO Class (ClassID, CourseID, TeacherID, Semester, TimeLocation) VALUES
        (1, 'C001', 'T001', '2023-秋', '周一3-4节 主楼301'),
        (2, 'C001', 'T002', '2023-秋', '周三5-6节 主楼302'),
        (3, 'C002', 'T003', '2023-秋', '周二1-2节 主楼201'),
        (4, 'C003', 'T001', '2023-秋', '周四7-8节 主楼401')
        """)
        
        # 插入学生选课数据
        print("插入学生选课数据...")
        cursor.execute("""
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
        ('S005', 3, '2023-08-03 14:05:00')
        """)
        
        # 插入评价数据
        print("插入评价数据...")
        cursor.execute("""
        INSERT INTO Evaluation (EvaluationID, StudentID, ClassID, Score, Comment, EvaluationTime) VALUES
        (1, 'S001', 1, 5, '课程内容丰富，教师讲解清晰', '2023-12-20 15:30:00'),
        (2, 'S002', 1, 4, '整体不错，希望增加实践环节', '2023-12-21 10:20:00'),
        (3, 'S003', 2, 5, '教师教学认真负责，课程内容实用', '2023-12-22 16:45:00'),
        (4, 'S004', 2, 3, '课程内容较多，建议调整教学进度', '2023-12-23 09:15:00'),
        (5, 'S005', 1, 4, '教学质量很好，希望增加交流环节', '2023-12-24 14:30:00')
        """)
        
        connection.commit()
        print("所有初始数据插入成功")
    except Error as e:
        print(f"插入初始数据错误: {e}")
        raise

def create_procedures(connection, cursor):
    """创建存储过程"""
    print("开始创建存储过程...")
    procedures = [
        # 存储过程1：计算课程平均评分
        ("""
        CREATE PROCEDURE CalculateAverageScore(IN class_id INT, OUT avg_score FLOAT)
        BEGIN
          SELECT AVG(Score) INTO avg_score
          FROM Evaluation
          WHERE ClassID = class_id;
        END
        """, "CalculateAverageScore"),
        
        # 存储过程2：查询教师所授课程及评价
        ("""
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
        END
        """, "GetTeacherClassesWithEvaluation"),
        
        # 存储过程3：获取学生未评价课程列表
        ("""
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
        END
        """, "GetStudentUnevaluatedClasses"),
        
        # 存储过程4：获取学生已评价课程列表
        ("""
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
        END
        """, "GetStudentEvaluatedClasses"),
        
        # 存储过程5：添加课程评价
        ("""
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
        END
        """, "AddEvaluation"),
        
        # 存储过程6：获取教学班评价详情
        ("""
        CREATE PROCEDURE GetClassEvaluationDetails(IN class_id INT)
        BEGIN
          SELECT e.EvaluationID, e.Score, e.Comment, e.EvaluationTime,
                 s.StudentID, s.Name AS StudentName, s.Major
          FROM Evaluation e
          JOIN Student s ON e.StudentID = s.StudentID
          WHERE e.ClassID = class_id
          ORDER BY e.EvaluationTime DESC;
        END
        """, "GetClassEvaluationDetails")
    ]
    
    for proc_sql, proc_name in procedures:
        try:
            print(f"创建存储过程: {proc_name}...")
            # 首先尝试删除存在的存储过程
            try:
                cursor.execute(f"DROP PROCEDURE IF EXISTS {proc_name}")
                connection.commit()
            except Error as e:
                print(f"删除已存在的存储过程 {proc_name} 时出错 (可忽略): {e}")
            
            # 创建新的存储过程
            cursor.execute(proc_sql)
            connection.commit()
            print(f"存储过程 {proc_name} 创建成功")
        except Error as e:
            print(f"创建存储过程 {proc_name} 错误: {e}")
            traceback.print_exc()
    
    print("所有存储过程创建完成")

def create_triggers(connection, cursor):
    """创建触发器"""
    print("开始创建触发器...")
    triggers = [
        # 触发器1：验证评价唯一性
        ("""
        CREATE TRIGGER CheckUniqueEvaluation
        BEFORE INSERT ON Evaluation
        FOR EACH ROW
        BEGIN
          DECLARE count_val INT;
          SELECT COUNT(*) INTO count_val FROM Evaluation
          WHERE StudentID = NEW.StudentID AND ClassID = NEW.ClassID;
          
          IF count_val > 0 THEN
            SIGNAL SQLSTATE '45000' 
            SET MESSAGE_TEXT = '每个学生只能评价一次每个教学班';
          END IF;
        END
        """, "CheckUniqueEvaluation"),
        
        # 触发器2：评价验证触发器
        ("""
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
        END
        """, "ValidateEvaluation"),
        
        # 触发器3：添加评价时自动设置评价时间
        ("""
        CREATE TRIGGER SetEvaluationTime
        BEFORE INSERT ON Evaluation
        FOR EACH ROW
        BEGIN
          IF NEW.EvaluationTime IS NULL THEN
            SET NEW.EvaluationTime = NOW();
          END IF;
        END
        """, "SetEvaluationTime")
    ]
    
    for trigger_sql, trigger_name in triggers:
        try:
            print(f"创建触发器: {trigger_name}...")
            # 首先尝试删除存在的触发器
            try:
                cursor.execute(f"DROP TRIGGER IF EXISTS {trigger_name}")
                connection.commit()
            except Error as e:
                print(f"删除已存在的触发器 {trigger_name} 时出错 (可忽略): {e}")
            
            # 创建新的触发器
            cursor.execute(trigger_sql)
            connection.commit()
            print(f"触发器 {trigger_name} 创建成功")
        except Error as e:
            print(f"创建触发器 {trigger_name} 错误: {e}")
            traceback.print_exc()
    
    print("所有触发器创建完成")

def create_views(connection, cursor):
    """创建视图"""
    print("开始创建视图...")
    views = [
        # 视图1：课程评价统计视图
        ("""
        CREATE VIEW CourseEvaluationStats AS
        SELECT c.ClassID, co.CourseID, co.Name AS CourseName, 
               t.Name AS TeacherName, c.Semester,
               COUNT(e.EvaluationID) AS EvaluationCount,
               IFNULL(AVG(e.Score), 0) AS AverageScore
        FROM Class c
        JOIN Course co ON c.CourseID = co.CourseID
        JOIN Teacher t ON c.TeacherID = t.TeacherID
        LEFT JOIN Evaluation e ON c.ClassID = e.ClassID
        GROUP BY c.ClassID, co.CourseID, co.Name, t.Name, c.Semester
        """, "CourseEvaluationStats"),
        
        # 视图2：学生选课与评价视图
        ("""
        CREATE VIEW StudentClassEvaluation AS
        SELECT sc.StudentID, s.Name AS StudentName,
               c.ClassID, co.Name AS CourseName, t.Name AS TeacherName,
               c.Semester, e.Score, e.Comment, e.EvaluationTime
        FROM StudentClass sc
        JOIN Student s ON sc.StudentID = s.StudentID
        JOIN Class c ON sc.ClassID = c.ClassID
        JOIN Course co ON c.CourseID = co.CourseID
        JOIN Teacher t ON c.TeacherID = t.TeacherID
        LEFT JOIN Evaluation e ON sc.StudentID = e.StudentID AND sc.ClassID = e.ClassID
        """, "StudentClassEvaluation"),
        
        # 视图3：教师课程评价详情视图
        ("""
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
        GROUP BY t.TeacherID, t.Name, c.ClassID, co.Name, c.Semester
        """, "TeacherClassEvaluationDetails")
    ]
    
    for view_sql, view_name in views:
        try:
            print(f"创建视图: {view_name}...")
            # 首先尝试删除存在的视图
            try:
                cursor.execute(f"DROP VIEW IF EXISTS {view_name}")
                connection.commit()
            except Error as e:
                print(f"删除已存在的视图 {view_name} 时出错 (可忽略): {e}")
            
            # 创建新的视图
            cursor.execute(view_sql)
            connection.commit()
            print(f"视图 {view_name} 创建成功")
        except Error as e:
            print(f"创建视图 {view_name} 错误: {e}")
            traceback.print_exc()
    
    print("所有视图创建完成")

def main():
    """主函数"""
    connection = None
    cursor = None
    
    try:
        # 连接到MySQL
        print("正在连接到MySQL服务器...")
        connection = mysql.connector.connect(**DB_CONFIG)
        
        if connection.is_connected():
            print("数据库连接成功")
            cursor = connection.cursor()
            
            # 创建数据库
            create_database(connection, cursor, DB_NAME)
            
            # 创建表结构
            create_tables(connection, cursor)
            
            # 插入初始数据
            insert_initial_data(connection, cursor)
            
            # 创建存储过程
            create_procedures(connection, cursor)
            
            # 创建触发器
            create_triggers(connection, cursor)
            
            # 创建视图
            create_views(connection, cursor)
            
            print("数据库初始化完成！")
            
    except Exception as e:
        print(f"发生错误: {e}")
        traceback.print_exc()
        sys.exit(1)
        
    finally:
        # 关闭连接
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print("数据库连接已关闭")

if __name__ == "__main__":
    main() 