/*
 * 仪表盘页面JavaScript
 * 与index.html模板匹配
 */

// 全局变量
const REFRESH_INTERVAL = 3000; // 3秒刷新一次
let refreshTimer = null;

// API基础地址
const API_BASE = '/api';

// 页面加载完成后执行
$(document).ready(function() {
    console.log('仪表盘页面加载完成');
    
    // 加载统计数据
    loadDashboardStats();
    
    // 加载实时车辆状态
    loadRealtimeVehicles();
    
    // 加载最新预警
    loadRecentAlerts();
    
    // 设置导航栏活动项
    $('#nav-dashboard').addClass('active');
    
    // 启动自动刷新
    startAutoRefresh();
});

// 页面离开时停止刷新
$(window).on('beforeunload', function() {
    stopAutoRefresh();
});

// 刷新仪表盘
function refreshDashboard() {
    console.log('手动刷新仪表盘');
    loadDashboardStats();
    loadRealtimeVehicles();
    loadRecentAlerts();
}

// 启动自动刷新
function startAutoRefresh() {
    if (refreshTimer) {
        clearInterval(refreshTimer);
    }
    refreshTimer = setInterval(function() {
        // 定期刷新实时车辆状态
        loadRealtimeVehicles();
    }, REFRESH_INTERVAL);
    
    console.log('自动刷新已启动，间隔:', REFRESH_INTERVAL + 'ms');
}

// 停止自动刷新
function stopAutoRefresh() {
    if (refreshTimer) {
        clearInterval(refreshTimer);
        refreshTimer = null;
    }
}

// 加载仪表盘统计数据
function loadDashboardStats() {
    console.log('加载仪表盘统计数据');
    
    $.ajax({
        url: API_BASE + '/dashboard/stats',
        method: 'GET',
        dataType: 'json',
        success: function(response) {
            console.log('统计数据响应:', response);
            renderDashboardStats(response);
        },
        error: function(xhr, status, error) {
            console.error('加载统计数据失败:', error);
            // 显示默认值
            $('#stat-total-vehicles').text('0');
            $('#stat-online-vehicles').text('0');
            $('#stat-running-vehicles').text('0');
            $('#stat-active-geofences').text('0');
            $('#stat-active-alerts').text('0');
            $('#stat-today-trajectory').text('0');
        }
    });
}

// 渲染统计数据
function renderDashboardStats(stats) {
    const vehicleStats = stats.vehicle_stats || {};
    const alertStats = stats.alert_stats || {};
    const fenceStats = stats.fence_stats || {};
    const trajectoryStats = stats.trajectory_stats || {};
    
    // 更新统计数字
    $('#stat-total-vehicles').text(vehicleStats.total || 0);
    $('#stat-online-vehicles').text(vehicleStats.online || 0);
    $('#stat-running-vehicles').text(vehicleStats.running || 0);
    $('#stat-active-geofences').text(fenceStats.total || 0);
    $('#stat-active-alerts').text(alertStats.active || 0);
    $('#stat-today-trajectory').text(trajectoryStats.today || 0);
    
    // 渲染图表
    renderVehicleStatusChart(vehicleStats);
}

// 渲染车辆状态图表
function renderVehicleStatusChart(vehicleStats) {
    const ctx = document.getElementById('vehicleStatusChart');
    if (!ctx || !window.Chart) {
        console.log('Chart.js不可用，跳过图表渲染');
        return;
    }
    
    // 准备数据
    const online = vehicleStats.online || 0;
    const running = vehicleStats.running || 0;
    const offline = (vehicleStats.total || 0) - online;
    const idle = online - running;
    
    // 销毁旧图表
    if (window.vehicleStatusChartInstance) {
        window.vehicleStatusChartInstance.destroy();
    }
    
    // 创建新图表
    window.vehicleStatusChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['运行中', '待机', '离线'],
            datasets: [{
                data: [running, idle, offline],
                backgroundColor: [
                    '#ffc107',  // warning - 运行中
                    '#28a745',  // success - 待机/在线
                    '#6c757d'   // secondary - 离线
                ],
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        font: {
                            size: 14
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.label + ': ' + context.raw + ' 辆';
                        }
                    }
                }
            }
        }
    });
}

// 加载实时车辆状态
function loadRealtimeVehicles() {
    console.log('加载实时车辆状态');
    
    $.ajax({
        url: API_BASE + '/realtime/locations',
        method: 'GET',
        dataType: 'json',
        success: function(response) {
            console.log('实时车辆响应:', response);
            renderRealtimeVehicles(response);
        },
        error: function(xhr, status, error) {
            console.error('加载实时车辆状态失败:', error);
            showRealtimeVehiclesEmpty();
        }
    });
}

