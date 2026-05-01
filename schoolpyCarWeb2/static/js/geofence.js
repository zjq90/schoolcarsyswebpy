/*
 * 电子围栏页面JavaScript
 * 与模板geofence.html匹配
 */

// 全局变量
let currentPage = 1;
const pageSize = 10;
let currentFilterType = '';

// API基础地址
const API_BASE = '/api';

// 页面加载完成后执行
$(document).ready(function() {
    console.log('电子围栏页面加载完成');
    
    // 加载围栏列表
    loadGeofences();
    
    // 绑定事件
    bindEvents();
    
    // 设置导航栏活动项
    $('#nav-geofence').addClass('active');
});

// 绑定事件
function bindEvents() {
    // 类型筛选变化
    $('#filter-fence-type').on('change', function() {
        currentFilterType = $(this).val();
        currentPage = 1;
        loadGeofences();
    });
    
    // 添加围栏表单提交
    $('#addGeofenceForm').on('submit', function(e) {
        e.preventDefault();
        submitAddGeofence();
    });
    
    // 编辑围栏表单提交
    $('#editGeofenceForm').on('submit', function(e) {
        e.preventDefault();
        submitEditGeofence();
    });
}

// 加载围栏列表
function loadGeofences() {
    console.log('加载围栏列表，页码:', currentPage);
    
    // 构建URL参数
    let params = {
        page: currentPage,
        page_size: pageSize
    };
    
    if (currentFilterType) {
        params.fence_type = currentFilterType;
    }
    
    // 显示加载中
    showLoadingState();
    
    // 发送AJAX请求
    $.ajax({
        url: API_BASE + '/geofences',
        method: 'GET',
        data: params,
        dataType: 'json',
        success: function(response) {
            console.log('围栏列表响应:', response);
            renderGeofences(response.data || []);
            updateFenceStats(response.data || []);
        },
        error: function(xhr, status, error) {
            console.error('加载围栏列表失败:', error);
            showError('加载围栏列表失败: ' + error);
            showEmptyState();
        }
    });
}

// 显示加载状态
function showLoadingState() {
    $('#geofence-table tbody').html(`
        <tr>
            <td colspan="10" class="text-center text-muted py-5">
                <i class="fas fa-spinner fa-spin mr-2"></i>加载中...
            </td>
        </tr>
    `);
}

// 显示空状态
function showEmptyState() {
    $('#geofence-table tbody').html(`
        <tr>
            <td colspan="10" class="text-center text-muted py-5">
                <i class="fas fa-map-marked-alt fa-3x mb-3"></i>
                <h5>暂无围栏数据</h5>
                <p class="mb-0">点击"添加围栏"按钮创建新围栏</p>
            </td>
        </tr>
    `);
}

// 渲染围栏列表
function renderGeofences(fences) {
    const tbody = $('#geofence-table tbody');
    tbody.empty();
    
    if (!fences || fences.length === 0) {
        showEmptyState();
        return;
    }
    
    fences.forEach(function(fence, index) {
        const rowIndex = (currentPage - 1) * pageSize + index + 1;
        const typeBadge = getFenceTypeBadge(fence.fence_type);
        const statusBadge = fence.is_active 
            ? '<span class="badge badge-success">启用</span>' 
            : '<span class="badge badge-secondary">禁用</span>';
        
        const row = `
            <tr>
                <td>${rowIndex}</td>
                <td><strong>${escapeHtml(fence.name)}</strong></td>
                <td>${typeBadge}</td>
                <td>
                    <small class="text-monospace">
                        纬度: ${fence.center_lat?.toFixed(6) || '-'}<br>
                        经度: ${fence.center_lng?.toFixed(6) || '-'}
                    </small>
                </td>
                <td>${formatDistance(fence.radius)}</td>
                <td>${fence.threshold || 3}次</td>
                <td>${statusBadge}</td>
                <td class="text-wrap" style="max-width: 200px;">${escapeHtml(fence.description || '-')}</td>
                <td>${formatDateTime(fence.created_at)}</td>
                <td>
                    <button class="btn btn-sm btn-outline-info" title="编辑" onclick="openEditGeofenceModal(${fence.id})">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-sm ${fence.is_active ? 'btn-outline-warning' : 'btn-outline-success'}" 
                            title="${fence.is_active ? '禁用' : '启用'}" 
                            onclick="toggleFenceStatus(${fence.id}, ${!fence.is_active})">
                        <i class="fas fa-${fence.is_active ? 'pause' : 'play'}"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger" title="删除" onclick="openDeleteGeofenceModal(${fence.id}, '${escapeHtml(fence.name)}')">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            </tr>
        `;
        tbody.append(row);
    });
}

