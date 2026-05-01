/*
校车后台管理系统 - JavaScript文件
包含报警音频效果、抖屏动画、轮询功能等
*/

// 全局变量
let alarmAudioContext = null;
let alarmOscillator = null;
let alarmGain = null;
let alarmPollingInterval = null;
let currentActiveAlarm = null;
let isAlarmActive = false;

// API基础URL
const API_BASE = '';

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 初始化报警音频系统
    initAlarmAudio();
    
    // 开始轮询最新报警
    startAlarmPolling();
    
    // 绑定事件
    bindEvents();
    
    // 如果是首页，加载统计数据
    if (window.location.pathname === '/' || window.location.pathname === '/index') {
        loadDashboardData();
    }
});

// 初始化报警音频系统
function initAlarmAudio() {
    try {
        // 创建AudioContext
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        alarmAudioContext = new AudioContext();
    } catch (e) {
        console.warn('Web Audio API not supported', e);
    }
}

// 开始播放警报声
function startAlarmSound(level = 1) {
    if (!alarmAudioContext) return;
    
    // 停止之前的声音
    stopAlarmSound();
    
    // 根据级别设置不同的频率
    let frequency = 800;
    let volume = 0.3;
    
    if (level === 1) {
        frequency = 1000;
        volume = 0.5;
    } else if (level === 2) {
        frequency = 700;
        volume = 0.3;
    } else {
        frequency = 500;
        volume = 0.2;
    }
    
    // 创建振荡器
    alarmOscillator = alarmAudioContext.createOscillator();
    alarmGain = alarmAudioContext.createGain();
    
    alarmOscillator.type = 'square';
    alarmOscillator.frequency.value = frequency;
    
    // 创建脉冲效果
    const now = alarmAudioContext.currentTime;
    alarmGain.gain.setValueAtTime(0, now);
    alarmGain.gain.linearRampToValueAtTime(volume, now + 0.1);
    alarmGain.gain.linearRampToValueAtTime(0, now + 0.3);
    
    // 循环播放
    alarmOscillator.connect(alarmGain);
    alarmGain.connect(alarmAudioContext.destination);
    alarmOscillator.start(now);
    
    // 脉冲循环
    const pulseInterval = setInterval(() => {
        if (!isAlarmActive) {
            clearInterval(pulseInterval);
            return;
        }
        const time = alarmAudioContext.currentTime;
        alarmGain.gain.setValueAtTime(0, time);
        alarmGain.gain.linearRampToValueAtTime(volume, time + 0.1);
        alarmGain.gain.linearRampToValueAtTime(0, time + 0.3);
    }, 500);
    
    // 保存interval以便清除
    alarmOscillator._pulseInterval = pulseInterval;
}

// 停止警报声
function stopAlarmSound() {
    if (alarmOscillator) {
        if (alarmOscillator._pulseInterval) {
            clearInterval(alarmOscillator._pulseInterval);
        }
        try {
            alarmOscillator.stop();
            alarmOscillator.disconnect();
        } catch (e) {}
        alarmOscillator = null;
    }
    if (alarmGain) {
        try {
            alarmGain.disconnect();
        } catch (e) {}
        alarmGain = null;
    }
}

// 开始抖屏效果
function startShakeEffect(level = 1) {
    // 移除之前的效果
    document.body.classList.remove('shake', 'alarm-level-red', 'alarm-level-orange', 'alarm-level-blue');
    
    // 添加新效果
    let colorClass = 'alarm-level-blue';
    if (level === 1) {
        colorClass = 'alarm-level-red';
    } else if (level === 2) {
        colorClass = 'alarm-level-orange';
    }
    
    document.body.classList.add('shake', colorClass);
}

// 停止抖屏效果
function stopShakeEffect() {
    document.body.classList.remove('shake', 'alarm-level-red', 'alarm-level-orange', 'alarm-level-blue');
}

