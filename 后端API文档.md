
# 课程评价系统 API 文档

## 基础信息

- **基础URL**: `http://localhost:8000/api`
- **认证方式**: Bearer Token (JWT)
- **内容类型**: application/json

## 认证相关API

### 登录

- **URL**: `/auth/login`
- **方法**: POST
- **描述**: 用户登录获取访问令牌
- **请求体**:
  ```json
  {
    "user_id": "用户ID",
    "password": "密码",
    "role": 角色ID (1=学生, 2=教师, 3=管理员)
  }
  ```
- **成功响应** (200 OK):
  ```json
  {
    "access_token": "JWT令牌字符串",
    "token_type": "bearer",
    "user_info": {
      "id": "用户ID",
      "name": "用户姓名",
      "role": 角色ID
    }
  }
  ```
- **错误响应** (401 Unauthorized):
  ```json
  {
    "detail": "用户名或密码错误"
  }
  ```

## 学生相关API

### 获取学生课程列表

- **URL**: `/student/classes`
- **方法**: GET
- **描述**: 获取学生已选课程列表，包括已评价和未评价的课程
- **请求头**: Authorization: Bearer {access_token}
- **成功响应** (200 OK):
  ```json
  [
    {
      "ClassID": 1,
      "ClassName": "数据库原理",
      "TeacherName": "刘教授",
      "evaluated": true,
      "Semester": "2023-春季",
      "TimeLocation": "周二3-4节 教学楼B201"
    },
    {
      "ClassID": 2,
      "ClassName": "操作系统",
      "TeacherName": "杨讲师", 
      "evaluated": false,
      "Semester": "2023-春季",
      "TimeLocation": "周四1-2节 教学楼A302"
    }
  ]
  ```
- **错误响应** (403 Forbidden):
  ```json
  {
    "detail": "仅学生可访问"
  }
  ```

### 提交课程评价

- **URL**: `/student/evaluate`
- **方法**: POST
- **描述**: 学生对课程进行评价
- **请求头**: Authorization: Bearer {access_token}
- **请求体**:
  ```json
  {
    "student_id": "学生ID",
    "class_id": 课程ID,
    "score": 评分(1-5),
    "comment": "评价内容"
  }
  ```
- **成功响应** (200 OK):
  ```json
  {
    "success": true,
    "message": "评价提交成功"
  }
  ```
- **错误响应** (400 Bad Request):
  ```json
  {
    "success": false,
    "message": "评价提交失败：可能已经评价过或未选该课程"
  }
  ```

### 获取已提交的评价

- **URL**: `/student/evaluations`
- **方法**: GET
- **描述**: 获取学生已提交的评价列表
- **请求头**: Authorization: Bearer {access_token}
- **成功响应** (200 OK):
  ```json
  [
    {
      "ClassID": 1,
      "ClassName": "数据库原理",
      "TeacherName": "刘教授",
      "Score": 5,
      "Comment": "老师讲解清晰，课程内容实用",
      "EvaluationTime": "2023-06-10T14:30:00"
    }
  ]
  ```

## 教师相关API

### 获取教师课程列表

- **URL**: `/teacher/classes`
- **方法**: GET
- **描述**: 获取教师所授课程及评价统计
- **请求头**: Authorization: Bearer {access_token}
- **成功响应** (200 OK):
  ```json
  [
    {
      "ClassID": 1,
      "ClassName": "数据库原理",
      "EvaluationCount": 25,
      "AverageScore": 4.7,
      "CourseID": "C001",
      "Semester": "2023-春季"
    },
    {
      "ClassID": 3,
      "ClassName": "计算机网络",
      "EvaluationCount": 18,
      "AverageScore": 4.2,
      "CourseID": "C003",
      "Semester": "2023-春季"
    }
  ]
  ```
- **错误响应** (403 Forbidden):
  ```json
  {
    "detail": "仅教师可访问"
  }
  ```

### 获取教师统计数据

- **URL**: `/teacher/statistics`
- **方法**: GET
- **描述**: 获取教师所有课程的评价统计信息
- **请求头**: Authorization: Bearer {access_token}
- **成功响应** (200 OK):
  ```json
  {
    "overall_stats": {
      "OverallAverageScore": 4.5,
      "TotalEvaluations": 43,
      "TotalClasses": 2
    },
    "score_distribution": {
      "Score5Count": 25,
      "Score4Count": 10,
      "Score3Count": 5,
      "Score2Count": 2,
      "Score1Count": 1
    }
  }
  ```

### 获取课程评价详情

- **URL**: `/teacher/class/{class_id}/evaluations`
- **方法**: GET
- **描述**: 获取特定课程的学生评价详情
- **请求头**: Authorization: Bearer {access_token}
- **路径参数**: class_id - 课程ID
- **成功响应** (200 OK):
  ```json
  [
    {
      "StudentName": "张三",
      "Score": 5,
      "Comment": "非常好的课程",
      "EvaluationTime": "2023-06-08T10:30:00"
    },
    {
      "StudentName": "李四",
      "Score": 4,
      "Comment": "内容丰富，讲解清晰",
      "EvaluationTime": "2023-06-09T14:20:00"
    }
  ]
  ```
