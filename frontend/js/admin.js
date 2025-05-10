$(document).ready(function() {
    // 检查认证状态
    if (!utils.checkAuth()) return;
    
    // 显示用户信息
    const userInfo = JSON.parse(localStorage.getItem(STORAGE_KEYS.USER_INFO));
    $('#userName').text(`${userInfo.name}（管理员）`);
    
    // 加载统计数据
    loadStatistics();
    
    // 加载学生列表
    loadStudents();
    
    // 加载课程列表
    loadCourses();
    
    // 加载班级列表
    loadClasses();
    
    // 加载选课记录
    loadEnrollments();
    
    // 添加学生表单提交
    $('#addStudentForm').on('submit', function(e) {
        e.preventDefault();
        
        const studentId = $('#studentId').val();
        const name = $('#studentName').val();
        const major = $('#studentMajor').val();
        const password = $('#studentPassword').val();
        
        if (!studentId || !name || !major || !password) {
            utils.showMessage($('#addStudentMessage'), '请填写完整的学生信息');
            return;
        }
        
        // API文档: POST /admin/students 添加新学生
        const adminApiPath = ROLE_API_PATHS[3];
        
        $.ajax({
            url: getFullApiPath(adminApiPath, '/students'),
            type: 'POST',
            headers: utils.getAuthHeader(),
            contentType: 'application/json',
            data: JSON.stringify({
                student_id: studentId,
                name: name,
                major: major,
                password: password
            }),
            success: function(response) {
                if (response.success) {
                    utils.showMessage($('#addStudentMessage'), '学生添加成功！', 'success');
                    $('#addStudentForm')[0].reset();
                    loadStudents(); // 刷新学生列表
                    loadStatistics(); // 刷新统计数据
                    
                    // 关闭模态框
                    setTimeout(() => {
                        const modal = bootstrap.Modal.getInstance(document.getElementById('addStudentModal'));
                        modal.hide();
                    }, 1500);
                } else {
                    utils.showMessage($('#addStudentMessage'), response.message || '学生添加失败', 'danger');
                }
            },
            error: function(xhr) {
                let errorMessage = '学生添加失败';
                try {
                    if (xhr.responseJSON && xhr.responseJSON.detail) {
                        errorMessage = xhr.responseJSON.detail;
                    } else if (xhr.responseText) {
                        const response = JSON.parse(xhr.responseText);
                        errorMessage = response.message || response.error || errorMessage;
                    }
                } catch (e) {}
                utils.showMessage($('#addStudentMessage'), errorMessage, 'danger');
            }
        });
    });
    
    // 添加课程表单提交
    $('#addCourseForm').on('submit', function(e) {
        e.preventDefault();
        
        const courseId = $('#courseId').val();
        const name = $('#courseName').val();
        const credit = $('#courseCredit').val();
        
        if (!courseId || !name || !credit) {
            utils.showMessage($('#addCourseMessage'), '请填写完整的课程信息');
            return;
        }
        
        // API文档: POST /admin/courses 添加新课程
        const adminApiPath = ROLE_API_PATHS[3];
        
        $.ajax({
            url: getFullApiPath(adminApiPath, '/courses'),
            type: 'POST',
            headers: utils.getAuthHeader(),
            contentType: 'application/json',
            data: JSON.stringify({
                course_id: courseId,
                name: name,
                credit: parseInt(credit)
            }),
            success: function(response) {
                if (response.success) {
                    utils.showMessage($('#addCourseMessage'), '课程添加成功！', 'success');
                    $('#addCourseForm')[0].reset();
                    loadCourses(); // 刷新课程列表
                    loadStatistics(); // 刷新统计数据
                    
                    // 关闭模态框
                    setTimeout(() => {
                        const modal = bootstrap.Modal.getInstance(document.getElementById('addCourseModal'));
                        modal.hide();
                    }, 1500);
                } else {
                    utils.showMessage($('#addCourseMessage'), response.message || '课程添加失败', 'danger');
                }
            },
            error: function(xhr) {
                let errorMessage = '课程添加失败';
                try {
                    if (xhr.responseJSON && xhr.responseJSON.detail) {
                        errorMessage = xhr.responseJSON.detail;
                    } else if (xhr.responseText) {
                        const response = JSON.parse(xhr.responseText);
                        errorMessage = response.message || response.error || errorMessage;
                    }
                } catch (e) {}
                utils.showMessage($('#addCourseMessage'), errorMessage, 'danger');
            }
        });
    });
    
    // 添加选课记录表单提交
    $('#addStudentClassForm').on('submit', function(e) {
        e.preventDefault();
        
        const studentId = $('#scStudentId').val();
        const classId = $('#scClassId').val();
        
        if (!studentId || !classId) {
            utils.showMessage($('#addStudentClassMessage'), '请填写完整的选课信息');
            return;
        }
        
        // API文档: POST /admin/student-class 为学生添加选课记录
        const adminApiPath = ROLE_API_PATHS[3];
        
        $.ajax({
            url: getFullApiPath(adminApiPath, '/student-class'),
            type: 'POST',
            headers: utils.getAuthHeader(),
            contentType: 'application/json',
            data: JSON.stringify({
                student_id: studentId,
                class_id: parseInt(classId)
            }),
            success: function(response) {
                if (response.success) {
                    utils.showMessage($('#addStudentClassMessage'), '选课记录添加成功！', 'success');
                    $('#addStudentClassForm')[0].reset();
                    loadClasses(); // 刷新班级列表
                    loadStatistics(); // 刷新统计数据
                    
                    // 关闭模态框
                    setTimeout(() => {
                        const modal = bootstrap.Modal.getInstance(document.getElementById('addStudentClassModal'));
                        modal.hide();
                    }, 1500);
                } else {
                    utils.showMessage($('#addStudentClassMessage'), response.message || '选课记录添加失败', 'danger');
                }
            },
            error: function(xhr) {
                let errorMessage = '选课记录添加失败';
                try {
                    if (xhr.responseJSON && xhr.responseJSON.detail) {
                        errorMessage = xhr.responseJSON.detail;
                    } else if (xhr.responseText) {
                        const response = JSON.parse(xhr.responseText);
                        errorMessage = response.message || response.error || errorMessage;
                    }
                } catch (e) {}
                utils.showMessage($('#addStudentClassMessage'), errorMessage, 'danger');
            }
        });
    });
    
    // 添加教学班表单提交
    $('#addClassForm').on('submit', function(e) {
        e.preventDefault();
        
        const courseId = $('#classCourseId').val();
        const teacherId = $('#classTeacherId').val();
        const semester = $('#classSemester').val();
        const timeLocation = $('#classTimeLocation').val();
        
        if (!courseId || !teacherId || !semester || !timeLocation) {
            utils.showMessage($('#addClassMessage'), '请填写完整的教学班信息');
            return;
        }
        
        // API: POST /admin/classes 添加新教学班
        const adminApiPath = ROLE_API_PATHS[3];
        
        $.ajax({
            url: getFullApiPath(adminApiPath, '/classes'),
            type: 'POST',
            headers: utils.getAuthHeader(),
            contentType: 'application/json',
            data: JSON.stringify({
                course_id: courseId,
                teacher_id: teacherId,
                semester: semester,
                time_location: timeLocation
            }),
            success: function(response) {
                if (response.success) {
                    utils.showMessage($('#addClassMessage'), '教学班添加成功！', 'success');
                    $('#addClassForm')[0].reset();
                    loadClasses(); // 刷新班级列表
                    loadStatistics(); // 刷新统计数据
                    
                    // 关闭模态框
                    setTimeout(() => {
                        const modal = bootstrap.Modal.getInstance(document.getElementById('addClassModal'));
                        modal.hide();
                    }, 1500);
                } else {
                    utils.showMessage($('#addClassMessage'), response.message || '教学班添加失败', 'danger');
                }
            },
            error: function(xhr) {
                let errorMessage = '教学班添加失败';
                try {
                    if (xhr.responseJSON && xhr.responseJSON.detail) {
                        errorMessage = xhr.responseJSON.detail;
                    } else if (xhr.responseText) {
                        const response = JSON.parse(xhr.responseText);
                        errorMessage = response.message || response.error || errorMessage;
                    }
                } catch (e) {}
                utils.showMessage($('#addClassMessage'), errorMessage, 'danger');
            }
        });
    });
    
    // 确认删除按钮点击事件
    $('#confirmDeleteBtn').on('click', function() {
        const deleteType = $('#deleteType').val();
        const deleteId = $('#deleteId').val();
        
        if (!deleteType || !deleteId) {
            return;
        }
        
        const adminApiPath = ROLE_API_PATHS[3];
        let apiEndpoint = '';
        let successMessage = '';
        let requestMethod = 'DELETE';
        let postData = {};
        
        switch (deleteType) {
            case 'student':
                apiEndpoint = `/students/${deleteId}`;
                successMessage = '学生删除成功';
                break;
            case 'course':
                apiEndpoint = `/courses/${deleteId}`;
                successMessage = '课程删除成功';
                break;
            case 'student-class':
                // 学生选课记录删除需要传入参数
                const [studentId, classId] = deleteId.split('-');
                apiEndpoint = `/student-class?student_id=${studentId}&class_id=${parseInt(classId)}`;
                successMessage = '选课记录删除成功';
                break;
            default:
                return;
        }
        
        $.ajax({
            url: getFullApiPath(adminApiPath, apiEndpoint),
            type: requestMethod,
            headers: utils.getAuthHeader(),
            contentType: 'application/json',
            data: deleteType === 'student-class' ? JSON.stringify(postData) : null,
            success: function(response) {
                // 关闭确认模态框
                const modal = bootstrap.Modal.getInstance(document.getElementById('confirmDeleteModal'));
                modal.hide();
                
                if (response.success) {
                    let messageElement;
                    switch (deleteType) {
                        case 'student':
                            messageElement = $('#studentMessage');
                            loadStudents();
                            break;
                        case 'course':
                            messageElement = $('#courseMessage');
                            loadCourses();
                            break;
                        case 'student-class':
                            messageElement = $('#classMessage');
                            loadClasses();
                            break;
                    }
                    
                    utils.showMessage(messageElement, successMessage, 'success');
                    // 刷新统计数据
                    loadStatistics();
                } else {
                    let messageElement = $(`#${deleteType}Message`);
                    utils.showMessage(messageElement, response.message || '删除失败', 'danger');
                }
            },
            error: function(xhr) {
                // 关闭确认模态框
                const modal = bootstrap.Modal.getInstance(document.getElementById('confirmDeleteModal'));
                modal.hide();
                
                let errorMessage = '删除操作失败';
                try {
                    if (xhr.responseJSON && xhr.responseJSON.detail) {
                        errorMessage = xhr.responseJSON.detail;
                    } else if (xhr.responseText) {
                        const response = JSON.parse(xhr.responseText);
                        errorMessage = response.message || response.error || errorMessage;
                    }
                } catch (e) {}
                
                let messageElement;
                switch (deleteType) {
                    case 'student':
                        messageElement = $('#studentMessage');
                        break;
                    case 'course':
                        messageElement = $('#courseMessage');
                        break;
                    case 'student-class':
                        messageElement = $('#classMessage');
                        break;
                }
                
                utils.showMessage(messageElement, errorMessage, 'danger');
            }
        });
    });
});