// 显示报警弹窗
function showAlarmModal(alarm) {
    // 检查是否已有相同报警在显示
    if (currentActiveAlarm && currentActiveAlarm.id === alarm.id) {
        return;
    }
    
    currentActiveAlarm = alarm;
    isAlarmActive = true;
    
    // 获取级别信息
    let levelName = '三级报警';
    let levelNum = 3;
    
    if (alarm.level_name === '一级报警' || alarm.level_color === 'red') {
        levelName = '一级报警';
        levelNum = 1;
    } else if (alarm.level_name === '二级报警' || alarm.level_color === 'orange') {
        levelName = '二级报警';
        levelNum = 2;
    }
    
    // 开始报警效果
    startAlarmSound(levelNum);
    startShakeEffect(levelNum);
    
    // 显示声音控制按钮
    const soundBtn = document.getElementById('alarm-sound-btn');
    if (soundBtn) {
        soundBtn.classList.add('active');
    }
    
    // 创建或更新弹窗
    let overlay = document.getElementById('alarm-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'alarm-overlay';
        overlay.className = 'alarm-overlay';
        document.body.appendChild(overlay);
    }
    
    // 构建弹窗HTML
    overlay.innerHTML = `
        <div class="alarm-modal">
            <div class="alarm-modal-header level-${levelNum}">
                <h4><i class="fas fa-exclamation-triangle"></i> ${levelName}</h4>
                <div class="level-badge">${alarm.type_name}</div>
            </div>
            <div class="alarm-modal-body">
                <div class="alarm-info-row">
                    <div class="alarm-info-label">报警编号</div>
                    <div class="alarm-info-value">${alarm.alarm_number}</div>
                </div>
                <div class="alarm-info-row">
                    <div class="alarm-info-label">校车牌号</div>
                    <div class="alarm-info-value">${alarm.bus_plate} (${alarm.bus_number})</div>
                </div>
                <div class="alarm-info-row">
                    <div class="alarm-info-label">报警位置</div>
                    <div class="alarm-info-value">
                        <i class="fas fa-map-marker-alt"></i> ${alarm.location_name || '未知位置'}
                        <br>
                        <small>经度: ${alarm.longitude}, 纬度: ${alarm.latitude}</small>
                    </div>
                </div>
                <div class="alarm-info-row">
                    <div class="alarm-info-label">触发时间</div>
                    <div class="alarm-info-value">${formatDateTime(alarm.triggered_at)}</div>
                </div>
                <div class="alarm-info-row">
                    <div class="alarm-info-label">报警描述</div>
                    <div class="alarm-info-value">${alarm.description || '暂无描述'}</div>
                </div>
            </div>
            <div class="alarm-modal-footer">
                <button class="btn btn-secondary" onclick="muteAlarm()">
                    <i class="fas fa-volume-mute"></i> 静音
                </button>
                <button class="btn btn-primary" onclick="handleAlarm(${alarm.id}, 'processing')">
                    <i class="fas fa-play"></i> 开始处理
                </button>
                <button class="btn btn-success" onclick="handleAlarm(${alarm.id}, 'resolved')">
                    <i class="fas fa-check"></i> 标记解决
                </button>
            </div>
        </div>
    `;
    
    // 显示弹窗
    overlay.classList.add('active');
}

// 隐藏报警弹窗
function hideAlarmModal() {
    const overlay = document.getElementById('alarm-overlay');
    if (overlay) {
        overlay.classList.remove('active');
    }
    
    // 停止所有效果
    stopAlarmSound();
    stopShakeEffect();
    
    // 隐藏声音控制按钮
    const soundBtn = document.getElementById('alarm-sound-btn');
    if (soundBtn) {
        soundBtn.classList.remove('active');
    }
    
    currentActiveAlarm = null;
    isAlarmActive = false;
}

// 静音报警
function muteAlarm() {
    stopAlarmSound();
    // 只停止声音，不停止视觉效果
}

