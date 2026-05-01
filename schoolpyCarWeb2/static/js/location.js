/*
 * 实时定位页面JavaScript
 * 与location.html模板匹配
 */

// 全局变量
const REFRESH_INTERVAL = 3000; // 3秒刷新一次
let refreshTimer = null;
let isAutoRefresh = true;
let selectedVehicleId = '';
let filterStatus = '';
let logLineCount = 0;
const MAX_LOG_LINES = 100;

// API基础地址
const API_BASE = '/api';

// 页面加载完成后执行
$(document).ready(function() {
    console.log('实时定位页面加载完成');
    
    // 设置导航栏活动项
    $('#nav-location').addClass('active');
    
    // 初始化车辆下拉框
    loadVehicleSelect();
    
    // 加载实时定位数据
    loadRealtimeLocations();
    
    // 启动自动刷新
    startAutoRefresh();
    
    // 绑定事件
    bindEvents();
    
    // 添加启动日志
    addGpsLog('系统启动，等待GPS数据...', 'info');
});

// 页面离开时停止刷新
$(window).on('beforeunload', function() {
    stopAutoRefresh();
});

// 绑定事件
function bindEvents() {
    // 查询表单提交
    $('#queryForm').on('submit', function(e) {
        e.preventDefault();
        applyFilters();
    });
}

// 切换自动刷新
function toggleAutoRefresh() {
    isAutoRefresh = !isAutoRefresh;
    
    const refreshIcon = $('#refresh-icon');
    const refreshText = $('#refresh-text');
    const toggleBtn = $('#toggle-refresh');
    
    if (isAutoRefresh) {
        // 启动刷新
        refreshIcon.removeClass('fa-play').addClass('fa-pause');
        refreshText.text('暂停刷新');
        toggleBtn.removeClass('btn-outline-success').addClass('btn-outline-secondary');
        startAutoRefresh();
        addGpsLog('自动刷新已启动', 'info');
    } else {
        // 暂停刷新
        refreshIcon.removeClass('fa-pause').addClass('fa-play');
        refreshText.text('继续刷新');
        toggleBtn.removeClass('btn-outline-secondary').addClass('btn-outline-success');
        stopAutoRefresh();
        addGpsLog('自动刷新已暂停', 'warning');
    }
}

// 启动自动刷新
function startAutoRefresh() {
    if (refreshTimer) {
        clearInterval(refreshTimer);
    }
    refreshTimer = setInterval(function() {
        loadRealtimeLocations();
    }, REFRESH_INTERVAL);
}

// 停止自动刷新
function stopAutoRefresh() {
    if (refreshTimer) {
        clearInterval(refreshTimer);
        refreshTimer = null;
    }
}

// 加载车辆下拉框
function loadVehicleSelect() {
    $.ajax({
        url: API_BASE + '/vehicles?page_size=100',
        method: 'GET',
        dataType: 'json',
        success: function(response) {
            const vehicles = response.data || [];
            const select = $('#select-vehicle');
            
            // 清空现有选项（保留请选择）
            select.find('option:not(:first)').remove();
            
            // 添加车辆选项
            vehicles.forEach(function(vehicle) {
                select.append($('<option>', {
                    value: vehicle.id,
                    text: vehicle.plate_number + ' - ' + (vehicle.driver_name || '未分配')
                }));
            });
        },
        error: function(xhr, status, error) {
            console.error('加载车辆列表失败:', error);
        }
    });
}

// 应用筛选
function applyFilters() {
    selectedVehicleId = $('#select-vehicle').val();
    filterStatus = $('#filter-vehicle-status').val();
    
    console.log('应用筛选，车辆ID:', selectedVehicleId, '状态:', filterStatus);
    
    addGpsLog('筛选条件已更新', 'info');
    loadRealtimeLocations();
}

// 加载实时定位数据
function loadRealtimeLocations() {
    console.log('加载实时定位数据');
    
    let url = API_BASE + '/realtime/locations';
    let urlParams = {};
    
    if (filterStatus) {
        urlParams.status = filterStatus;
    }
    
    $.ajax({
        url: url,
        method: 'GET',
        data: urlParams,
        dataType: 'json',
        success: function(response) {
            console.log('实时定位响应:', response);
            
            // 筛选数据
            let locations = response;
            if (!Array.isArray(locations)) {
                locations = locations.data || [];
            }
            
            // 根据选中的车辆筛选
            if (selectedVehicleId) {
                locations = locations.filter(l => l.vehicle_id == selectedVehicleId);
            }
            
            renderRealtimeLocations(locations);
            renderVehicleStatusList(locations);
            updateLastUpdateTime();
        },
        error: function(xhr, status, error) {
            console.error('加载实时定位数据失败:', error);
            addGpsLog('加载定位数据失败: ' + error, 'error');
        }
    });
}

