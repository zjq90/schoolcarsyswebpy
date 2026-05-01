<template>
    <view class="login-page">
        <view class="header">
            <view class="back-btn" @click="goBack">
                <text>←</text>
            </view>
            <view class="logo-area">
                <view class="logo-icon">👨‍👩‍👧</view>
                <text class="title">家长端登录</text>
                <text class="subtitle">安全守护，家校连心</text>
            </view>
        </view>

        <view class="login-tabs">
            <view 
                class="tab-item" 
                :class="{ active: loginType === 'password' }"
                @click="loginType = 'password'"
            >
                <text>密码登录</text>
            </view>
            <view 
                class="tab-item" 
                :class="{ active: loginType === 'code' }"
                @click="loginType = 'code'"
            >
                <text>验证码登录</text>
            </view>
        </view>

        <view class="login-form">
            <view class="input-group">
                <view class="input-prefix">📱</view>
                <input 
                    type="number" 
                    v-model="form.phone" 
                    placeholder="请输入手机号" 
                    maxlength="11"
                />
            </view>

            <view v-if="loginType === 'password'" class="input-group">
                <view class="input-prefix">🔒</view>
                <input 
                    :type="showPassword ? 'text' : 'password'" 
                    v-model="form.password" 
                    placeholder="请输入密码" 
                    maxlength="16"
                />
                <view class="input-suffix" @click="showPassword = !showPassword">
                    <text>{{ showPassword ? '🙈' : '👁️' }}</text>
                </view>
            </view>

            <view v-if="loginType === 'code'" class="input-group">
                <view class="input-prefix">🔑</view>
                <input 
                    type="number" 
                    v-model="form.code" 
                    placeholder="请输入验证码" 
                    maxlength="6"
                />
                <view class="code-btn" :class="{ disabled: countdown > 0 }" @click="sendCode">
                    <text>{{ countdown > 0 ? countdown + 's' : '获取验证码' }}</text>
                </view>
            </view>

            <view v-if="loginType === 'password'" class="forgot-password">
                <text class="link" @click="goForget">忘记密码？</text>
            </view>

            <view class="login-btn" @click="handleLogin">
                <text>登 录</text>
            </view>

            <view class="other-login">
                <text class="label">其他登录方式</text>
                <view class="other-btns">
                    <view class="other-btn wechat" @click="wechatLogin">
                        <text>💬</text>
                    </view>
                    <view class="other-btn qq" @click="qqLogin">
                        <text>🐧</text>
                    </view>
                </view>
            </view>

            <view class="register-link">
                <text>还没有账号？</text>
                <text class="link" @click="goRegister">立即注册</text>
            </view>
        </view>

        <view class="footer">
            <text class="agreement">
                登录即表示同意
                <text class="link" @click="showAgreement">《用户协议》</text>
                和
                <text class="link" @click="showPrivacy">《隐私政策》</text>
            </text>
        </view>
    </view>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/store'

const userStore = useUserStore()

const loginType = ref('password')
const showPassword = ref(false)
const countdown = ref(0)

const form = ref({
    phone: '13800138000',
    password: '123456',
    code: ''
})

function goBack() {
    uni.navigateBack()
}

function sendCode() {
    if (countdown.value > 0) return
    
    if (!form.value.phone || form.value.phone.length !== 11) {
        uni.showToast({
            title: '请输入正确的手机号',
            icon: 'none'
        })
        return
    }
    
    countdown.value = 60
    const timer = setInterval(() => {
        countdown.value--
        if (countdown.value <= 0) {
            clearInterval(timer)
        }
    }, 1000)
    
    uni.showToast({
        title: '验证码已发送',
        icon: 'success'
    })
}

function handleLogin() {
    if (!form.value.phone || form.value.phone.length !== 11) {
        uni.showToast({
            title: '请输入正确的手机号',
            icon: 'none'
        })
        return
    }
    
    if (loginType.value === 'password') {
        if (!form.value.password) {
            uni.showToast({
                title: '请输入密码',
                icon: 'none'
            })
            return
        }
    } else {
        if (!form.value.code || form.value.code.length !== 6) {
            uni.showToast({
                title: '请输入正确的验证码',
                icon: 'none'
            })
            return
        }
    }
    
    uni.showLoading({
        title: '登录中...'
    })
    
    setTimeout(() => {
        uni.hideLoading()
        
        userStore.login({
            phone: form.value.phone,
            name: '张女士',
            avatar: '',
            userType: 'parent'
        })
        
        uni.showToast({
            title: '登录成功',
            icon: 'success'
        })
        
        setTimeout(() => {
            uni.switchTab({
                url: '/pages/parent/home/home'
            })
        }, 1000)
    }, 1500)
}

function wechatLogin() {
    uni.showToast({
        title: '微信登录功能开发中',
        icon: 'none'
    })
}

function qqLogin() {
    uni.showToast({
        title: 'QQ登录功能开发中',
        icon: 'none'
    })
}

