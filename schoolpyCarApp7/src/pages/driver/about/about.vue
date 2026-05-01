<template>
    <view class="about-page">
        <view class="header-section">
            <view class="logo-area">
                <view class="logo-icon">
                    <text>🚌</text>
                </view>
                <text class="app-name">校园接送车</text>
                <text class="app-slogan">安全出行，快乐成长</text>
            </view>
            <view class="version-info">
                <text>司机端 v1.0.0</text>
            </view>
        </view>

        <view class="info-section">
            <view class="section-header">
                <text class="section-title">关于我们</text>
            </view>
            <view class="info-content">
                <text class="info-text">
                    校园接送车系统是一款专为学校和家长打造的智能接送管理平台。通过先进的GPS定位技术和实时通讯系统，实现学生上下学的全程监控，确保每位学生的安全出行。
                </text>
                <text class="info-text">
                    系统支持多角色协作，家长可实时查看孩子的接送状态，司机可高效管理路线和学生，学校可全面监控接送安全。
                </text>
            </view>
        </view>

        <view class="feature-section">
            <view class="section-header">
                <text class="section-title">核心功能</text>
            </view>
            <view class="feature-list">
                <view class="feature-item">
                    <view class="feature-icon">
                        <text>📍</text>
                    </view>
                    <view class="feature-info">
                        <text class="feature-title">实时定位</text>
                        <text class="feature-desc">GPS实时追踪车辆位置，随时掌握路线进度</text>
                    </view>
                </view>
                <view class="feature-item">
                    <view class="feature-icon">
                        <text>👶</text>
                    </view>
                    <view class="feature-info">
                        <text class="feature-title">学生管理</text>
                        <text class="feature-desc">上下车打卡确认，学生状态一目了然</text>
                    </view>
                </view>
                <view class="feature-item">
                    <view class="feature-icon">
                        <text>🔔</text>
                    </view>
                    <view class="feature-info">
                        <text class="feature-title">消息推送</text>
                        <text class="feature-desc">实时消息提醒，重要事件不遗漏</text>
                    </view>
                </view>
                <view class="feature-item">
                    <view class="feature-icon">
                        <text>🗺️</text>
                    </view>
                    <view class="feature-info">
                        <text class="feature-title">路线规划</text>
                        <text class="feature-desc">智能路线优化，提高接送效率</text>
                    </view>
                </view>
                <view class="feature-item">
                    <view class="feature-icon">
                        <text>🚨</text>
                    </view>
                    <view class="feature-info">
                        <text class="feature-title">紧急呼叫</text>
                        <text class="feature-desc">一键紧急呼救，快速响应保障安全</text>
                    </view>
                </view>
                <view class="feature-item">
                    <view class="feature-icon">
                        <text>📊</text>
                    </view>
                    <view class="feature-info">
                        <text class="feature-title">数据统计</text>
                        <text class="feature-desc">工作数据统计，绩效一目了然</text>
                    </view>
                </view>
            </view>
        </view>

        <view class="contact-section">
            <view class="section-header">
                <text class="section-title">联系我们</text>
            </view>
            <view class="contact-list">
                <view class="contact-item" @click="callPhone('4001234567')">
                    <view class="contact-icon">
                        <text>📞</text>
                    </view>
                    <view class="contact-info">
                        <text class="contact-label">客服热线</text>
                        <text class="contact-value">400-123-4567</text>
                    </view>
                    <view class="contact-arrow">
                        <text>›</text>
                    </view>
                </view>
                <view class="contact-item" @click="callPhone('13800008888')">
                    <view class="contact-icon">
                        <text>🚨</text>
                    </view>
                    <view class="contact-info">
                        <text class="contact-label">紧急联系</text>
                        <text class="contact-value">138-0000-8888</text>
                    </view>
                    <view class="contact-arrow">
                        <text>›</text>
                    </view>
                </view>
                <view class="contact-item">
                    <view class="contact-icon">
                        <text>📧</text>
                    </view>
                    <view class="contact-info">
                        <text class="contact-label">电子邮箱</text>
                        <text class="contact-value">service@schoolbus.com</text>
                    </view>
                </view>
                <view class="contact-item">
                    <view class="contact-icon">
                        <text>🏢</text>
                    </view>
                    <view class="contact-info">
                        <text class="contact-label">公司地址</text>
                        <text class="contact-value">北京市海淀区中关村科技园</text>
                    </view>
                </view>
            </view>
        </view>

        <view class="agreement-section">
            <view class="agreement-item" @click="showAgreement('user')">
                <text class="agreement-text">用户协议</text>
                <view class="agreement-arrow">
                    <text>›</text>
                </view>
            </view>
            <view class="agreement-item" @click="showAgreement('privacy')">
                <text class="agreement-text">隐私政策</text>
                <view class="agreement-arrow">
                    <text>›</text>
                </view>
            </view>
        </view>

        <view class="copyright-section">
            <text class="copyright-text">Copyright © 2024 校园接送车系统</text>
            <text class="copyright-text">All Rights Reserved</text>
        </view>
    </view>
</template>

<script setup>
import { onLoad } from '@dcloudio/uni-app'

function callPhone(phoneNumber) {
    uni.showModal({
        title: '拨打电话',
        content: `确定要拨打 ${phoneNumber} 吗？`,
        success: (res) => {
            if (res.confirm) {
                uni.makePhoneCall({
                    phoneNumber: phoneNumber,
                    fail: () => {
                        uni.showToast({
                            title: '拨号功能需真机测试',
                            icon: 'none'
                        })
                    }
                })
            }
        }
    })
}

