import pytest
from requests import Response

def test_get_all_users(test_client, base_url, admin_token):
    """测试获取所有用户列表"""
    response = test_client.get(
        f"{base_url}/admin/students",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:  # 如果有用户数据
        user = data[0]
        assert "StudentID" in user
        assert "Name" in user
        assert "Major" in user

def test_get_all_courses(test_client, base_url, admin_token):
    """测试获取所有课程列表"""
    response = test_client.get(
        f"{base_url}/admin/courses",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:  # 如果有课程数据
        course = data[0]
        assert "CourseID" in course
        assert "Name" in course
        assert "Credit" in course

def test_get_all_reviews(test_client, base_url, admin_token):
    """测试获取所有评价列表"""
    response = test_client.get(
        f"{base_url}/admin/statistics",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "evaluation_count" in data
    assert "average_score" in data

def test_delete_review(test_client, base_url, admin_token):
    """测试删除评价"""
    # 先获取评价列表
    response = test_client.get(
        f"{base_url}/admin/statistics",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "evaluation_count" in data

def test_delete_nonexistent_review(test_client, base_url, admin_token):
    """测试删除不存在的评价"""
    response = test_client.delete(
        f"{base_url}/admin/reviews/999",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 404

def test_unauthorized_access(test_client, base_url, student_token):
    """测试未授权访问管理员接口"""
    response = test_client.get(
        f"{base_url}/admin/students",
        headers={"Authorization": f"Bearer {student_token}"}
    )
    assert response.status_code == 403 