// 加载统计数据
function loadStatistics() {
    // API文档: GET /admin/statistics 获取系统整体统计信息
    const adminApiPath = ROLE_API_PATHS[3];
    const endpoint = '/statistics';
    const url = getFullApiPath(adminApiPath, endpoint);
    
    // 如果有调试工具，记录请求
    if (window.debugTools) {
        window.debugTools.logApiRequest('GET', url);
    }
    
    $.ajax({
        url: url,
        type: 'GET',
        headers: utils.getAuthHeader(),
        success: function(stats) {
            // 如果有调试工具，分析响应
            if (window.debugTools) {
                window.debugTools.logApiResponse(url, stats);
                // 检查预期字段是否存在
                window.debugTools.analyzeApiResponse(endpoint, stats, [
                    'student_count', 'teacher_count', 'course_count', 
                    'class_count', 'evaluation_count', 'average_score'
                ]);
            }
            
            if (!stats) {
                utils.showMessage($('#studentMessage'), '获取到的统计数据为空', 'warning');
                return;
            }
            
            // 记录原始数据和字段名
            console.log('管理员统计数据:', stats);
            console.log('统计数据字段:', Object.keys(stats));
            
            // 兼容多种可能的字段命名
            const studentCount = stats.student_count || stats.studentCount || stats.StudentCount || 0;
            const teacherCount = stats.teacher_count || stats.teacherCount || stats.TeacherCount || 0;
            const courseCount = stats.course_count || stats.courseCount || stats.CourseCount || 0;
            const classCount = stats.class_count || stats.classCount || stats.ClassCount || 0;
            const evaluationCount = stats.evaluation_count || stats.evaluationCount || stats.EvaluationCount || 0;
            const averageScore = stats.average_score || stats.averageScore || stats.AverageScore || null;
            
            // 更新UI
            $('#studentCount').text(studentCount);
            $('#teacherCount').text(teacherCount);
            $('#courseCount').text(courseCount);
            $('#classCount').text(classCount);
            $('#evaluationCount').text(evaluationCount);
            $('#averageScore').text(
                averageScore
                ? parseFloat(averageScore).toFixed(1)
                : '0.0'
            );
        },
        error: function(xhr, status, error) {
            utils.showMessage($('#studentMessage'), '加载统计数据失败', 'danger');
            console.error('加载统计数据错误:', xhr);
            
            // 如果有调试工具，记录错误
            if (window.debugTools) {
                window.debugTools.logApiResponse(url, xhr.responseText, xhr.status);
            }
        }
    });
}

