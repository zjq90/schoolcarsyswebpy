/*
 * 车辆管理页面JavaScript
 * 与模板vehicles.html匹配
 */

// 全局变量
let currentPage = 1;
const pageSize = 10;
let currentFilterStatus = '';
let currentSearchKeyword = '';

// API基础地址
const API_BASE = '/api';

// 页面加载完成后执行
$(document).ready(function() {
    console.log('车辆管理页面加载完成');
    
    // 加载车辆列表
    loadVehicles();
    
    // 绑定事件
    bindEvents();
    
    // 设置导航栏活动项
    $('#nav-vehicles').addClass('active');
});

// 绑定事件
function bindEvents() {
    // 状态筛选变化
    $('#filter-status').on('change', function() {
        currentFilterStatus = $(this).val();
        currentPage = 1;
        loadVehicles();
    });
    
    // 搜索按钮点击
    $('#search-keyword').on('keypress', function(e) {
        if (e.which === 13) {
            searchVehicles();
        }
    });
    
    // 添加车辆表单提交
    $('#addVehicleForm').on('submit', function(e) {
        e.preventDefault();
        submitAddVehicle();
    });
    
    // 编辑车辆表单提交
    $('#editVehicleForm').on('submit', function(e) {
        e.preventDefault();
        submitEditVehicle();
    });
}

// 搜索车辆
function searchVehicles() {
    currentSearchKeyword = $('#search-keyword').val().trim();
    currentPage = 1;
    loadVehicles();
}

// 加载车辆列表
function loadVehicles() {
    console.log('加载车辆列表，页码:', currentPage);
    
    // 构建URL参数
    let params = {
        page: currentPage,
        page_size: pageSize
    };
    
    if (currentFilterStatus) {
        params.status = currentFilterStatus;
    }
    
    if (currentSearchKeyword) {
        params.keyword = currentSearchKeyword;
    }
    
    // 显示加载中
    showLoadingState();
    
    // 发送AJAX请求
    $.ajax({
        url: API_BASE + '/vehicles',
        method: 'GET',
        data: params,
        dataType: 'json',
        success: function(response) {
            console.log('车辆列表响应:', response);
            renderVehicles(response.data || []);
            renderPagination(response.page_info || {});
            $('#vehicle-count').text(response.page_info?.total_items || 0);
        },
        error: function(xhr, status, error) {
            console.error('加载车辆列表失败:', error);
            showError('加载车辆列表失败: ' + error);
            showEmptyState();
        }
    });
}

// 显示加载状态
function showLoadingState() {
    $('#vehicles-table tbody').html(`
        <tr>
            <td colspan="10" class="text-center text-muted py-5">
                <i class="fas fa-spinner fa-spin mr-2"></i>加载中...
            </td>
        </tr>
    `);
}

// 显示空状态
function showEmptyState() {
    $('#vehicles-table tbody').html(`
        <tr>
            <td colspan="10" class="text-center text-muted py-5">
                <i class="fas fa-bus fa-3x mb-3"></i>
                <h5>暂无车辆数据</h5>
                <p class="mb-0">点击"添加车辆"按钮创建新车辆</p>
            </td>
        </tr>
    `);
    $('#pagination').empty();
}

// 渲染车辆列表
function renderVehicles(vehicles) {
    const tbody = $('#vehicles-table tbody');
    tbody.empty();
    
    if (!vehicles || vehicles.length === 0) {
        showEmptyState();
        return;
    }
    
    vehicles.forEach(function(vehicle, index) {
        const rowIndex = (currentPage - 1) * pageSize + index + 1;
        const statusBadge = getStatusBadge(vehicle.status);
        
        const row = `
            <tr>
                <td>${rowIndex}</td>
                <td><strong>${escapeHtml(vehicle.plate_number)}</strong></td>
                <td>${escapeHtml(vehicle.vehicle_type || vehicle.vehicle_model || '-')}</td>
                <td>${vehicle.capacity || 0}人</td>
                <td>${escapeHtml(vehicle.driver_name || '-')}</td>
                <td>${escapeHtml(vehicle.driver_phone || '-')}</td>
                <td>${statusBadge}</td>
                <td>${escapeHtml(vehicle.school || '-')}</td>
                <td>${formatDateTime(vehicle.created_at)}</td>
                <td>
                    <button class="btn btn-sm btn-outline-info" title="编辑" onclick="openEditVehicleModal(${vehicle.id})">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger" title="删除" onclick="openDeleteVehicleModal(${vehicle.id}, '${escapeHtml(vehicle.plate_number)}')">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            </tr>
        `;
        tbody.append(row);
    });
}