function showAgreement(type) {
    let title = ''
    let content = ''

    if (type === 'user') {
        title = '用户协议'
        content = `一、服务说明
1. 校园接送车系统（以下简称"本系统"）是一款专为学校、家长和司机提供的智能接送管理平台。
2. 本系统提供的服务包括但不限于：实时定位追踪、学生上下车打卡、消息推送、路线规划等。

二、用户权利与义务
1. 用户有权使用本系统提供的各项服务。
2. 用户应保证提供的个人信息真实、准确、完整。
3. 用户应妥善保管自己的账号密码，不得转借他人使用。

三、服务条款
1. 本系统保留随时修改服务内容的权利。
2. 如遇系统维护，本系统将提前通知用户。
3. 因不可抗力导致的服务中断，本系统不承担责任。

四、联系方式
如有任何问题，请联系客服：400-123-4567`
    } else {
        title = '隐私政策'
        content = `一、信息收集
1. 本系统会收集用户的基本信息，包括姓名、联系方式、学生信息等。
2. 本系统会收集位置信息，用于实时定位和路线追踪功能。

二、信息使用
1. 收集的信息仅用于提供系统服务，不会泄露给第三方。
2. 位置信息仅在接送时段收集，非工作时间不会追踪。

三、信息保护
1. 本系统采用加密技术保护用户信息安全。
2. 本系统会定期更新安全措施，确保数据安全。

四、用户权利
1. 用户有权查看、修改自己的个人信息。
2. 用户有权要求删除不再需要的信息。

五、联系方式
如有隐私相关问题，请联系：service@schoolbus.com`
    }

    uni.showModal({
        title: title,
        content: content,
        showCancel: false,
        confirmText: '已知晓'
    })
}

onLoad(() => {
    console.log('关于页面加载')
})
</script>

<style lang="scss" scoped>
.about-page {
    min-height: 100vh;
    background: #F5F7FA;
    padding-bottom: 40rpx;
}

.header-section {
    background: linear-gradient(135deg, #4CAF50 0%, #81C784 100%);
    padding: 60rpx 30rpx 50rpx;
    display: flex;
    flex-direction: column;
    align-items: center;

    .logo-area {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-bottom: 30rpx;

        .logo-icon {
            width: 140rpx;
            height: 140rpx;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 20rpx;
            font-size: 72rpx;
            box-shadow: 0 8rpx 24rpx rgba(0, 0, 0, 0.1);
        }

        .app-name {
            font-size: 40rpx;
            font-weight: 700;
            color: #FFFFFF;
            margin-bottom: 8rpx;
        }

        .app-slogan {
            font-size: 26rpx;
            color: rgba(255, 255, 255, 0.85);
        }
    }

    .version-info {
        padding: 10rpx 28rpx;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 30rpx;

        text {
            font-size: 24rpx;
            color: #FFFFFF;
        }
    }
}

.info-section,
.feature-section,
.contact-section {
    background: #FFFFFF;
    margin: 20rpx 30rpx;
    border-radius: 20rpx;
    padding: 30rpx;

    .section-header {
        margin-bottom: 20rpx;
        padding-bottom: 16rpx;
        border-bottom: 1rpx solid #F0F0F0;

        .section-title {
            font-size: 30rpx;
            font-weight: 600;
            color: #333333;
        }
    }
}

.info-section {
    .info-content {
        .info-text {
            display: block;
            font-size: 26rpx;
            color: #666666;
            line-height: 1.8;
            margin-bottom: 16rpx;

            &:last-child {
                margin-bottom: 0;
            }
        }
    }
}

.feature-section {
    .feature-list {
        .feature-item {
            display: flex;
            align-items: center;
            padding: 20rpx 0;
            border-bottom: 1rpx solid #F5F5F5;

            &:last-child {
                border-bottom: none;
            }

            .feature-icon {
                width: 72rpx;
                height: 72rpx;
                background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
                border-radius: 16rpx;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-right: 20rpx;
                font-size: 36rpx;
            }

            .feature-info {
                flex: 1;
                display: flex;
                flex-direction: column;

                .feature-title {
                    font-size: 28rpx;
                    font-weight: 500;
                    color: #333333;
                    margin-bottom: 6rpx;
                }

                .feature-desc {
                    font-size: 24rpx;
                    color: #999999;
                }
            }
        }
    }
}

.contact-section {
    .contact-list {
        .contact-item {
            display: flex;
            align-items: center;
            padding: 20rpx 0;
            border-bottom: 1rpx solid #F5F5F5;

            &:last-child {
                border-bottom: none;
            }

            &:active {
                background: #F8FAFC;
                margin: 0 -30rpx;
                padding: 20rpx 30rpx;
            }

            .contact-icon {
                width: 64rpx;
                height: 64rpx;
                background: #F8FAFC;
                border-radius: 12rpx;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-right: 16rpx;
                font-size: 32rpx;
            }

            .contact-info {
                flex: 1;
                display: flex;
                flex-direction: column;

                .contact-label {
                    font-size: 24rpx;
                    color: #999999;
                    margin-bottom: 4rpx;
                }

                .contact-value {
                    font-size: 28rpx;
                    color: #333333;
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
}

.agreement-section {
    background: #FFFFFF;
    margin: 20rpx 30rpx;
    border-radius: 20rpx;
    overflow: hidden;

    .agreement-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 30rpx;
        border-bottom: 1rpx solid #F5F5F5;

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
            text {
                font-size: 36rpx;
                color: #CCCCCC;
            }
        }
    }
}

.copyright-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40rpx 0;

    .copyright-text {
        font-size: 22rpx;
        color: #CCCCCC;
        margin-bottom: 8rpx;

        &:last-child {
            margin-bottom: 0;
        }
    }
}
</style>
