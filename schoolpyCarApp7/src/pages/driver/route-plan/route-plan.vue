<template>
    <view class="route-plan-page">
        <view class="header">
            <view class="route-info">
                <text class="route-name">{{ currentRoute.name }}</text>
                <view class="route-status" :class="currentRoute.status === '进行中' ? 'active' : ''">
                    <text>{{ currentRoute.status }}</text>
                </view>
            </view>
            <view class="route-date">
                <text>{{ currentDate }}</text>
            </view>
        </view>

        <view class="route-summary">
            <view class="summary-item">
                <view class="summary-icon">
                    <text>🚌</text>
                </view>
                <view class="summary-content">
                    <text class="summary-num">{{ currentRoute.stops.length }}</text>
                    <text class="summary-label">站点数</text>
                </view>
            </view>
            <view class="summary-item">
                <view class="summary-icon">
                    <text>👶</text>
                </view>
                <view class="summary-content">
                    <text class="summary-num">{{ totalStudents }}</text>
                    <text class="summary-label">接送学生</text>
                </view>
            </view>
            <view class="summary-item">
                <view class="summary-icon">
                    <text>⏱️</text>
                </view>
                <view class="summary-content">
                    <text class="summary-num">{{ currentRoute.estimatedTime }}</text>
                    <text class="summary-label">预计时长</text>
                </view>
            </view>
            <view class="summary-item">
                <view class="summary-icon">
                    <text>📏</text>
                </view>
                <view class="summary-content">
                    <text class="summary-num">{{ currentRoute.distance }}</text>
                    <text class="summary-label">总里程</text>
                </view>
            </view>
        </view>

        <view class="section-header">
            <text class="section-title">今日路线</text>
            <view class="switch-btn" @click="showRouteSelect">
                <text>切换路线</text>
            </view>
        </view>

        <view class="route-stops">
            <view 
                v-for="(stop, index) in currentRoute.stops" 
                :key="index" 
                class="stop-item"
                :class="{ 
                    current: stop.isCurrent, 
                    completed: stop.isCompleted,
                    'last-item': index === currentRoute.stops.length - 1
                }"
            >
                <view class="stop-dot-wrapper">
                    <view class="stop-dot" :class="{ current: stop.isCurrent, completed: stop.isCompleted }">
                        <text v-if="stop.isCompleted">✓</text>
                        <text v-else-if="stop.isCurrent">📍</text>
                    </view>
                    <view v-if="index < currentRoute.stops.length - 1" class="stop-line" :class="{ completed: stop.isCompleted }"></view>
                </view>
                <view class="stop-content">
                    <view class="stop-header">
                        <text class="stop-name">{{ stop.name }}</text>
                        <view class="stop-time-tag" :class="{ current: stop.isCurrent, completed: stop.isCompleted }">
                            <text>{{ stop.time }}</text>
                        </view>
                    </view>
                    <view class="stop-details" v-if="stop.studentCount > 0">
                        <view class="detail-tag">
                            <text>需接送 {{ stop.studentCount }} 人</text>
                        </view>
                        <view class="student-list" v-if="stop.students && stop.students.length > 0">
                            <view class="student-item" v-for="(stu, idx) in stop.students" :key="idx">
                                <text class="student-avatar">👶</text>
                                <text class="student-name">{{ stu.name }}</text>
                                <view class="student-status" :class="stu.status">
                                    <text>{{ stu.statusText }}</text>
                                </view>
                            </view>
                        </view>
                    </view>
                    <view class="stop-actions" v-if="stop.isCurrent">
                        <view class="action-btn confirm" @click="confirmArrival(stop)">
                            <text>确认到达</text>
                        </view>
                        <view class="action-btn navigate" @click="startNavigation(stop)">
                            <text>开始导航</text>
                        </view>
                    </view>
                </view>
            </view>
        </view>

        <view class="section-header" style="margin-top: 30rpx;">
            <text class="section-title">明日路线预览</text>
        </view>

        <view class="tomorrow-route">
            <view class="tomorrow-card">
                <view class="tomorrow-header">
                    <view class="tomorrow-icon">
                        <text>📅</text>
                    </view>
                    <view class="tomorrow-info">
                        <text class="tomorrow-name">路线B：实验二小 - 阳光社区</text>
                        <text class="tomorrow-time">上午 07:00 - 08:30</text>
                    </view>
                </view>
                <view class="tomorrow-stats">
                    <text>6个站点 · 24名学生 · 预计1小时30分</text>
                </view>
            </view>
        </view>
    </view>
</template>

<script setup>
import { ref, computed } from 'vue'
import { onLoad } from '@dcloudio/uni-app'

const currentDate = computed(() => {
    const now = new Date()
    const year = now.getFullYear()
    const month = now.getMonth() + 1
    const day = now.getDate()
    const weekDays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
    const weekDay = weekDays[now.getDay()]
    return `${year}年${month}月${day}日 ${weekDay}`
})

