from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any, Optional
from ..models.models import (
    StudentCreate, Student, 
    TeacherCreate, Teacher, 
    CourseCreate, Course,
    ClassCreate, Class, StudentClassCreate
)
from ..utils.auth import get_current_user
from ..utils.db import execute_query, execute_update

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={401: {"description": "Unauthorized"}},
)

# 仅管理员访问的验证函数
async def admin_only(user: Dict[str, Any] = Depends(get_current_user)):
    if user["role"] != 3:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="仅管理员可访问"
        )
    return user

# 学生管理
@router.get("/students", response_model=List[Dict[str, Any]])
async def get_students(_: Dict[str, Any] = Depends(admin_only)):
    """获取所有学生信息"""
    query = "SELECT StudentID, Name, Major, RoleID FROM Student"
    students = execute_query(query)
    return students

@router.post("/students", response_model=Dict[str, Any])
async def create_student(student: StudentCreate, _: Dict[str, Any] = Depends(admin_only)):
    """添加新学生"""
    query = """
    INSERT INTO Student (StudentID, Name, Major, Password, RoleID)
    VALUES (%s, %s, %s, %s, %s)
    """
    try:
        affected_rows = execute_update(
            query, 
            (student.student_id, student.name, student.major, student.password, student.role_id)
        )
        if affected_rows:
            return {"success": True, "message": "学生添加成功"}
        else:
            return {"success": False, "message": "学生添加失败"}
    except Exception as e:
        return {"success": False, "message": f"学生添加失败: {str(e)}"}

@router.put("/students/{student_id}", response_model=Dict[str, Any])
async def update_student(
    student_id: str, 
    student: StudentCreate, 
    _: Dict[str, Any] = Depends(admin_only)
):
    """更新学生信息"""
    query = """
    UPDATE Student
    SET Name = %s, Major = %s, Password = %s, RoleID = %s
    WHERE StudentID = %s
    """
    try:
        affected_rows = execute_update(
            query, 
            (student.name, student.major, student.password, student.role_id, student_id)
        )
        if affected_rows:
            return {"success": True, "message": "学生信息更新成功"}
        else:
            return {"success": False, "message": "学生不存在或信息未更改"}
    except Exception as e:
        return {"success": False, "message": f"学生信息更新失败: {str(e)}"}

@router.delete("/students/{student_id}", response_model=Dict[str, Any])
async def delete_student(student_id: str, _: Dict[str, Any] = Depends(admin_only)):
    """删除学生"""
    query = "DELETE FROM Student WHERE StudentID = %s"
    try:
        affected_rows = execute_update(query, (student_id,))
        if affected_rows:
            return {"success": True, "message": "学生删除成功"}
        else:
            return {"success": False, "message": "学生不存在"}
    except Exception as e:
        return {"success": False, "message": f"学生删除失败: {str(e)}"}

# 教师管理
@router.get("/teachers", response_model=List[Dict[str, Any]])
async def get_teachers(_: Dict[str, Any] = Depends(admin_only)):
    """获取所有教师信息"""
    query = "SELECT TeacherID, Name, Title, RoleID FROM Teacher"
    teachers = execute_query(query)
    return teachers

@router.post("/teachers", response_model=Dict[str, Any])
async def create_teacher(teacher: TeacherCreate, _: Dict[str, Any] = Depends(admin_only)):
    """添加新教师"""
    query = """
    INSERT INTO Teacher (TeacherID, Name, Title, Password, RoleID)
    VALUES (%s, %s, %s, %s, %s)
    """
    try:
        affected_rows = execute_update(
            query, 
            (teacher.teacher_id, teacher.name, teacher.title, teacher.password, teacher.role_id)
        )
        if affected_rows:
            return {"success": True, "message": "教师添加成功"}
        else:
            return {"success": False, "message": "教师添加失败"}
    except Exception as e:
        return {"success": False, "message": f"教师添加失败: {str(e)}"}

