import pytest
from requests import Response

def test_login_student(test_client, base_url):
    """测试学生登录"""
    response = test_client.post(
        f"{base_url}/auth/token",
        json={"user_id": "S001", "password": "123456", "role": 1}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"

def test_login_teacher(test_client, base_url):
    """测试教师登录"""
    response = test_client.post(
        f"{base_url}/auth/token",
        json={"user_id": "T001", "password": "123456", "role": 2}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"

def test_login_admin(test_client, base_url):
    """测试管理员登录"""
    response = test_client.post(
        f"{base_url}/auth/token",
        json={"user_id": "A001", "password": "admin123", "role": 3}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(test_client, base_url):
    """测试无效登录"""
    response = test_client.post(
        f"{base_url}/auth/token",
        json={"user_id": "invalid", "password": "invalid", "role": 1}
    )
    assert response.status_code == 401

def test_get_current_user_student(test_client, base_url, student_token):
    """测试获取当前学生用户信息"""
    response = test_client.get(
        f"{base_url}/auth/me",
        headers={"Authorization": f"Bearer {student_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "张三"
    assert data["role"] == 1

def test_get_current_user_teacher(test_client, base_url, teacher_token):
    """测试获取当前教师用户信息"""
    response = test_client.get(
        f"{base_url}/auth/me",
        headers={"Authorization": f"Bearer {teacher_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "刘教授"
    assert data["role"] == 2

def test_get_current_user_admin(test_client, base_url, admin_token):
    """测试获取当前管理员用户信息"""
    response = test_client.get(
        f"{base_url}/auth/me",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "管理员"
    assert data["role"] == 3

def test_get_current_user_invalid_token(test_client, base_url):
    """测试无效token"""
    response = test_client.get(
        f"{base_url}/auth/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401 