- **错误响应** (403 Forbidden):
  ```json
  {
    "detail": "只能查看自己所授课程的评价"
  }
  ```

## 管理员相关API

### 获取统计数据

- **URL**: `/admin/statistics`
- **方法**: GET
- **描述**: 获取系统整体统计信息
- **请求头**: Authorization: Bearer {access_token}
- **成功响应** (200 OK):
  ```json
  {
    "student_count": 5,
    "teacher_count": 3,
    "course_count": 4,
    "class_count": 6,
    "evaluation_count": 12,
    "average_score": 4.3
  }
  ```

### 获取学生列表

- **URL**: `/admin/students`
- **方法**: GET
- **描述**: 获取所有学生信息
- **请求头**: Authorization: Bearer {access_token}
- **成功响应** (200 OK):
  ```json
  [
    {
      "StudentID": "S001",
      "Name": "张三",
      "Major": "计算机科学",
      "RoleID": 1
    },
    {
      "StudentID": "S002",
      "Name": "李四",
      "Major": "软件工程",
      "RoleID": 1
    }
  ]
  ```

### 添加新学生

- **URL**: `/admin/students`
- **方法**: POST
- **描述**: 添加新学生
- **请求头**: Authorization: Bearer {access_token}
- **请求体**:
  ```json
  {
    "student_id": "S006",
    "name": "钱七",
    "major": "人工智能",
    "password": "password123"
  }
  ```
- **成功响应** (200 OK):
  ```json
  {
    "success": true,
    "message": "学生添加成功"
  }
  ```

### 获取课程列表

- **URL**: `/admin/courses`
- **方法**: GET
- **描述**: 获取所有课程信息
- **请求头**: Authorization: Bearer {access_token}
- **成功响应** (200 OK):
  ```json
  [
    {
      "CourseID": "C001",
      "Name": "数据库原理",
      "Credit": 3
    },
    {
      "CourseID": "C002",
      "Name": "操作系统",
      "Credit": 4
    },
    {
      "CourseID": "C003",
      "Name": "计算机网络",
      "Credit": 3
    }
  ]
  ```

### 添加新课程

- **URL**: `/admin/courses`
- **方法**: POST
- **描述**: 添加新课程
- **请求头**: Authorization: Bearer {access_token}
- **请求体**:
  ```json
  {
    "course_id": "C005",
    "name": "人工智能导论",
    "credit": 3
  }
  ```
- **成功响应** (200 OK):
  ```json
  {
    "success": true,
    "message": "课程添加成功"
  }
  ```

### 获取教学班列表

- **URL**: `/admin/classes`
- **方法**: GET
- **描述**: 获取所有教学班信息
- **请求头**: Authorization: Bearer {access_token}
- **成功响应** (200 OK):
  ```json
  [
    {
      "ClassID": 1,
      "CourseID": "C001",
      "CourseName": "数据库原理",
      "TeacherID": "T001",
      "TeacherName": "刘教授",
      "Semester": "2023-春季",
      "TimeLocation": "周二3-4节 教学楼B201"
    }
  ]
  ```

### 学生选课记录添加

- **URL**: `/admin/student-class`
- **方法**: POST
- **描述**: 为学生添加选课记录
- **请求头**: Authorization: Bearer {access_token}
- **请求体**:
  ```json
  {
    "student_id": "S001",
    "class_id": 1
  }
  ```
- **成功响应** (200 OK):
  ```json
  {
    "success": true,
    "message": "选课记录添加成功"
  }
  ```

## 数据模型

### 学生 (Student)
- StudentID: 学生ID (字符串)
- Name: 姓名
- Major: 专业
- Password: 密码
- RoleID: 角色ID (固定为1)

### 教师 (Teacher)
- TeacherID: 教师ID (字符串)
- Name: 姓名
- Title: 职称
- Password: 密码
- RoleID: 角色ID (2=普通教师, 3=管理员)

### 课程 (Course)
- CourseID: 课程ID (字符串)
- Name: 课程名称
- Credit: 学分

### 教学班 (Class)
- ClassID: 教学班ID (整数)
- CourseID: 课程ID (外键)
- TeacherID: 教师ID (外键)
- Semester: 学期
- TimeLocation: 上课时间和地点

### 评价 (Evaluation)
- EvaluationID: 评价ID (整数)
- StudentID: 学生ID (外键)
- ClassID: 教学班ID (外键)
- Score: 评分 (1-5)
- Comment: 评价内容
- EvaluationTime: 评价时间

## 错误码说明

- 200 OK: 请求成功
- 400 Bad Request: 请求参数错误
- 401 Unauthorized: 未认证或认证失败
- 403 Forbidden: 权限不足
- 404 Not Found: 资源不存在
- 500 Internal Server Error: 服务器内部错误

## 认证说明

所有API（除登录接口外）都需要在请求头中携带JWT令牌进行认证：
```
Authorization: Bearer {access_token}
```

令牌有效期为120分钟，过期后需要重新登录获取新令牌。
