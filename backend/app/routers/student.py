from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any, Optional
from ..models.models import EvaluationCreate, ClassDetail, Evaluation
from ..utils.auth import get_current_user
from ..utils.db import call_procedure, execute_update

router = APIRouter(
    prefix="/student",
    tags=["student"],
    responses={401: {"description": "Unauthorized"}},
)

@router.get("/classes", response_model=List[Dict[str, Any]])
async def get_student_classes(user: Dict[str, Any] = Depends(get_current_user)):
    """获取学生选课列表"""
    # 检查是否为学生
    if user["role"] != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="仅学生可访问"
        )
    
    # 调用存储过程获取未评价课程
    unevaluated_classes, _ = call_procedure("GetStudentUnevaluatedClasses", (user["id"],))
    
    # 调用存储过程获取已评价课程
    evaluated_classes, _ = call_procedure("GetStudentEvaluatedClasses", (user["id"],))
    
    # 合并结果并添加评价状态
    all_classes = []
    
    for cls in unevaluated_classes:
        cls["evaluated"] = False
        all_classes.append(cls)
    
    for cls in evaluated_classes:
        cls["evaluated"] = True
        all_classes.append(cls)
    
    return all_classes

@router.post("/evaluate", response_model=Dict[str, Any])
async def evaluate_class(
    evaluation: EvaluationCreate,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """学生评价课程"""
    # 检查是否为学生
    if user["role"] != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="仅学生可访问"
        )
    
    # 检查是否是当前用户的评价
    if evaluation.student_id != user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只能评价自己选的课程"
        )
    
    # 调用存储过程添加评价
    # success_param = None
    # results, output_params = call_procedure(
    #     "AddEvaluation", 
    #     (evaluation.student_id, evaluation.class_id, evaluation.score, evaluation.comment, success_param)
    # )
    
    # 简化处理，直接尝试插入评价
    insert_query = """
    INSERT INTO Evaluation (StudentID, ClassID, Score, Comment, EvaluationTime)
    VALUES (%s, %s, %s, %s, NOW())
    """
    try:
        affected_rows = execute_update(
            insert_query, 
            (evaluation.student_id, evaluation.class_id, evaluation.score, evaluation.comment)
        )
        
        if affected_rows:
            return {"success": True, "message": "评价提交成功"}
        else:
            return {"success": False, "message": "评价提交失败，可能已经评价过或未选该课程"}
    except Exception as e:
        return {"success": False, "message": f"评价提交失败: {str(e)}"}

@router.get("/evaluations", response_model=List[Dict[str, Any]])
async def get_student_evaluations(user: Dict[str, Any] = Depends(get_current_user)):
    """获取学生已提交的评价列表"""
    # 检查是否为学生
    if user["role"] != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="仅学生可访问"
        )
    
    # 调用存储过程获取已评价课程
    evaluated_classes, _ = call_procedure("GetStudentEvaluatedClasses", (user["id"],))
    
    return evaluated_classes 