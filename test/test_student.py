import pytest
from requests import Response

def test_get_available_courses(test_client, base_url, student_token):
    """测试获取可评价课程"""
    response = test_client.get(
        f"{base_url}/student/classes",
        headers={"Authorization": f"Bearer {student_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:  # 如果有课程数据
        course = data[0]
        assert "ClassID" in course
        assert "CourseName" in course
        assert "TeacherName" in course
        assert "evaluated" in course

def test_submit_review(test_client, base_url, student_token):
    """测试提交课程评价"""
    # 先获取可评价课程
    response = test_client.get(
        f"{base_url}/student/classes",
        headers={"Authorization": f"Bearer {student_token}"}
    )
    assert response.status_code == 200
    courses = response.json()
    
    if not courses:
        pytest.skip("没有可评价的课程")
    
    # 找到未评价的课程
    unevaluated_course = next((c for c in courses if not c["evaluated"]), None)
    if not unevaluated_course:
        pytest.skip("没有未评价的课程")
    
    # 提交评价
    review = {
        "student_id": "S001",  # 使用测试学生的ID
        "class_id": unevaluated_course["ClassID"],
        "score": 4,  # 改为整数
        "comment": "这是一条测试评价"
    }
    
    response = test_client.post(
        f"{base_url}/student/evaluate",
        headers={"Authorization": f"Bearer {student_token}"},
        json=review
    )
    assert response.status_code == 200
    data = response.json()
    # 检查返回的消息
    assert "message" in data
    if "success" in data:
        assert data["success"] is True

def test_get_my_reviews(test_client, base_url, student_token):
    """测试获取我的评价"""
    response = test_client.get(
        f"{base_url}/student/evaluations",
        headers={"Authorization": f"Bearer {student_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:  # 如果有评价数据
        review = data[0]
        assert "ClassID" in review
        assert "CourseName" in review
        assert "TeacherName" in review
        assert "Score" in review
        assert "Comment" in review

def test_submit_invalid_review(test_client, base_url, student_token):
    """测试提交无效评价"""
    invalid_review = {
        "student_id": "S001",
        "class_id": 999,  # 不存在的课程ID
        "score": 6,  # 超出范围的分数
        "comment": ""  # 空内容
    }

    response = test_client.post(
        f"{base_url}/student/evaluate",
        headers={"Authorization": f"Bearer {student_token}"},
        json=invalid_review
    )
    assert response.status_code == 422  # FastAPI 验证错误返回 422 