// 加载学生列表
function loadStudents() {
    // API文档: GET /admin/students 获取所有学生信息
    const adminApiPath = ROLE_API_PATHS[3];
    
    $.ajax({
        url: getFullApiPath(adminApiPath, '/students'),
        type: 'GET',
        headers: utils.getAuthHeader(),
        success: function(students) {
            const $studentList = $('#studentList');
            $studentList.empty();
            
            if (!Array.isArray(students) || students.length === 0) {
                $studentList.append('<tr><td colspan="5" class="text-center">暂无学生数据</td></tr>');
                return;
            }
            
            students.forEach(function(student) {
                // API文档中的字段: StudentID, Name, Major, RoleID
                $studentList.append(`
                    <tr>
                        <td>${utils.escapeHtml(student.StudentID)}</td>
                        <td>${utils.escapeHtml(student.Name)}</td>
                        <td>${utils.escapeHtml(student.Major)}</td>
                        <td>学生</td>
                        <td>
                            <button class="btn btn-sm btn-danger" onclick="showDeleteConfirm('student', '${student.StudentID}', '学生: ${student.Name}')">
                                删除
                            </button>
                        </td>
                    </tr>
                `);
            });
        },
        error: function(xhr) {
            utils.showMessage($('#studentMessage'), '加载学生列表失败', 'danger');
        }
    });
}

