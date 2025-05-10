from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any
from ..models.models import ClassDetail, Evaluation
from ..utils.auth import get_current_user
from ..utils.db import call_procedure, execute_query

router = APIRouter(
    prefix="/teacher",
    tags=["teacher"],
    responses={401: {"description": "Unauthorized"}},
)

@router.get("/classes", response_model=List[Dict[str, Any]])
async def get_teacher_classes(user: Dict[str, Any] = Depends(get_current_user)):
    """获取教师所授课程及评价统计"""
    # 检查是否为教师
    if user["role"] != 2:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="仅教师可访问"
        )
    
    # 调用存储过程获取教师所授课程及评价统计
    classes, _ = call_procedure("GetTeacherClassesWithEvaluation", (user["id"],))
    
    return classes

@router.get("/class/{class_id}/evaluations", response_model=List[Dict[str, Any]])
async def get_class_evaluations(
    class_id: int,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """获取特定教学班的评价详情"""
    # 检查是否为教师
    if user["role"] != 2:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="仅教师可访问"
        )
    
    # 检查是否是该教师的课程
    verify_query = """
    SELECT COUNT(*) as count FROM Class 
    WHERE ClassID = %s AND TeacherID = %s
    """
    results = execute_query(verify_query, (class_id, user["id"]))
    
    if not results or results[0]["count"] == 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只能查看自己所授课程的评价"
        )
    
    # 调用存储过程获取课程评价详情
    evaluations, _ = call_procedure("GetClassEvaluationDetails", (class_id,))
    
    return evaluations

@router.get("/statistics", response_model=Dict[str, Any])
async def get_teacher_statistics(user: Dict[str, Any] = Depends(get_current_user)):
    """获取教师所有课程的评价统计"""
    # 检查是否为教师
    if user["role"] != 2:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="仅教师可访问"
        )
    
    # 查询教师评价统计
    stats_query = """
    SELECT 
        AVG(stats.AverageScore) AS OverallAverageScore,
        SUM(stats.EvaluationCount) AS TotalEvaluations,
        COUNT(DISTINCT stats.ClassID) AS TotalClasses
    FROM TeacherClassEvaluationDetails stats
    WHERE stats.TeacherID = %s
    """
    
    overall_stats = execute_query(stats_query, (user["id"],))
    
    # 查询评分分布
    distribution_query = """
    SELECT 
        SUM(Score5Count) AS Score5Count,
        SUM(Score4Count) AS Score4Count,
        SUM(Score3Count) AS Score3Count,
        SUM(Score2Count) AS Score2Count,
        SUM(Score1Count) AS Score1Count
    FROM TeacherClassEvaluationDetails
    WHERE TeacherID = %s
    """
    
    score_distribution = execute_query(distribution_query, (user["id"],))
    
    # 组合结果
    result = {
        "overall_stats": overall_stats[0] if overall_stats else {},
        "score_distribution": score_distribution[0] if score_distribution else {}
    }
    
    return result 