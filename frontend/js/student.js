$(document).ready(function() {
    // 检查认证状态
    if (!utils.checkAuth()) return;
    
    // 显示用户信息
    const userInfo = JSON.parse(localStorage.getItem(STORAGE_KEYS.USER_INFO));
    $('#userName').text(`${userInfo.name}（学生）`);
    
    // 加载课程列表
    loadCourses();
    
    // 加载已提交的评价列表
    loadEvaluations();
    
    // 评价表单提交
    $('#evaluationForm').on('submit', function(e) {
        e.preventDefault();
        
        const classId = $('#selectedClassId').val();
        const score = $('input[name="score"]:checked').val();
        const comment = $('#comment').val();
        
        if (!classId || !score || !comment) {
            utils.showMessage($('#evaluationMessage'), '请填写完整的评价信息');
            return;
        }
        
        // 显示提交中状态
        const $submitButton = $(this).find('button[type="submit"]');
        const originalText = $submitButton.text();
        $submitButton.prop('disabled', true).text('提交中...');
        
        // API文档: POST /student/evaluate 提交课程评价
        const studentApiPath = ROLE_API_PATHS[1];
        const requestData = {
            student_id: userInfo.id,
            class_id: parseInt(classId),
            score: parseInt(score),
            comment: comment.trim()
        };
        
        // 控制台显示请求数据，便于调试
        console.log('提交评价请求:', requestData);
        
        $.ajax({
            url: getFullApiPath(studentApiPath, '/evaluate'),
            type: 'POST',
            headers: utils.getAuthHeader(),
            contentType: 'application/json',
            data: JSON.stringify(requestData),
            success: function(response) {
                // 恢复按钮状态
                $submitButton.prop('disabled', false).text(originalText);
                
                // 记录完整响应便于调试
                console.log('评价提交响应:', response);
                
                if (response.success) {
                    utils.showMessage($('#evaluationMessage'), '评价提交成功！', 'success');
                    $('#evaluationForm')[0].reset();
                    $('#selectedClassId').val('');
                    
                    // 延迟刷新数据，给后端时间处理
                    setTimeout(() => {
                        loadCourses(); // 刷新课程列表
                        loadEvaluations(); // 刷新评价列表
                    }, 500);
                    
                    // 关闭模态框
                    setTimeout(() => {
                        const modal = bootstrap.Modal.getInstance(document.getElementById('evaluationModal'));
                        modal.hide();
                    }, 1500);
                } else {
                    let errorMsg = response.message || '评价提交失败';
                    if (errorMsg.includes('已经评价过') || errorMsg.includes('未选该课程')) {
                        errorMsg = '评价失败: 您可能已经评价过此课程或未选择此课程';
                    }
                    utils.showMessage($('#evaluationMessage'), errorMsg, 'danger');
                }
            },
            error: function(xhr, status, error) {
                // 恢复按钮状态
                $submitButton.prop('disabled', false).text(originalText);
                
                let errorMessage = '评价提交失败';
                console.error('评价提交错误:', {xhr, status, error});
                
                try {
                    if (xhr.responseJSON && xhr.responseJSON.detail) {
                        errorMessage = xhr.responseJSON.detail;
                    } else if (xhr.responseText) {
                        const response = JSON.parse(xhr.responseText);
                        errorMessage = response.message || response.error || errorMessage;
                        console.error('服务器错误响应:', response);
                    }
                } catch (e) {
                    console.error('解析错误响应失败:', e);
                }
                
                utils.showMessage($('#evaluationMessage'), errorMessage, 'danger');
            }
        });
    });
});

// 获取课程名称（兼容不同的字段名）
function getCourseName(course) {
    // 尝试各种可能的字段名
    return course.ClassName || course.CourseName || course.courseName || course.Name || course.name || '未知课程';
}

// 获取教师名称（兼容不同的字段名）
function getTeacherName(course) {
    return course.TeacherName || course.teacherName || course.Teacher || course.teacher || '未知教师';
}

