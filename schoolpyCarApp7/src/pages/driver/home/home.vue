<template>
    <view class="home-page">
        <view class="header">
            <view class="user-info">
                <view class="avatar">
                    <text>👨‍✈️</text>
                </view>
                <view class="info">
                    <text class="greeting">{{ greetingText }}</text>
                    <text class="name">{{ userInfo.name }}</text>
                </view>
            </view>
            <view class="header-actions">
                <view class="action-item" @click="goMessage">
                    <text>🔔</text>
                    <view v-if="unreadCount > 0" class="badge">{{ unreadCount }}</view>
                </view>
            </view>
        </view>

        <view class="work-status-card">
            <view class="status-header">
                <text class="status-label">今日工作状态</text>
                <view class="status-toggle" :class="isWorking ? 'on' : 'off'" @click="toggleWorkStatus">
                    <view class="toggle-dot"></view>
                </view>
            </view>

            <view class="work-info">
                <view class="info-item">
                    <view class="info-icon on">
                        <text>🚗</text>
                    </view>
                    <view class="info-content">
                        <text class="info-label">当前车辆</text>
                        <text class="info-value">{{ vehicle.plateNo }}</text>
                    </view>
                </view>
                <view class="info-item">
                    <view class="info-icon">
                        <text>📍</text>
                    </view>
                    <view class="info-content">
                        <text class="info-label">当前路线</text>
                        <text class="info-value">{{ route.name }}</text>
                    </view>
                </view>
            </view>

            <view class="work-actions">
                <view class="action-btn start" :class="{ disabled: isWorking }" @click="startWork">
                    <text>上班打卡</text>
                </view>
                <view class="action-btn end" :class="{ disabled: !isWorking }" @click="endWork">
                    <text>下班打卡</text>
                </view>
            </view>
        </view>

        <view class="quick-stats">
            <view class="stat-card">
                <text class="stat-num">{{ todayStats.students }}</text>
                <text class="stat-label">今日接送</text>
            </view>
            <view class="stat-card">
                <text class="stat-num">{{ todayStats.routes }}</text>
                <text class="stat-label">路线班次</text>
            </view>
            <view class="stat-card">
                <text class="stat-num">{{ todayStats.mileage }}km</text>
                <text class="stat-label">行驶里程</text>
            </view>
            <view class="stat-card">
                <text class="stat-num">{{ todayStats.time }}h</text>
                <text class="stat-label">工作时长</text>
            </view>
        </view>

        <view class="vehicle-section">
            <view class="section-header">
                <text class="section-title">车辆信息</text>
                <view class="detail-btn" @click="showVehicleDetail">
                    <text>详情 ›</text>
                </view>
            </view>

            <view class="vehicle-card">
                <view class="vehicle-main">
                    <view class="vehicle-icon">
                        <text>🚌</text>
                    </view>
                    <view class="vehicle-info">
                        <text class="vehicle-name">{{ vehicle.name }}</text>
                        <text class="vehicle-plate">{{ vehicle.plateNo }}</text>
                    </view>
                </view>

                <view class="vehicle-details">
                    <view class="detail-row">
                        <view class="detail-col">
                            <text class="detail-label">载客量</text>
                            <text class="detail-value">{{ vehicle.capacity }}人</text>
                        </view>
                        <view class="detail-col">
                            <text class="detail-label">车长</text>
                            <text class="detail-value">{{ vehicle.length }}m</text>
                        </view>
                        <view class="detail-col">
                            <text class="detail-label">状态</text>
                            <text class="detail-value good">{{ vehicle.status }}</text>
                        </view>
                    </view>
                </view>

                <view class="vehicle-warnings" v-if="vehicle.warnings.length > 0">
                    <view class="warning-item" v-for="(warning, index) in vehicle.warnings" :key="index">
                        <view class="warning-icon">
                            <text>⚠️</text>
                        </view>
                        <text class="warning-text">{{ warning }}</text>
                    </view>
                </view>
            </view>
        </view>

        <view class="route-section">
            <view class="section-header">
                <text class="section-title">今日路线</text>
                <view class="detail-btn" @click="goRoutePlan">
                    <text>路线规划 ›</text>
                </view>
            </view>

            <view class="route-card">
                <view class="route-header">
                    <text class="route-name">{{ route.name }}</text>
                    <view class="route-status">
                        <text>{{ route.status }}</text>
                    </view>
                </view>

                <view class="route-stops">
                    <view 
                        v-for="(stop, index) in route.stops" 
                        :key="index" 
                        class="stop-item"
                        :class="{ current: stop.isCurrent, completed: stop.isCompleted }"
                    >
                        <view class="stop-dot">
                            <text v-if="stop.isCompleted">✓</text>
                            <text v-else-if="stop.isCurrent">📍</text>
                        </view>
                        <view class="stop-info">
                            <text class="stop-name">{{ stop.name }}</text>
                            <text class="stop-time">{{ stop.time }}</text>
                            <text class="stop-students" v-if="stop.studentCount">需接送 {{ stop.studentCount }} 人</text>
                        </view>
                    </view>
                </view>
            </view>
        </view>
    </view>
