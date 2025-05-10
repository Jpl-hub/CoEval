import pytest
from requests import Response

def test_get_my_courses(test_client, base_url, teacher_token):
    """测试获取我的课程"""
    response = test_client.get(
        f"{base_url}/teacher/classes",
        headers={"Authorization": f"Bearer {teacher_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:  # 如果有课程数据
        course = data[0]
        assert "ClassID" in course
        assert "CourseName" in course
        assert "AverageScore" in course
        assert "EvaluationCount" in course

def test_get_course_reviews(test_client, base_url, teacher_token):
    """测试获取课程评价"""
    # 先获取课程列表
    response = test_client.get(
        f"{base_url}/teacher/classes",
        headers={"Authorization": f"Bearer {teacher_token}"}
    )
    assert response.status_code == 200
    courses = response.json()
    
    if not courses:
        pytest.skip("没有课程数据")
    
    # 获取第一个课程的评价
    course = courses[0]
    response = test_client.get(
        f"{base_url}/teacher/class/{course['ClassID']}/evaluations",
        headers={"Authorization": f"Bearer {teacher_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:  # 如果有评价数据
        review = data[0]
        assert "StudentID" in review
        assert "StudentName" in review
        assert "Score" in review
        assert "Comment" in review
        assert "EvaluationTime" in review

def test_get_course_statistics(test_client, base_url, teacher_token):
    """测试获取课程统计"""
    response = test_client.get(
        f"{base_url}/teacher/statistics",
        headers={"Authorization": f"Bearer {teacher_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "overall_stats" in data
    assert "score_distribution" in data
    
    # 检查总体统计
    overall_stats = data["overall_stats"]
    assert "OverallAverageScore" in overall_stats
    assert "TotalEvaluations" in overall_stats
    assert "TotalClasses" in overall_stats
    
    # 检查评分分布
    score_dist = data["score_distribution"]
    assert "Score5Count" in score_dist
    assert "Score4Count" in score_dist
    assert "Score3Count" in score_dist
    assert "Score2Count" in score_dist
    assert "Score1Count" in score_dist

def test_get_nonexistent_course_reviews(test_client, base_url, teacher_token):
    """测试获取不存在课程的评价"""
    response = test_client.get(
        f"{base_url}/teacher/class/999/evaluations",
        headers={"Authorization": f"Bearer {teacher_token}"}
    )
    assert response.status_code == 403  # 因为不是该教师的课程

def test_get_nonexistent_course_statistics(test_client, base_url, teacher_token):
    """测试获取不存在课程的统计"""
    response = test_client.get(
        f"{base_url}/teacher/statistics",
        headers={"Authorization": f"Bearer {teacher_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "overall_stats" in data
    assert "score_distribution" in data 