// 加载课程列表
function loadCourses() {
    // API文档: GET /student/classes 获取学生课程列表
    const studentApiPath = ROLE_API_PATHS[1];
    const endpoint = '/classes';
    const url = getFullApiPath(studentApiPath, endpoint);
    
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
                    'ClassID', 'ClassName', 'TeacherName', 'evaluated', 'Semester', 'TimeLocation'
                ]);
            }
            
            const $courseList = $('#courseList');
            $courseList.empty();
            
            if (!Array.isArray(courses) || courses.length === 0) {
                $courseList.append('<tr><td colspan="7" class="text-center">暂无课程数据</td></tr>');
                return;
            }
            
            // 详细记录API返回的字段
            console.log('学生课程数据样例:', courses[0]);
            console.log('全部课程数据字段:', Object.keys(courses[0]));
            
            courses.forEach(function(course) {
                // 确保课程ID存在
                const classId = course.ClassID || course.classId || course.class_id || course.id || '';
                
                // 获取课程评价状态，兼容不同命名规则
                const evaluated = course.evaluated || course.isEvaluated || course.hasEvaluated || course.has_evaluated || false;
                
                const status = evaluated ? 
                    '<span class="badge bg-success">已评价</span>' : 
                    '<span class="badge bg-warning">未评价</span>';
                
                const action = evaluated ? 
                    '<button class="btn btn-sm btn-secondary" disabled>已评价</button>' :
                    `<button class="btn btn-sm btn-primary" onclick="selectCourse(${classId})">评价</button>`;
                
                // 使用兼容函数获取课程名称和教师名称
                const courseName = getCourseName(course);
                const teacherName = getTeacherName(course);
                const semester = course.Semester || course.semester || '';
                const timeLocation = course.TimeLocation || course.timeLocation || course.time_location || '';
                
                $courseList.append(`
                    <tr>
                        <td>${utils.escapeHtml(classId)}</td>
                        <td>${utils.escapeHtml(courseName)}</td>
                        <td>${utils.escapeHtml(teacherName)}</td>
                        <td>${utils.escapeHtml(semester)}</td>
                        <td>${utils.escapeHtml(timeLocation)}</td>
                        <td>${status}</td>
                        <td>${action}</td>
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

// 加载已提交的评价列表
function loadEvaluations() {
    // API文档: GET /student/evaluations 获取学生已提交的评价列表
    const studentApiPath = ROLE_API_PATHS[1];
    
    $.ajax({
        url: getFullApiPath(studentApiPath, '/evaluations'),
        type: 'GET',
        headers: utils.getAuthHeader(),
        success: function(evaluations) {
            const $evaluationList = $('#evaluationListTable');
            $evaluationList.empty();
            
            if (!Array.isArray(evaluations) || evaluations.length === 0) {
                $evaluationList.append('<tr><td colspan="6" class="text-center">暂无评价数据</td></tr>');
                return;
            }
            
            // 详细记录API返回的字段
            if (evaluations.length > 0) {
                console.log('学生评价数据样例:', evaluations[0]);
                console.log('全部评价数据字段:', Object.keys(evaluations[0]));
            }
            
            evaluations.forEach(function(evaluation) {
                // 计算星级显示
                const score = parseInt(evaluation.Score) || 0;
                const safeScore = Math.min(Math.max(score, 0), 5);
                const stars = '★'.repeat(safeScore) + '☆'.repeat(5-safeScore);
                
                // 使用兼容函数获取课程名称和教师名称
                $evaluationList.append(`
                    <tr>
                        <td>${utils.escapeHtml(evaluation.ClassID)}</td>
                        <td>${utils.escapeHtml(getCourseName(evaluation))}</td>
                        <td>${utils.escapeHtml(getTeacherName(evaluation))}</td>
                        <td>
                            <div class="rating">
                                ${stars}
                            </div>
                        </td>
                        <td>${utils.escapeHtml(evaluation.Comment)}</td>
                        <td>${utils.formatDate(evaluation.EvaluationTime)}</td>
                    </tr>
                `);
            });
        },
        error: function(xhr) {
            utils.showMessage($('#evaluationListMessage'), '加载评价列表失败', 'danger');
            console.error('加载评价列表错误:', xhr);
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

// 选择课程进行评价
function selectCourse(classId) {
    $('#selectedClassId').val(classId);
    $('#evaluationForm')[0].reset();
    $('#evaluationMessage').addClass('d-none');
    
    // 显示模态框
    const modal = new bootstrap.Modal(document.getElementById('evaluationModal'));
    modal.show();
} 