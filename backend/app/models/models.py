from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# 登录相关模型
class LoginRequest(BaseModel):
    user_id: str
    password: str
    role: int  # 1-学生, 2-教师, 3-管理员

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user_info: dict

# 用户相关模型
class StudentBase(BaseModel):
    student_id: str = Field(..., description="学号")
    name: str = Field(..., description="姓名")
    major: Optional[str] = Field(None, description="专业")
    
class StudentCreate(StudentBase):
    password: str = Field(..., description="密码")
    role_id: int = Field(1, description="角色ID, 默认为学生(1)")

class Student(StudentBase):
    role_id: int = Field(..., description="角色ID")
    
    class Config:
        from_attributes = True

class TeacherBase(BaseModel):
    teacher_id: str = Field(..., description="工号")
    name: str = Field(..., description="姓名")
    title: Optional[str] = Field(None, description="职称")
    
class TeacherCreate(TeacherBase):
    password: str = Field(..., description="密码")
    role_id: int = Field(2, description="角色ID, 默认为教师(2)")

class Teacher(TeacherBase):
    role_id: int = Field(..., description="角色ID")
    
    class Config:
        from_attributes = True

# 课程相关模型
class CourseBase(BaseModel):
    course_id: str = Field(..., description="课程号")
    name: str = Field(..., description="课程名称")
    credit: float = Field(..., description="学分")

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    class Config:
        from_attributes = True

# 教学班相关模型
class ClassBase(BaseModel):
    course_id: str = Field(..., description="课程号")
    teacher_id: str = Field(..., description="教师工号")
    semester: str = Field(..., description="学期")
    time_location: Optional[str] = Field(None, description="上课时间地点")

class ClassCreate(ClassBase):
    pass

class Class(ClassBase):
    class_id: int = Field(..., description="教学班ID")
    
    class Config:
        from_attributes = True

class ClassDetail(Class):
    course_name: str = Field(..., description="课程名称")
    teacher_name: str = Field(..., description="教师姓名")
    evaluation_count: Optional[int] = Field(0, description="评价数量")
    average_score: Optional[float] = Field(0.0, description="平均评分")

# 评价相关模型
class EvaluationBase(BaseModel):
    student_id: str = Field(..., description="学生学号")
    class_id: int = Field(..., description="教学班ID")
    score: int = Field(..., ge=1, le=5, description="评分(1-5)")
    comment: Optional[str] = Field(None, description="评语")

class EvaluationCreate(EvaluationBase):
    pass

class Evaluation(EvaluationBase):
    evaluation_id: int = Field(..., description="评价ID")
    evaluation_time: datetime = Field(..., description="评价时间")
    
    class Config:
        from_attributes = True

class EvaluationDetail(Evaluation):
    student_name: str = Field(..., description="学生姓名")
    course_name: str = Field(..., description="课程名称")
    
    class Config:
        from_attributes = True

# 学生选课相关模型
class StudentClassBase(BaseModel):
    student_id: str = Field(..., description="学生学号")
    class_id: int = Field(..., description="教学班ID")

class StudentClassCreate(StudentClassBase):
    pass

class StudentClass(StudentClassBase):
    select_time: datetime = Field(..., description="选课时间")
    
    class Config:
        from_attributes = True 