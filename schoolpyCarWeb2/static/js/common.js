/*
 * 公共JavaScript文件
 * 与base.html模板匹配
 */

// API基础地址
const API_BASE = '/api';

// 页面加载完成后执行
$(document).ready(function() {
    console.log('公共JS加载完成');
    
    // 更新当前时间
    updateCurrentTime();
    setInterval(updateCurrentTime, 1000);
    
    // 获取活跃预警数量
    getActiveAlertsCount();
    
    // 设置导航栏活动项
    setActiveNavItem();
});

// 更新当前时间
function updateCurrentTime() {
    const now = new Date();
    const timeStr = now.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
    const currentTimeElement = $('#current-time');
    if (currentTimeElement.length > 0) {
        currentTimeElement.text(timeStr);
    }
}

// 获取活跃预警数量
function getActiveAlertsCount() {
    $.ajax({
        url: API_BASE + '/alerts/active/count',
        method: 'GET',
        dataType: 'json',
        success: function(response) {
            const count = response.count || 0;
            const badge = $('#alert-badge');
            if (badge.length > 0) {
                if (count > 0) {
                    badge.text(count).show();
                } else {
                    badge.hide();
                }
            }
        },
        error: function(xhr, status, error) {
            console.log('获取活跃预警数量失败:', error);
            // 静默失败，不显示错误
        }
    });
}

// 设置导航栏活动项
function setActiveNavItem() {
    const path = window.location.pathname;
    const navItems = {
        '/': 'nav-dashboard',
        '/vehicles': 'nav-vehicles',
        '/location': 'nav-location',
        '/trajectory': 'nav-trajectory',
        '/geofence': 'nav-geofence',
        '/alerts': 'nav-alerts'
    };
    
    const activeNavId = navItems[path];
    if (activeNavId) {
        $('#' + activeNavId).addClass('active');
    }
}

// 格式化日期时间
function formatDateTime(dateTimeStr) {
    if (!dateTimeStr) return '-';
    try {
        const date = new Date(dateTimeStr);
        return date.toLocaleString('zh-CN', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        });
    } catch (e) {
        return dateTimeStr;
    }
}

// HTML转义
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// 显示成功消息
function showSuccess(message) {
    alert('✓ ' + message);
}

// 显示错误消息
function showError(message) {
    alert('✗ ' + message);
}

// 显示警告消息
function showWarning(message) {
    alert('⚠ ' + message);
}

// 显示信息消息
function showInfo(message) {
    alert('ℹ ' + message);
}

// 防抖函数
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// 节流函数
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}
