<template>
    <view class="detail-page">
        <view class="detail-header">
            <view class="type-badge" :class="message.type">
                <text>{{ getTypeText(message.type) }}</text>
            </view>
            <text class="detail-title">{{ message.title }}</text>
            <text class="detail-time">{{ message.time }}</text>
        </view>

        <view class="detail-content">
            <view class="info-bar" v-if="message.studentName">
                <text class="info-label">涉及学生</text>
                <text class="info-value">{{ message.studentName }}</text>
            </view>

            <view class="content-text">
                {{ message.content }}
            </view>

            <view class="content-text" v-if="message.additional">
                {{ message.additional }}
            </view>
        </view>

        <view class="action-section" v-if="message.type === 'violation'">
            <view class="action-btn primary" @click="handleFeedback">
                <text>我已知晓</text>
            </view>
            <view class="action-btn outline" @click="contactTeacher">
                <text>联系老师</text>
            </view>
        </view>
    </view>
</template>

<script setup>
import { ref, computed } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { useMessageStore } from '@/store'

const messageStore = useMessageStore()

const messageId = ref(null)
const message = ref({
    id: 0,
    type: '',
    typeName: '',
    title: '',
    content: '',
    time: '',
    read: false,
    studentName: ''
})

function getTypeText(type) {
    const typeMap = {
        'violation': '学生违规',
        'school': '上下学通知',
        'vehicle': '车辆状况'
    }
    return typeMap[type] || '系统消息'
}

function handleFeedback() {
    uni.showToast({
        title: '已标记为已知晓',
        icon: 'success'
    })
}

function contactTeacher() {
    uni.showActionSheet({
        itemList: ['拨打电话', '发送消息'],
        success: (res) => {
            if (res.tapIndex === 0) {
                uni.makePhoneCall({
                    phoneNumber: '13900139001',
                    fail: () => {
                        uni.showToast({
                            title: '拨号功能需要真机测试',
                            icon: 'none'
                        })
                    }
                })
            } else {
                uni.showToast({
                    title: '消息功能开发中',
                    icon: 'none'
                })
            }
        }
    })
}

onLoad((options) => {
    messageId.value = options.id
    const msg = messageStore.parentMessages.find(m => m.id === parseInt(options.id))
    if (msg) {
        message.value = msg
        messageStore.markAsRead(msg.id)
    }
})
</script>

<style lang="scss" scoped>
.detail-page {
    min-height: 100vh;
    background: #F5F7FA;
    padding-bottom: 40rpx;
}

.detail-header {
    background: #FFFFFF;
    padding: 40rpx 30rpx;
    margin-bottom: 20rpx;

    .type-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 8rpx 24rpx;
        border-radius: 20rpx;
        margin-bottom: 20rpx;

        text {
            font-size: 24rpx;
        }

        &.violation {
            background: #FFF3E0;
            text { color: #FF9800; }
        }

        &.school {
            background: #E8F5E9;
            text { color: #4CAF50; }
        }

        &.vehicle {
            background: #E3F2FD;
            text { color: #1E88E5; }
        }
    }

    .detail-title {
        display: block;
        font-size: 36rpx;
        font-weight: 600;
        color: #333333;
        margin-bottom: 16rpx;
        line-height: 1.5;
    }

    .detail-time {
        font-size: 24rpx;
        color: #999999;
    }
}

.detail-content {
    background: #FFFFFF;
    padding: 30rpx;
    margin-bottom: 20rpx;

    .info-bar {
        display: flex;
        align-items: center;
        padding: 20rpx;
        background: #F8FAFC;
        border-radius: 12rpx;
        margin-bottom: 24rpx;

        .info-label {
            font-size: 26rpx;
            color: #666666;
            margin-right: 16rpx;
        }

        .info-value {
            font-size: 28rpx;
            color: #1E88E5;
            font-weight: 500;
        }
    }

    .content-text {
        font-size: 30rpx;
        color: #333333;
        line-height: 2;
    }
}

.action-section {
    padding: 0 30rpx;
    display: flex;
    gap: 20rpx;
    margin-top: 40rpx;

    .action-btn {
        flex: 1;
        height: 88rpx;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 44rpx;

        text {
            font-size: 30rpx;
        }

        &.primary {
            background: linear-gradient(135deg, #1E88E5 0%, #64B5F6 100%);
            text { color: #FFFFFF; }
            box-shadow: 0 8rpx 20rpx rgba(30, 136, 229, 0.3);
        }

        &.outline {
            border: 2rpx solid #1E88E5;
            text { color: #1E88E5; }
        }
    }
}
</style>
