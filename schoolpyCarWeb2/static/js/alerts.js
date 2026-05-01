/*
 * 预警管理页面JavaScript
 * 与模板alerts.html匹配
 */

// 全局变量
let currentPage = 1;
const pageSize = 10;
let currentFilterStatus = '';
let currentFilterSeverity = '';

// API基础地址
const API_BASE = '/api';

// 页面加载完成后执行
$(document).ready(function() {
    console.log('预警管理页面加载完成');
    
    // 加载预警列表
    loadAlerts();
    
    // 绑定事件
    bindEvents();
    
    // 设置导航栏活动项
    $('#nav-alerts').addClass('active');
});

// 绑定事件
function bindEvents() {
    // 处理预警表单提交
    $('#handleAlertForm').on('submit', function(e) {
        e.preventDefault();
        submitHandleAlert();
    });
}

// 刷新预警
function refreshAlerts() {
    currentPage = 1;
    loadAlerts();
}

// 应用筛选条件
function applyAlertFilters() {
    currentFilterStatus = $('#filter-alert-status').val();
    currentFilterSeverity = $('#filter-severity').val();
    currentPage = 1;
    loadAlerts();
}

// 加载预警列表
function loadAlerts() {
    console.log('加载预警列表，页码:', currentPage);
    
    // 构建URL参数
    let params = {
        page: currentPage,
        page_size: pageSize
    };
    
    if (currentFilterStatus) {
        params.status = currentFilterStatus;
    }
    
    if (currentFilterSeverity) {
        params.severity = currentFilterSeverity;
    }
    
    // 显示加载中
    showLoadingState();
    
    // 发送AJAX请求
    $.ajax({
        url: API_BASE + '/alerts',
        method: 'GET',
        data: params,
        dataType: 'json',
        success: function(response) {
            console.log('预警列表响应:', response);
            renderAlerts(response.data || []);
            renderPagination(response.page_info || {});
            updateAlertStats(response.data || []);
        },
        error: function(xhr, status, error) {
            console.error('加载预警列表失败:', error);
            showError('加载预警列表失败: ' + error);
            showEmptyState();
        }
    });
}

// 显示加载状态
function showLoadingState() {
    $('#alerts-table tbody').html(`
        <tr>
            <td colspan="12" class="text-center text-muted py-5">
                <i class="fas fa-spinner fa-spin mr-2"></i>加载中...
            </td>
        </tr>
    `);
}

// 显示空状态
function showEmptyState() {
    $('#alerts-table tbody').html(`
        <tr>
            <td colspan="12" class="text-center text-muted py-5">
                <i class="fas fa-exclamation-triangle fa-3x mb-3"></i>
                <h5>暂无预警数据</h5>
                <p class="mb-0">系统运行正常，暂无越界预警</p>
            </td>
        </tr>
    `);
    $('#alerts-pagination').empty();
}

// 渲染预警列表
function renderAlerts(alerts) {
    const tbody = $('#alerts-table tbody');
    tbody.empty();
    
    if (!alerts || alerts.length === 0) {
        showEmptyState();
        return;
    }
    
    alerts.forEach(function(alert, index) {
        const rowIndex = (currentPage - 1) * pageSize + index + 1;
        const statusBadge = getAlertStatusBadge(alert.status);
        const severityBadge = getSeverityBadge(alert.severity);
        const fenceTypeBadge = getFenceTypeBadge(alert.fence_type);
        
        const row = `
            <tr class="${alert.status === 'active' ? 'table-warning' : ''}">
                <td>${alert.id}</td>
                <td>${formatDateTime(alert.created_at)}</td>
                <td>${escapeHtml(alert.fence_name || '-')}</td>
                <td>${fenceTypeBadge}</td>
                <td><strong>${escapeHtml(alert.plate_number || '-')}</strong></td>
                <td>
                    <small class="text-monospace">
                        ${alert.latitude?.toFixed(4) || '-'}, ${alert.longitude?.toFixed(4) || '-'}
                    </small>
                </td>
                <td><span class="font-weight-bold text-danger">${alert.violation_count || 1}</span></td>
                <td>${severityBadge}</td>
                <td>${statusBadge}</td>
                <td>${escapeHtml(alert.resolved_by || '-')}</td>
                <td>${formatDateTime(alert.resolved_at)}</td>
                <td>
                    <button class="btn btn-sm btn-outline-info" title="查看详情" onclick="openViewAlertModal(${alert.id})">
                        <i class="fas fa-eye"></i>
                    </button>
                    ${alert.status === 'active' ? `
                    <button class="btn btn-sm btn-outline-primary" title="处理预警" onclick="openHandleAlertModal(${alert.id})">
                        <i class="fas fa-edit"></i>
                    </button>
                    ` : ''}
                </td>
            </tr>
        `;
        tbody.append(row);
    });
}

