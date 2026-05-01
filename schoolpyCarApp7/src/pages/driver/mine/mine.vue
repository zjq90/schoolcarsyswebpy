<template>
    <view class="mine-page">
        <view class="user-card">
            <view class="avatar-area">
                <view class="avatar">
                    <text>👨‍✈️</text>
                </view>
                <view class="user-info">
                    <text class="user-name">{{ userInfo.name }}</text>
                    <text class="user-phone">{{ userInfo.phone }}</text>
                    <view class="driver-badge">
                        <text>认证司机</text>
                    </view>
                </view>
                <view class="edit-btn" @click="goEditProfile">
                    <text>编辑</text>
                </view>
            </view>

            <view class="stats-row">
                <view class="stat-item" @click="showDriverInfo">
                    <text class="stat-num">{{ driverStats.days }}</text>
                    <text class="stat-label">工作天数</text>
                </view>
                <view class="stat-item" @click="goMessage">
                    <text class="stat-num">{{ unreadCount }}</text>
                    <text class="stat-label">未读消息</text>
                </view>
                <view class="stat-item">
                    <text class="stat-num">{{ driverStats.students }}</text>
                    <text class="stat-label">接送学生</text>
                </view>
            </view>
        </view>

        <view class="menu-section">
            <view class="menu-group">
                <view class="menu-item" @click="showDriverInfo">
                    <view class="menu-icon info">
                        <text>📋</text>
                    </view>
                    <text class="menu-text">个人信息</text>
                    <view class="menu-arrow">
                        <text>›</text>
                    </view>
                </view>

                <view class="menu-item" @click="goFeedback">
                    <view class="menu-icon feedback">
                        <text>✅</text>
                    </view>
                    <text class="menu-text">处理结果反馈</text>
                    <view class="menu-arrow">
                        <text>›</text>
                    </view>
                </view>

                <view class="menu-item" @click="goMaintenance">
                    <view class="menu-icon maintenance">
                        <text>🔧</text>
                    </view>
                    <text class="menu-text">车辆保养反馈</text>
                    <view class="menu-arrow">
                        <text>›</text>
                    </view>
                </view>

                <view class="menu-item" @click="goEmergency">
                    <view class="menu-icon emergency">
                        <text>🚨</text>
                    </view>
                    <text class="menu-text">紧急状况申请</text>
                    <view class="menu-arrow">
                        <text>›</text>
                    </view>
                </view>
            </view>

            <view class="menu-group">
                <view class="menu-item" @click="goAbout">
                    <view class="menu-icon about">
                        <text>ℹ️</text>
                    </view>
                    <text class="menu-text">关于我们</text>
                    <view class="menu-arrow">
                        <text>›</text>
                    </view>
                </view>

                <view class="menu-item" @click="goSettings">
                    <view class="menu-icon settings">
                        <text>⚙️</text>
                    </view>
                    <text class="menu-text">设置</text>
                    <view class="menu-arrow">
                        <text>›</text>
                    </view>
                </view>

                <view class="menu-item" @click="showHelp">
                    <view class="menu-icon help">
                        <text>❓</text>
                    </view>
                    <text class="menu-text">帮助中心</text>
                    <view class="menu-arrow">
                        <text>›</text>
                    </view>
                </view>
            </view>
        </view>

        <view class="logout-section">
            <view class="logout-btn" @click="handleLogout">
                <text>退出登录</text>
            </view>
        </view>

        <view class="version-info">
            <text>版本 v1.0.0</text>
        </view>
    </view>
</template>

<script setup>
import { ref, computed } from 'vue'
import { onLoad, onShow } from '@dcloudio/uni-app'
import { useUserStore, useMessageStore } from '@/store'

const userStore = useUserStore()
const messageStore = useMessageStore()

const userInfo = ref({
    name: '王师傅',
    phone: '139****0000',
    driverId: 'DRV20240001',
    license: 'A1证'
})

const driverStats = ref({
    days: 156,
    students: 248,
    routes: 624
})

const unreadCount = computed(() => {
    return messageStore.driverMessages.filter(m => !m.read).length
})

function goEditProfile() {
    uni.showToast({
        title: '编辑功能开发中',
        icon: 'none'
    })
}

function showDriverInfo() {
    uni.showModal({
        title: '司机信息',
        content: `姓名：${userInfo.value.name}\n手机号：${userInfo.value.phone}\n司机编号：${userInfo.value.driverId}\n驾照类型：${userInfo.value.license}\n工作天数：${driverStats.value.days}天\n接送学生：${driverStats.value.students}人次`,
        showCancel: false
    })
}

function goMessage() {
    uni.navigateTo({
        url: '/pages/driver/message/message'
    })
}

function goFeedback() {
    uni.navigateTo({
        url: '/pages/driver/feedback/feedback'
    })
}