const currentRoute = ref({
    name: '路线A：实验一小 - 幸福小区',
    status: '进行中',
    estimatedTime: '1小时10分',
    distance: '25.6km',
    stops: [
        {
            name: '实验一小',
            time: '08:15',
            studentCount: 8,
            isCurrent: false,
            isCompleted: true,
            students: [
                { name: '张三', status: 'arrived', statusText: '已到校' },
                { name: '李四', status: 'arrived', statusText: '已到校' },
                { name: '王五', status: 'arrived', statusText: '已到校' }
            ]
        },
        {
            name: '阳光花园',
            time: '08:30',
            studentCount: 3,
            isCurrent: true,
            isCompleted: false,
            students: [
                { name: '赵六', status: 'waiting', statusText: '等待中' },
                { name: '钱七', status: 'waiting', statusText: '等待中' },
                { name: '孙八', status: 'absent', statusText: '未到' }
            ]
        },
        {
            name: '幸福小区',
            time: '08:45',
            studentCount: 1,
            isCurrent: false,
            isCompleted: false,
            students: [
                { name: '周九', status: 'waiting', statusText: '等待中' }
            ]
        },
        {
            name: '金色家园',
            time: '09:00',
            studentCount: 0,
            isCurrent: false,
            isCompleted: false
        },
        {
            name: '东方明珠',
            time: '09:15',
            studentCount: 2,
            isCurrent: false,
            isCompleted: false,
            students: [
                { name: '吴十', status: 'waiting', statusText: '等待中' },
                { name: '郑十一', status: 'waiting', statusText: '等待中' }
            ]
        }
    ]
})

const totalStudents = computed(() => {
    return currentRoute.value.stops.reduce((sum, stop) => sum + stop.studentCount, 0)
})

function confirmArrival(stop) {
    uni.showModal({
        title: '确认到达',
        content: `确定已到达「${stop.name}」？`,
        success: (res) => {
            if (res.confirm) {
                stop.isCompleted = true
                stop.isCurrent = false
                const currentIndex = currentRoute.value.stops.findIndex(s => s.isCurrent)
                if (currentIndex > -1 && currentIndex < currentRoute.value.stops.length - 1) {
                    currentRoute.value.stops[currentIndex + 1].isCurrent = true
                }
                uni.showToast({
                    title: '已确认到达',
                    icon: 'success'
                })
            }
        }
    })
}

function startNavigation(stop) {
    uni.showToast({
        title: '正在启动导航...',
        icon: 'loading'
    })
    setTimeout(() => {
        uni.showModal({
            title: '导航',
            content: `即将导航至「${stop.name}」\n预计5分钟到达`,
            showCancel: false
        })
    }, 1000)
}

function showRouteSelect() {
    uni.showActionSheet({
        itemList: ['路线A：实验一小 - 幸福小区', '路线B：实验二小 - 阳光社区', '路线C：实验三小 - 绿色家园'],
        success: (res) => {
            if (res.tapIndex === 0) {
                uni.showToast({
                    title: '已选择路线A',
                    icon: 'success'
                })
            } else {
                uni.showToast({
                    title: '功能开发中',
                    icon: 'none'
                })
            }
        }
    })
}

onLoad(() => {
    console.log('路线规划页加载')
})
</script>

<style lang="scss" scoped>
.route-plan-page {
    min-height: 100vh;
    background: #F5F7FA;
    padding-bottom: 40rpx;
}

.header {
    background: linear-gradient(135deg, #4CAF50 0%, #81C784 100%);
    padding: 30rpx;

    .route-info {
        display: flex;
        align-items: center;
        margin-bottom: 12rpx;

        .route-name {
            font-size: 34rpx;
            font-weight: 600;
            color: #FFFFFF;
            margin-right: 16rpx;
        }

        .route-status {
            padding: 6rpx 20rpx;
            background: rgba(255, 255, 255, 0.3);
            border-radius: 20rpx;

            text {
                font-size: 22rpx;
                color: #FFFFFF;
            }

            &.active {
                background: #FFFFFF;
                text {
                    color: #4CAF50;
                }
            }
        }
    }

    .route-date {
        text {
            font-size: 24rpx;
            color: rgba(255, 255, 255, 0.85);
        }
    }
}

.route-summary {
    display: flex;
    background: #FFFFFF;
    margin: -20rpx 30rpx 20rpx;
    border-radius: 20rpx;
    padding: 24rpx 0;
    box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.08);
    position: relative;
    z-index: 10;

    .summary-item {
        flex: 1;
        display: flex;
        flex-direction: column;
        align-items: center;

        .summary-icon {
            width: 64rpx;
            height: 64rpx;
            background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
            border-radius: 16rpx;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 12rpx;
            font-size: 32rpx;
        }

        .summary-content {
            display: flex;
            flex-direction: column;
            align-items: center;

            .summary-num {
                font-size: 32rpx;
                font-weight: 700;
                color: #333333;
                margin-bottom: 4rpx;
            }

            .summary-label {
                font-size: 22rpx;
                color: #999999;
            }
        }
    }
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20rpx 30rpx;

    .section-title {
        font-size: 30rpx;
        font-weight: 600;
        color: #333333;
    }

    .switch-btn {
        padding: 8rpx 20rpx;
        background: #E8F5E9;
        border-radius: 20rpx;

        text {
            font-size: 24rpx;
            color: #4CAF50;
        }
    }
}

