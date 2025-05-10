import pytest
import requests
import time
from typing import Generator
import os

# 从环境变量获取基础URL，如果没有则使用默认值
BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api")

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

def wait_for_server(base_url: str, max_retries: int = 30, delay: int = 2) -> None:
    """等待服务器启动"""
    for i in range(max_retries):
        try:
            # 尝试访问任何API端点，不一定是health
            response = requests.get(f"{base_url}/auth/token")
            if response.status_code in [200, 401]:  # 401也是正常的，表示需要认证
                print(f"Server is up! (Attempt {i+1})")
                return
        except requests.exceptions.ConnectionError:
            if i < max_retries - 1:
                print(f"Attempt {i+1}: Server not ready yet...")
                time.sleep(delay)
            continue
    raise Exception("Server did not start in time")
@pytest.fixture(scope="session", autouse=True)
def setup_test_environment(base_url: str):
    """设置测试环境"""
    wait_for_server(base_url)

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