// 渲染分页
function renderPagination(pageInfo) {
    const pagination = $('#alerts-pagination');
    pagination.empty();
    
    if (!pageInfo || pageInfo.total_pages <= 1) {
        return;
    }
    
    const current = pageInfo.current_page || 1;
    const total = pageInfo.total_pages || 1;
    
    // 上一页
    const prevDisabled = current <= 1 ? 'disabled' : '';
    pagination.append(`
        <li class="page-item ${prevDisabled}">
            <a class="page-link" href="#" onclick="goToPage(${current - 1}); return false;">
                <i class="fas fa-chevron-left"></i>
            </a>
        </li>
    `);
    
    // 页码
    const startPage = Math.max(1, current - 2);
    const endPage = Math.min(total, current + 2);
    
    if (startPage > 1) {
        pagination.append(`
            <li class="page-item">
                <a class="page-link" href="#" onclick="goToPage(1); return false;">1</a>
            </li>
        `);
        if (startPage > 2) {
            pagination.append('<li class="page-item disabled"><span class="page-link">...</span></li>');
        }
    }
    
    for (let i = startPage; i <= endPage; i++) {
        const active = i === current ? 'active' : '';
        pagination.append(`
            <li class="page-item ${active}">
                <a class="page-link" href="#" onclick="goToPage(${i}); return false;">${i}</a>
            </li>
        `);
    }
    
    if (endPage < total) {
        if (endPage < total - 1) {
            pagination.append('<li class="page-item disabled"><span class="page-link">...</span></li>');
        }
        pagination.append(`
            <li class="page-item">
                <a class="page-link" href="#" onclick="goToPage(${total}); return false;">${total}</a>
            </li>
        `);
    }
    
    // 下一页
    const nextDisabled = current >= total ? 'disabled' : '';
    pagination.append(`
        <li class="page-item ${nextDisabled}">
            <a class="page-link" href="#" onclick="goToPage(${current + 1}); return false;">
                <i class="fas fa-chevron-right"></i>
            </a>
        </li>
    `);
}

// 跳转到指定页
function goToPage(page) {
    currentPage = page;
    loadAlerts();
    // 滚动到顶部
    $('html, body').animate({ scrollTop: 0 }, 300);
}

// 更新预警统计
function updateAlertStats(alerts) {
    if (!alerts) return;
    
    // 从API获取统计数据
    $.ajax({
        url: API_BASE + '/dashboard/stats',
        method: 'GET',
        dataType: 'json',
        success: function(response) {
            console.log('统计数据:', response);
            
            const alertStats = response.alert_stats || {};
            
            $('#stat-active-alerts').text(alertStats.active || 0);
            $('#stat-today-alerts').text(alertStats.today || 0);
            $('#stat-resolved-alerts').text('已处理');
            $('#stat-total-alerts').text('统计中...');
        },
        error: function(xhr, status, error) {
            console.error('获取统计数据失败:', error);
        }
    });
}

