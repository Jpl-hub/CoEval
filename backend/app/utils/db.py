import mysql.connector
from mysql.connector import Error
from typing import Dict, List, Any, Optional, Tuple
import os

# 数据库连接配置
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', 'abc123'),
    'database': os.environ.get('DB_NAME', 'course_evaluation_system')
}

def get_db_connection():
    """获取数据库连接"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"数据库连接错误: {e}")
        return None

def execute_query(query: str, params: tuple = None) -> List[Dict[str, Any]]:
    """执行SQL查询"""
    conn = get_db_connection()
    result = []
    
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params or ())
            result = cursor.fetchall()
            cursor.close()
        except Error as e:
            print(f"查询执行错误: {e}")
        finally:
            conn.close()
    
    return result

def execute_update(query: str, params: tuple = None) -> Optional[int]:
    """执行SQL更新（插入、更新、删除）"""
    conn = get_db_connection()
    affected_rows = None
    
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            conn.commit()
            affected_rows = cursor.rowcount
            cursor.close()
        except Error as e:
            conn.rollback()
            print(f"更新执行错误: {e}")
        finally:
            conn.close()
    
    return affected_rows

def call_procedure(proc_name: str, params: tuple = None) -> Tuple[List[Dict[str, Any]], List[Any]]:
    """调用存储过程"""
    conn = get_db_connection()
    results = []
    output_params = []
    
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.callproc(proc_name, params or ())
            
            # 收集结果集
            for result in cursor.stored_results():
                results = result.fetchall()
            
            # 获取输出参数（如果有）
            if params:
                # 对于存储过程中的OUT参数，需要在call之后获取
                # 这里简化处理，仅获取第一个结果集
                output_params = list(params)
            
            conn.commit()
            cursor.close()
        except Error as e:
            conn.rollback()
            print(f"存储过程调用错误: {e}")
        finally:
            conn.close()
    
    return results, output_params 