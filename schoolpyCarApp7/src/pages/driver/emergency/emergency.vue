<template>
    <view class="emergency-page">
        <view class="quick-actions">
            <view class="action-item emergency-call" @click="makeEmergencyCall">
                <view class="action-icon">
                    <text>🚨</text>
                </view>
                <text class="action-title">紧急呼救</text>
                <text class="action-desc">一键拨打紧急电话</text>
            </view>
            <view class="action-item dispatch-call" @click="callDispatch">
                <view class="action-icon">
                    <text>📞</text>
                </view>
                <text class="action-title">联系调度</text>
                <text class="action-desc">拨打调度中心电话</text>
            </view>
        </view>

        <view class="form-section">
            <view class="section-header">
                <text class="section-title">紧急状况申请</text>
            </view>

            <view class="form-item">
                <text class="label">紧急类型</text>
                <view class="type-selector">
                    <view 
                        v-for="(type, index) in emergencyTypes" 
                        :key="index"
                        class="type-item"
                        :class="{ active: form.type === type.value }"
                        @click="form.type = type.value"
                    >
                        <view class="type-icon" :class="type.value">
                            <text>{{ type.icon }}</text>
                        </view>
                        <text class="type-label">{{ type.label }}</text>
                    </view>
                </view>
            </view>

            <view class="form-item">
                <text class="label">紧急程度</text>
                <view class="level-selector">
                    <view 
                        v-for="(level, index) in emergencyLevels" 
                        :key="index"
                        class="level-item"
                        :class="{ active: form.level === level.value }"
                        @click="form.level = level.value"
                    >
                        <view class="level-indicator" :class="level.value">
                            <view class="indicator-bars">
                                <view class="bar" v-for="i in level.bars" :key="i"></view>
                            </view>
                        </view>
                        <text class="level-label">{{ level.label }}</text>
                    </view>
                </view>
            </view>

            <view class="form-item">
                <text class="label">发生时间</text>
                <picker 
                    mode="multiSelector" 
                    :value="timeValue" 
                    :range="timeRange"
                    @change="onTimeChange"
                >
                    <view class="picker-field">
                        <text class="picker-text">{{ form.time || '请选择发生时间' }}</text>
                        <text class="picker-arrow">›</text>
                    </view>
                </picker>
            </view>

            <view class="form-item">
                <text class="label">详细描述</text>
                <textarea 
                    class="content-textarea" 
                    v-model="form.content"
                    placeholder="请详细描述紧急情况，包括地点、人员、损失等信息..."
                    maxlength="500"
                />
                <text class="word-count">{{ form.content.length }}/500</text>
            </view>

            <view class="form-item">
                <text class="label">现场照片（必填）</text>
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
                        <text class="add-text">上传照片</text>
                    </view>
                </view>
                <text class="image-hint">请至少上传1张现场照片</text>
            </view>

            <view class="form-item">
                <text class="label">联系电话</text>
                <input 
                    class="input" 
                    type="number" 
                    v-model="form.phone"
                    placeholder="请输入您的联系电话"
                    maxlength="11"
                />
            </view>
        </view>

        <view class="submit-section">
            <view class="submit-btn" @click="submitEmergency">
                <text>提交申请</text>
            </view>
        </view>

        <view class="history-section">
            <view class="section-header">
                <text class="section-title">历史申请</text>
            </view>

            <view v-for="(item, index) in historyList" :key="index" class="history-item">
                <view class="history-header">
                    <view class="type-badge" :class="item.type">
                        <text>{{ getTypeLabel(item.type) }}</text>
                    </view>
                    <view class="status-badge" :class="item.status">
                        <text>{{ getStatusText(item.status) }}</text>
                    </view>
                </view>
                <view class="history-info">
                    <text class="info-label">紧急程度：</text>
                    <view class="level-tag" :class="item.level">
                        <text>{{ getLevelText(item.level) }}</text>
                    </view>
                </view>
                <text class="history-content">{{ item.content }}</text>
                <view class="history-footer">
                    <text class="history-time">{{ item.time }}</text>
                </view>
            </view>

            <view v-if="historyList.length === 0" class="empty-history">
                <text class="empty-icon">📋</text>
                <text class="empty-text">暂无紧急申请记录</text>
            </view>
        </view>
    </view>
</template>

