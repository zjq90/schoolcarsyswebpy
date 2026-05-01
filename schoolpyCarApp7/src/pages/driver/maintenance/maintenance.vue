<template>
    <view class="maintenance-page">
        <view class="vehicle-summary">
            <view class="vehicle-card">
                <view class="vehicle-main">
                    <view class="vehicle-icon">
                        <text>🚌</text>
                    </view>
                    <view class="vehicle-info">
                        <text class="vehicle-name">{{ vehicle.name }}</text>
                        <text class="vehicle-plate">{{ vehicle.plateNo }}</text>
                    </view>
                </view>
                <view class="vehicle-stats">
                    <view class="stat-item">
                        <text class="stat-value">{{ vehicle.mileage }}</text>
                        <text class="stat-label">总里程(km)</text>
                    </view>
                    <view class="stat-item">
                        <text class="stat-value">{{ vehicle.nextMaintenance }}</text>
                        <text class="stat-label">下次保养(km)</text>
                    </view>
                    <view class="stat-item">
                        <text class="stat-value">{{ vehicle.lastMaintenance }}</text>
                        <text class="stat-label">上次保养</text>
                    </view>
                </view>
            </view>
        </view>

        <view class="warning-section" v-if="warnings.length > 0">
            <view class="section-header">
                <text class="section-title">⚠️ 待处理提醒</text>
            </view>
            <view class="warning-list">
                <view v-for="(warning, index) in warnings" :key="index" class="warning-item" @click="useWarning(warning)">
                    <view class="warning-icon">
                        <text>{{ warning.icon }}</text>
                    </view>
                    <view class="warning-content">
                        <text class="warning-title">{{ warning.title }}</text>
                        <text class="warning-desc">{{ warning.desc }}</text>
                    </view>
                    <view class="warning-arrow">
                        <text>›</text>
                    </view>
                </view>
            </view>
        </view>

        <view class="form-section">
            <view class="section-header">
                <text class="section-title">保养/维修反馈</text>
            </view>

            <view class="form-item">
                <text class="label">反馈类型</text>
                <view class="type-selector">
                    <view 
                        v-for="(type, index) in maintenanceTypes" 
                        :key="index"
                        class="type-item"
                        :class="{ active: form.type === type.value }"
                        @click="form.type = type.value"
                    >
                        <view class="type-icon">
                            <text>{{ type.icon }}</text>
                        </view>
                        <text>{{ type.label }}</text>
                    </view>
                </view>
            </view>

            <view class="form-item">
                <text class="label">问题部位</text>
                <view class="part-selector">
                    <view 
                        v-for="(part, index) in partOptions" 
                        :key="index"
                        class="part-item"
                        :class="{ active: form.parts.includes(part.value) }"
                        @click="togglePart(part.value)"
                    >
                        <text>{{ part.label }}</text>
                    </view>
                </view>
            </view>

            <view class="form-item">
                <text class="label">紧急程度</text>
                <view class="urgency-selector">
                    <view 
                        v-for="(level, index) in urgencyLevels" 
                        :key="index"
                        class="urgency-item"
                        :class="{ active: form.urgency === level.value }"
                        @click="form.urgency = level.value"
                    >
                        <view class="urgency-dot" :class="level.value"></view>
                        <text>{{ level.label }}</text>
                    </view>
                </view>
            </view>

            <view class="form-item">
                <text class="label">详细描述</text>
                <textarea 
                    class="content-textarea" 
                    v-model="form.content"
                    placeholder="请详细描述车辆状况，如异响位置、发生时间、频率等..."
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
            <view class="submit-btn" @click="submitMaintenance">
                <text>提交反馈</text>
            </view>
        </view>

        <view class="history-section">
            <view class="section-header">
                <text class="section-title">历史记录</text>
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
                <view class="history-parts">
                    <text class="parts-label">问题部位：</text>
                    <text class="parts-text">{{ item.parts.join('、') }}</text>
                </view>
                <text class="history-content">{{ item.content }}</text>
                <view class="history-footer">
                    <text class="history-time">{{ item.time }}</text>
                </view>
            </view>

            <view v-if="historyList.length === 0" class="empty-history">
                <text class="empty-icon">🔧</text>
                <text class="empty-text">暂无保养记录</text>
            </view>
        </view>
    </view>