// 渲染实时车辆状态
function renderRealtimeVehicles(vehicles) {
    const tbody = $('#realtime-vehicles-table tbody');
    tbody.empty();
    
    if (!vehicles || vehicles.length === 0) {
        showRealtimeVehiclesEmpty();
        return;
    }
    
    vehicles.forEach(function(vehicle) {
        const statusBadge = getStatusBadge(vehicle.status);
        const speed = vehicle.speed !== null && vehicle.speed !== undefined 
            ? vehicle.speed.toFixed(1) + ' km/h' 
            : '-';
        const lastUpdate = formatDateTime(vehicle.location_time);
        
        const row = `
            <tr>
                <td><strong>${escapeHtml(vehicle.plate_number || '-')}</strong></td>
                <td>${escapeHtml(vehicle.driver_name || '-')}</td>
                <td>${statusBadge}</td>
                <td>${speed}</td>
                <td class="text-muted small">${lastUpdate}</td>
            </tr>
        `;
        tbody.append(row);
    });
}

// 显示实时车辆空状态
function showRealtimeVehiclesEmpty() {
    const tbody = $('#realtime-vehicles-table tbody');
    tbody.html(`
        <tr>
            <td colspan="5" class="text-center text-muted">
                <i class="fas fa-bus mr-2"></i>暂无车辆数据
            </td>
        </tr>
    `);
}

// 加载最新预警
function loadRecentAlerts() {
    console.log('加载最新预警');
    
    $.ajax({
        url: API_BASE + '/alerts?page_size=10',
        method: 'GET',
        dataType: 'json',
        success: function(response) {
            console.log('最新预警响应:', response);
            renderRecentAlerts(response.data || []);
        },
        error: function(xhr, status, error) {
            console.error('加载最新预警失败:', error);
            showRecentAlertsEmpty();
        }
    });
}

// 渲染最新预警
function renderRecentAlerts(alerts) {
    const tbody = $('#recent-alerts-table tbody');
    tbody.empty();
    
    if (!alerts || alerts.length === 0) {
        showRecentAlertsEmpty();
        return;
    }
    
    alerts.forEach(function(alert) {
        const alertTime = formatDateTime(alert.created_at);
        const statusBadge = getAlertStatusBadge(alert.status);
        const severityBadge = getSeverityBadge(alert.severity);
        const fenceTypeBadge = getFenceTypeBadge(alert.fence_type);
        
        const row = `
            <tr class="${alert.status === 'active' ? 'table-warning' : ''}">
                <td class="text-muted small">${alertTime}</td>
                <td>${escapeHtml(alert.fence_name || '-')}</td>
                <td>${fenceTypeBadge}</td>
                <td><strong>${escapeHtml(alert.plate_number || '-')}</strong></td>
                <td><span class="text-danger font-weight-bold">${alert.violation_count || 1}</span></td>
                <td>${severityBadge}</td>
                <td>${statusBadge}</td>
                <td>
                    <button class="btn btn-sm btn-outline-info" title="查看详情" onclick="viewAlert(${alert.id})">
                        <i class="fas fa-eye"></i>
                    </button>
                    ${alert.status === 'active' ? `
                    <button class="btn btn-sm btn-outline-primary" title="处理" onclick="handleAlert(${alert.id})">
                        <i class="fas fa-edit"></i>
                    </button>
                    ` : ''}
                </td>
            </tr>
        `;
        tbody.append(row);
    });
}

// 显示最新预警空状态
function showRecentAlertsEmpty() {
    const tbody = $('#recent-alerts-table tbody');
    tbody.html(`
        <tr>
            <td colspan="8" class="text-center text-muted">
                <i class="fas fa-check-circle mr-2 text-success"></i>暂无预警信息
            </td>
        </tr>
    `);
}

// 查看预警详情
function viewAlert(alertId) {
    console.log('查看预警详情，ID:', alertId);
    // 跳转到预警管理页面
    window.location.href = '/alerts';
}

// 处理预警
function handleAlert(alertId) {
    console.log('处理预警，ID:', alertId);
    // 跳转到预警管理页面
    window.location.href = '/alerts';
}

// 获取状态标签HTML
function getStatusBadge(status) {
    const statusMap = {
        'online': { class: 'badge-success', text: '在线' },
        'offline': { class: 'badge-danger', text: '离线' },
        'running': { class: 'badge-warning', text: '运行中' },
        'idle': { class: 'badge-secondary', text: '待机' },
        'maintenance': { class: 'badge-info', text: '维护中' }
    };
    
    const s = statusMap[status] || { class: 'badge-secondary', text: status };
    return `<span class="badge ${s.class}">${s.text}</span>`;
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

// 格式化日期时间
function formatDateTime(dateTimeStr) {
    if (!dateTimeStr) return '-';
    try {
        const date = new Date(dateTimeStr);
        return date.toLocaleString('zh-CN', {
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