// 加载课程列表
function loadCourses() {
    // API文档: GET /admin/courses 获取所有课程信息
    const adminApiPath = ROLE_API_PATHS[3];
    
    $.ajax({
        url: getFullApiPath(adminApiPath, '/courses'),
        type: 'GET',
        headers: utils.getAuthHeader(),
        success: function(courses) {
            const $courseList = $('#courseList');
            $courseList.empty();
            
            if (!Array.isArray(courses) || courses.length === 0) {
                $courseList.append('<tr><td colspan="4" class="text-center">暂无课程数据</td></tr>');
                return;
            }
            
            courses.forEach(function(course) {
                // API文档中的字段: CourseID, Name, Credit
                $courseList.append(`
                    <tr>
                        <td>${utils.escapeHtml(course.CourseID)}</td>
                        <td>${utils.escapeHtml(course.Name)}</td>
                        <td>${course.Credit || 0}</td>
                        <td>
                            <button class="btn btn-sm btn-danger" onclick="showDeleteConfirm('course', '${course.CourseID}', '课程: ${course.Name}')">
                                删除
                            </button>
                        </td>
                    </tr>
                `);
            });
        },
        error: function(xhr) {
            utils.showMessage($('#courseMessage'), '加载课程列表失败', 'danger');
        }
    });
}