</template>

<script setup>
import { ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'

const vehicle = ref({
    name: '宇通客车',
    plateNo: '京A12345',
    mileage: 25680,
    nextMaintenance: 200,
    lastMaintenance: '2024-01-01'
})

const warnings = ref([
    {
        icon: '🔧',
        title: '保养提醒',
        desc: '距离下次保养还有200公里',
        type: 'maintenance',
        parts: ['全车检查']
    },
    {
        icon: '⚠️',
        title: '刹车检查',
        desc: '刹车系统需要检查维护',
        type: 'repair',
        parts: ['刹车系统']
    }
])

const maintenanceTypes = [
    { label: '常规保养', value: 'maintenance', icon: '🔧' },
    { label: '故障维修', value: 'repair', icon: '🔨' },
    { label: '事故报修', value: 'accident', icon: '🚨' }
]

const partOptions = [
    { label: '发动机', value: 'engine' },
    { label: '变速箱', value: 'transmission' },
    { label: '刹车系统', value: 'brake' },
    { label: '轮胎', value: 'tire' },
    { label: '空调系统', value: 'ac' },
    { label: '电气系统', value: 'electrical' },
    { label: '车身', value: 'body' },
    { label: '其他', value: 'other' }
]

const urgencyLevels = [
    { label: '一般', value: 'normal' },
    { label: '紧急', value: 'urgent' },
    { label: '非常紧急', value: 'critical' }
]

const form = ref({
    type: 'maintenance',
    parts: [],
    urgency: 'normal',
    content: '',
    images: []
})

const historyList = ref([
    {
        id: 1,
        type: 'maintenance',
        parts: ['全车检查', '机油更换'],
        status: 'completed',
        content: '常规保养，已更换机油、机滤，检查全车车况良好。',
        time: '2024-01-01 10:30'
    },
    {
        id: 2,
        type: 'repair',
        parts: ['刹车系统'],
        status: 'processing',
        content: '刹车有异响，已上报维修部门待处理。',
        time: '2024-01-10 16:00'
    }
])

function useWarning(warning) {
    form.value.type = warning.type
    form.value.parts = warning.parts.map(p => {
        const part = partOptions.find(po => po.label === p)
        return part ? part.value : p
    })
    uni.showToast({
        title: '已填入表单',
        icon: 'success'
    })
}

function togglePart(part) {
    const index = form.value.parts.indexOf(part)
    if (index > -1) {
        form.value.parts.splice(index, 1)
    } else {
        form.value.parts.push(part)
    }
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
        'maintenance': '常规保养',
        'repair': '故障维修',
        'accident': '事故报修'
    }
    return map[type] || '其他'
}

function getStatusText(status) {
    const map = {
        'pending': '待处理',
        'processing': '处理中',
        'completed': '已完成'
    }
    return map[status] || '待处理'
}

function submitMaintenance() {
    if (form.value.parts.length === 0) {
        uni.showToast({
            title: '请选择问题部位',
            icon: 'none'
        })
        return
    }

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
            content: '您的反馈已提交，维修部门将尽快处理。',
            showCancel: false,
            success: () => {
                form.value = {
                    type: 'maintenance',
                    parts: [],
                    urgency: 'normal',
                    content: '',
                    images: []
                }
            }
        })
    }, 1500)
}

onLoad(() => {
    console.log('车辆保养反馈页加载')
})
</script>

<style lang="scss" scoped>
.maintenance-page {
    min-height: 100vh;
    background: #F5F7FA;
    padding-bottom: 180rpx;
}

