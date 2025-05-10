$(document).ready(function() {
    // 检查认证状态
    if (!utils.checkAuth()) return;
    
    // 显示用户信息
    const userInfo = JSON.parse(localStorage.getItem(STORAGE_KEYS.USER_INFO));
    $('#userName').text(`${userInfo.name}（教师）`);
    
    // 加载统计数据
    loadStatistics();
    
    // 加载课程列表
    loadCourses();
});

// 获取课程名称（兼容不同的字段名）
function getCourseName(course) {
    // 尝试各种可能的字段名
    return course.ClassName || course.CourseName || course.courseName || course.Name || course.name || '未知课程';
}

// 加载统计数据
function loadStatistics() {
    // API文档: GET /teacher/statistics 获取教师统计数据
    const teacherApiPath = ROLE_API_PATHS[2];
    
    $.ajax({
        url: getFullApiPath(teacherApiPath, '/statistics'),
        type: 'GET',
        headers: utils.getAuthHeader(),
        success: function(stats) {
            if (!stats) {
                utils.showMessage($('#courseMessage'), '获取到的统计数据为空', 'warning');
                return;
            }
            
            console.log('教师统计数据:', stats);
            
            // 根据API文档中的字段获取数据
            const overallStats = stats.overall_stats || {};
            $('#totalClasses').text(overallStats.TotalClasses || 0);
            $('#totalEvaluations').text(overallStats.TotalEvaluations || 0);
            $('#averageScore').text(
                overallStats.OverallAverageScore 
                ? parseFloat(overallStats.OverallAverageScore).toFixed(1) 
                : '暂无'
            );
        },
        error: function(xhr) {
            utils.showMessage($('#courseMessage'), '加载统计数据失败', 'danger');
            console.error('加载统计数据错误:', xhr);
            // 显示更详细的错误信息
            if (xhr.responseText) {
                try {
                    const error = JSON.parse(xhr.responseText);
                    console.error('错误详情:', error);
                } catch (e) {
                    console.error('原始错误响应:', xhr.responseText);
                }
            }
        }
    });
}

// 加载课程列表
function loadCourses() {
    // API文档: GET /teacher/classes 获取教师课程列表
    const teacherApiPath = ROLE_API_PATHS[2];
    const endpoint = '/classes';
    const url = getFullApiPath(teacherApiPath, endpoint);
    
    // 如果有调试工具，记录请求
    if (window.debugTools) {
        window.debugTools.logApiRequest('GET', url);
    }
    
    $.ajax({
        url: url,
        type: 'GET',
        headers: utils.getAuthHeader(),
        success: function(courses) {
            // 如果有调试工具，分析响应
            if (window.debugTools) {
                window.debugTools.logApiResponse(url, courses);
                // 检查预期字段是否存在
                window.debugTools.analyzeApiResponse(endpoint, courses, [
                    'ClassID', 'ClassName', 'EvaluationCount', 'AverageScore', 'CourseID', 'Semester'
                ]);
            }
            
            const $courseList = $('#courseList');
            $courseList.empty();
            
            if (!Array.isArray(courses) || courses.length === 0) {
                $courseList.append('<tr><td colspan="5" class="text-center">暂无课程数据</td></tr>');
                return;
            }
            
            // 详细记录API返回的字段
            console.log('教师课程数据样例:', courses[0]);
            console.log('全部课程数据字段:', Object.keys(courses[0]));
            
            courses.forEach(function(course) {
                // 确保课程ID存在
                const classId = course.ClassID || course.classId || course.class_id || course.id || '';
                
                // 获取课程名称和评分数据
                const courseName = getCourseName(course);
                const evaluationCount = course.EvaluationCount || course.evaluationCount || course.evaluation_count || 0;
                const avgScoreValue = course.AverageScore || course.averageScore || course.average_score || null;
                const avgScore = avgScoreValue ? parseFloat(avgScoreValue).toFixed(1) : '暂无';
                
                $courseList.append(`
                    <tr>
                        <td>${utils.escapeHtml(classId)}</td>
                        <td>${utils.escapeHtml(courseName)}</td>
                        <td>${evaluationCount}</td>
                        <td>${avgScore}</td>
                        <td>
                            <button class="btn btn-sm btn-primary" onclick="showEvaluations(${classId})">
                                查看评价
                            </button>
                        </td>
                    </tr>
                `);
            });
        },
        error: function(xhr, status, error) {
            utils.showMessage($('#courseMessage'), '加载课程列表失败', 'danger');
            console.error('加载课程列表错误:', xhr);
            
            // 如果有调试工具，记录错误
            if (window.debugTools) {
                window.debugTools.logApiResponse(url, xhr.responseText, xhr.status);
            }
            
            // 显示更详细的错误信息
            if (xhr.responseText) {
                try {
                    const errorData = JSON.parse(xhr.responseText);
                    console.error('错误详情:', errorData);
                } catch (e) {
                    console.error('原始错误响应:', xhr.responseText);
                }
            }
        }
    });
}

// 显示课程评价
function showEvaluations(classId) {
    if (!classId) {
        utils.showMessage($('#evaluationMessage'), '课程ID无效', 'danger');
        return;
    }

    // 清除之前的消息
    $('#evaluationMessage').addClass('d-none');
    
    // API文档: GET /teacher/class/{class_id}/evaluations 获取课程评价详情
    const teacherApiPath = ROLE_API_PATHS[2];
    
    $.ajax({
        url: getFullApiPath(teacherApiPath, `/class/${classId}/evaluations`),
        type: 'GET',
        headers: utils.getAuthHeader(),
        success: function(evaluations) {
            const $evaluationList = $('#evaluationList');
            $evaluationList.empty();
            
            if (!Array.isArray(evaluations) || evaluations.length === 0) {
                $evaluationList.append('<tr><td colspan="4" class="text-center">暂无评价数据</td></tr>');
                return;
            }
            
            // 详细记录API返回的字段
            console.log('评价详情数据样例:', evaluations[0]);
            console.log('评价详情字段:', Object.keys(evaluations[0]));
            
            evaluations.forEach(function(evaluation) {
                // 处理学生名称字段可能的多种命名
                const studentName = evaluation.StudentName || evaluation.studentName || evaluation.Student || evaluation.student || '匿名学生';
                
                // 显示评分星级
                const score = parseInt(evaluation.Score) || 0;
                const safeScore = Math.min(Math.max(score, 0), 5);
                
                $evaluationList.append(`
                    <tr>
                        <td>${utils.escapeHtml(studentName)}</td>
                        <td>
                            <div class="rating">
                                ${'★'.repeat(safeScore)}${'☆'.repeat(5-safeScore)}
                            </div>
                        </td>
                        <td>${utils.escapeHtml(evaluation.Comment)}</td>
                        <td>${utils.formatDate(evaluation.EvaluationTime)}</td>
                    </tr>
                `);
            });
            
            // 显示模态框
            const modal = new bootstrap.Modal(document.getElementById('evaluationModal'));
            modal.show();
        },
        error: function(xhr) {
            utils.showMessage($('#evaluationMessage'), '加载评价数据失败', 'danger');
            console.error('加载评价数据错误:', xhr);
            // 显示更详细的错误信息
            if (xhr.responseText) {
                try {
                    const error = JSON.parse(xhr.responseText);
                    console.error('错误详情:', error);
                } catch (e) {
                    console.error('原始错误响应:', xhr.responseText);
                }
            }
        }
    });
} 