@router.put("/teachers/{teacher_id}", response_model=Dict[str, Any])
async def update_teacher(
    teacher_id: str, 
    teacher: TeacherCreate, 
    _: Dict[str, Any] = Depends(admin_only)
):
    """更新教师信息"""
    query = """
    UPDATE Teacher
    SET Name = %s, Title = %s, Password = %s, RoleID = %s
    WHERE TeacherID = %s
    """
    try:
        affected_rows = execute_update(
            query, 
            (teacher.name, teacher.title, teacher.password, teacher.role_id, teacher_id)
        )
        if affected_rows:
            return {"success": True, "message": "教师信息更新成功"}
        else:
            return {"success": False, "message": "教师不存在或信息未更改"}
    except Exception as e:
        return {"success": False, "message": f"教师信息更新失败: {str(e)}"}

@router.delete("/teachers/{teacher_id}", response_model=Dict[str, Any])
async def delete_teacher(teacher_id: str, _: Dict[str, Any] = Depends(admin_only)):
    """删除教师"""
    query = "DELETE FROM Teacher WHERE TeacherID = %s"
    try:
        affected_rows = execute_update(query, (teacher_id,))
        if affected_rows:
            return {"success": True, "message": "教师删除成功"}
        else:
            return {"success": False, "message": "教师不存在"}
    except Exception as e:
        return {"success": False, "message": f"教师删除失败: {str(e)}"}

# 课程管理
@router.get("/courses", response_model=List[Dict[str, Any]])
async def get_courses(_: Dict[str, Any] = Depends(admin_only)):
    """获取所有课程信息"""
    query = "SELECT CourseID, Name, Credit FROM Course"
    courses = execute_query(query)
    return courses

@router.post("/courses", response_model=Dict[str, Any])
async def create_course(course: CourseCreate, _: Dict[str, Any] = Depends(admin_only)):
    """添加新课程"""
    query = """
    INSERT INTO Course (CourseID, Name, Credit)
    VALUES (%s, %s, %s)
    """
    try:
        affected_rows = execute_update(
            query, 
            (course.course_id, course.name, course.credit)
        )
        if affected_rows:
            return {"success": True, "message": "课程添加成功"}
        else:
            return {"success": False, "message": "课程添加失败"}
    except Exception as e:
        return {"success": False, "message": f"课程添加失败: {str(e)}"}

@router.delete("/courses/{course_id}", response_model=Dict[str, Any])
async def delete_course(course_id: str, _: Dict[str, Any] = Depends(admin_only)):
    """删除课程"""
    query = "DELETE FROM Course WHERE CourseID = %s"
    try:
        affected_rows = execute_update(query, (course_id,))
        if affected_rows:
            return {"success": True, "message": "课程删除成功"}
        else:
            return {"success": False, "message": "课程不存在或无法删除"}
    except Exception as e:
        return {"success": False, "message": f"课程删除失败: {str(e)}"}

# 教学班管理
@router.get("/classes", response_model=List[Dict[str, Any]])
async def get_classes(_: Dict[str, Any] = Depends(admin_only)):
    """获取所有教学班信息"""
    query = """
    SELECT c.ClassID, c.CourseID, co.Name AS CourseName, 
           c.TeacherID, t.Name AS TeacherName, 
           c.Semester, c.TimeLocation,
           COUNT(e.EvaluationID) AS EvaluationCount,
           IFNULL(AVG(e.Score), 0) AS AverageScore
    FROM Class c
    JOIN Course co ON c.CourseID = co.CourseID
    JOIN Teacher t ON c.TeacherID = t.TeacherID
    LEFT JOIN Evaluation e ON c.ClassID = e.ClassID
    GROUP BY c.ClassID, c.CourseID, co.Name, c.TeacherID, t.Name, c.Semester, c.TimeLocation
    """
    classes = execute_query(query)
    return classes

@router.post("/classes", response_model=Dict[str, Any])
async def create_class(class_info: ClassCreate, _: Dict[str, Any] = Depends(admin_only)):
    """添加新教学班"""
    query = """
    INSERT INTO Class (CourseID, TeacherID, Semester, TimeLocation)
    VALUES (%s, %s, %s, %s)
    """
    try:
        affected_rows = execute_update(
            query, 
            (class_info.course_id, class_info.teacher_id, class_info.semester, class_info.time_location)
        )
        if affected_rows:
            return {"success": True, "message": "教学班添加成功"}
        else:
            return {"success": False, "message": "教学班添加失败"}
    except Exception as e:
        return {"success": False, "message": f"教学班添加失败: {str(e)}"}

