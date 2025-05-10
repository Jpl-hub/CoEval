$(document).ready(function() {
    // 检查是否已登录
    const token = localStorage.getItem(STORAGE_KEYS.TOKEN);
    const userInfo = JSON.parse(localStorage.getItem(STORAGE_KEYS.USER_INFO) || '{}');
    
    if (token && userInfo.id && userInfo.role) {
        // 已登录，跳转到相应角色页面
        window.location.href = ROLE_PAGES[userInfo.role];
        return;
    }
    
    // 登录表单提交
    $('#loginForm').on('submit', function(e) {
        e.preventDefault();
        
        const userId = $('#userId').val();
        const password = $('#password').val();
        const role = $('input[name="role"]:checked').val();
        const $loginMessage = $('#loginMessage');
        
        if (!userId || !password) {
            utils.showMessage($loginMessage, '请输入用户ID和密码');
            return;
        }
        
        // 按API文档发送登录请求
        $.ajax({
            url: `${API_BASE_URL}/auth/login`,
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                user_id: userId,
                password: password,
                role: parseInt(role)
            }),
            success: function(response) {
                // 保存令牌
                localStorage.setItem(STORAGE_KEYS.TOKEN, response.access_token);
                
                // 保存用户信息
                localStorage.setItem(STORAGE_KEYS.USER_INFO, JSON.stringify({
                    id: userId,
                    name: response.user_info.name,
                    role: response.user_info.role
                }));
                
                utils.showMessage($loginMessage, '登录成功，正在跳转...', 'success');
                
                // 跳转到对应角色的页面
                setTimeout(function() {
                    window.location.href = ROLE_PAGES[response.user_info.role];
                }, 1000);
            },
            error: function(xhr, status, error) {
                let errorMessage = '登录失败，请检查用户名和密码';
                
                try {
                    if (xhr.responseJSON && xhr.responseJSON.detail) {
                        errorMessage = xhr.responseJSON.detail;
                    } else if (xhr.responseText) {
                        const response = JSON.parse(xhr.responseText);
                        errorMessage = response.message || response.error || errorMessage;
                    }
                } catch (e) {
                    console.error('解析错误响应失败');
                }
                
                utils.showMessage($loginMessage, errorMessage);
            }
        });
    });
}); 