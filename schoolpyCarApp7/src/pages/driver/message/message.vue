<template>
    <view class="message-page">
        <view class="page-header">
            <text class="page-title">消息中心</text>
            <view class="header-action" @click="markAllRead">
                <text>全部已读</text>
            </view>
        </view>

        <view class="category-tabs">
            <scroll-view scroll-x class="tabs-scroll">
                <view class="tabs-container">
                    <view 
                        v-for="cat in categories" 
                        :key="cat.type"
                        class="tab-item"
                        :class="{ active: activeCategory === cat.type }"
                        @click="switchCategory(cat.type)"
                    >
                        <text>{{ cat.name }}</text>
                        <view v-if="getUnreadByType(cat.type) > 0" class="tab-badge">{{ getUnreadByType(cat.type) }}</view>
                    </view>
                </view>
            </scroll-view>
        </view>

        <view class="message-list">
            <view 
                v-for="msg in filteredMessages" 
                :key="msg.id"
                class="message-card"
                :class="{ unread: !msg.read }"
                @click="viewMessage(msg)"
            >
                <view class="message-icon" :class="msg.type">
                    <text>{{ getMessageIcon(msg.type) }}</text>
                </view>
                <view class="message-content">
                    <view class="message-header">
                        <text class="message-type">{{ msg.typeName }}</text>
                        <view v-if="!msg.read" class="unread-dot"></view>
                    </view>
                    <text class="message-title">{{ msg.title }}</text>
                    <text class="message-preview">{{ msg.content }}</text>
                    <text class="message-time">{{ msg.time }}</text>
                </view>
                <view class="message-arrow">
                    <text>›</text>
                </view>
            </view>

            <view v-if="filteredMessages.length === 0" class="empty-state">
                <text class="empty-icon">📭</text>
                <text class="empty-text">暂无相关消息</text>
            </view>
        </view>
    </view>
</template>

<script setup>
import { ref, computed } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { useMessageStore } from '@/store'

const messageStore = useMessageStore()

const activeCategory = ref('all')

const categories = ref([
    { type: 'all', name: '全部' },
    { type: 'violation', name: '学生违规' },
    { type: 'emergency', name: '紧急状况' },
    { type: 'route', name: '路线规划' },
    { type: 'dispatch', name: '调度消息' }
])

const messages = computed(() => messageStore.driverMessages)

const filteredMessages = computed(() => {
    if (activeCategory.value === 'all') {
        return messages.value
    }
    return messages.value.filter(m => m.type === activeCategory.value)
})

function getUnreadByType(type) {
    if (type === 'all') {
        return messages.value.filter(m => !m.read).length
    }
    return messages.value.filter(m => m.type === type && !m.read).length
}

function getMessageIcon(type) {
    const iconMap = {
        'violation': '⚠️',
        'emergency': '🚨',
        'route': '🗺️',
        'dispatch': '📋'
    }
    return iconMap[type] || '📄'
}

function switchCategory(type) {
    activeCategory.value = type
}

function viewMessage(msg) {
    msg.read = true
    
    if (msg.type === 'route') {
        uni.navigateTo({
            url: '/pages/driver/route-plan/route-plan'
        })
    } else {
        uni.showModal({
            title: msg.title,
            content: msg.content,
            showCancel: false
        })
    }
}

function markAllRead() {
    messages.value.forEach(m => {
        m.read = true
    })
    uni.showToast({
        title: '已全部标记为已读',
        icon: 'success'
    })
}

onLoad(() => {
    console.log('司机消息页加载')
})
</script>

<style lang="scss" scoped>
.message-page {
    min-height: 100vh;
    background: #F5F7FA;
}

.page-header {
    background: linear-gradient(135deg, #4CAF50 0%, #81C784 100%);
    padding: 40rpx 30rpx 30rpx;
    display: flex;
    justify-content: space-between;
    align-items: center;

    .page-title {
        font-size: 36rpx;
        font-weight: 600;
        color: #FFFFFF;
    }

    .header-action {
        padding: 12rpx 24rpx;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 30rpx;

        text {
            font-size: 24rpx;
            color: #FFFFFF;
        }
    }
}

.category-tabs {
    background: #FFFFFF;
    padding: 20rpx 0;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.05);

    .tabs-scroll {
        white-space: nowrap;
    }

    .tabs-container {
        display: inline-flex;
        padding: 0 20rpx;
        gap: 10rpx;
    }

    .tab-item {
        position: relative;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 16rpx 32rpx;
        background: #F5F7FA;
        border-radius: 30rpx;
        margin-right: 10rpx;

        text {
            font-size: 26rpx;
            color: #666666;
        }

        .tab-badge {
            position: absolute;
            top: 8rpx;
            right: 8rpx;
            min-width: 28rpx;
            height: 28rpx;
            background: #F44336;
            border-radius: 14rpx;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18rpx;
            color: #FFFFFF;
            padding: 0 6rpx;
        }

        &.active {
            background: linear-gradient(135deg, #4CAF50 0%, #81C784 100%);

            text {
                color: #FFFFFF;
                font-weight: 500;
            }
        }
    }
}

.message-list {
    padding: 20rpx 30rpx;
    padding-bottom: 120rpx;
}

.message-card {
    display: flex;
    align-items: center;
    background: #FFFFFF;
    border-radius: 20rpx;
    padding: 30rpx;
    margin-bottom: 20rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.05);

    &.unread {
        background: linear-gradient(90deg, #E8F5E9 0%, #FFFFFF 100%);
    }

    .message-icon {
        width: 72rpx;
        height: 72rpx;
        border-radius: 16rpx;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 20rpx;
        font-size: 32rpx;

        &.violation { background: #FFF3E0; }
        &.emergency { background: #FFEBEE; }
        &.route { background: #E3F2FD; }
        &.dispatch { background: #F3E5F5; }
    }

    .message-content {
        flex: 1;
        min-width: 0;

        .message-header {
            display: flex;
            align-items: center;
            margin-bottom: 8rpx;

            .message-type {
                font-size: 22rpx;
                color: #4CAF50;
                background: #E8F5E9;
                padding: 4rpx 12rpx;
                border-radius: 8rpx;
                margin-right: 12rpx;
            }

            .unread-dot {
                width: 14rpx;
                height: 14rpx;
                background: #F44336;
                border-radius: 50%;
            }
        }

        .message-title {
            display: block;
            font-size: 28rpx;
            font-weight: 600;
            color: #333333;
            margin-bottom: 8rpx;
        }

        .message-preview {
            display: block;
            font-size: 26rpx;
            color: #666666;
            margin-bottom: 8rpx;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .message-time {
            font-size: 22rpx;
            color: #999999;
        }
    }

    .message-arrow {
        margin-left: 20rpx;

        text {
            font-size: 36rpx;
            color: #CCCCCC;
        }
    }
}

.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 100rpx 0;

    .empty-icon {
        font-size: 100rpx;
        margin-bottom: 24rpx;
        opacity: 0.5;
    }

    .empty-text {
        font-size: 28rpx;
        color: #999999;
    }
}
</style>