</template>

<script setup>
import { ref, computed } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { useMessageStore } from '@/store'

const messageStore = useMessageStore()

const userInfo = ref({
    name: '王师傅',
    phone: '139****0000'
})

const unreadCount = computed(() => {
    return messageStore.driverMessages.filter(m => !m.read).length
})

const isWorking = ref(false)

const greetingText = computed(() => {
    const hour = new Date().getHours()
    if (hour < 9) return '早上好'
    if (hour < 12) return '上午好'
    if (hour < 14) return '中午好'
    if (hour < 17) return '下午好'
    return '晚上好'
})

const todayStats = ref({
    students: 12,
    routes: 4,
    mileage: 86.5,
    time: 6.5
})

const vehicle = ref({
    name: '宇通客车',
    plateNo: '京A12345',
    capacity: 45,
    length: 10.5,
    status: '良好',
    warnings: ['下次保养剩余200公里']
})

const route = ref({
    name: '路线A：实验一小 - 幸福小区',
    status: '进行中',
    stops: [
        {
            name: '实验一小',
            time: '08:15',
            studentCount: 8,
            isCurrent: true,
            isCompleted: false
        },
        {
            name: '阳光花园',
            time: '08:30',
            studentCount: 3,
            isCurrent: false,
            isCompleted: false
        },
        {
            name: '幸福小区',
            time: '08:45',
            studentCount: 1,
            isCurrent: false,
            isCompleted: false
        }
    ]
})

function toggleWorkStatus() {
    if (!isWorking.value) {
        startWork()
    } else {
        endWork()
    }
}

function startWork() {
    if (isWorking.value) {
        uni.showToast({
            title: '您已处于上班状态',
            icon: 'none'
        })
        return
    }

    uni.showLoading({
        title: '打卡中...'
    })

    setTimeout(() => {
        uni.hideLoading()
        isWorking.value = true
        uni.showToast({
            title: '上班打卡成功',
            icon: 'success'
        })
    }, 1000)
}

function endWork() {
    if (!isWorking.value) {
        uni.showToast({
            title: '您还未上班',
            icon: 'none'
        })
        return
    }

    uni.showModal({
        title: '确认下班',
        content: '确定要下班打卡吗？',
        success: (res) => {
            if (res.confirm) {
                uni.showLoading({
                    title: '打卡中...'
                })
                setTimeout(() => {
                    uni.hideLoading()
                    isWorking.value = false
                    uni.showToast({
                        title: '下班打卡成功',
                        icon: 'success'
                    })
                }, 1000)
            }
        }
    })
}

function goMessage() {
    uni.navigateTo({
        url: '/pages/driver/message/message'
    })
}

function goRoutePlan() {
    uni.navigateTo({
        url: '/pages/driver/route-plan/route-plan'
    })
}

function showVehicleDetail() {
    uni.showModal({
        title: '车辆详情',
        content: `车型：${vehicle.value.name}\n车牌：${vehicle.value.plateNo}\n载客量：${vehicle.value.capacity}人\n车长：${vehicle.value.length}m\n车况：${vehicle.value.status}`,
        showCancel: false
    })
}

onLoad(() => {
    console.log('司机首页加载')
})
</script>