// 获取预警状态标签HTML
function getAlertStatusBadge(status) {
    const statusMap = {
        'active': { class: 'badge-danger', text: '活跃' },
        'resolved': { class: 'badge-success', text: '已处理' },
        'ignored': { class: 'badge-secondary', text: '已忽略' }
    };
    
    const s = statusMap[status] || { class: 'badge-secondary', text: status };
    return `<span class="badge ${s.class}">${s.text}</span>`;
}

// 获取严重程度标签HTML
function getSeverityBadge(severity) {
    const severityMap = {
        'high': { class: 'badge-danger', text: '高' },
        'medium': { class: 'badge-warning', text: '中' },
        'low': { class: 'badge-success', text: '低' }
    };
    
    const s = severityMap[severity] || { class: 'badge-secondary', text: severity };
    return `<span class="badge ${s.class}">${s.text}</span>`;
}

// 获取围栏类型标签HTML
function getFenceTypeBadge(fenceType) {
    const typeMap = {
        'school': { class: 'badge-success', text: '学校区域' },
        'danger': { class: 'badge-danger', text: '危险路段' },
        'home': { class: 'badge-info', text: '家庭区域' },
        'other': { class: 'badge-secondary', text: '其他区域' }
    };
    
    const t = typeMap[fenceType] || { class: 'badge-secondary', text: fenceType };
    return `<span class="badge ${t.class}">${t.text}</span>`;
}

// 打开处理预警模态框
function openHandleAlertModal(alertId) {
    console.log('打开处理预警模态框，ID:', alertId);
    
    // 获取预警详情
    $.ajax({
        url: API_BASE + '/alerts/' + alertId,
        method: 'GET',
        success: function(alert) {
            console.log('获取预警详情:', alert);
            
            // 填充详情
            $('#handle-alert-id').val(alert.id);
            
            const detailHtml = `
                <p><strong>预警ID：</strong>${alert.id}</p>
                <p><strong>车辆：</strong>${escapeHtml(alert.plate_number || '-')}</p>
                <p><strong>围栏：</strong>${escapeHtml(alert.fence_name || '-')}</p>
                <p><strong>越界次数：</strong><span class="text-danger font-weight-bold">${alert.violation_count || 1}</span></p>
                <p><strong>预警消息：</strong>${escapeHtml(alert.message || '-')}</p>
                <p><strong>预警时间：</strong>${formatDateTime(alert.created_at)}</p>
            `;
            $('#alert-detail-info').html(detailHtml);
            
            // 清空表单
            $('#handle-status').val('resolved');
            $('#handle-resolver').val('');
            $('#handle-note').val('');
            
            // 显示模态框
            $('#handleAlertModal').modal('show');
        },
        error: function(xhr, status, error) {
            console.error('获取预警详情失败:', error);
            showError('获取预警详情失败');
        }
    });
}

// 提交处理预警表单
function submitHandleAlert() {
    const form = $('#handleAlertForm');
    const alertId = form.find('#handle-alert-id').val();
    const resolvedBy = form.find('#handle-resolver').val().trim();
    const resolveNote = form.find('#handle-note').val().trim();
    
    // 验证必填字段
    if (!resolvedBy) {
        showError('请输入处理人姓名');
        return;
    }
    
    console.log('提交处理预警，ID:', alertId);
    
    // 发送AJAX请求
    $.ajax({
        url: API_BASE + '/alerts/' + alertId + '/resolve',
        method: 'POST',
        data: {
            resolved_by: resolvedBy,
            resolve_note: resolveNote
        },
        success: function(response) {
            console.log('处理预警成功:', response);
            $('#handleAlertModal').modal('hide');
            showSuccess('预警处理成功');
            // 重新加载列表
            loadAlerts();
        },
        error: function(xhr, status, error) {
            console.error('处理预警失败:', error);
            let errorMsg = '处理失败';
            if (xhr.responseJSON && xhr.responseJSON.detail) {
                errorMsg = xhr.responseJSON.detail;
            }
            showError(errorMsg);
        }
    });
}