function goForget() {
    uni.showToast({
        title: '忘记密码功能开发中',
        icon: 'none'
    })
}

function goRegister() {
    uni.showToast({
        title: '注册功能开发中',
        icon: 'none'
    })
}

function showAgreement() {
    uni.showModal({
        title: '用户协议',
        content: '欢迎使用校园接送车App。本协议是您与本平台之间关于使用服务的协议。请仔细阅读本协议。',
        showCancel: false
    })
}

function showPrivacy() {
    uni.showModal({
        title: '隐私政策',
        content: '我们重视您的隐私保护。您的个人信息将被严格保护，仅用于提供服务。',
        showCancel: false
    })
}
</script>

<style lang="scss" scoped>
.login-page {
    min-height: 100vh;
    background: linear-gradient(180deg, #E3F2FD 0%, #FFFFFF 40%);
}

.header {
    padding: 0 40rpx;
    padding-top: 40rpx;

    .back-btn {
        width: 64rpx;
        height: 64rpx;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 20rpx;

        text {
            font-size: 36rpx;
            color: #1E88E5;
        }
    }

    .logo-area {
        text-align: center;
        padding: 40rpx 0 60rpx;

        .logo-icon {
            width: 140rpx;
            height: 140rpx;
            background: linear-gradient(135deg, #1E88E5 0%, #64B5F6 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 30rpx;
            font-size: 64rpx;
            box-shadow: 0 8rpx 24rpx rgba(30, 136, 229, 0.3);
        }

        .title {
            display: block;
            font-size: 40rpx;
            font-weight: 600;
            color: #333333;
            margin-bottom: 12rpx;
        }

        .subtitle {
            display: block;
            font-size: 26rpx;
            color: #999999;
        }
    }
}

.login-tabs {
    display: flex;
    margin: 0 60rpx 40rpx;
    background: #F5F7FA;
    border-radius: 16rpx;
    padding: 8rpx;

    .tab-item {
        flex: 1;
        height: 72rpx;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 12rpx;
        transition: all 0.3s;

        text {
            font-size: 28rpx;
            color: #666666;
        }

        &.active {
            background: #FFFFFF;
            box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.05);

            text {
                color: #1E88E5;
                font-weight: 600;
            }
        }
    }
}

.login-form {
    padding: 0 40rpx;

    .input-group {
        background: #FFFFFF;
        border-radius: 16rpx;
        padding: 0 30rpx;
        margin-bottom: 20rpx;
        display: flex;
        align-items: center;
        height: 96rpx;
        box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.03);

        .input-prefix {
            margin-right: 20rpx;
            font-size: 32rpx;
        }

        input {
            flex: 1;
            height: 100%;
            font-size: 30rpx;
            color: #333333;
        }

        .input-suffix {
            margin-left: 20rpx;
            font-size: 32rpx;
            padding: 10rpx;
        }

        .code-btn {
            margin-left: 20rpx;
            padding: 12rpx 24rpx;
            background: linear-gradient(135deg, #1E88E5 0%, #64B5F6 100%);
            border-radius: 8rpx;

            text {
                font-size: 24rpx;
                color: #FFFFFF;
            }

            &.disabled {
                background: #CCCCCC;

                text {
                    color: #FFFFFF;
                }
            }
        }
    }

    .forgot-password {
        text-align: right;
        margin-bottom: 40rpx;

        .link {
            font-size: 26rpx;
            color: #1E88E5;
        }
    }

    .login-btn {
        height: 96rpx;
        background: linear-gradient(135deg, #1E88E5 0%, #64B5F6 100%);
        border-radius: 48rpx;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 40rpx 0;
        box-shadow: 0 8rpx 24rpx rgba(30, 136, 229, 0.3);

        text {
            font-size: 34rpx;
            font-weight: 600;
            color: #FFFFFF;
        }

        &:active {
            opacity: 0.9;
        }
    }

    .other-login {
        text-align: center;
        margin-bottom: 40rpx;

        .label {
            display: block;
            font-size: 24rpx;
            color: #999999;
            margin-bottom: 30rpx;
        }

        .other-btns {
            display: flex;
            justify-content: center;
            gap: 40rpx;
        }

        .other-btn {
            width: 88rpx;
            height: 88rpx;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 40rpx;

            &.wechat {
                background: #07C160;
            }

            &.qq {
                background: #12B7F5;
            }
        }
    }

    .register-link {
        text-align: center;

        text {
            font-size: 26rpx;
            color: #666666;
        }

        .link {
            color: #1E88E5;
            margin-left: 8rpx;
        }
    }
}

.footer {
    position: fixed;
    bottom: 40rpx;
    left: 0;
    right: 0;
    text-align: center;

    .agreement {
        font-size: 22rpx;
        color: #999999;

        .link {
            color: #1E88E5;
        }
    }
}
</style>