.vehicle-summary {
    background: linear-gradient(135deg, #4CAF50 0%, #81C784 100%);
    padding: 30rpx;
}

.vehicle-card {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20rpx;
    padding: 24rpx;

    .vehicle-main {
        display: flex;
        align-items: center;
        margin-bottom: 24rpx;

        .vehicle-icon {
            width: 72rpx;
            height: 72rpx;
            background: linear-gradient(135deg, #4CAF50 0%, #81C784 100%);
            border-radius: 16rpx;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 16rpx;
            font-size: 36rpx;
        }

        .vehicle-info {
            .vehicle-name {
                display: block;
                font-size: 30rpx;
                font-weight: 600;
                color: #333333;
                margin-bottom: 4rpx;
            }

            .vehicle-plate {
                font-size: 24rpx;
                color: #666666;
            }
        }
    }

    .vehicle-stats {
        display: flex;
        background: #F8FAFC;
        border-radius: 12rpx;
        padding: 20rpx 0;

        .stat-item {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;

            .stat-value {
                font-size: 28rpx;
                font-weight: 700;
                color: #4CAF50;
                margin-bottom: 4rpx;
            }

            .stat-label {
                font-size: 20rpx;
                color: #999999;
            }
        }
    }
}

.warning-section {
    background: #FFFFFF;
    margin: 20rpx 30rpx;
    border-radius: 20rpx;
    padding: 24rpx;

    .section-header {
        margin-bottom: 20rpx;

        .section-title {
            font-size: 28rpx;
            font-weight: 600;
            color: #FF9800;
        }
    }

    .warning-list {
        .warning-item {
            display: flex;
            align-items: center;
            padding: 20rpx;
            background: #FFF8E1;
            border-radius: 12rpx;
            margin-bottom: 16rpx;

            &:last-child {
                margin-bottom: 0;
            }

            &:active {
                opacity: 0.8;
            }

            .warning-icon {
                width: 56rpx;
                height: 56rpx;
                background: #FFE0B2;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-right: 16rpx;
                font-size: 28rpx;
            }

            .warning-content {
                flex: 1;
                display: flex;
                flex-direction: column;

                .warning-title {
                    font-size: 28rpx;
                    color: #E65100;
                    font-weight: 500;
                    margin-bottom: 4rpx;
                }

                .warning-desc {
                    font-size: 22rpx;
                    color: #FF9800;
                }
            }

            .warning-arrow {
                text {
                    font-size: 36rpx;
                    color: #FFB74D;
                }
            }
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
}

.type-selector {
    display: flex;
    gap: 20rpx;

    .type-item {
        flex: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 24rpx 16rpx;
        background: #F8FAFC;
        border-radius: 16rpx;
        border: 2rpx solid transparent;

        .type-icon {
            font-size: 40rpx;
            margin-bottom: 12rpx;
        }

        text {
            font-size: 24rpx;
            color: #666666;
        }

        &.active {
            border-color: #4CAF50;
            background: #E8F5E9;

            text {
                color: #4CAF50;
                font-weight: 500;
            }
        }
    }
}

.part-selector {
    display: flex;
    flex-wrap: wrap;
    gap: 16rpx;

    .part-item {
        padding: 14rpx 28rpx;
        background: #F8FAFC;
        border-radius: 30rpx;
        border: 2rpx solid transparent;

        text {
            font-size: 26rpx;
            color: #666666;
        }

        &.active {
            border-color: #4CAF50;
            background: #E8F5E9;

            text {
                color: #4CAF50;
            }
        }
    }
}

.urgency-selector {
    display: flex;
    gap: 20rpx;

    .urgency-item {
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 20rpx 16rpx;
        background: #F8FAFC;
        border-radius: 12rpx;
        border: 2rpx solid transparent;

        .urgency-dot {
            width: 20rpx;
            height: 20rpx;
            border-radius: 50%;
            margin-right: 12rpx;

            &.normal {
                background: #4CAF50;
            }

            &.urgent {
                background: #FF9800;
            }

            &.critical {
                background: #F44336;
            }
        }

        text {
            font-size: 26rpx;
            color: #666666;
        }

        &.active {
            border-color: #4CAF50;
            background: #E8F5E9;

            text {
                color: #4CAF50;
                font-weight: 500;
            }
        }
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
        margin-bottom: 12rpx;

        .type-badge {
            padding: 4rpx 16rpx;
            border-radius: 12rpx;

            text {
                font-size: 22rpx;
            }

            &.maintenance {
                background: #E8F5E9;
                text { color: #4CAF50; }
            }

            &.repair {
                background: #FFF3E0;
                text { color: #FF9800; }
            }

            &.accident {
                background: #FFEBEE;
                text { color: #F44336; }
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

            &.completed {
                background: #E8F5E9;
                text { color: #4CAF50; }
            }
        }
    }

    .history-parts {
        margin-bottom: 12rpx;

        .parts-label {
            font-size: 24rpx;
            color: #999999;
        }

        .parts-text {
            font-size: 24rpx;
            color: #666666;
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