// 渲染实时定位表格
function renderRealtimeLocations(locations) {
    const tbody = $('#location-data-table tbody');
    tbody.empty();
    
    if (!locations || locations.length === 0) {
        tbody.html(`
            <tr>
                <td colspan="12" class="text-center text-muted">
                    <i class="fas fa-location-arrow mr-2"></i>暂无定位数据
                </td>
            </tr>
        `);
        return;
    }
    
    locations.forEach(function(location) {
        const statusBadge = getStatusBadge(location.status);
        const speed = location.speed !== null && location.speed !== undefined 
            ? location.speed.toFixed(1) + ' km/h' 
            : '-';
        const altitude = location.altitude !== null && location.altitude !== undefined 
            ? location.altitude.toFixed(1) + ' m' 
            : '-';
        const direction = location.direction || 0;
        const satellites = location.satellites || '-';
        const locationTime = formatDateTime(location.location_time);
        
        const row = `
            <tr>
                <td><strong>${escapeHtml(location.plate_number || '-')}</strong></td>
                <td>${escapeHtml(location.driver_name || '-')}</td>
                <td class="text-monospace">${location.latitude?.toFixed(6) || '-'}</td>
                <td class="text-monospace">${location.longitude?.toFixed(6) || '-'}</td>
                <td>${altitude}</td>
                <td>${speed}</td>
                <td>${direction}°</td>
                <td>${escapeHtml(location.data_source || 'GPS')}</td>
                <td>${satellites}</td>
                <td><span class="text-success">良好</span></td>
                <td>${statusBadge}</td>
                <td class="text-muted small">${locationTime}</td>
            </tr>
        `;
        tbody.append(row);
        
        // 添加日志
        addGpsLog(`车辆 ${location.plate_number} - 位置: ${location.latitude?.toFixed(4)}, ${location.longitude?.toFixed(4)}, 速度: ${location.speed || 0} km/h`, 'success');
    });
}

// 渲染车辆状态列表
function renderVehicleStatusList(locations) {
    const listContainer = $('#vehicle-status-list');
    listContainer.empty();
    
    if (!locations || locations.length === 0) {
        listContainer.html(`
            <div class="list-group-item text-center text-muted">
                <i class="fas fa-bus mr-2"></i>暂无车辆数据
            </div>
        `);
        $('#online-count').text('0 辆在线');
        return;
    }
    
    // 更新在线车辆数
    const onlineCount = locations.filter(l => l.status === 'online' || l.status === 'running').length;
    $('#online-count').text(onlineCount + ' 辆在线');
    
    locations.forEach(function(location) {
        const statusBadge = getStatusBadge(location.status);
        const speed = location.speed !== null && location.speed !== undefined 
            ? location.speed.toFixed(1) + ' km/h' 
            : '-';
        
        const item = `
            <div class="list-group-item">
                <div class="d-flex w-100 justify-content-between">
                    <h6 class="mb-1">
                        <i class="fas fa-bus mr-2"></i>
                        <strong>${escapeHtml(location.plate_number || '-')}</strong>
                    </h6>
                    ${statusBadge}
                </div>
                <p class="mb-1">
                    <i class="fas fa-user mr-1"></i> ${escapeHtml(location.driver_name || '未分配')}
                    <span class="mx-2">|</span>
                    <i class="fas fa-tachometer-alt mr-1"></i> ${speed}
                </p>
                <small class="text-muted">
                    <i class="fas fa-map-marker-alt mr-1"></i>
                    ${location.latitude?.toFixed(4) || '-'}, ${location.longitude?.toFixed(4) || '-'}
                </small>
            </div>
        `;
        listContainer.append(item);
    });
}

// 更新最后更新时间
function updateLastUpdateTime() {
    const now = new Date();
    const timeStr = now.toLocaleString('zh-CN', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
    $('#last-update-time').text(timeStr);
}

// 清空日志
function clearLogs() {
    $('#gps-log-container').html(`
        <div class="text-success">
            <i class="fas fa-check-circle mr-1"></i>[系统] 日志已清空
        </div>
    `);
    logLineCount = 0;
}

// 添加GPS日志
function addGpsLog(message, type) {
    const container = $('#gps-log-container');
    const timestamp = new Date().toLocaleTimeString('zh-CN', {
        hour12: false,
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
    
    const typeClasses = {
        'success': 'text-success',
        'error': 'text-danger',
        'warning': 'text-warning',
        'info': 'text-info'
    };
    
    const typeIcons = {
        'success': 'check-circle',
        'error': 'times-circle',
        'warning': 'exclamation-triangle',
        'info': 'info-circle'
    };
    
    const cssClass = typeClasses[type] || 'text-secondary';
    const icon = typeIcons[type] || 'circle';
    
    const logLine = `
        <div class="${cssClass}">
            <i class="fas fa-${icon} mr-1"></i>[${timestamp}] ${message}
        </div>
    `;
    
    // 追加到容器
    container.append(logLine);
    
    // 滚动到底部
    container.scrollTop(container[0].scrollHeight);
    
    // 限制行数
    logLineCount++;
    if (logLineCount > MAX_LOG_LINES) {
        container.find('div').first().remove();
        logLineCount--;
    }
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
