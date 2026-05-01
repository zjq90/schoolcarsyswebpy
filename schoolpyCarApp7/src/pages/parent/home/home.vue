<template>
    <view class="home-page">
        <view class="header">
            <view class="user-info">
                <view class="avatar">
                    <text>👩</text>
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
                <view class="action-item" @click="goMine">
                    <text>⚙️</text>
                </view>
            </view>
        </view>

        <view class="quick-stats">
            <view class="stat-card">
                <view class="stat-icon">👶</view>
                <view class="stat-info">
                    <text class="stat-num">{{ students.length }}</text>
                    <text class="stat-label">已绑定学生</text>
                </view>
            </view>
            <view class="stat-card">
                <view class="stat-icon">🚍</view>
                <view class="stat-info">
                    <text class="stat-num">{{ onWayCount }}</text>
                    <text class="stat-label">接送中</text>
                </view>
            </view>
            <view class="stat-card">
                <view class="stat-icon">✅</view>
                <view class="stat-info">
                    <text class="stat-num">{{ atSchoolCount }}</text>
                    <text class="stat-label">已到校</text>
                </view>
            </view>
        </view>

        <view class="student-section">
            <view class="section-header">
                <text class="section-title">我的孩子</text>
                <view class="add-btn" @click="goBindStudent">
                    <text>+ 添加</text>
                </view>
            </view>

            <view class="student-list">
                <view 
                    v-for="student in students" 
                    :key="student.id" 
                    class="student-card"
                    @click="showStudentDetail(student)"
                >
                    <view class="student-header">
                        <view class="student-avatar">
                            <text>👦</text>
                        </view>
                        <view class="student-info">
                            <text class="student-name">{{ student.name }}</text>
                            <text class="student-school">{{ student.school }} {{ student.className }}</text>
                        </view>
                        <view class="status-badge" :class="student.status">
                            <text>{{ getStatusText(student.status) }}</text>
                        </view>
                    </view>

                    <view class="student-details">
                        <view class="detail-item">
                            <text class="detail-label">学号</text>
                            <text class="detail-value">{{ student.cardNo }}</text>
                        </view>
                        <view class="detail-item">
                            <text class="detail-label">路线</text>
                            <text class="detail-value">{{ student.route }}</text>
                        </view>
                        <view class="detail-item">
                            <text class="detail-label">车牌号</text>
                            <text class="detail-value">{{ student.busNo }}</text>
                        </view>
                    </view>

                    <view class="student-actions">
                        <view class="action-btn" @click.stop="locateBus(student)">
                            <text>📍 实时位置</text>
                        </view>
                        <view class="action-btn" @click.stop="contactDriver(student)">
                            <text>📞 联系司机</text>
                        </view>
                    </view>
                </view>
            </view>

            <view v-if="students.length === 0" class="empty-state">
                <text class="empty-icon">📭</text>
                <text class="empty-text">暂无绑定的学生</text>
                <view class="empty-btn" @click="goBindStudent">
                    <text>绑定学生</text>
                </view>
            </view>
        </view>

        <view class="announcement-section">
            <view class="section-header">
                <text class="section-title">📢 最新公告</text>
            </view>
            <view class="announcement-card" @click="showAnnouncement(announcements[0])">
                <view class="announcement-header">
                    <text class="announcement-title">{{ announcements[0].title }}</text>
                    <text class="announcement-time">{{ announcements[0].time }}</text>
                </view>
                <text class="announcement-content">{{ announcements[0].content }}</text>
            </view>
        </view>
    </view>
</template>

