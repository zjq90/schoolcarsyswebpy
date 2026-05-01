<template>
    <view class="feedback-page">
        <view class="form-section">
            <view class="form-item">
                <text class="label">反馈类型</text>
                <view class="type-selector">
                    <view 
                        v-for="(type, index) in feedbackTypes" 
                        :key="index"
                        class="type-item"
                        :class="{ active: form.type === type.value }"
                        @click="form.type = type.value"
                    >
                        <text>{{ type.label }}</text>
                    </view>
                </view>
            </view>

            <view class="form-item">
                <text class="label">相关事件</text>
                <picker 
                    :value="eventIndex" 
                    :range="eventOptions" 
                    @change="onEventChange"
                >
                    <view class="picker-field">
                        <text class="picker-text" :class="{ placeholder: !form.eventName }">
                            {{ form.eventName || '请选择相关事件' }}
                        </text>
                        <text class="picker-arrow">›</text>
                    </view>
                </picker>
            </view>

            <view class="form-item">
                <text class="label">处理结果</text>
                <view class="result-selector">
                    <view 
                        v-for="(result, index) in resultOptions" 
                        :key="index"
                        class="result-item"
                        :class="{ active: form.result === result.value }"
                        @click="form.result = result.value"
                    >
                        <view class="result-icon" :class="result.value">
                            <text>{{ result.icon }}</text>
                        </view>
                        <text class="result-text">{{ result.label }}</text>
                    </view>
                </view>
            </view>

            <view class="form-item">
                <text class="label">详细描述</text>
                <textarea 
                    class="content-textarea" 
                    v-model="form.content"
                    placeholder="请详细描述处理过程和结果，以便后续查阅..."
                    maxlength="500"
                />
                <text class="word-count">{{ form.content.length }}/500</text>
            </view>

            <view class="form-item">
                <text class="label">上传图片（选填）</text>
                <view class="image-uploader">
                    <view 
                        v-for="(img, index) in form.images" 
                        :key="index"
                        class="image-item"
                    >
                        <image :src="img" mode="aspectFill" class="preview-image" />
                        <view class="delete-btn" @click="removeImage(index)">
                            <text>✕</text>
                        </view>
                    </view>
                    <view 
                        v-if="form.images.length < 6" 
                        class="add-image"
                        @click="uploadImage"
                    >
                        <text class="add-icon">+</text>
                        <text class="add-text">上传图片</text>
                    </view>
                </view>
            </view>
        </view>

        <view class="submit-section">
            <view class="submit-btn" @click="submitFeedback">
                <text>提交反馈</text>
            </view>
        </view>

        <view class="history-section">
            <view class="section-header">
                <text class="section-title">历史反馈</text>
            </view>

            <view v-for="(item, index) in historyList" :key="index" class="history-item">
                <view class="history-header">
                    <view class="type-badge" :class="item.type">
                        <text>{{ getTypeLabel(item.type) }}</text>
                    </view>
                    <view class="result-badge" :class="item.result">
                        <text>{{ getResultText(item.result) }}</text>
                    </view>
                </view>
                <text class="history-content">{{ item.content }}</text>
                <view class="history-footer">
                    <text class="history-time">{{ item.time }}</text>
                </view>
            </view>

            <view v-if="historyList.length === 0" class="empty-history">
                <text class="empty-icon">📋</text>
                <text class="empty-text">暂无反馈记录</text>
            </view>
        </view>
    </view>
</template>

