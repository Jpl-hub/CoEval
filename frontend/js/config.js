// API配置
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:8000/api'
    : window.location.origin + '/api';

// 角色API路径前缀
const ROLE_API_PATHS = {
    1: '/student',  // 学生
    2: '/teacher',  // 教师
    3: '/admin'     // 管理员
};

// 获取完整API路径
function getFullApiPath(rolePath, endpoint) {
    return `${API_BASE_URL}${rolePath}${endpoint}`;
}

// 存储键名
const STORAGE_KEYS = {
    TOKEN: 'token',
    USER_INFO: 'userInfo'
};

// 角色页面映射（与后端一致：1-学生，2-教师，3-管理员）
const ROLE_PAGES = {
    1: 'pages/student.html',  // 学生
    2: 'pages/teacher.html',  // 教师
    3: 'pages/admin.html'     // 管理员
};

// 角色名称映射
const ROLE_NAMES = {
    1: '学生',
    2: '教师',
    3: '管理员'
};

// 评分选项
const RATING_OPTIONS = [
    { value: 1, text: '非常不满意' },
    { value: 2, text: '不满意' },
    { value: 3, text: '一般' },
    { value: 4, text: '满意' },
    { value: 5, text: '非常满意' }
];

// 通用工具函数
const utils = {
    // 显示消息
    showMessage: function($element, message, type = 'danger') {
        if (!$element || !$element.length) return;
        
        // 清除其他消息
        $('.alert').addClass('d-none').removeClass('alert-success alert-warning alert-danger');
        
        $element
            .removeClass('d-none')
            .removeClass('alert-success alert-warning alert-danger')
            .addClass(`alert-${type}`)
            .text(message || '发生未知错误');
            
        // 如果是成功消息，3秒后自动消失
        if (type === 'success') {
            setTimeout(() => {
                $element.addClass('d-none');
            }, 3000);
        }
    },
    
    // 格式化日期
    formatDate: function(dateString) {
        try {
            const date = new Date(dateString);
            if (isNaN(date.getTime())) {
                return '无效日期';
            }
            return date.toLocaleDateString('zh-CN', {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit'
            });
        } catch (e) {
            console.error('日期格式化错误:', e);
            return '无效日期';
        }
    },
    
    // 检查认证状态
    checkAuth: function() {
        const token = localStorage.getItem(STORAGE_KEYS.TOKEN);
        let userInfo;
        
        try {
            userInfo = JSON.parse(localStorage.getItem(STORAGE_KEYS.USER_INFO) || '{}');
        } catch (e) {
            console.error('本地存储的用户信息无效');
            this.logout();
            return false;
        }
        
        if (!token || !userInfo.id || !userInfo.role || !ROLE_NAMES[userInfo.role]) {
            this.logout();
            return false;
        }
        
        // 检查页面权限
        const path = window.location.pathname;
        const expectedPage = ROLE_PAGES[userInfo.role];
        
        if (path && expectedPage && !path.includes(expectedPage.split('/').pop())) {
            console.log('重定向到正确的角色页面:', expectedPage);
            setTimeout(() => {
                window.location.href = '../' + expectedPage;
            }, 100);
            return false;
        }
        
        return true;
    },
    
    // 获取认证头部
    getAuthHeader: function() {
        const token = localStorage.getItem(STORAGE_KEYS.TOKEN);
        if (!token) {
            this.logout();
            return {};
        }
        return {
            'Authorization': `Bearer ${token}`
        };
    },
    
    // 登出
    logout: function() {
        localStorage.removeItem(STORAGE_KEYS.TOKEN);
        localStorage.removeItem(STORAGE_KEYS.USER_INFO);
        window.location.href = '../index.html';
    },
    
    // HTML转义
    escapeHtml: function(unsafe) {
        if (unsafe == null) return '';
        return unsafe
            .toString()
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
}; 