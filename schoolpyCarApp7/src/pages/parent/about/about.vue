<template>
    <view class="about-page">
        <view class="app-info">
            <view class="app-logo">
                <text>🚍</text>
            </view>
            <text class="app-name">校园接送车</text>
            <text class="app-version">版本 v1.0.0</text>
        </view>

        <view class="about-content">
            <view class="about-section">
                <view class="section-header">
                    <text class="section-title">关于我们</text>
                </view>
                <text class="section-content">
                    校园接送车是一款专为学生上下学打造的安全接送管理平台。我们致力于为家长提供实时、便捷的孩子接送状态查询服务，让家长放心，让学校省心。
                </text>
            </view>

            <view class="about-section">
                <view class="section-header">
                    <text class="section-title">核心功能</text>
                </view>
                <view class="feature-list">
                    <view class="feature-item">
                        <view class="feature-icon">👶</view>
                        <view class="feature-info">
                            <text class="feature-title">多学生绑定</text>
                            <text class="feature-desc">支持绑定多个孩子信息</text>
                        </view>
                    </view>
                    <view class="feature-item">
                        <view class="feature-icon">📍</view>
                        <view class="feature-info">
                            <text class="feature-title">实时位置</text>
                            <text class="feature-desc">车辆实时位置追踪</text>
                        </view>
                    </view>
                    <view class="feature-item">
                        <view class="feature-icon">🔔</view>
                        <view class="feature-info">
                            <text class="feature-title">消息推送</text>
                            <text class="feature-desc">及时接收各类通知</text>
                        </view>
                    </view>
                    <view class="feature-item">
                        <view class="feature-icon">📞</view>
                        <view class="feature-info">
                            <text class="feature-title">一键联系</text>
                            <text class="feature-desc">快速联系司机/老师</text>
                        </view>
                    </view>
                </view>
            </view>
        </view>

        <view class="contact-section">
            <view class="section-header">
                <text class="section-title">联系我们</text>
            </view>
            <view class="contact-list">
                <view class="contact-item" @click="makeCall('400-123-4567')">
                    <view class="contact-icon phone">
                        <text>📞</text>
                    </view>
                    <view class="contact-info">
                        <text class="contact-title">客服热线</text>
                        <text class="contact-value">400-123-4567</text>
                    </view>
                    <view class="contact-arrow">
                        <text>›</text>
                    </view>
                </view>
                <view class="contact-item" @click="makeCall('service@schoolcar.com')">
                    <view class="contact-icon email">
                        <text>📧</text>
                    </view>
                    <view class="contact-info">
                        <text class="contact-title">客服邮箱</text>
                        <text class="contact-value">service@schoolcar.com</text>
                    </view>
                    <view class="contact-arrow">
                        <text>›</text>
                    </view>
                </view>
                <view class="contact-item">
                    <view class="contact-icon work">
                        <text>🕐</text>
                    </view>
                    <view class="contact-info">
                        <text class="contact-title">工作时间</text>
                        <text class="contact-value">周一至周五 9:00-18:00</text>
                    </view>
                </view>
            </view>
        </view>

        <view class="agreement-section">
            <view class="agreement-item" @click="showAgreement">
                <text class="agreement-text">用户协议</text>
                <text class="agreement-arrow">›</text>
            </view>
            <view class="agreement-item" @click="showPrivacy">
                <text class="agreement-text">隐私政策</text>
                <text class="agreement-arrow">›</text>
            </view>
        </view>

        <view class="copyright">
            <text>© 2024 校园接送车管理系统</text>
            <text>All Rights Reserved</text>
        </view>
    </view>
</template>

<script setup>
import { onLoad } from '@dcloudio/uni-app'

function makeCall(phone) {
    if (phone.includes('@')) {
        uni.showToast({
            title: '邮件功能开发中',
            icon: 'none'
        })
        return
    }
    
    uni.makePhoneCall({
        phoneNumber: phone.replace('-', ''),
        fail: () => {
            uni.showToast({
                title: '拨号功能需要真机测试',
                icon: 'none'
            })
        }
    })
}

function showAgreement() {
    uni.showModal({
        title: '用户协议',
        content: `一、服务说明
本平台提供学生接送信息查询服务，包括车辆位置追踪、消息通知等功能。

二、用户注册
用户需提供真实、准确的个人信息进行注册。

三、服务使用
用户应合法使用本平台服务，不得进行任何违法活动。

四、隐私保护
我们严格保护用户隐私，不会向第三方泄露用户信息。

五、免责声明
因不可抗力导致的服务中断，本平台不承担责任。`,
        showCancel: false
    })
}