// 更新围栏统计
function updateFenceStats(fences) {
    if (!fences) return;
    
    const activeCount = fences.filter(f => f.is_active).length;
    const inactiveCount = fences.filter(f => !f.is_active).length;
    
    $('#stat-active-fences').text(activeCount);
    $('#stat-inactive-fences').text(inactiveCount);
    
    // 更新图表（简单模拟）
    renderFenceChart(fences);
}

// 渲染围栏类型图表
function renderFenceChart(fences) {
    if (!fences || fences.length === 0) return;
    
    const typeCounts = {
        school: 0,
        danger: 0,
        home: 0,
        other: 0
    };
    
    fences.forEach(f => {
        if (typeCounts.hasOwnProperty(f.fence_type)) {
            typeCounts[f.fence_type]++;
        } else {
            typeCounts.other++;
        }
    });
    
    const ctx = document.getElementById('geofenceTypeChart');
    if (ctx && window.Chart) {
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['学校区域', '危险路段', '家庭区域', '其他区域'],
                datasets: [{
                    data: [typeCounts.school, typeCounts.danger, typeCounts.home, typeCounts.other],
                    backgroundColor: [
                        '#28a745',  // success
                        '#dc3545',  // danger
                        '#17a2b8',  // info
                        '#6c757d'   // secondary
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }
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

// 格式化距离
function formatDistance(distance) {
    if (distance === null || distance === undefined) return '-';
    if (distance >= 1000) {
        return (distance / 1000).toFixed(2) + ' 公里';
    }
    return distance + ' 米';
}

// 切换围栏状态
function toggleFenceStatus(fenceId, isActive) {
    const action = isActive ? '启用' : '禁用';
    console.log(`切换围栏状态，ID: ${fenceId}, 状态: ${isActive ? '启用' : '禁用'}`);
    
    $.ajax({
        url: API_BASE + '/geofences/' + fenceId,
        method: 'PUT',
        contentType: 'application/json',
        data: JSON.stringify({ is_active: isActive }),
        success: function(response) {
            console.log('切换状态成功:', response);
            showSuccess(action + '成功');
            loadGeofences();
        },
        error: function(xhr, status, error) {
            console.error('切换状态失败:', error);
            let errorMsg = action + '失败';
            if (xhr.responseJSON && xhr.responseJSON.detail) {
                errorMsg = xhr.responseJSON.detail;
            }
            showError(errorMsg);
        }
    });
}

// 提交添加围栏表单
function submitAddGeofence() {
    const form = $('#addGeofenceForm');
    
    // 构建数据
    const data = {
        name: form.find('#add-fence-name').val().trim(),
        fence_type: form.find('#add-fence-type').val(),
        center_lat: parseFloat(form.find('#add-fence-lat').val()),
        center_lng: parseFloat(form.find('#add-fence-lng').val()),
        radius: parseInt(form.find('#add-fence-radius').val()) || 500,
        threshold: parseInt(form.find('#add-alert-threshold').val()) || 3,
        description: form.find('#add-fence-desc').val().trim(),
        is_active: form.find('#add-fence-status').val() === 'true'
    };
    
    // 验证必填字段
    if (!data.name) {
        showError('请输入围栏名称');
        return;
    }
    if (!data.fence_type) {
        showError('请选择围栏类型');
        return;
    }
    if (!data.center_lat || isNaN(data.center_lat)) {
        showError('请输入有效的纬度');
        return;
    }
    if (!data.center_lng || isNaN(data.center_lng)) {
        showError('请输入有效的经度');
        return;
    }
    
    console.log('提交添加围栏:', data);
    
    // 发送AJAX请求
    $.ajax({
        url: API_BASE + '/geofences',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function(response) {
            console.log('添加围栏成功:', response);
            $('#addGeofenceModal').modal('hide');
            showSuccess('围栏添加成功');
            // 重置表单
            form[0].reset();
            form.find('#add-fence-status').val('true');
            form.find('#add-alert-threshold').val('3');
            // 重新加载列表
            currentPage = 1;
            loadGeofences();
        },
        error: function(xhr, status, error) {
            console.error('添加围栏失败:', error);
            let errorMsg = '添加失败';
            if (xhr.responseJSON && xhr.responseJSON.detail) {
                errorMsg = xhr.responseJSON.detail;
            }
            showError(errorMsg);
        }
    });
}

// 打开编辑围栏模态框
function openEditGeofenceModal(fenceId) {
    console.log('打开编辑围栏模态框，ID:', fenceId);
    
    // 获取围栏详情
    $.ajax({
        url: API_BASE + '/geofences/' + fenceId,
        method: 'GET',
        success: function(fence) {
            console.log('获取围栏详情:', fence);
            
            // 填充表单
            const form = $('#editGeofenceForm');
            form.find('#edit-fence-id').val(fence.id);
            form.find('#edit-fence-name').val(fence.name);
            form.find('#edit-fence-type').val(fence.fence_type || 'other');
            form.find('#edit-fence-lat').val(fence.center_lat);
            form.find('#edit-fence-lng').val(fence.center_lng);
            form.find('#edit-fence-radius').val(fence.radius || 500);
            form.find('#edit-alert-threshold').val(fence.threshold || 3);
            form.find('#edit-fence-status').val(fence.is_active ? 'true' : 'false');
            form.find('#edit-fence-desc').val(fence.description || '');
            
            // 显示模态框
            $('#editGeofenceModal').modal('show');
        },
        error: function(xhr, status, error) {
            console.error('获取围栏详情失败:', error);
            showError('获取围栏详情失败');
        }
    });
}

// 提交编辑围栏表单
function submitEditGeofence() {
    const form = $('#editGeofenceForm');
    const fenceId = form.find('#edit-fence-id').val();
    
    // 构建数据
    const data = {
        name: form.find('#edit-fence-name').val().trim(),
        fence_type: form.find('#edit-fence-type').val(),
        center_lat: parseFloat(form.find('#edit-fence-lat').val()),
        center_lng: parseFloat(form.find('#edit-fence-lng').val()),
        radius: parseInt(form.find('#edit-fence-radius').val()) || 500,
        threshold: parseInt(form.find('#edit-alert-threshold').val()) || 3,
        description: form.find('#edit-fence-desc').val().trim(),
        is_active: form.find('#edit-fence-status').val() === 'true'
    };
    
    console.log('提交编辑围栏:', data);
    
    // 发送AJAX请求
    $.ajax({
        url: API_BASE + '/geofences/' + fenceId,
        method: 'PUT',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function(response) {
            console.log('编辑围栏成功:', response);
            $('#editGeofenceModal').modal('hide');
            showSuccess('围栏信息更新成功');
            // 重新加载列表
            loadGeofences();
        },
        error: function(xhr, status, error) {
            console.error('编辑围栏失败:', error);
            let errorMsg = '编辑失败';
            if (xhr.responseJSON && xhr.responseJSON.detail) {
                errorMsg = xhr.responseJSON.detail;
            }
            showError(errorMsg);
        }
    });
}

// 打开删除围栏模态框
function openDeleteGeofenceModal(fenceId, fenceName) {
    console.log('打开删除确认模态框，ID:', fenceId, '名称:', fenceName);
    
    $('#delete-fence-id').val(fenceId);
    $('#delete-fence-name').text(fenceName);
    $('#deleteGeofenceModal').modal('show');
}

// 确认删除围栏
function confirmDeleteGeofence() {
    const fenceId = $('#delete-fence-id').val();
    const fenceName = $('#delete-fence-name').text();
    
    console.log('确认删除围栏，ID:', fenceId);
    
    $.ajax({
        url: API_BASE + '/geofences/' + fenceId,
        method: 'DELETE',
        success: function(response) {
            console.log('删除围栏成功:', response);
            $('#deleteGeofenceModal').modal('hide');
            showSuccess('围栏「' + fenceName + '」删除成功');
            // 重新加载列表
            currentPage = 1;
            loadGeofences();
        },
        error: function(xhr, status, error) {
            console.error('删除围栏失败:', error);
            let errorMsg = '删除失败';
            if (xhr.responseJSON && xhr.responseJSON.detail) {
                errorMsg = xhr.responseJSON.detail;
            }
            showError(errorMsg);
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
    // 简单的alert显示
    alert('✓ ' + message);
}

// 显示错误消息
function showError(message) {
    // 简单的alert显示
    alert('✗ ' + message);
}