function goMaintenance() {
    uni.navigateTo({
        url: '/pages/driver/maintenance/maintenance'
    })
}

function goEmergency() {
    uni.navigateTo({
        url: '/pages/driver/emergency/emergency'
    })
}

function goAbout() {
    uni.navigateTo({
        url: '/pages/driver/about/about'
    })
}

function goSettings() {
    uni.showToast({
        title: '设置功能开发中',
        icon: 'none'
    })
}

function showHelp() {
    uni.showModal({
        title: '帮助中心',
        content: '如有问题请联系调度中心：400-123-4567\n工作时间：全天24小时\n紧急联系：138-0000-8888',
        showCancel: false
    })
}

function handleLogout() {
    uni.showModal({
        title: '提示',
        content: '确定要退出登录吗？',
        success: (res) => {
            if (res.confirm) {
                userStore.logout()
                uni.navigateTo({
                    url: '/pages/role-select/role-select'
                })
            }
        }
    })
}

onLoad(() => {
    console.log('司机个人页加载')
})

onShow(() => {
    console.log('司机个人页显示')
})
</script>

<style lang="scss" scoped>
.mine-page {
    min-height: 100vh;
    background: #F5F7FA;
    padding-bottom: 40rpx;
}

.user-card {
    background: linear-gradient(135deg, #4CAF50 0%, #81C784 100%);
    padding: 40rpx 30rpx 30rpx;
    border-radius: 0 0 40rpx 40rpx;

    .avatar-area {
        display: flex;
        align-items: center;
        margin-bottom: 40rpx;

        .avatar {
            width: 120rpx;
            height: 120rpx;
            background: rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 24rpx;
            font-size: 56rpx;
            border: 4rpx solid rgba(255, 255, 255, 0.5);
        }

        .user-info {
            flex: 1;
            display: flex;
            flex-direction: column;

            .user-name {
                font-size: 36rpx;
                font-weight: 600;
                color: #FFFFFF;
                margin-bottom: 8rpx;
            }

            .user-phone {
                font-size: 26rpx;
                color: rgba(255, 255, 255, 0.8);
                margin-bottom: 12rpx;
            }

            .driver-badge {
                display: inline-flex;
                align-self: flex-start;
                padding: 4rpx 16rpx;
                background: rgba(255, 255, 255, 0.3);
                border-radius: 20rpx;

                text {
                    font-size: 20rpx;
                    color: #FFFFFF;
                }
            }
        }

        .edit-btn {
            padding: 12rpx 28rpx;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 30rpx;

            text {
                font-size: 26rpx;
                color: #FFFFFF;
            }
        }
    }

    .stats-row {
        display: flex;
        background: rgba(255, 255, 255, 0.15);
        border-radius: 20rpx;
        padding: 24rpx 0;

        .stat-item {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;

            .stat-num {
                font-size: 40rpx;
                font-weight: 700;
                color: #FFFFFF;
                margin-bottom: 8rpx;
            }

            .stat-label {
                font-size: 24rpx;
                color: rgba(255, 255, 255, 0.8);
            }
        }
    }
}

.menu-section {
    padding: 30rpx;
    margin-top: 20rpx;

    .menu-group {
        background: #FFFFFF;
        border-radius: 20rpx;
        margin-bottom: 20rpx;
        overflow: hidden;
        box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.05);

        .menu-item {
            display: flex;
            align-items: center;
            padding: 30rpx;
            border-bottom: 1rpx solid #F5F7FA;

            &:last-child {
                border-bottom: none;
            }

            &:active {
                background: #F5F7FA;
            }

            .menu-icon {
                width: 72rpx;
                height: 72rpx;
                border-radius: 16rpx;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-right: 20rpx;
                font-size: 36rpx;

                &.info { background: #E8F5E9; }
                &.feedback { background: #E3F2FD; }
                &.maintenance { background: #FFF3E0; }
                &.emergency { background: #FFEBEE; }
                &.about { background: #F3E5F5; }
                &.settings { background: #FFF8E1; }
                &.help { background: #E0F7FA; }
            }

            .menu-text {
                flex: 1;
                font-size: 30rpx;
                color: #333333;
            }

            .menu-arrow {
                text {
                    font-size: 40rpx;
                    color: #CCCCCC;
                }
            }
        }
    }
}

.logout-section {
    padding: 0 30rpx;
    margin-top: 40rpx;

    .logout-btn {
        height: 88rpx;
        background: #FFFFFF;
        border-radius: 44rpx;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 2rpx solid #FFCDD2;

        text {
            font-size: 30rpx;
            color: #F44336;
        }

        &:active {
            background: #FFEBEE;
        }
    }
}

.version-info {
    text-align: center;
    margin-top: 40rpx;
    padding-bottom: 40rpx;

    text {
        font-size: 24rpx;
        color: #CCCCCC;
    }
}
</style>