// 渲染分页
function renderPagination(pageInfo) {
    const pagination = $('#pagination');
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
    loadVehicles();
    // 滚动到顶部
    $('html, body').animate({ scrollTop: 0 }, 300);
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

// 提交添加车辆表单
function submitAddVehicle() {
    const form = $('#addVehicleForm');
    
    // 构建数据
    const data = {
        plate_number: form.find('#add-plate-number').val().trim(),
        vehicle_type: form.find('#add-vehicle-type').val(),
        capacity: parseInt(form.find('#add-capacity').val()) || 45,
        school: form.find('#add-school').val().trim(),
        driver_name: form.find('#add-driver-name').val().trim(),
        driver_phone: form.find('#add-driver-phone').val().trim(),
        status: form.find('#add-status').val()
    };
    
    // 验证必填字段
    if (!data.plate_number) {
        showError('请输入车牌号');
        return;
    }
    if (!data.vehicle_type) {
        showError('请选择车辆类型');
        return;
    }
    if (!data.school) {
        showError('请输入所属学校');
        return;
    }
    if (!data.driver_name) {
        showError('请输入司机姓名');
        return;
    }
    if (!data.driver_phone) {
        showError('请输入司机电话');
        return;
    }
    
    console.log('提交添加车辆:', data);
    
    // 发送AJAX请求
    $.ajax({
        url: API_BASE + '/vehicles',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function(response) {
            console.log('添加车辆成功:', response);
            $('#addVehicleModal').modal('hide');
            showSuccess('车辆添加成功');
            // 重置表单
            form[0].reset();
            // 重新加载列表
            currentPage = 1;
            loadVehicles();
        },
        error: function(xhr, status, error) {
            console.error('添加车辆失败:', error);
            let errorMsg = '添加失败';
            if (xhr.responseJSON && xhr.responseJSON.detail) {
                errorMsg = xhr.responseJSON.detail;
            }
            showError(errorMsg);
        }
    });
}

// 打开编辑车辆模态框
function openEditVehicleModal(vehicleId) {
    console.log('打开编辑车辆模态框，ID:', vehicleId);
    
    // 获取车辆详情
    $.ajax({
        url: API_BASE + '/vehicles/' + vehicleId,
        method: 'GET',
        success: function(vehicle) {
            console.log('获取车辆详情:', vehicle);
            
            // 填充表单
            const form = $('#editVehicleForm');
            form.find('#edit-vehicle-id').val(vehicle.id);
            form.find('#edit-plate-number').val(vehicle.plate_number);
            form.find('#edit-vehicle-type').val(vehicle.vehicle_type || vehicle.vehicle_model || '中型校车');
            form.find('#edit-capacity').val(vehicle.capacity || 45);
            form.find('#edit-school').val(vehicle.school || '');
            form.find('#edit-driver-name').val(vehicle.driver_name || '');
            form.find('#edit-driver-phone').val(vehicle.driver_phone || '');
            form.find('#edit-status').val(vehicle.status || 'online');
            
            // 显示模态框
            $('#editVehicleModal').modal('show');
        },
        error: function(xhr, status, error) {
            console.error('获取车辆详情失败:', error);
            showError('获取车辆详情失败');
        }
    });
}

// 提交编辑车辆表单
function submitEditVehicle() {
    const form = $('#editVehicleForm');
    const vehicleId = form.find('#edit-vehicle-id').val();
    
    // 构建数据
    const data = {
        plate_number: form.find('#edit-plate-number').val().trim(),
        vehicle_type: form.find('#edit-vehicle-type').val(),
        capacity: parseInt(form.find('#edit-capacity').val()) || 45,
        school: form.find('#edit-school').val().trim(),
        driver_name: form.find('#edit-driver-name').val().trim(),
        driver_phone: form.find('#edit-driver-phone').val().trim(),
        status: form.find('#edit-status').val()
    };
    
    console.log('提交编辑车辆:', data);
    
    // 发送AJAX请求
    $.ajax({
        url: API_BASE + '/vehicles/' + vehicleId,
        method: 'PUT',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function(response) {
            console.log('编辑车辆成功:', response);
            $('#editVehicleModal').modal('hide');
            showSuccess('车辆信息更新成功');
            // 重新加载列表
            loadVehicles();
        },
        error: function(xhr, status, error) {
            console.error('编辑车辆失败:', error);
            let errorMsg = '编辑失败';
            if (xhr.responseJSON && xhr.responseJSON.detail) {
                errorMsg = xhr.responseJSON.detail;
            }
            showError(errorMsg);
        }
    });
}

// 打开删除车辆模态框
function openDeleteVehicleModal(vehicleId, plateNumber) {
    console.log('打开删除确认模态框，ID:', vehicleId, '车牌:', plateNumber);
    
    $('#delete-vehicle-id').val(vehicleId);
    $('#delete-vehicle-name').text(plateNumber);
    $('#deleteVehicleModal').modal('show');
}

// 确认删除车辆
function confirmDeleteVehicle() {
    const vehicleId = $('#delete-vehicle-id').val();
    const plateNumber = $('#delete-vehicle-name').text();
    
    console.log('确认删除车辆，ID:', vehicleId);
    
    $.ajax({
        url: API_BASE + '/vehicles/' + vehicleId,
        method: 'DELETE',
        success: function(response) {
            console.log('删除车辆成功:', response);
            $('#deleteVehicleModal').modal('hide');
            showSuccess('车辆「' + plateNumber + '」删除成功');
            // 重新加载列表
            currentPage = 1;
            loadVehicles();
        },
        error: function(xhr, status, error) {
            console.error('删除车辆失败:', error);
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