.route-stops {
    background: #FFFFFF;
    margin: 0 30rpx;
    border-radius: 20rpx;
    padding: 30rpx;
    box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.06);

    .stop-item {
        display: flex;
        padding-bottom: 30rpx;
        position: relative;

        &.last-item {
            padding-bottom: 0;
        }

        .stop-dot-wrapper {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-right: 20rpx;

            .stop-dot {
                width: 48rpx;
                height: 48rpx;
                background: #F5F7FA;
                border: 3rpx solid #E0E0E0;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                flex-shrink: 0;

                text {
                    font-size: 22rpx;
                    color: #CCCCCC;
                }

                &.completed {
                    background: linear-gradient(135deg, #4CAF50 0%, #81C784 100%);
                    border-color: #4CAF50;

                    text {
                        color: #FFFFFF;
                    }
                }

                &.current {
                    background: #FFFFFF;
                    border-color: #4CAF50;
                    width: 56rpx;
                    height: 56rpx;
                    box-shadow: 0 0 0 8rpx rgba(76, 175, 80, 0.15);

                    text {
                        color: #4CAF50;
                        font-size: 26rpx;
                    }
                }
            }

            .stop-line {
                flex: 1;
                width: 2rpx;
                background: #E0E0E0;
                margin-top: 10rpx;

                &.completed {
                    background: #4CAF50;
                }
            }
        }

        .stop-content {
            flex: 1;
            padding-top: 8rpx;

            .stop-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 12rpx;

                .stop-name {
                    font-size: 30rpx;
                    font-weight: 600;
                    color: #333333;
                }

                .stop-time-tag {
                    padding: 6rpx 16rpx;
                    background: #F5F7FA;
                    border-radius: 20rpx;

                    text {
                        font-size: 22rpx;
                        color: #666666;
                    }

                    &.current {
                        background: linear-gradient(135deg, #4CAF50 0%, #81C784 100%);
                        text {
                            color: #FFFFFF;
                        }
                    }

                    &.completed {
                        background: #E8F5E9;
                        text {
                            color: #4CAF50;
                        }
                    }
                }
            }

            .stop-details {
                .detail-tag {
                    display: inline-block;
                    padding: 6rpx 16rpx;
                    background: #FFF8E1;
                    border-radius: 8rpx;
                    margin-bottom: 16rpx;

                    text {
                        font-size: 22rpx;
                        color: #FF9800;
                    }
                }

                .student-list {
                    background: #F8FAFC;
                    border-radius: 12rpx;
                    padding: 16rpx;

                    .student-item {
                        display: flex;
                        align-items: center;
                        padding: 12rpx 0;
                        border-bottom: 1rpx solid #EEEEEE;

                        &:last-child {
                            border-bottom: none;
                        }

                        .student-avatar {
                            font-size: 28rpx;
                            margin-right: 12rpx;
                        }

                        .student-name {
                            flex: 1;
                            font-size: 26rpx;
                            color: #333333;
                        }

                        .student-status {
                            padding: 4rpx 12rpx;
                            border-radius: 8rpx;

                            text {
                                font-size: 20rpx;
                            }

                            &.arrived {
                                background: #E8F5E9;
                                text { color: #4CAF50; }
                            }

                            &.waiting {
                                background: #E3F2FD;
                                text { color: #2196F3; }
                            }

                            &.absent {
                                background: #FFEBEE;
                                text { color: #F44336; }
                            }
                        }
                    }
                }
            }

            .stop-actions {
                display: flex;
                gap: 20rpx;
                margin-top: 20rpx;

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

                    &.confirm {
                        background: linear-gradient(135deg, #4CAF50 0%, #81C784 100%);
                        text { color: #FFFFFF; }
                    }

                    &.navigate {
                        background: #E3F2FD;
                        text { color: #2196F3; }
                    }
                }
            }
        }

        &.completed {
            .stop-content {
                .stop-header {
                    .stop-name {
                        color: #999999;
                    }
                }
            }
        }
    }
}

.tomorrow-route {
    padding: 0 30rpx;

    .tomorrow-card {
        background: #FFFFFF;
        border-radius: 20rpx;
        padding: 24rpx;
        box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.06);

        .tomorrow-header {
            display: flex;
            align-items: center;
            margin-bottom: 16rpx;

            .tomorrow-icon {
                width: 56rpx;
                height: 56rpx;
                background: #FFF8E1;
                border-radius: 12rpx;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-right: 16rpx;
                font-size: 28rpx;
            }

            .tomorrow-info {
                flex: 1;
                display: flex;
                flex-direction: column;

                .tomorrow-name {
                    font-size: 28rpx;
                    color: #333333;
                    font-weight: 500;
                    margin-bottom: 4rpx;
                }

                .tomorrow-time {
                    font-size: 22rpx;
                    color: #999999;
                }
            }
        }

        .tomorrow-stats {
            text {
                font-size: 24rpx;
                color: #666666;
            }
        }
    }
}
</style>