// 处理报警
async function handleAlarm(alarmId, status) {
    try {
        const response = await fetch(`${API_BASE}/api/alarms/${alarmId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                status: status,
                is_read: true
            })
        });
        
        if (response.ok) {
            if (status === 'resolved' || status === 'closed') {
                hideAlarmModal();
            }
            // 刷新页面数据
            if (typeof loadAlarmList === 'function') {
                loadAlarmList();
            }
            if (typeof loadDashboardData === 'function') {
                loadDashboardData();
            }
        }
    } catch (error) {
        console.error('处理报警失败:', error);
    }
}

// 开始轮询最新报警
function startAlarmPolling() {
    // 立即执行一次
    checkNewAlarms();
    
    // 设置定时轮询
    alarmPollingInterval = setInterval(() => {
        checkNewAlarms();
    }, 5000); // 每5秒轮询一次
}

// 检查新报警
async function checkNewAlarms() {
    try {
        const response = await fetch(`${API_BASE}/api/alarms/unread/latest`);
        const alarms = await response.json();
        
        if (alarms && alarms.length > 0) {
            // 更新未读报警数量
            updateUnreadCount(alarms.length);
            
            // 如果没有当前活动的报警，显示第一个
            if (!isAlarmActive) {
                showAlarmModal(alarms[0]);
            }
        }
    } catch (error) {
        console.error('轮询报警失败:', error);
    }
}

// 更新未读报警数量
function updateUnreadCount(count) {
    const badge = document.getElementById('alarm-badge');
    if (badge) {
        if (count > 0) {
            badge.textContent = count > 99 ? '99+' : count;
            badge.style.display = 'flex';
        } else {
            badge.style.display = 'none';
        }
    }
}

// 绑定事件
function bindEvents() {
    // 声音控制按钮
    const soundBtn = document.getElementById('alarm-sound-btn');
    if (soundBtn) {
        soundBtn.addEventListener('click', () => {
            if (isAlarmActive) {
                muteAlarm();
                soundBtn.innerHTML = '<i class="fas fa-volume-up"></i>';
                soundBtn.onclick = () => {
                    if (currentActiveAlarm) {
                        let level = 3;
                        if (currentActiveAlarm.level_color === 'red') level = 1;
                        else if (currentActiveAlarm.level_color === 'orange') level = 2;
                        startAlarmSound(level);
                        soundBtn.innerHTML = '<i class="fas fa-volume-mute"></i>';
                    }
                };
            }
        });
    }
}

// 格式化日期时间
function formatDateTime(dateStr) {
    if (!dateStr) return '-';
    const date = new Date(dateStr);
    return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
}

// 加载首页统计数据
async function loadDashboardData() {
    try {
        // 加载报警统计
        const alarmStatsResponse = await fetch(`${API_BASE}/api/alarms/stats/overview`);
        const alarmStats = await alarmStatsResponse.json();
        
        // 更新报警统计显示
        updateAlarmStats(alarmStats);
        
        // 加载校车统计
        const busStatsResponse = await fetch(`${API_BASE}/api/buses/stats/overview`);
        const busStats = await busStatsResponse.json();
        
        // 加载司机统计
        const driverStatsResponse = await fetch(`${API_BASE}/api/drivers/stats/overview`);
        const driverStats = await driverStatsResponse.json();
        
        // 加载学生统计
        const studentStatsResponse = await fetch(`${API_BASE}/api/students/stats/overview`);
        const studentStats = await studentStatsResponse.json();
        
        // 更新其他统计
        const totalBusesEl = document.getElementById('total-buses');
        const runningBusesEl = document.getElementById('running-buses');
        const totalDriversEl = document.getElementById('total-drivers');
        const totalStudentsEl = document.getElementById('total-students');
        
        if (totalBusesEl) totalBusesEl.textContent = busStats.total || 0;
        if (runningBusesEl) runningBusesEl.textContent = busStats.running || 0;
        if (totalDriversEl) totalDriversEl.textContent = driverStats.total || 0;
        if (totalStudentsEl) totalStudentsEl.textContent = studentStats.total || 0;
        
    } catch (error) {
        console.error('加载统计数据失败:', error);
    }
}

// 更新报警统计显示
function updateAlarmStats(stats) {
    if (!stats) return;
    
    const pendingEl = document.getElementById('pending-alarms');
    const processingEl = document.getElementById('processing-alarms');
    const resolvedEl = document.getElementById('resolved-alarms');
    const level1El = document.getElementById('level1-alarms');
    const level2El = document.getElementById('level2-alarms');
    const level3El = document.getElementById('level3-alarms');
    const unreadEl = document.getElementById('unread-alarms');
    
    if (pendingEl && stats.status_stats) pendingEl.textContent = stats.status_stats.pending || 0;
    if (processingEl && stats.status_stats) processingEl.textContent = stats.status_stats.processing || 0;
    if (resolvedEl && stats.status_stats) resolvedEl.textContent = stats.status_stats.resolved || 0;
    if (level1El && stats.level_stats) level1El.textContent = stats.level_stats.level1 || 0;
    if (level2El && stats.level_stats) level2El.textContent = stats.level_stats.level2 || 0;
    if (level3El && stats.level_stats) level3El.textContent = stats.level_stats.level3 || 0;
    if (unreadEl) unreadEl.textContent = stats.unread_count || 0;
}

// 通用API请求函数
async function apiRequest(url, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json'
        },
        ...options
    };
    
    try {
        const response = await fetch(`${API_BASE}${url}`, defaultOptions);
        const data = await response.json();
        return { ok: response.ok, data, status: response.status };
    } catch (error) {
        console.error('API请求失败:', error);
        return { ok: false, error: error.message };
    }
}

// 显示提示消息
function showToast(message, type = 'info') {
    // 创建toast元素
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 25px;
        border-radius: 8px;
        color: #fff;
        font-weight: 500;
        z-index: 10001;
        animation: slideIn 0.3s ease;
        max-width: 300px;
    `;
    
    // 设置背景颜色
    if (type === 'success') {
        toast.style.backgroundColor = '#28a745';
    } else if (type === 'error') {
        toast.style.backgroundColor = '#dc3545';
    } else if (type === 'warning') {
        toast.style.backgroundColor = '#ffc107';
        toast.style.color = '#212529';
    } else {
        toast.style.backgroundColor = '#007bff';
    }
    
    toast.textContent = message;
    document.body.appendChild(toast);
    
    // 3秒后移除
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 300);
    }, 3000);
}

// 添加CSS动画
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
