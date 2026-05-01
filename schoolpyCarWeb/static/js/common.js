/**
 * 校车管理系统 - 公共JavaScript工具类
 * 包含API请求封装、用户认证、通用工具函数等
 */

// 全局配置
const API_CONFIG = {
    baseUrl: '/api',
    timeout: 10000
};

// 全局存储
window.authToken = localStorage.getItem('authToken');
window.currentUser = JSON.parse(localStorage.getItem('currentUser') || 'null');

/**
 * API请求封装
 * @param {string} url - API地址
 * @param {object} options - 请求选项
 */
async function apiRequest(url, options = {}) {
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };
    
    if (window.authToken) {
        headers['Authorization'] = `Bearer ${window.authToken}`;
    }
    
    const config = {
        ...options,
        headers
    };
    
    if (config.body && typeof config.body === 'object') {
        config.body = JSON.stringify(config.body);
    }
    
    try {
        const response = await fetch(`${API_CONFIG.baseUrl}${url}`, config);
        
        if (response.status === 401) {
            // 未授权，跳转到登录页
            logout();
            throw new Error('登录已过期，请重新登录');
        }
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || '请求失败');
        }
        
        return data;
    } catch (error) {
        console.error('API请求错误:', error);
        throw error;
    }
}

/**
 * GET请求
 */
function apiGet(url, params = {}) {
    const queryString = new URLSearchParams(params).toString();
    const fullUrl = queryString ? `${url}?${queryString}` : url;
    return apiRequest(fullUrl, { method: 'GET' });
}

/**
 * POST请求
 */
function apiPost(url, data = {}) {
    return apiRequest(url, {
        method: 'POST',
        body: data
    });
}

/**
 * PUT请求
 */
function apiPut(url, data = {}) {
    return apiRequest(url, {
        method: 'PUT',
        body: data
    });
}

/**
 * DELETE请求
 */
function apiDelete(url) {
    return apiRequest(url, { method: 'DELETE' });
}

/**
 * 退出登录
 */
function logout() {
    localStorage.removeItem('authToken');
    localStorage.removeItem('currentUser');
    window.authToken = null;
    window.currentUser = null;
    window.location.href = '/';
}

/**
 * 检查登录状态
 */
function checkAuth() {
    if (!window.authToken || !window.currentUser) {
        logout();
        return false;
    }
    return true;
}

/**
 * 检查是否是教育局管理员
 */
function isEducationBureau() {
    return window.currentUser && window.currentUser.role === 'education_bureau';
}

/**
 * 检查是否是学校管理员
 */
function isSchoolAdmin() {
    return window.currentUser && window.currentUser.role === 'school_admin';
}

/**
 * 获取当前用户的学校ID
 */
function getCurrentSchoolId() {
    return window.currentUser ? window.currentUser.school_id : null;
}

/**
 * 显示通知消息
 * @param {string} message - 消息内容
 * @param {string} type - 类型: success, info, warning, danger
 */
function showToast(message, type = 'info') {
    const toastId = 'toast_' + Date.now();
    const bgColors = {
        success: 'bg-success',
        info: 'bg-info',
        warning: 'bg-warning',
        danger: 'bg-danger'
    };
    
    const iconClasses = {
        success: 'fa-check-circle',
        info: 'fa-info-circle',
        warning: 'fa-exclamation-triangle',
        danger: 'fa-times-circle'
    };
    
    const toastHtml = `
        <div id="${toastId}" class="toast ${bgColors[type]} text-white" data-delay="3000" style="position: fixed; top: 20px; right: 20px; z-index: 9999;">
            <div class="toast-header ${bgColors[type]} text-white">
                <i class="fa ${iconClasses[type]} mr-2"></i>
                <strong class="mr-auto">提示</strong>
                <button type="button" class="ml-2 mb-1 close text-white" data-dismiss="toast">
                    <span>&times;</span>
                </button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
    `;
    
    $('body').append(toastHtml);
    $(`#${toastId}`).toast('show');
    
    // 自动移除
    setTimeout(() => {
        $(`#${toastId}`).remove();
    }, 3500);
}

/**
 * 显示确认对话框
 * @param {string} title - 标题
 * @param {string} message - 内容
 * @returns {Promise<boolean>}
 */