// 打开查看预警详情模态框
function openViewAlertModal(alertId) {
    console.log('打开查看预警详情模态框，ID:', alertId);
    
    // 获取预警详情
    $.ajax({
        url: API_BASE + '/alerts/' + alertId,
        method: 'GET',
        success: function(alert) {
            console.log('获取预警详情:', alert);
            
            const statusBadge = getAlertStatusBadge(alert.status);
            const severityBadge = getSeverityBadge(alert.severity);
            const fenceTypeBadge = getFenceTypeBadge(alert.fence_type);
            
            const detailHtml = `
                <div class="row">
                    <div class="col-md-6">
                        <h6 class="text-primary mb-3"><i class="fas fa-info-circle mr-2"></i>基本信息</h6>
                        <p><strong>预警ID：</strong>${alert.id}</p>
                        <p><strong>预警类型：</strong>${escapeHtml(alert.alert_type || '越界预警')}</p>
                        <p><strong>严重程度：</strong>${severityBadge}</p>
                        <p><strong>状态：</strong>${statusBadge}</p>
                    </div>
                    <div class="col-md-6">
                        <h6 class="text-primary mb-3"><i class="fas fa-bus mr-2"></i>车辆信息</h6>
                        <p><strong>车牌号：</strong>${escapeHtml(alert.plate_number || '-')}</p>
                        <p><strong>围栏名称：</strong>${escapeHtml(alert.fence_name || '-')}</p>
                        <p><strong>围栏类型：</strong>${fenceTypeBadge}</p>
                        <p><strong>越界次数：</strong><span class="text-danger font-weight-bold">${alert.violation_count || 1}</span></p>
                    </div>
                </div>
                <hr>
                <div class="row">
                    <div class="col-md-6">
                        <h6 class="text-primary mb-3"><i class="fas fa-map-marker-alt mr-2"></i>位置信息</h6>
                        <p><strong>纬度：</strong><span class="text-monospace">${alert.latitude?.toFixed(6) || '-'}</span></p>
                        <p><strong>经度：</strong><span class="text-monospace">${alert.longitude?.toFixed(6) || '-'}</span></p>
                        <p><strong>速度：</strong>${alert.speed?.toFixed(1) || '-'} km/h</p>
                        <p><strong>方向：</strong>${alert.direction || '-'}°</p>
                    </div>
                    <div class="col-md-6">
                        <h6 class="text-primary mb-3"><i class="fas fa-clock mr-2"></i>时间信息</h6>
                        <p><strong>预警时间：</strong>${formatDateTime(alert.created_at)}</p>
                        <p><strong>处理人：</strong>${escapeHtml(alert.resolved_by || '-')}</p>
                        <p><strong>处理时间：</strong>${formatDateTime(alert.resolved_at)}</p>
                    </div>
                </div>
                <hr>
                <h6 class="text-primary mb-3"><i class="fas fa-comment mr-2"></i>预警消息</h6>
                <div class="alert alert-info">
                    <p class="mb-0">${escapeHtml(alert.message || '暂无消息')}</p>
                </div>
                ${alert.resolve_note ? `
                <h6 class="text-primary mb-3 mt-3"><i class="fas fa-edit mr-2"></i>处理备注</h6>
                <div class="alert alert-success">
                    <p class="mb-0">${escapeHtml(alert.resolve_note)}</p>
                </div>
                ` : ''}
            `;
            $('#view-alert-detail').html(detailHtml);
            
            // 显示模态框
            $('#viewAlertModal').modal('show');
        },
        error: function(xhr, status, error) {
            console.error('获取预警详情失败:', error);
            showError('获取预警详情失败');
        }
    });
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
            minute: '2-digit',
            second: '2-digit'
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
    // 简单的alert显示
    alert('✓ ' + message);
}

// 显示错误消息
function showError(message) {
    // 简单的alert显示
    alert('✗ ' + message);
}
