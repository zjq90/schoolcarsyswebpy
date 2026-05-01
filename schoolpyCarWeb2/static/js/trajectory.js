/*
 * 历史轨迹页面JavaScript
 * 与trajectory.html模板匹配
 */

// 全局变量
let currentPage = 1;
const pageSize = 20;
let selectedVehicleId = '';
let trajectoryData = [];

// API基础地址
const API_BASE = '/api';

// 页面加载完成后执行
$(document).ready(function() {
    console.log('历史轨迹页面加载完成');
    
    // 设置导航栏活动项
    $('#nav-trajectory').addClass('active');
    
    // 初始化日期
    initDates();
    
    // 初始化车辆下拉框
    loadVehicleSelect();
    
    // 绑定事件
    bindEvents();
    
    // 设置数据保留天数显示
    $('#data-retention-days').text('90');
});

// 绑定事件
function bindEvents() {
    // 查询表单提交
    $('#queryForm').on('submit', function(e) {
        e.preventDefault();
        queryTrajectory();
    });
}

// 初始化日期
function initDates() {
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);
    
    // 设置默认日期
    $('#start-date').val(formatDateForInput(yesterday));
    $('#end-date').val(formatDateForInput(today));
}

// 格式化日期用于input
function formatDateForInput(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
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

// 设置快捷日期
function setQuickDate(days) {
    const endDate = new Date();
    const startDate = new Date();
    startDate.setDate(startDate.getDate() - days + 1);
    
    $('#start-date').val(formatDateForInput(startDate));
    $('#end-date').val(formatDateForInput(endDate));
    
    console.log('设置快捷日期，天数:', days);
}

// 查询轨迹
function queryTrajectory() {
    selectedVehicleId = $('#select-vehicle').val();
    const startDate = $('#start-date').val();
    const endDate = $('#end-date').val();
    
    // 验证
    if (!selectedVehicleId) {
        alert('请选择车辆');
        return;
    }
    if (!startDate) {
        alert('请选择开始日期');
        return;
    }
    if (!endDate) {
        alert('请选择结束日期');
        return;
    }
    
    console.log('查询轨迹，车辆ID:', selectedVehicleId, '开始:', startDate, '结束:', endDate);
    
    // 重置页码
    currentPage = 1;
    
    // 加载轨迹数据
    loadTrajectoryData();
}

// 加载轨迹数据
function loadTrajectoryData() {
    const startDate = $('#start-date').val();
    const endDate = $('#end-date').val();
    
    // 构建参数
    let params = {
        page: currentPage,
        page_size: pageSize
    };
    
    if (startDate) {
        params.start_time = startDate + ' 00:00:00';
    }
    if (endDate) {
        params.end_time = endDate + ' 23:59:59';
    }
    
    // 显示加载状态
    showLoadingState();
    
    $.ajax({
        url: API_BASE + '/trajectory/' + selectedVehicleId,
        method: 'GET',
        data: params,
        dataType: 'json',
        success: function(response) {
            console.log('轨迹数据响应:', response);
            
            trajectoryData = response.data || [];
            
            renderTrajectoryTable(trajectoryData);
            renderTrajectoryPagination(response.page_info || {});
            renderTrajectoryStats(trajectoryData);
            
            // 更新轨迹信息显示
            const vehicleName = $('#select-vehicle option:selected').text();
            $('#trajectory-info').html(`
                <i class="fas fa-bus mr-1"></i>${vehicleName}
                <span class="mx-2">|</span>
                <i class="fas fa-database mr-1"></i>共 ${response.page_info?.total_items || 0} 条记录
            `);
        },
        error: function(xhr, status, error) {
            console.error('加载轨迹数据失败:', error);
            showError('加载轨迹数据失败: ' + error);
        }
    });
}

// 显示加载状态
function showLoadingState() {
    $('#trajectory-table tbody').html(`
        <tr>
            <td colspan="8" class="text-center text-muted">
                <i class="fas fa-spinner fa-spin mr-2"></i>加载中...
            </td>
        </tr>
    `);
}

// 渲染轨迹表格
function renderTrajectoryTable(trajectories) {
    const tbody = $('#trajectory-table tbody');
    tbody.empty();
    
    if (!trajectories || trajectories.length === 0) {
        tbody.html(`
            <tr>
                <td colspan="8" class="text-center text-muted">
                    <i class="fas fa-route mr-2"></i>暂无轨迹数据
                </td>
            </tr>
        `);
        return;
    }
    
    trajectories.forEach(function(trajectory, index) {
        const rowIndex = (currentPage - 1) * pageSize + index + 1;
        const speed = trajectory.speed !== null && trajectory.speed !== undefined 
            ? trajectory.speed.toFixed(1) + ' km/h' 
            : '-';
        const altitude = trajectory.altitude !== null && trajectory.altitude !== undefined 
            ? trajectory.altitude.toFixed(1) + ' m' 
            : '-';
        const direction = trajectory.direction || 0;
        const locationTime = formatDateTime(trajectory.location_time);
        
        const row = `
            <tr>
                <td>${rowIndex}</td>
                <td class="text-muted small">${locationTime}</td>
                <td>${escapeHtml(trajectory.plate_number || '-')}</td>
                <td class="text-monospace">${trajectory.latitude?.toFixed(6) || '-'}</td>
                <td class="text-monospace">${trajectory.longitude?.toFixed(6) || '-'}</td>
                <td>${altitude}</td>
                <td>${speed}</td>
                <td>${direction}°</td>
            </tr>
        `;
        tbody.append(row);
    });
}

// 渲染轨迹分页
function renderTrajectoryPagination(pageInfo) {
    const pagination = $('#trajectory-pagination');
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
    loadTrajectoryData();
    // 滚动到顶部
    $('html, body').animate({ scrollTop: 0 }, 300);
}

// 渲染轨迹统计
function renderTrajectoryStats(trajectories) {
    const statsContainer = $('#trajectory-stats');
    
    if (!trajectories || trajectories.length === 0) {
        statsContainer.html(`
            <div class="text-center text-muted">
                <i class="fas fa-info-circle fa-3x mb-3"></i>
                <p>暂无统计数据</p>
            </div>
        `);
        return;
    }
    
    // 计算统计数据
    let totalSpeed = 0;
    let maxSpeed = 0;
    let validSpeedCount = 0;
    let avgLat = 0;
    let avgLng = 0;
    
    trajectories.forEach(function(t) {
        avgLat += t.latitude || 0;
        avgLng += t.longitude || 0;
        
        if (t.speed !== null && t.speed !== undefined) {
            totalSpeed += t.speed;
            maxSpeed = Math.max(maxSpeed, t.speed);
            validSpeedCount++;
        }
    });
    
    avgLat = avgLat / trajectories.length;
    avgLng = avgLng / trajectories.length;
    
    const avgSpeed = validSpeedCount > 0 ? (totalSpeed / validSpeedCount).toFixed(1) : 0;
    
    statsContainer.html(`
        <div class="row text-center">
            <div class="col-6 mb-4">
                <div class="h4 font-weight-bold text-primary">${trajectories.length}</div>
                <div class="text-muted small">轨迹点数</div>
            </div>
            <div class="col-6 mb-4">
                <div class="h4 font-weight-bold text-success">${avgSpeed} km/h</div>
                <div class="text-muted small">平均速度</div>
            </div>
            <div class="col-6 mb-4">
                <div class="h4 font-weight-bold text-warning">${maxSpeed.toFixed(1)} km/h</div>
                <div class="text-muted small">最高速度</div>
            </div>
            <div class="col-6 mb-4">
                <div class="h4 font-weight-bold text-info">
                    <small class="text-monospace">${avgLat.toFixed(4)}, ${avgLng.toFixed(4)}</small>
                </div>
                <div class="text-muted small">平均位置</div>
            </div>
        </div>
    `);
}

// 导出轨迹
function exportTrajectory() {
    if (!trajectoryData || trajectoryData.length === 0) {
        alert('暂无轨迹数据可导出');
        return;
    }
    
    console.log('导出轨迹数据，数量:', trajectoryData.length);
    
    // 构建CSV内容
    let csv = '序号,记录时间,车牌号,纬度,经度,海拔,速度,方向\n';
    
    trajectoryData.forEach(function(t, index) {
        const rowIndex = (currentPage - 1) * pageSize + index + 1;
        csv += `${rowIndex},`;
        csv += `"${formatDateTime(t.location_time)}",`;
        csv += `"${escapeHtml(t.plate_number || '-')}",`;
        csv += `${t.latitude?.toFixed(6) || ''},`;
        csv += `${t.longitude?.toFixed(6) || ''},`;
        csv += `${t.altitude?.toFixed(1) || ''},`;
        csv += `${t.speed?.toFixed(1) || ''},`;
        csv += `${t.direction || 0}\n`;
    });
    
    // 创建下载链接
    const blob = new Blob(['\ufeff' + csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `轨迹数据_${new Date().toLocaleDateString('zh-CN').replace(/\//g, '-')}.csv`;
    link.click();
    
    alert('✓ 导出成功，共 ' + trajectoryData.length + ' 条记录');
}

// 播放轨迹
function playTrajectory() {
    if (!trajectoryData || trajectoryData.length === 0) {
        alert('请先查询轨迹数据');
        return;
    }
    
    console.log('播放轨迹回放');
    
    // 显示回放控制栏
    $('#replay-card').show();
    
    alert('轨迹回放功能已启动');
}

// 切换回放
function toggleReplay() {
    console.log('切换回放状态');
}

// 停止回放
function stopReplay() {
    console.log('停止回放');
    $('#replay-card').hide();
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

// 显示错误消息
function showError(message) {
    alert('✗ ' + message);
}