<script setup>
import { computed, ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { useUserStore, useStudentStore, useMessageStore } from '@/store'

const userStore = useUserStore()
const studentStore = useStudentStore()
const messageStore = useMessageStore()

const userInfo = ref({
    name: '张女士',
    phone: '138****8000'
})

const students = computed(() => studentStore.students)
const unreadCount = computed(() => messageStore.unreadCount)

const onWayCount = computed(() => students.value.filter(s => s.status === 'onway').length)
const atSchoolCount = computed(() => students.value.filter(s => s.status === 'atschool').length)

const greetingText = computed(() => {
    const hour = new Date().getHours()
    if (hour < 9) return '早上好'
    if (hour < 12) return '上午好'
    if (hour < 14) return '中午好'
    if (hour < 17) return '下午好'
    if (hour < 19) return '傍晚好'
    return '晚上好'
})

const announcements = ref([
    {
        id: 1,
        title: '关于冬季作息时间调整的通知',
        time: '2024-01-15',
        content: '根据季节变化，自11月1日起，校车接送时间调整为早上7:30，下午17:00，请家长提前做好准备。'
    }
])

function getStatusText(status) {
    const statusMap = {
        'onway': '接送中',
        'atschool': '已到校',
        'home': '已到家',
        'normal': '正常'
    }
    return statusMap[status] || '正常'
}

function showStudentDetail(student) {
    uni.showModal({
        title: student.name + ' 详情',
        content: `学校：${student.school}\n班级：${student.className}\n学号：${student.cardNo}\n路线：${student.route}\n车牌号：${student.busNo}`,
        showCancel: false
    })
}

function locateBus(student) {
    uni.showToast({
        title: '正在获取车辆位置...',
        icon: 'loading'
    })
    setTimeout(() => {
        uni.showModal({
            title: '车辆位置',
            content: `车辆 ${student.busNo} 当前位置：距学校约2.5公里，预计10分钟到达。`,
            showCancel: false
        })
    }, 1000)
}

function contactDriver(student) {
    uni.makePhoneCall({
        phoneNumber: '13900139000',
        fail: () => {
            uni.showToast({
                title: '拨号功能需要真机测试',
                icon: 'none'
            })
        }
    })
}

function goBindStudent() {
    uni.navigateTo({
        url: '/pages/parent/student-bind/student-bind'
    })
}

function goMessage() {
    uni.switchTab({
        url: '/pages/parent/message/message'
    })
}

function goMine() {
    uni.switchTab({
        url: '/pages/parent/mine/mine'
    })
}

function showAnnouncement(ann) {
    uni.showModal({
        title: ann.title,
        content: ann.content,
        showCancel: false
    })
}

onLoad(() => {
    console.log('家长首页加载')
})
</script>

<style lang="scss" scoped>
.home-page {
    min-height: 100vh;
    background: linear-gradient(180deg, #1E88E5 0%, #E3F2FD 30%);
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

.quick-stats {
    display: flex;
    gap: 20rpx;
    padding: 0 30rpx;
    margin-bottom: 30rpx;

    .stat-card {
        flex: 1;
        background: #FFFFFF;
        border-radius: 20rpx;
        padding: 30rpx 20rpx;
        display: flex;
        flex-direction: column;
        align-items: center;
        box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.06);

        .stat-icon {
            font-size: 48rpx;
            margin-bottom: 16rpx;
        }

        .stat-info {
            display: flex;
            flex-direction: column;
            align-items: center;

            .stat-num {
                font-size: 40rpx;
                font-weight: 700;
                color: #1E88E5;
                margin-bottom: 4rpx;
            }

            .stat-label {
                font-size: 22rpx;
                color: #999999;
            }
        }
    }
}

.student-section {
    padding: 0 30rpx;
    margin-bottom: 30rpx;

    .section-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20rpx;

        .section-title {
            font-size: 32rpx;
            font-weight: 600;
            color: #333333;
        }

        .add-btn {
            padding: 12rpx 24rpx;
            background: linear-gradient(135deg, #1E88E5 0%, #64B5F6 100%);
            border-radius: 30rpx;

            text {
                font-size: 24rpx;
                color: #FFFFFF;
            }
        }
    }

    .student-list {
        display: flex;
        flex-direction: column;
        gap: 20rpx;
    }

    .student-card {
        background: #FFFFFF;
        border-radius: 20rpx;
        padding: 30rpx;
        box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.06);

        .student-header {
            display: flex;
            align-items: center;
            margin-bottom: 24rpx;

            .student-avatar {
                width: 80rpx;
                height: 80rpx;
                background: #E3F2FD;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-right: 20rpx;
                font-size: 40rpx;
            }

            .student-info {
                flex: 1;
                display: flex;
                flex-direction: column;

                .student-name {
                    font-size: 32rpx;
                    font-weight: 600;
                    color: #333333;
                    margin-bottom: 4rpx;
                }

                .student-school {
                    font-size: 24rpx;
                    color: #999999;
                }
            }

            .status-badge {
                padding: 8rpx 20rpx;
                border-radius: 20rpx;

                text {
                    font-size: 22rpx;
                }

                &.onway {
                    background: #FFF3E0;
                    text { color: #FF9800; }
                }

                &.atschool {
                    background: #E8F5E9;
                    text { color: #4CAF50; }
                }

                &.home {
                    background: #E3F2FD;
                    text { color: #1E88E5; }
                }

                &.normal {
                    background: #F5F5F5;
                    text { color: #666666; }
                }
            }
        }

        .student-details {
            display: flex;
            gap: 40rpx;
            padding: 20rpx;
            background: #F8FAFC;
            border-radius: 12rpx;
            margin-bottom: 24rpx;

            .detail-item {
                display: flex;
                flex-direction: column;

                .detail-label {
                    font-size: 22rpx;
                    color: #999999;
                    margin-bottom: 4rpx;
                }

                .detail-value {
                    font-size: 26rpx;
                    color: #333333;
                    font-weight: 500;
                }
            }
        }

        .student-actions {
            display: flex;
            gap: 20rpx;

            .action-btn {
                flex: 1;
                height: 72rpx;
                border-radius: 36rpx;
                display: flex;
                align-items: center;
                justify-content: center;
                border: 2rpx solid #E0E0E0;

                text {
                    font-size: 26rpx;
                    color: #666666;
                }

                &:active {
                    background: #F5F5F5;
                }
            }
        }
    }

    .empty-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 80rpx 0;
        background: #FFFFFF;
        border-radius: 20rpx;

        .empty-icon {
            font-size: 80rpx;
            margin-bottom: 20rpx;
        }

        .empty-text {
            font-size: 28rpx;
            color: #999999;
            margin-bottom: 30rpx;
        }

        .empty-btn {
            padding: 16rpx 48rpx;
            background: linear-gradient(135deg, #1E88E5 0%, #64B5F6 100%);
            border-radius: 36rpx;

            text {
                font-size: 28rpx;
                color: #FFFFFF;
            }
        }
    }
}

.announcement-section {
    padding: 0 30rpx;

    .section-header {
        margin-bottom: 20rpx;

        .section-title {
            font-size: 32rpx;
            font-weight: 600;
            color: #333333;
        }
    }

    .announcement-card {
        background: #FFFFFF;
        border-radius: 20rpx;
        padding: 30rpx;
        box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.06);

        .announcement-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16rpx;

            .announcement-title {
                font-size: 28rpx;
                font-weight: 600;
                color: #333333;
                flex: 1;
            }

            .announcement-time {
                font-size: 22rpx;
                color: #999999;
            }
        }

        .announcement-content {
            font-size: 26rpx;
            color: #666666;
            line-height: 1.8;
            overflow: hidden;
            text-overflow: ellipsis;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
        }
    }
}
</style>
