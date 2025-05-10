# 简易课程评价系统

一个基于Web的课程评价系统，用于学生对所修课程进行评价，教师查看课程评价，管理员管理系统数据。

## 项目结构

```
CoEval/
├── backend/                # 后端目录
│   ├── app/                # FastAPI应用
│   │   ├── main.py         # 入口文件
│   │   ├── routers/        # 路由模块
│   │   ├── models/         # 数据模型
│   │   └── utils/          # 工具函数
│   ├── requirements.txt    # 依赖包
│   └── run.py              # 启动脚本
├── frontend/               # 前端目录  
│   ├── index.html          # 主页
│   ├── css/                # 样式文件
│   ├── js/                 # JavaScript文件
│   └── pages/              # 页面文件
└── database/               # 数据库脚本
    ├── init.sql            # 数据库初始化脚本
    ├── procedures.sql      # 存储过程
    ├── triggers.sql        # 触发器
    ├── views.sql           # 视图
    ├── init_manual.py      # 本地数据库初始化脚本
```

## 技术架构

- **前端**：HTML, CSS, JavaScript, jQuery, Bootstrap
- **后端**：Python, FastAPI
- **数据库**：MySQL

## 安装与使用

### 1. 数据库准备

#### 方式一:使用Python脚本初始化

本项目提供了Python脚本，可自动创建和初始化数据库：

- 本地开发环境：

```bash
cd database
# 确保脚本有执行权限
python init_manual.py
```


#### 方式二：手动执行SQL脚本

如果您偏好手动方式，可以按以下顺序执行SQL脚本：

```bash
mysql -u root -p < database/init.sql
mysql -u root -p course_evaluation_system < database/procedures.sql
mysql -u root -p course_evaluation_system < database/triggers.sql
mysql -u root -p course_evaluation_system < database/views.sql
```

### 2. 后端设置

1. 安装Python 3.8+
2. 安装依赖包：

```bash
cd backend
pip install -r requirements.txt
```

3. 修改数据库连接配置（如需要）：
   - 编辑 `backend/app/utils/db.py` 中的 `DB_CONFIG` 变量，确保与您的数据库配置一致

4. 启动后端服务：

```bash
cd backend
python run.py
```

### 3. 前端使用

1. 启动前端（可以使用任意Web服务器托管前端文件）
   - 可以使用Python自带的HTTP服务器：

```bash
cd frontend
python -m http.server 8080
```

2. 在浏览器中访问: `http://localhost:8080`



## 用户角色和功能

### 学生 (Student)
- 账号格式: S001, S002, ...
- 默认密码: 123456
- 功能:
  - 查看所修课程
  - 提交课程评价（1-5分评分和文字评语）
  - 查看已提交的评价

### 教师 (Teacher)
- 账号格式: T001, T002, ...
- 默认密码: 123456
- 功能:
  - 查看所授课程及评价统计
  - 查看课程的详细评价内容
  - 查看评价统计数据

### 管理员 (Admin)
- 账号: A001
- 密码: admin123
- 功能:
  - 学生管理（添加、编辑、删除）
  - 教师管理（添加、编辑、删除）
  - 课程管理（添加、编辑）
  - 教学班管理（添加、为教学班添加学生）
  - 查看系统统计数据

## 数据库特性展示

系统展示了几种数据库高级特性的应用：

1. **存储过程**：
   - 计算课程平均评分
   - 获取学生未评价课程列表
   - 查询教师所授课程及评价
   - 添加课程评价

2. **触发器**：
   - 验证评价唯一性
   - 评价验证（学生必须选了该课程，评分范围1-5）
   - 自动设置评价时间

3. **视图**：
   - 课程评价统计视图
   - 学生选课与评价视图
   - 教师课程评价详情视图

## 开发者

本项目为数据库课程设计作业，展示了关系型数据库的设计和应用，以及前后端分离架构的Web应用开发。 