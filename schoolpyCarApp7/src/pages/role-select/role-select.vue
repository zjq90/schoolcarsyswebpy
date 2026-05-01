<template>
    <view class="role-select-page">
        <view class="header">
            <view class="logo">
                <view class="logo-icon">🚍</view>
            </view>
            <text class="app-name">校园接送车</text>
            <text class="app-desc">安全出行，家校连心</text>
        </view>

        <view class="role-cards">
            <view class="role-card parent" @click="selectRole('parent')">
                <view class="role-icon">👨‍👩‍👧</view>
                <text class="role-title">家长端</text>
                <text class="role-desc">查看孩子接送状态，接收消息通知</text>
                <view class="role-arrow">
                    <text>→</text>
                </view>
            </view>

            <view class="role-card driver" @click="selectRole('driver')">
                <view class="role-icon">👨‍✈️</view>
                <text class="role-title">司机端</text>
                <text class="role-desc">打卡上下班，查看路线规划，接收调度</text>
                <view class="role-arrow">
                    <text>→</text>
                </view>
            </view>
        </view>

        <view class="footer">
            <text class="footer-text">© 2024 校园接送车管理系统</text>
        </view>
    </view>
</template>

<script setup>
import { useUserStore } from '@/store'

const userStore = useUserStore()

function selectRole(role) {
    userStore.setUserType(role)
    if (role === 'parent') {
        uni.navigateTo({
            url: '/pages/parent/login/login'
        })
    } else {
        uni.navigateTo({
            url: '/pages/driver/login/login'
        })
    }
}
</script>

<style lang="scss" scoped>
.role-select-page {
    min-height: 100vh;
    background: linear-gradient(180deg, #E3F2FD 0%, #FFFFFF 100%);
    padding: 0 40rpx;
    display: flex;
    flex-direction: column;
}

.header {
    padding-top: 120rpx;
    padding-bottom: 80rpx;
    text-align: center;

    .logo {
        margin-bottom: 30rpx;

        .logo-icon {
            width: 160rpx;
            height: 160rpx;
            background: linear-gradient(135deg, #1E88E5 0%, #64B5F6 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto;
            font-size: 80rpx;
            box-shadow: 0 12rpx 40rpx rgba(30, 136, 229, 0.3);
        }
    }

    .app-name {
        display: block;
        font-size: 48rpx;
        font-weight: 600;
        color: #1E88E5;
        margin-bottom: 16rpx;
    }

    .app-desc {
        display: block;
        font-size: 28rpx;
        color: #666666;
    }
}

.role-cards {
    flex: 1;
    padding-bottom: 60rpx;
}

.role-card {
    background: #FFFFFF;
    border-radius: 24rpx;
    padding: 40rpx;
    margin-bottom: 30rpx;
    position: relative;
    overflow: hidden;
    box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.08);
    transition: transform 0.2s, box-shadow 0.2s;

    &:active {
        transform: scale(0.98);
        box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.05);
    }

    &.parent::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 8rpx;
        height: 100%;
        background: linear-gradient(180deg, #1E88E5 0%, #64B5F6 100%);
    }

    &.driver::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 8rpx;
        height: 100%;
        background: linear-gradient(180deg, #4CAF50 0%, #81C784 100%);
    }

    .role-icon {
        font-size: 60rpx;
        margin-bottom: 20rpx;
    }

    .role-title {
        display: block;
        font-size: 36rpx;
        font-weight: 600;
        color: #333333;
        margin-bottom: 12rpx;
    }

    .role-desc {
        display: block;
        font-size: 26rpx;
        color: #999999;
        padding-right: 60rpx;
    }

    .role-arrow {
        position: absolute;
        right: 40rpx;
        top: 50%;
        transform: translateY(-50%);
        width: 60rpx;
        height: 60rpx;
        background: linear-gradient(135deg, #1E88E5 0%, #64B5F6 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;

        text {
            color: #FFFFFF;
            font-size: 32rpx;
            font-weight: 600;
        }
    }

    &.driver .role-arrow {
        background: linear-gradient(135deg, #4CAF50 0%, #81C784 100%);
    }
}

.footer {
    padding-bottom: 40rpx;
    text-align: center;

    .footer-text {
        font-size: 24rpx;
        color: #CCCCCC;
    }
}
</style>
