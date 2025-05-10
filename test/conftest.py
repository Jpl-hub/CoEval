import pytest
import requests
from typing import Generator

# 修改为实际的后端服务地址
BASE_URL = "http://localhost:8000/api"  # 添加/api前缀

@pytest.fixture(scope="session")
def base_url() -> str:
    """返回API基础URL"""
    return BASE_URL

@pytest.fixture(scope="session")
def test_client() -> Generator:
    """创建测试客户端"""
    session = requests.Session()
    yield session
    session.close()

@pytest.fixture
def student_token(test_client, base_url) -> str:
    """获取学生token"""
    response = test_client.post(
        f"{base_url}/auth/token",
        json={"user_id": "S001", "password": "123456", "role": 1}
    )
    assert response.status_code == 200
    return response.json()["access_token"]

@pytest.fixture
def teacher_token(test_client, base_url) -> str:
    """获取教师token"""
    response = test_client.post(
        f"{base_url}/auth/token",
        json={"user_id": "T001", "password": "123456", "role": 2}
    )
    assert response.status_code == 200
    return response.json()["access_token"]

@pytest.fixture
def admin_token(test_client, base_url) -> str:
    """获取管理员token"""
    response = test_client.post(
        f"{base_url}/auth/token",
        json={"user_id": "A001", "password": "admin123", "role": 3}
    )
    assert response.status_code == 200
    return response.json()["access_token"]