# 学生选课管理
@router.post("/student-class", response_model=Dict[str, Any])
async def create_student_class(
    student_class: StudentClassCreate, 
    _: Dict[str, Any] = Depends(admin_only)
):
    """为学生添加选课记录"""
    query = """
    INSERT INTO StudentClass (StudentID, ClassID, SelectTime)
    VALUES (%s, %s, NOW())
    """
    try:
        affected_rows = execute_update(
            query, 
            (student_class.student_id, student_class.class_id)
        )
        if affected_rows:
            return {"success": True, "message": "选课记录添加成功"}
        else:
            return {"success": False, "message": "选课记录添加失败"}
    except Exception as e:
        return {"success": False, "message": f"选课记录添加失败: {str(e)}"}

@router.get("/enrollments", response_model=List[Dict[str, Any]])
async def get_student_enrollments(_: Dict[str, Any] = Depends(admin_only)):
    """获取学生选课记录"""
    query = """
    SELECT sc.StudentID, s.Name AS StudentName, 
           sc.ClassID, c.CourseID, co.Name AS CourseName, 
           sc.SelectTime,
           (SELECT COUNT(*) FROM Evaluation e 
            WHERE e.StudentID = sc.StudentID AND e.ClassID = sc.ClassID) > 0 AS HasEvaluated
    FROM StudentClass sc
    JOIN Student s ON sc.StudentID = s.StudentID
    JOIN Class c ON sc.ClassID = c.ClassID
    JOIN Course co ON c.CourseID = co.CourseID
    ORDER BY sc.SelectTime DESC
    """
    enrollments = execute_query(query)
    return enrollments

@router.delete("/student-class", response_model=Dict[str, Any])
async def delete_student_class(
    student_id: str,
    class_id: int,
    _: Dict[str, Any] = Depends(admin_only)
):
    """删除学生选课记录"""
    query = "DELETE FROM StudentClass WHERE StudentID = %s AND ClassID = %s"
    try:
        affected_rows = execute_update(query, (student_id, class_id))
        if affected_rows:
            return {"success": True, "message": "选课记录删除成功"}
        else:
            return {"success": False, "message": "选课记录不存在"}
    except Exception as e:
        return {"success": False, "message": f"选课记录删除失败: {str(e)}"}

# 系统统计信息
@router.get("/statistics", response_model=Dict[str, Any])
async def get_system_statistics(_: Dict[str, Any] = Depends(admin_only)):
    """获取系统统计信息"""
    # 学生数量
    student_count_query = "SELECT COUNT(*) as count FROM Student"
    student_count = execute_query(student_count_query)
    
    # 教师数量
    teacher_count_query = "SELECT COUNT(*) as count FROM Teacher WHERE RoleID = 2"
    teacher_count = execute_query(teacher_count_query)
    
    # 课程数量
    course_count_query = "SELECT COUNT(*) as count FROM Course"
    course_count = execute_query(course_count_query)
    
    # 教学班数量
    class_count_query = "SELECT COUNT(*) as count FROM Class"
    class_count = execute_query(class_count_query)
    
    # 评价数量
    evaluation_count_query = "SELECT COUNT(*) as count FROM Evaluation"
    evaluation_count = execute_query(evaluation_count_query)
    
    # 平均评分
    avg_score_query = "SELECT AVG(Score) as avg_score FROM Evaluation"
    avg_score = execute_query(avg_score_query)
    
    # 返回统计结果
    return {
        "student_count": student_count[0]["count"] if student_count else 0,
        "teacher_count": teacher_count[0]["count"] if teacher_count else 0,
        "course_count": course_count[0]["count"] if course_count else 0,
        "class_count": class_count[0]["count"] if class_count else 0,
        "evaluation_count": evaluation_count[0]["count"] if evaluation_count else 0,
        "average_score": avg_score[0]["avg_score"] if avg_score and avg_score[0]["avg_score"] else 0
    } 