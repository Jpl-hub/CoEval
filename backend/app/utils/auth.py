from typing import Optional, Dict, Any
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .db import execute_query

# JWT相关配置
SECRET_KEY = "71d4e0c3f47e4d22a9ccb51d42bb9549"  # 生产环境中应从安全位置获取
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120  # 2小时过期

# OAuth2密码流Bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def authenticate_user(user_id: str, password: str, role: int) -> Optional[Dict[str, Any]]:
    """验证用户"""
    user = None
    
    if role == 1:  # 学生
        query = "SELECT * FROM Student WHERE StudentID = %s"
        users = execute_query(query, (user_id,))
        if users and users[0]["Password"] == password:
            user = {
                "id": users[0]["StudentID"],
                "name": users[0]["Name"],
                "role": users[0]["RoleID"],
                "major": users[0]["Major"]
            }
    elif role == 2:  # 教师
        query = "SELECT * FROM Teacher WHERE TeacherID = %s AND RoleID = 2"
        users = execute_query(query, (user_id,))
        if users and users[0]["Password"] == password:
            user = {
                "id": users[0]["TeacherID"],
                "name": users[0]["Name"],
                "role": users[0]["RoleID"],
                "title": users[0]["Title"]
            }
    elif role == 3:  # 管理员
        query = "SELECT * FROM Teacher WHERE TeacherID = %s AND RoleID = 3"
        users = execute_query(query, (user_id,))
        if users and users[0]["Password"] == password:
            user = {
                "id": users[0]["TeacherID"],
                "name": users[0]["Name"],
                "role": users[0]["RoleID"]
            }
    
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """创建JWT访问令牌"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    """获取当前用户（从令牌）"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        user_data = {
            "id": user_id,
            "name": payload.get("name"),
            "role": payload.get("role")
        }
        # 根据角色添加特定字段
        if payload.get("role") == 1:  # 学生
            user_data["major"] = payload.get("major", "")
        elif payload.get("role") == 2:  # 教师
            user_data["title"] = payload.get("title", "")
        
        return user_data
    except JWTError:
        raise credentials_exception 