<script setup>
import { ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'

const emergencyTypes = [
    { label: '交通事故', value: 'accident', icon: '🚗' },
    { label: '车辆故障', value: 'breakdown', icon: '🔧' },
    { label: '学生紧急', value: 'student', icon: '👶' },
    { label: '其他紧急', value: 'other', icon: '⚠️' }
]

const emergencyLevels = [
    { label: '一般', value: 'normal', bars: 1 },
    { label: '紧急', value: 'urgent', bars: 2 },
    { label: '非常紧急', value: 'critical', bars: 3 }
]

const timeRange = [
    ['现在', '10分钟前', '30分钟前', '1小时前', '2小时前'],
    ['刚刚', '5分钟前', '15分钟前', '30分钟前', '1小时前']
]

const timeValue = ref([0, 0])

const form = ref({
    type: 'accident',
    level: 'urgent',
    time: '',
    content: '',
    images: [],
    phone: ''
})

const historyList = ref([
    {
        id: 1,
        type: 'breakdown',
        level: 'urgent',
        status: 'resolved',
        content: '车辆在幸福小区附近爆胎，已联系救援车辆处理。',
        time: '2024-01-10 08:30'
    },
    {
        id: 2,
        type: 'student',
        level: 'normal',
        status: 'processing',
        content: '学生张三在乘车途中出现身体不适，已联系家长。',
        time: '2024-01-12 16:00'
    }
])

function makeEmergencyCall() {
    uni.showModal({
        title: '紧急呼救',
        content: '确定要拨打紧急电话 110 吗？',
        success: (res) => {
            if (res.confirm) {
                uni.makePhoneCall({
                    phoneNumber: '110',
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

function callDispatch() {
    uni.showModal({
        title: '联系调度',
        content: '确定要拨打调度中心电话 400-123-4567 吗？',
        success: (res) => {
            if (res.confirm) {
                uni.makePhoneCall({
                    phoneNumber: '4001234567',
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

function onTimeChange(e) {
    timeValue.value = e.detail.value
    form.value.time = timeRange[0][e.detail.value[0]] + ' ' + timeRange[1][e.detail.value[1]]
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
        'accident': '交通事故',
        'breakdown': '车辆故障',
        'student': '学生紧急',
        'other': '其他紧急'
    }
    return map[type] || '其他'
}

function getLevelText(level) {
    const map = {
        'normal': '一般',
        'urgent': '紧急',
        'critical': '非常紧急'
    }
    return map[level] || '一般'
}

function getStatusText(status) {
    const map = {
        'pending': '待处理',
        'processing': '处理中',
        'resolved': '已处理'
    }
    return map[status] || '待处理'
}

function submitEmergency() {
    if (!form.value.content) {
        uni.showToast({
            title: '请填写详细描述',
            icon: 'none'
        })
        return
    }

    if (form.value.images.length === 0) {
        uni.showToast({
            title: '请上传现场照片',
            icon: 'none'
        })
        return
    }

    if (!form.value.phone) {
        uni.showToast({
            title: '请填写联系电话',
            icon: 'none'
        })
        return
    }

    uni.showModal({
        title: '确认提交',
        content: '您正在提交紧急状况申请，请确认信息准确无误。',
        success: (res) => {
            if (res.confirm) {
                uni.showLoading({
                    title: '提交中...'
                })

                setTimeout(() => {
                    uni.hideLoading()
                    uni.showModal({
                        title: '提交成功',
                        content: '您的紧急申请已提交，调度中心将立即处理。\n请保持电话畅通。',
                        showCancel: false,
                        success: () => {
                            form.value = {
                                type: 'accident',
                                level: 'urgent',
                                time: '',
                                content: '',
                                images: [],
                                phone: ''
                            }
                        }
                    })
                }, 1500)
            }
        }
    })
}

onLoad(() => {
    console.log('紧急状况申请页加载')
})
</script>

<style lang="scss" scoped>
.emergency-page {
    min-height: 100vh;
    background: #F5F7FA;
    padding-bottom: 180rpx;
}

.quick-actions {
    display: flex;
    gap: 20rpx;
    padding: 30rpx;
    background: linear-gradient(135deg, #4CAF50 0%, #81C784 100%);

    .action-item {
        flex: 1;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20rpx;
        padding: 30rpx 20rpx;
        display: flex;
        flex-direction: column;
        align-items: center;

        &.emergency-call {
            .action-icon {
                background: linear-gradient(135deg, #F44336 0%, #E57373 100%);
            }
        }

        &.dispatch-call {
            .action-icon {
                background: linear-gradient(135deg, #2196F3 0%, #64B5F6 100%);
            }
        }

        &:active {
            opacity: 0.9;
            transform: scale(0.98);
        }

        .action-icon {
            width: 80rpx;
            height: 80rpx;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 16rpx;
            font-size: 40rpx;
        }

        .action-title {
            font-size: 30rpx;
            font-weight: 600;
            color: #333333;
            margin-bottom: 6rpx;
        }

        .action-desc {
            font-size: 22rpx;
            color: #999999;
        }
    }
}

.form-section {
    background: #FFFFFF;
    padding: 30rpx;
    margin-bottom: 20rpx;

    .section-header {
        margin-bottom: 24rpx;

        .section-title {
            font-size: 30rpx;
            font-weight: 600;
            color: #333333;
        }
    }
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
        height: 200rpx;
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

    .image-hint {
        display: block;
        font-size: 22rpx;
        color: #FF9800;
        margin-top: 12rpx;
    }
}

.type-selector {
    display: flex;
    flex-wrap: wrap;
    gap: 16rpx;

    .type-item {
        width: calc(50% - 8rpx);
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 24rpx 16rpx;
        background: #F8FAFC;
        border-radius: 16rpx;
        border: 2rpx solid transparent;

        .type-icon {
            width: 64rpx;
            height: 64rpx;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 12rpx;
            font-size: 32rpx;

            &.accident { background: linear-gradient(135deg, #F44336 0%, #E57373 100%); }
            &.breakdown { background: linear-gradient(135deg, #FF9800 0%, #FFB74D 100%); }
            &.student { background: linear-gradient(135deg, #2196F3 0%, #64B5F6 100%); }
            &.other { background: linear-gradient(135deg, #9C27B0 0%, #BA68C8 100%); }
        }

        .type-label {
            font-size: 26rpx;
            color: #666666;
        }

        &.active {
            border-color: #4CAF50;
            background: #E8F5E9;

            .type-label {
                color: #4CAF50;
                font-weight: 500;
            }
        }
    }
}

.level-selector {
    display: flex;
    gap: 20rpx;

    .level-item {
        flex: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 24rpx 16rpx;
        background: #F8FAFC;
        border-radius: 16rpx;
        border: 2rpx solid transparent;

        .level-indicator {
            margin-bottom: 12rpx;

            .indicator-bars {
                display: flex;
                align-items: flex-end;
                gap: 6rpx;
                height: 48rpx;

                .bar {
                    width: 12rpx;
                    background: #CCCCCC;
                    border-radius: 6rpx;

                    &:nth-child(1) { height: 24rpx; }
                    &:nth-child(2) { height: 36rpx; }
                    &:nth-child(3) { height: 48rpx; }
                }
            }
        }

        .level-label {
            font-size: 24rpx;
            color: #666666;
        }

        &.active {
            border-color: #4CAF50;
            background: #E8F5E9;

            .level-label {
                color: #4CAF50;
                font-weight: 500;
            }

            &.normal .indicator-bars .bar { background: #4CAF50; }
            &.urgent .indicator-bars .bar { background: #FF9800; }
            &.critical .indicator-bars .bar { background: #F44336; }
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
    background: linear-gradient(135deg, #F44336 0%, #E57373 100%);
    border-radius: 44rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 8rpx 20rpx rgba(244, 67, 54, 0.3);

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
        margin-bottom: 12rpx;

        .type-badge {
            padding: 4rpx 16rpx;
            border-radius: 12rpx;

            text {
                font-size: 22rpx;
            }

            &.accident {
                background: #FFEBEE;
                text { color: #F44336; }
            }

            &.breakdown {
                background: #FFF3E0;
                text { color: #FF9800; }
            }

            &.student {
                background: #E3F2FD;
                text { color: #2196F3; }
            }

            &.other {
                background: #F3E5F5;
                text { color: #9C27B0; }
            }
        }

        .status-badge {
            padding: 4rpx 16rpx;
            border-radius: 12rpx;

            text {
                font-size: 22rpx;
            }

            &.pending {
                background: #FFF3E0;
                text { color: #FF9800; }
            }

            &.processing {
                background: #E3F2FD;
                text { color: #2196F3; }
            }

            &.resolved {
                background: #E8F5E9;
                text { color: #4CAF50; }
            }
        }
    }

    .history-info {
        display: flex;
        align-items: center;
        margin-bottom: 12rpx;

        .info-label {
            font-size: 24rpx;
            color: #999999;
        }

        .level-tag {
            padding: 2rpx 12rpx;
            border-radius: 8rpx;

            text {
                font-size: 20rpx;
            }

            &.normal {
                background: #E8F5E9;
                text { color: #4CAF50; }
            }

            &.urgent {
                background: #FFF3E0;
                text { color: #FF9800; }
            }

            &.critical {
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