// 加载班级列表
function loadClasses() {
    // API文档: GET /admin/classes 获取所有教学班信息
    const adminApiPath = ROLE_API_PATHS[3];
    
    $.ajax({
        url: getFullApiPath(adminApiPath, '/classes'),
        type: 'GET',
        headers: utils.getAuthHeader(),
        success: function(classes) {
            const $classList = $('#classList');
            $classList.empty();
            
            if (!Array.isArray(classes) || classes.length === 0) {
                $classList.append('<tr><td colspan="7" class="text-center">暂无班级数据</td></tr>');
                return;
            }
            
            classes.forEach(function(cls) {
                // 获取评价数量和平均分（如果后端提供）
                const evaluationCount = cls.EvaluationCount || cls.evaluationCount || 0;
                const avgScore = cls.AverageScore || cls.averageScore ? 
                    parseFloat(cls.AverageScore || cls.averageScore).toFixed(1) : 
                    '暂无';
                
                // API文档中的字段: ClassID, CourseName, TeacherName, Semester, TimeLocation
                $classList.append(`
                    <tr>
                        <td>${utils.escapeHtml(cls.ClassID)}</td>
                        <td>${utils.escapeHtml(cls.CourseName)}</td>
                        <td>${utils.escapeHtml(cls.TeacherName)}</td>
                        <td>${utils.escapeHtml(cls.Semester)}</td>
                        <td>${utils.escapeHtml(cls.TimeLocation)}</td>
                        <td>
                            ${evaluationCount} / ${avgScore}
                        </td>
                        <td>
                            <button class="btn btn-sm btn-primary" onclick="showAddStudentToClassModal(${cls.ClassID}, '${cls.CourseName}')">
                                添加学生
                            </button>
                        </td>
                    </tr>
                `);
            });
        },
        error: function(xhr) {
            utils.showMessage($('#classMessage'), '加载班级列表失败', 'danger');
        }
    });
}

// 加载选课记录
function loadEnrollments() {
    // 获取学生选课记录
    const adminApiPath = ROLE_API_PATHS[3];
    
    $.ajax({
        url: getFullApiPath(adminApiPath, '/enrollments'),
        type: 'GET',
        headers: utils.getAuthHeader(),
        success: function(enrollments) {
            const $enrollmentList = $('#enrollmentList');
            $enrollmentList.empty();
            
            if (!Array.isArray(enrollments) || enrollments.length === 0) {
                $enrollmentList.append('<tr><td colspan="7" class="text-center">暂无选课记录</td></tr>');
                return;
            }
            
            enrollments.forEach(function(enrollment) {
                // 学生选课状态
                const hasEvaluated = enrollment.HasEvaluated || enrollment.hasEvaluated || false;
                const evaluationStatus = hasEvaluated ? 
                    '<span class="badge bg-success">已评价</span>' : 
                    '<span class="badge bg-warning">未评价</span>';
                
                // 学生选课记录
                $enrollmentList.append(`
                    <tr>
                        <td>${utils.escapeHtml(enrollment.StudentID)}</td>
                        <td>${utils.escapeHtml(enrollment.StudentName)}</td>
                        <td>${utils.escapeHtml(enrollment.ClassID)}</td>
                        <td>${utils.escapeHtml(enrollment.CourseName)}</td>
                        <td>${utils.formatDate(enrollment.SelectTime)}</td>
                        <td>${evaluationStatus}</td>
                        <td>
                            <button class="btn btn-sm btn-danger" onclick="showDeleteConfirm('student-class', '${enrollment.StudentID}-${enrollment.ClassID}', '选课记录: ${enrollment.StudentName} - ${enrollment.CourseName}')">
                                删除
                            </button>
                        </td>
                    </tr>
                `);
            });
        },
        error: function(xhr) {
            utils.showMessage($('#enrollmentMessage'), '加载选课记录失败', 'danger');
        }
    });
}

// 显示添加学生到班级模态框
function showAddStudentToClassModal(classId, courseName) {
    // 设置班级信息
    $('#scClassId').val(classId);
    $('#selectedCourseName').text(courseName);
    
    // 显示模态框
    const modal = new bootstrap.Modal(document.getElementById('addStudentClassModal'));
    modal.show();
}

// 显示删除确认对话框
function showDeleteConfirm(type, id, name) {
    $('#deleteType').val(type);
    $('#deleteId').val(id);
    $('#deleteConfirmText').text(`确定要删除${name}吗？此操作不可恢复。`);
    
    const modal = new bootstrap.Modal(document.getElementById('confirmDeleteModal'));
    modal.show();
} 