<template>
    <view class="complaint-page">
        <view class="form-section">
            <view class="form-item">
                <text class="label">投诉类型</text>
                <view class="type-selector">
                    <view 
                        v-for="(type, index) in complaintTypes" 
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
                <text class="label">涉及学生</text>
                <picker 
                    :value="studentIndex" 
                    :range="studentNames" 
                    @change="onStudentChange"
                >
                    <view class="picker-field">
                        <text class="picker-text" :class="{ placeholder: !form.studentName }">
                            {{ form.studentName || '请选择学生' }}
                        </text>
                        <text class="picker-arrow">›</text>
                    </view>
                </picker>
            </view>

            <view class="form-item">
                <text class="label">投诉内容</text>
                <textarea 
                    class="content-textarea" 
                    v-model="form.content"
                    placeholder="请详细描述您遇到的问题，以便我们更好地为您解决..."
                    maxlength="500"
                />
                <text class="word-count">{{ form.content.length }}/500</text>
            </view>

            <view class="form-item">
                <text class="label">联系电话</text>
                <input 
                    class="input" 
                    type="number" 
                    v-model="form.phone"
                    placeholder="请留下您的联系电话"
                    maxlength="11"
                />
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
            <view class="submit-btn" @click="submitComplaint">
                <text>提交投诉</text>
            </view>
        </view>

        <view class="history-section">
            <view class="section-header">
                <text class="section-title">历史记录</text>
            </view>

            <view v-for="(item, index) in historyList" :key="index" class="history-item">
                <view class="history-header">
                    <text class="history-type">{{ getTypeLabel(item.type) }}</text>
                    <view class="status-badge" :class="item.status">
                        <text>{{ getStatusText(item.status) }}</text>
                    </view>
                </view>
                <text class="history-content">{{ item.content }}</text>
                <view class="history-footer">
                    <text class="history-time">{{ item.time }}</text>
                </view>
            </view>

            <view v-if="historyList.length === 0" class="empty-history">
                <text class="empty-icon">📋</text>
                <text class="empty-text">暂无投诉记录</text>
            </view>
        </view>
    </view>
</template>

<script setup>
import { ref, computed } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { useStudentStore } from '@/store'

const studentStore = useStudentStore()

const complaintTypes = [
    { label: '司机服务', value: 'driver' },
    { label: '车辆问题', value: 'vehicle' },
    { label: '路线问题', value: 'route' },
    { label: '其他问题', value: 'other' }
]

const studentIndex = ref(0)

const form = ref({
    type: 'driver',
    studentName: '',
    studentId: null,
    content: '',
    phone: '',
    images: []
})

const studentNames = computed(() => {
    return studentStore.students.map(s => s.name)
})

const historyList = ref([
    {
        id: 1,
        type: 'driver',
        content: '司机师傅今天迟到了20分钟，孩子差点迟到。',
        time: '2024-01-14 08:30',
        status: 'resolved'
    },
    {
        id: 2,
        type: 'vehicle',
        content: '车内空调有异味，希望能检查一下。',
        time: '2024-01-10 16:00',
        status: 'processing'
    }
])

function onStudentChange(e) {
    studentIndex.value = e.detail.value
    form.value.studentName = studentNames.value[e.detail.value]
    form.value.studentId = studentStore.students[e.detail.value].id
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
        'driver': '司机服务',
        'vehicle': '车辆问题',
        'route': '路线问题',
        'other': '其他问题'
    }
    return map[type] || '其他问题'
}

function getStatusText(status) {
    const map = {
        'pending': '待处理',
        'processing': '处理中',
        'resolved': '已解决',
        'rejected': '已驳回'
    }
    return map[status] || '待处理'
}

function submitComplaint() {
    if (!form.value.content) {
        uni.showToast({
            title: '请填写投诉内容',
            icon: 'none'
        })
        return
    }

    if (!form.value.phone) {
        uni.showToast({
            title: '请留下联系电话',
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
            content: '您的投诉已提交，我们将尽快处理并与您联系。',
            showCancel: false,
            success: () => {
                form.value = {
                    type: 'driver',
                    studentName: '',
                    studentId: null,
                    content: '',
                    phone: '',
                    images: []
                }
            }
        })
    }, 1500)
}

onLoad(() => {
    console.log('投诉页加载')
})
</script>

<style lang="scss" scoped>
.complaint-page {
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
            background: linear-gradient(135deg, #1E88E5 0%, #64B5F6 100%);

            text {
                color: #FFFFFF;
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
    background: linear-gradient(135deg, #1E88E5 0%, #64B5F6 100%);
    border-radius: 44rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 8rpx 20rpx rgba(30, 136, 229, 0.3);

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

        .history-type {
            font-size: 28rpx;
            font-weight: 500;
            color: #333333;
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
                text { color: #1E88E5; }
            }

            &.resolved {
                background: #E8F5E9;
                text { color: #4CAF50; }
            }

            &.rejected {
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