function showConfirm(title, message) {
    return new Promise((resolve) => {
        const modalId = 'confirm_' + Date.now();
        const modalHtml = `
            <div id="${modalId}" class="modal fade" tabindex="-1" role="dialog">
                <div class="modal-dialog" role="document">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title"><i class="fa fa-question-circle text-warning"></i> ${title}</h5>
                            <button type="button" class="close" data-dismiss="modal">
                                <span>&times;</span>
                            </button>
                        </div>
                        <div class="modal-body">
                            <p>${message}</p>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary btn-cancel" data-dismiss="modal">取消</button>
                            <button type="button" class="btn btn-primary btn-confirm">确定</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        $('body').append(modalHtml);
        const $modal = $(`#${modalId}`);
        
        $modal.modal('show');
        
        $modal.find('.btn-confirm').on('click', () => {
            $modal.modal('hide');
            setTimeout(() => {
                $modal.remove();
                resolve(true);
            }, 200);
        });
        
        $modal.find('.btn-cancel, .close').on('click', () => {
            setTimeout(() => {
                $modal.remove();
                resolve(false);
            }, 200);
        });
    });
}

/**
 * 格式化日期
 * @param {string|Date} date - 日期
 * @param {string} format - 格式
 */
function formatDate(date, format = 'YYYY-MM-DD') {
    if (!date) return '';
    
    const d = new Date(date);
    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    const hours = String(d.getHours()).padStart(2, '0');
    const minutes = String(d.getMinutes()).padStart(2, '0');
    const seconds = String(d.getSeconds()).padStart(2, '0');
    
    return format
        .replace('YYYY', year)
        .replace('MM', month)
        .replace('DD', day)
        .replace('HH', hours)
        .replace('mm', minutes)
        .replace('ss', seconds);
}

/**
 * 获取状态标签样式
 * @param {string} status - 状态值
 * @param {object} mapping - 状态映射
 */
function getStatusBadge(status, mapping = {}) {
    const defaultMapping = {
        'active': { class: 'success', text: '启用' },
        'inactive': { class: 'secondary', text: '停用' },
        'available': { class: 'success', text: '可用' },
        'in_use': { class: 'primary', text: '使用中' },
        'maintenance': { class: 'warning', text: '维护中' },
        'disabled': { class: 'danger', text: '停用' },
        'on_duty': { class: 'primary', text: '值班' },
        'on_leave': { class: 'warning', text: '休假' },
        'published': { class: 'success', text: '已发布' },
        'draft': { class: 'secondary', text: '草稿' },
        'pending': { class: 'warning', text: '待执行' },
        'in_progress': { class: 'primary', text: '执行中' },
        'completed': { class: 'success', text: '已完成' },
        'cancelled': { class: 'secondary', text: '已取消' }
    };
    
    const config = mapping[status] || defaultMapping[status] || { class: 'secondary', text: status };
    return `<span class="badge badge-${config.class}">${config.text}</span>`;
}

/**
 * 初始化页面
 */
function initPage() {
    // 检查登录状态
    if (!checkAuth()) {
        return;
    }
    
    // 更新用户信息显示
    updateUserInfo();
    
    // 设置侧边栏激活状态
    setActiveSidebar();
}

/**
 * 更新用户信息显示
 */
function updateUserInfo() {
    if (window.currentUser) {
        $('#userName').text(window.currentUser.real_name);
        $('#userRole').text(isEducationBureau() ? '教育局管理员' : '学校管理员');
        
        // 根据角色显示/隐藏菜单项
        if (!isEducationBureau()) {
            $('.menu-education-only').hide();
        }
    }
}

/**
 * 设置侧边栏激活状态
 */
function setActiveSidebar() {
    const path = window.location.pathname;
    $('.sidebar-nav .nav-link').each(function() {
        const href = $(this).attr('href');
        if (href === path) {
            $(this).addClass('active');
            $(this).closest('.nav-item').addClass('menu-open');
        }
    });
}

// 页面加载时初始化
$(document).ready(function() {
    // 只有在非登录页面才初始化
    if (window.location.pathname !== '/') {
        initPage();
    }
});
