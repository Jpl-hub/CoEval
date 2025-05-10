# 课程评价系统 API 测试

使用 pytest 框架进行后端 API 测试。

## 测试环境准备

1. 安装测试依赖：
```bash
pip install -r requirements.txt
```

2. 确保后端服务已启动并运行在 `http://localhost:8000`

## 运行测试

运行所有测试：
```bash
pytest
```

运行特定测试文件：
```bash
pytest test_auth.py
pytest test_student.py
pytest test_teacher.py
pytest test_admin.py
```

运行特定测试用例：
```bash
pytest test_auth.py::test_login_student
```

## 测试文件说明

- `conftest.py`: 测试配置和通用 fixtures
- `test_auth.py`: 认证相关测试
- `test_student.py`: 学生功能测试
- `test_teacher.py`: 教师功能测试
- `test_admin.py`: 管理员功能测试

## 测试覆盖范围

1. 认证功能
   - 登录验证
   - Token 验证
   - 用户信息获取

2. 学生功能
   - 获取可评价课程
   - 提交课程评价
   - 查看个人评价

3. 教师功能
   - 获取教授课程
   - 查看课程评价
   - 查看课程统计

4. 管理员功能
   - 用户管理
   - 课程管理
   - 评价管理 