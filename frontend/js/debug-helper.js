/**
 * 前后端字段匹配调试工具
 * 帮助识别和解决API响应字段与前端期望字段不匹配问题
 */

// 调试日志级别
const DEBUG_LEVEL = {
    NONE: 0,
    ERROR: 1,
    WARNING: 2,
    INFO: 3,
    ALL: 4
};

// 当前调试级别
let currentDebugLevel = DEBUG_LEVEL.ALL;

// 设置调试级别
function setDebugLevel(level) {
    if (level >= DEBUG_LEVEL.NONE && level <= DEBUG_LEVEL.ALL) {
        currentDebugLevel = level;
        logDebug(`调试级别设置为: ${level}`, DEBUG_LEVEL.INFO);
    }
}

// 调试日志
function logDebug(message, level = DEBUG_LEVEL.INFO, data = null) {
    if (level <= currentDebugLevel) {
        const prefix = {
            [DEBUG_LEVEL.ERROR]: '❌ 错误',
            [DEBUG_LEVEL.WARNING]: '⚠️ 警告',
            [DEBUG_LEVEL.INFO]: 'ℹ️ 信息',
            [DEBUG_LEVEL.ALL]: '🔍 详细'
        }[level] || '';
        
        console.log(`[调试] ${prefix}: ${message}`);
        if (data) {
            console.log('数据:', data);
        }
    }
}

// 分析API响应
function analyzeApiResponse(endpoint, response, expectedFields) {
    logDebug(`分析API响应: ${endpoint}`, DEBUG_LEVEL.INFO);
    
    if (!response) {
        logDebug('响应为空', DEBUG_LEVEL.ERROR);
        return;
    }
    
    // 对数组响应，检查第一个元素
    const sampleData = Array.isArray(response) ? response[0] : response;
    
    if (!sampleData) {
        logDebug('响应数据为空', DEBUG_LEVEL.WARNING);
        return;
    }
    
    // 记录所有实际字段
    const actualFields = Object.keys(sampleData);
    logDebug('实际返回字段:', DEBUG_LEVEL.INFO, actualFields);
    
    // 检查期望字段是否存在
    if (expectedFields && expectedFields.length) {
        logDebug('期望字段:', DEBUG_LEVEL.INFO, expectedFields);
        
        const missingFields = expectedFields.filter(field => !actualFields.includes(field));
        if (missingFields.length) {
            logDebug('缺失字段:', DEBUG_LEVEL.ERROR, missingFields);
        }
        
        // 尝试智能映射字段
        if (missingFields.length) {
            const possibleMatches = findPossibleMatches(missingFields, actualFields);
            if (Object.keys(possibleMatches).length) {
                logDebug('可能的字段映射:', DEBUG_LEVEL.INFO, possibleMatches);
            }
        }
    }
    
    return {
        actualFields,
        sampleData
    };
}

// 查找可能匹配的字段（大小写不敏感比较）
function findPossibleMatches(missingFields, actualFields) {
    const possibleMatches = {};
    
    missingFields.forEach(missing => {
        const lowerMissing = missing.toLowerCase();
        const matches = actualFields.filter(actual => 
            actual.toLowerCase() === lowerMissing || 
            actual.toLowerCase().includes(lowerMissing) ||
            lowerMissing.includes(actual.toLowerCase())
        );
        
        if (matches.length) {
            possibleMatches[missing] = matches;
        }
    });
    
    return possibleMatches;
}

// 记录API请求
function logApiRequest(method, url, data = null) {
    logDebug(`API请求: ${method} ${url}`, DEBUG_LEVEL.INFO, data);
}

// 记录API响应
function logApiResponse(url, response, status = 200) {
    if (status >= 200 && status < 300) {
        logDebug(`API响应: ${url}`, DEBUG_LEVEL.INFO, response);
    } else {
        logDebug(`API错误响应: ${url}, 状态码: ${status}`, DEBUG_LEVEL.ERROR, response);
    }
}

// 导出调试工具
window.debugTools = {
    setDebugLevel,
    logDebug,
    analyzeApiResponse,
    logApiRequest,
    logApiResponse,
    DEBUG_LEVEL
}; 