<script setup>
import { ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'

const feedbackTypes = [
    { label: '学生问题', value: 'student' },
    { label: '车辆问题', value: 'vehicle' },
    { label: '路线问题', value: 'route' },
    { label: '其他问题', value: 'other' }
]

const resultOptions = [
    { label: '已解决', value: 'resolved', icon: '✓' },
    { label: '已转交', value: 'forwarded', icon: '→' },
    { label: '未解决', value: 'unresolved', icon: '✕' }
]

const eventOptions = [
    '学生张三违规事件',
    '车辆故障报修',
    '路线拥堵调整',
    '学生上下车安全检查'
]

const eventIndex = ref(0)

const form = ref({
    type: 'student',
    eventName: '',
    result: 'resolved',
    content: '',
    images: []
})

const historyList = ref([
    {
        id: 1,
        type: 'student',
        result: 'resolved',
        content: '学生张三在车内打闹，已进行安全教育，家长已确认知晓。',
        time: '2024-01-15 14:30'
    },
    {
        id: 2,
        type: 'vehicle',
        result: 'forwarded',
        content: '车辆刹车有异响，已上报维修部门处理。',
        time: '2024-01-14 09:00'
    }
])

function onEventChange(e) {
    eventIndex.value = e.detail.value
    form.value.eventName = eventOptions[e.detail.value]
}

function uploadImage() {
    uni.chooseImage({
        count: 6 - form.value.images.length,
        sizeType: ['compressed'],
        sourceType: ['album', 'camera'],
        success: (res) => {
            form.value.images = [...form.value.images, ...res.tempFilePaths]
        }
    })
}

function removeImage(index) {
    form.value.images.splice(index, 1)
}

function getTypeLabel(type) {
    const map = {
        'student': '学生问题',
        'vehicle': '车辆问题',
        'route': '路线问题',
        'other': '其他问题'
    }
    return map[type] || '其他问题'
}

function getResultText(result) {
    const map = {
        'resolved': '已解决',
        'forwarded': '已转交',
        'unresolved': '未解决'
    }
    return map[result] || '待处理'
}

function submitFeedback() {
    if (!form.value.content) {
        uni.showToast({
            title: '请填写详细描述',
            icon: 'none'
        })
        return
    }

    uni.showLoading({
        title: '提交中...'
    })

    setTimeout(() => {
        uni.hideLoading()
        uni.showModal({
            title: '提交成功',
            content: '您的反馈已提交成功。',
            showCancel: false,
            success: () => {
                form.value = {
                    type: 'student',
                    eventName: '',
                    result: 'resolved',
                    content: '',
                    images: []
                }
            }
        })
    }, 1500)
}

onLoad(() => {
    console.log('处理结果反馈页加载')
})
</script>

<style lang="scss" scoped>
.feedback-page {
    min-height: 100vh;
    background: #F5F7FA;
    padding-bottom: 180rpx;
}

.form-section {
    background: #FFFFFF;
    padding: 30rpx;
    margin-bottom: 20rpx;
}

.form-item {
    margin-bottom: 30rpx;

    &:last-child {
        margin-bottom: 0;
    }

    .label {
        display: block;
        font-size: 28rpx;
        color: #333333;
        margin-bottom: 16rpx;
        font-weight: 500;
    }

    .input {
        width: 100%;
        height: 88rpx;
        background: #F8FAFC;
        border-radius: 12rpx;
        padding: 0 24rpx;
        font-size: 28rpx;
        color: #333333;
    }

    .content-textarea {
        width: 100%;
        height: 240rpx;
        background: #F8FAFC;
        border-radius: 12rpx;
        padding: 20rpx 24rpx;
        font-size: 28rpx;
        color: #333333;
    }

    .word-count {
        display: block;
        text-align: right;
        font-size: 22rpx;
        color: #999999;
        margin-top: 10rpx;
    }
}

.type-selector {
    display: flex;
    flex-wrap: wrap;
    gap: 16rpx;

    .type-item {
        padding: 16rpx 32rpx;
        background: #F8FAFC;
        border-radius: 30rpx;

        text {
            font-size: 26rpx;
            color: #666666;
        }

        &.active {
            background: linear-gradient(135deg, #4CAF50 0%, #81C784 100%);

            text {
                color: #FFFFFF;
            }
        }
    }
}

.result-selector {
    display: flex;
    gap: 20rpx;

    .result-item {
        flex: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 24rpx 16rpx;
        background: #F8FAFC;
        border-radius: 16rpx;
        border: 2rpx solid transparent;

        .result-icon {
            width: 64rpx;
            height: 64rpx;
            background: #E0E0E0;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 12rpx;

            text {
                font-size: 32rpx;
                color: #FFFFFF;
            }

            &.resolved {
                background: linear-gradient(135deg, #4CAF50 0%, #81C784 100%);
            }

            &.forwarded {
                background: linear-gradient(135deg, #2196F3 0%, #64B5F6 100%);
            }

            &.unresolved {
                background: linear-gradient(135deg, #FF9800 0%, #FFB74D 100%);
            }
        }

        .result-text {
            font-size: 24rpx;
            color: #666666;
        }

        &.active {
            border-color: #4CAF50;
            background: #E8F5E9;

            .result-text {
                color: #4CAF50;
                font-weight: 500;
            }
        }
    }
}

.picker-field {
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 88rpx;
    background: #F8FAFC;
    border-radius: 12rpx;
    padding: 0 24rpx;

    .picker-text {
        font-size: 28rpx;
        color: #333333;

        &.placeholder {
            color: #999999;
        }
    }

    .picker-arrow {
        font-size: 32rpx;
        color: #CCCCCC;
    }
}

.image-uploader {
    display: flex;
    flex-wrap: wrap;
    gap: 16rpx;
}

.image-item {
    position: relative;
    width: 180rpx;
    height: 180rpx;

    .preview-image {
        width: 100%;
        height: 100%;
        border-radius: 12rpx;
    }

    .delete-btn {
        position: absolute;
        top: -10rpx;
        right: -10rpx;
        width: 40rpx;
        height: 40rpx;
        background: rgba(0, 0, 0, 0.6);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;

        text {
            font-size: 24rpx;
            color: #FFFFFF;
        }
    }
}

.add-image {
    width: 180rpx;
    height: 180rpx;
    background: #F8FAFC;
    border-radius: 12rpx;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;

    .add-icon {
        font-size: 48rpx;
        color: #CCCCCC;
        margin-bottom: 8rpx;
    }

    .add-text {
        font-size: 24rpx;
        color: #999999;
    }
}

.submit-section {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: #FFFFFF;
    padding: 24rpx 30rpx;
    padding-bottom: calc(24rpx + env(safe-area-inset-bottom));
    box-shadow: 0 -4rpx 12rpx rgba(0, 0, 0, 0.05);
}

.submit-btn {
    height: 88rpx;
    background: linear-gradient(135deg, #4CAF50 0%, #81C784 100%);
    border-radius: 44rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 8rpx 20rpx rgba(76, 175, 80, 0.3);

    text {
        font-size: 32rpx;
        font-weight: 600;
        color: #FFFFFF;
    }

    &:active {
        opacity: 0.9;
    }
}

.history-section {
    background: #FFFFFF;
    padding: 30rpx;

    .section-header {
        margin-bottom: 24rpx;

        .section-title {
            font-size: 30rpx;
            font-weight: 600;
            color: #333333;
        }
    }
}

.history-item {
    padding: 24rpx;
    background: #F8FAFC;
    border-radius: 16rpx;
    margin-bottom: 20rpx;

    .history-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 16rpx;

        .type-badge {
            padding: 4rpx 16rpx;
            border-radius: 12rpx;

            text {
                font-size: 22rpx;
            }

            &.student {
                background: #E3F2FD;
                text { color: #2196F3; }
            }

            &.vehicle {
                background: #FFF3E0;
                text { color: #FF9800; }
            }

            &.route {
                background: #E8F5E9;
                text { color: #4CAF50; }
            }

            &.other {
                background: #F3E5F5;
                text { color: #9C27B0; }
            }
        }

        .result-badge {
            padding: 4rpx 16rpx;
            border-radius: 12rpx;

            text {
                font-size: 22rpx;
            }

            &.resolved {
                background: #E8F5E9;
                text { color: #4CAF50; }
            }

            &.forwarded {
                background: #E3F2FD;
                text { color: #2196F3; }
            }

            &.unresolved {
                background: #FFEBEE;
                text { color: #F44336; }
            }
        }
    }

    .history-content {
        display: block;
        font-size: 26rpx;
        color: #666666;
        margin-bottom: 16rpx;
        line-height: 1.6;
    }

    .history-footer {
        .history-time {
            font-size: 22rpx;
            color: #999999;
        }
    }
}

.empty-history {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 60rpx 0;

    .empty-icon {
        font-size: 80rpx;
        margin-bottom: 20rpx;
        opacity: 0.5;
    }

    .empty-text {
        font-size: 26rpx;
        color: #999999;
    }
}
</style>