<style lang="scss" scoped>
.home-page {
    min-height: 100vh;
    background: linear-gradient(180deg, #4CAF50 0%, #F5F7FA 30%);
    padding-bottom: 40rpx;
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 40rpx 30rpx 30rpx;

    .user-info {
        display: flex;
        align-items: center;

        .avatar {
            width: 96rpx;
            height: 96rpx;
            background: rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 20rpx;
            font-size: 48rpx;
        }

        .info {
            display: flex;
            flex-direction: column;

            .greeting {
                font-size: 26rpx;
                color: rgba(255, 255, 255, 0.8);
                margin-bottom: 4rpx;
            }

            .name {
                font-size: 34rpx;
                font-weight: 600;
                color: #FFFFFF;
            }
        }
    }

    .header-actions {
        display: flex;
        gap: 20rpx;

        .action-item {
            position: relative;
            width: 72rpx;
            height: 72rpx;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 36rpx;

            .badge {
                position: absolute;
                top: 8rpx;
                right: 8rpx;
                min-width: 32rpx;
                height: 32rpx;
                background: #F44336;
                border-radius: 16rpx;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 20rpx;
                color: #FFFFFF;
                padding: 0 6rpx;
            }
        }
    }
}

.work-status-card {
    background: #FFFFFF;
    border-radius: 24rpx;
    margin: 0 30rpx 20rpx;
    padding: 30rpx;
    box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.08);

    .status-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 24rpx;

        .status-label {
            font-size: 30rpx;
            font-weight: 600;
            color: #333333;
        }

        .status-toggle {
            width: 88rpx;
            height: 48rpx;
            background: #CCCCCC;
            border-radius: 24rpx;
            position: relative;
            transition: all 0.3s;

            .toggle-dot {
                position: absolute;
                top: 4rpx;
                left: 4rpx;
                width: 40rpx;
                height: 40rpx;
                background: #FFFFFF;
                border-radius: 50%;
                transition: all 0.3s;
            }

            &.on {
                background: linear-gradient(135deg, #4CAF50 0%, #81C784 100%);

                .toggle-dot {
                    left: 44rpx;
                }
            }
        }
    }

    .work-info {
        display: flex;
        gap: 40rpx;
        margin-bottom: 24rpx;

        .info-item {
            display: flex;
            align-items: center;

            .info-icon {
                width: 56rpx;
                height: 56rpx;
                background: #F5F7FA;
                border-radius: 12rpx;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-right: 16rpx;
                font-size: 28rpx;

                &.on {
                    background: linear-gradient(135deg, #4CAF50 0%, #81C784 100%);
                }
            }

            .info-content {
                display: flex;
                flex-direction: column;

                .info-label {
                    font-size: 22rpx;
                    color: #999999;
                    margin-bottom: 4rpx;
                }

                .info-value {
                    font-size: 28rpx;
                    color: #333333;
                    font-weight: 500;
                }
            }
        }
    }

    .work-actions {
        display: flex;
        gap: 20rpx;

        .action-btn {
            flex: 1;
            height: 72rpx;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 36rpx;

            text {
                font-size: 28rpx;
            }

            &.start {
                background: linear-gradient(135deg, #4CAF50 0%, #81C784 100%);
                text { color: #FFFFFF; }

                &.disabled {
                    background: #E0E0E0;
                    text { color: #999999; }
                }
            }

            &.end {
                background: #FFEBEE;
                text { color: #F44336; }

                &.disabled {
                    background: #F5F5F5;
                    text { color: #CCCCCC; }
                }
            }
        }
    }
}

.quick-stats {
    display: flex;
    padding: 0 20rpx;
    margin-bottom: 20rpx;

    .stat-card {
        flex: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 20rpx 0;

        .stat-num {
            font-size: 32rpx;
            font-weight: 700;
            color: #4CAF50;
            margin-bottom: 8rpx;
        }

        .stat-label {
            font-size: 22rpx;
            color: #999999;
        }
    }
}

.vehicle-section, .route-section {
    background: #FFFFFF;
    margin: 0 30rpx 20rpx;
    border-radius: 24rpx;
    padding: 30rpx;
    box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.06);

    .section-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20rpx;

        .section-title {
            font-size: 30rpx;
            font-weight: 600;
            color: #333333;
        }

        .detail-btn {
            text {
                font-size: 24rpx;
                color: #4CAF50;
            }
        }
    }
}

.vehicle-card {
    .vehicle-main {
        display: flex;
        align-items: center;
        margin-bottom: 24rpx;

        .vehicle-icon {
            width: 80rpx;
            height: 80rpx;
            background: linear-gradient(135deg, #4CAF50 0%, #81C784 100%);
            border-radius: 16rpx;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 20rpx;
            font-size: 40rpx;
        }

        .vehicle-info {
            display: flex;
            flex-direction: column;

            .vehicle-name {
                font-size: 30rpx;
                color: #333333;
                margin-bottom: 4rpx;
            }

            .vehicle-plate {
                font-size: 24rpx;
                color: #999999;
            }
        }
    }

    .vehicle-details {
        .detail-row {
            display: flex;
            background: #F8FAFC;
            border-radius: 12rpx;
            padding: 20rpx;

            .detail-col {
                flex: 1;
                display: flex;
                flex-direction: column;
                align-items: center;

                .detail-label {
                    font-size: 22rpx;
                    color: #999999;
                    margin-bottom: 8rpx;
                }

                .detail-value {
                    font-size: 26rpx;
                    color: #333333;
                    font-weight: 500;

                    &.good {
                        color: #4CAF50;
                    }
                }
            }
        }
    }

    .vehicle-warnings {
        margin-top: 20rpx;

        .warning-item {
            display: flex;
            align-items: center;
            padding: 16rpx 20rpx;
            background: #FFF3E0;
            border-radius: 12rpx;
            margin-bottom: 10rpx;

            &:last-child {
                margin-bottom: 0;
            }

            .warning-icon {
                margin-right: 12rpx;
                font-size: 28rpx;
            }

            .warning-text {
                font-size: 24rpx;
                color: #FF9800;
            }
        }
    }
}

.route-card {
    .route-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 24rpx;

        .route-name {
            font-size: 28rpx;
            color: #333333;
            flex: 1;
        }

        .route-status {
            padding: 6rpx 16rpx;
            background: linear-gradient(135deg, #4CAF50 0%, #81C784 100%);
            border-radius: 20rpx;

            text {
                font-size: 22rpx;
                color: #FFFFFF;
            }
        }
    }

    .route-stops {
        position: relative;
        padding-left: 40rpx;

        &::before {
            content: '';
            position: absolute;
            left: 20rpx;
            top: 20rpx;
            bottom: 20rpx;
            width: 2rpx;
            background: #E0E0E0;
        }

        .stop-item {
            position: relative;
            display: flex;
            align-items: flex-start;
            padding: 20rpx 0;

            .stop-dot {
                position: absolute;
                left: -40rpx;
                top: 20rpx;
                width: 40rpx;
                height: 40rpx;
                background: #FFFFFF;
                border: 3rpx solid #E0E0E0;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;

                text {
                    font-size: 20rpx;
                    color: #CCCCCC;
                }
            }

            .stop-info {
                display: flex;
                flex-direction: column;

                .stop-name {
                    font-size: 28rpx;
                    color: #333333;
                    margin-bottom: 4rpx;
                }

                .stop-time {
                    font-size: 24rpx;
                    color: #999999;
                    margin-bottom: 4rpx;
                }

                .stop-students {
                    font-size: 22rpx;
                    color: #4CAF50;
                }
            }

            &.completed {
                .stop-dot {
                    background: #4CAF50;
                    border-color: #4CAF50;

                    text {
                        color: #FFFFFF;
                    }
                }

                .stop-info {
                    .stop-name {
                        color: #999999;
                    }
                }
            }

            &.current {
                .stop-dot {
                    background: #FFFFFF;
                    border-color: #4CAF50;
                    width: 48rpx;
                    height: 48rpx;
                    left: -44rpx;

                    text {
                        color: #4CAF50;
                        font-size: 24rpx;
                    }
                }

                .stop-info {
                    .stop-name {
                        font-weight: 600;
                        color: #4CAF50;
                    }
                }
            }
        }
    }
}
</style>