function showPrivacy() {
    uni.showModal({
        title: '隐私政策',
        content: `我们非常重视您的隐私保护。

一、信息收集
我们仅收集必要的个人信息用于提供服务，包括手机号、学生信息等。

二、信息使用
收集的信息仅用于提供接送服务相关功能，不会用于其他商业用途。

三、信息保护
我们采用加密技术保护您的个人信息安全。

四、信息共享
未经您的同意，我们不会向任何第三方分享您的个人信息。

五、您的权利
您有权随时查询、更正或删除您的个人信息。`,
        showCancel: false
    })
}

onLoad(() => {
    console.log('关于页加载')
})
</script>

<style lang="scss" scoped>
.about-page {
    min-height: 100vh;
    background: #F5F7FA;
    padding-bottom: 40rpx;
}

.app-info {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 60rpx 0;
    background: linear-gradient(180deg, #1E88E5 0%, #64B5F6 100%);

    .app-logo {
        width: 160rpx;
        height: 160rpx;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 24rpx;
        font-size: 80rpx;
        border: 4rpx solid rgba(255, 255, 255, 0.4);
    }

    .app-name {
        font-size: 40rpx;
        font-weight: 600;
        color: #FFFFFF;
        margin-bottom: 12rpx;
    }

    .app-version {
        font-size: 26rpx;
        color: rgba(255, 255, 255, 0.8);
    }
}

.about-content {
    padding: 30rpx;
}

.about-section {
    background: #FFFFFF;
    border-radius: 20rpx;
    padding: 30rpx;
    margin-bottom: 20rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.05);

    .section-header {
        margin-bottom: 20rpx;
    }

    .section-title {
        font-size: 32rpx;
        font-weight: 600;
        color: #333333;
    }

    .section-content {
        font-size: 28rpx;
        color: #666666;
        line-height: 1.8;
    }
}

.feature-list {
    display: flex;
    flex-wrap: wrap;
    gap: 20rpx;
}

.feature-item {
    width: calc(50% - 10rpx);
    display: flex;
    align-items: center;
    padding: 24rpx;
    background: #F8FAFC;
    border-radius: 16rpx;

    .feature-icon {
        width: 72rpx;
        height: 72rpx;
        background: linear-gradient(135deg, #1E88E5 0%, #64B5F6 100%);
        border-radius: 16rpx;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 16rpx;
        font-size: 36rpx;
    }

    .feature-info {
        display: flex;
        flex-direction: column;

        .feature-title {
            font-size: 28rpx;
            font-weight: 500;
            color: #333333;
            margin-bottom: 4rpx;
        }

        .feature-desc {
            font-size: 22rpx;
            color: #999999;
        }
    }
}

.contact-section {
    background: #FFFFFF;
    margin: 0 30rpx 20rpx;
    border-radius: 20rpx;
    padding: 30rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.05);

    .section-header {
        margin-bottom: 20rpx;
    }

    .section-title {
        font-size: 32rpx;
        font-weight: 600;
        color: #333333;
    }
}

.contact-list {
    .contact-item {
        display: flex;
        align-items: center;
        padding: 24rpx 0;
        border-bottom: 1rpx solid #F0F0F0;

        &:last-child {
            border-bottom: none;
        }

        &:active {
            background: #F8FAFC;
            margin: 0 -30rpx;
            padding: 24rpx 30rpx;
        }

        .contact-icon {
            width: 64rpx;
            height: 64rpx;
            border-radius: 12rpx;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 20rpx;
            font-size: 32rpx;

            &.phone { background: #E3F2FD; }
            &.email { background: #FFF3E0; }
            &.work { background: #E8F5E9; }
        }

        .contact-info {
            flex: 1;
            display: flex;
            flex-direction: column;

            .contact-title {
                font-size: 28rpx;
                color: #333333;
                margin-bottom: 4rpx;
            }

            .contact-value {
                font-size: 24rpx;
                color: #999999;
            }
        }

        .contact-arrow {
            text {
                font-size: 36rpx;
                color: #CCCCCC;
            }
        }
    }
}

.agreement-section {
    background: #FFFFFF;
    margin: 0 30rpx 30rpx;
    border-radius: 20rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.05);

    .agreement-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 30rpx;
        border-bottom: 1rpx solid #F0F0F0;

        &:last-child {
            border-bottom: none;
        }

        &:active {
            background: #F8FAFC;
        }

        .agreement-text {
            font-size: 28rpx;
            color: #333333;
        }

        .agreement-arrow {
            font-size: 36rpx;
            color: #CCCCCC;
        }
    }
}

.copyright {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20rpx 0;

    text {
        font-size: 22rpx;
        color: #CCCCCC;
        margin-bottom: 8rpx;
    }
}
</style>
