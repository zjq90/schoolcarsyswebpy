<template>
    <view class="mine-page">
        <view class="user-card">
            <view class="avatar-area">
                <view class="avatar">
                    <text>👩</text>
                </view>
                <view class="user-info">
                    <text class="user-name">{{ userInfo.name }}</text>
                    <text class="user-phone">{{ userInfo.phone }}</text>
                </view>
                <view class="edit-btn" @click="goEditProfile">
                    <text>编辑</text>
                </view>
            </view>

            <view class="stats-row">
                <view class="stat-item" @click="goStudentManage">
                    <text class="stat-num">{{ studentCount }}</text>
                    <text class="stat-label">绑定学生</text>
                </view>
                <view class="stat-item" @click="goMessage">
                    <text class="stat-num">{{ unreadCount }}</text>
                    <text class="stat-label">未读消息</text>
                </view>
                <view class="stat-item">
                    <text class="stat-num">30</text>
                    <text class="stat-label">积分</text>
                </view>
            </view>
        </view>

        <view class="menu-section">
            <view class="menu-group">
                <view class="menu-item" @click="goStudentManage">
                    <view class="menu-icon student">
                        <text>👶</text>
                    </view>
                    <text class="menu-text">学生管理</text>
                    <view class="menu-arrow">
                        <text>›</text>
                    </view>
                </view>

                <view class="menu-item" @click="goComplaint">
                    <view class="menu-icon complaint">
                        <text>💬</text>
                    </view>
                    <text class="menu-text">投诉建议</text>
                    <view class="menu-arrow">
                        <text>›</text>
                    </view>
                </view>

                <view class="menu-item" @click="goAbout">
                    <view class="menu-icon about">
                        <text>ℹ️</text>
                    </view>
                    <text class="menu-text">关于我们</text>
                    <view class="menu-arrow">
                        <text>›</text>
                    </view>
                </view>
            </view>

            <view class="menu-group">
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
import { useUserStore, useStudentStore, useMessageStore } from '@/store'

const userStore = useUserStore()
const studentStore = useStudentStore()
const messageStore = useMessageStore()

const userInfo = ref({
    name: '张女士',
    phone: '138****8000'
})

const studentCount = computed(() => studentStore.students.length)
const unreadCount = computed(() => messageStore.unreadCount)

function goEditProfile() {
    uni.showToast({
        title: '编辑功能开发中',
        icon: 'none'
    })
}

function goStudentManage() {
    uni.navigateTo({
        url: '/pages/parent/student-bind/student-bind'
    })
}

function goMessage() {
    uni.switchTab({
        url: '/pages/parent/message/message'
    })
}

function goComplaint() {
    uni.navigateTo({
        url: '/pages/parent/complaint/complaint'
    })
}

function goAbout() {
    uni.navigateTo({
        url: '/pages/parent/about/about'
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
        content: '如有问题请联系客服：400-123-4567\n工作时间：周一至周五 9:00-18:00',
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
    console.log('个人页加载')
})

onShow(() => {
    console.log('个人页显示')
})
</script>

<style lang="scss" scoped>
.mine-page {
    min-height: 100vh;
    background: #F5F7FA;
    padding-bottom: 40rpx;
}

.user-card {
    background: linear-gradient(135deg, #1E88E5 0%, #64B5F6 100%);
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

                &.student { background: #E3F2FD; }
                &.complaint { background: #FFF3E0; }
                &.about { background: #E8F5E9; }
                &.settings { background: #F3E5F5; }
                &.help { background: #FFF8E1; }
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
