<template>
    <view class="bind-page">
        <view class="page-header">
            <text class="page-title">学生管理</text>
            <view class="add-btn" @click="showAddForm = true">
                <text>+ 绑定学生</text>
            </view>
        </view>

        <view class="student-list" v-if="students.length > 0">
            <view v-for="student in students" :key="student.id" class="student-item">
                <view class="student-info">
                    <view class="avatar">
                        <text>👦</text>
                    </view>
                    <view class="info">
                        <text class="name">{{ student.name }}</text>
                        <text class="school">{{ student.school }} {{ student.className }}</text>
                        <text class="card">学号：{{ student.cardNo }}</text>
                    </view>
                </view>
                <view class="student-actions">
                    <view class="action-btn edit" @click="editStudent(student)">
                        <text>编辑</text>
                    </view>
                    <view class="action-btn delete" @click="deleteStudent(student)">
                        <text>解绑</text>
                    </view>
                </view>
            </view>
        </view>

        <view class="empty-state" v-else>
            <text class="empty-icon">👶</text>
            <text class="empty-text">暂无绑定的学生</text>
            <text class="empty-hint">点击上方按钮绑定孩子信息</text>
        </view>

        <view class="modal-mask" v-if="showAddForm" @click="showAddForm = false">
            <view class="modal-content" @click.stop>
                <view class="modal-header">
                    <text class="modal-title">绑定新学生</text>
                    <view class="close-btn" @click="showAddForm = false">
                        <text>✕</text>
                    </view>
                </view>

                <view class="form-area">
                    <view class="form-item">
                        <text class="label">学生姓名</text>
                        <input class="input" v-model="newStudent.name" placeholder="请输入学生姓名" />
                    </view>

                    <view class="form-item">
                        <text class="label">学校</text>
                        <input class="input" v-model="newStudent.school" placeholder="请输入学校名称" />
                    </view>

                    <view class="form-item">
                        <text class="label">班级</text>
                        <input class="input" v-model="newStudent.className" placeholder="请输入班级名称" />
                    </view>

                    <view class="form-item">
                        <text class="label">学号</text>
                        <input class="input" v-model="newStudent.cardNo" placeholder="请输入学号" />
                    </view>

                    <view class="form-item">
                        <text class="label">绑定验证码</text>
                        <view class="code-input-group">
                            <input class="input code-input" v-model="newStudent.bindCode" placeholder="请输入绑定验证码" />
                            <view class="get-code-btn" @click="getBindCode">
                                <text>获取验证码</text>
                            </view>
                        </view>
                    </view>
                </view>

                <view class="modal-footer">
                    <view class="cancel-btn" @click="showAddForm = false">
                        <text>取消</text>
                    </view>
                    <view class="confirm-btn" @click="addNewStudent">
                        <text>确认绑定</text>
                    </view>
                </view>
            </view>
        </view>
    </view>
</template>

<script setup>
import { ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { useStudentStore } from '@/store'

const studentStore = useStudentStore()

const students = ref(studentStore.students)
const showAddForm = ref(false)

const newStudent = ref({
    name: '',
    school: '',
    className: '',
    cardNo: '',
    bindCode: ''
})

function getBindCode() {
    uni.showToast({
        title: '验证码已发送',
        icon: 'success'
    })
}

function addNewStudent() {
    if (!newStudent.value.name || !newStudent.value.school || !newStudent.value.className) {
        uni.showToast({
            title: '请填写完整信息',
            icon: 'none'
        })
        return
    }

    studentStore.addStudent(newStudent.value)
    uni.showToast({
        title: '绑定成功',
        icon: 'success'
    })
    showAddForm.value = false

    newStudent.value = {
        name: '',
        school: '',
        className: '',
        cardNo: '',
        bindCode: ''
    }
}

function editStudent(student) {
    uni.showToast({
        title: '编辑功能开发中',
        icon: 'none'
    })
}

function deleteStudent(student) {
    uni.showModal({
        title: '提示',
        content: `确定要解绑学生「${student.name}」吗？`,
        success: (res) => {
            if (res.confirm) {
                studentStore.removeStudent(student.id)
                uni.showToast({
                    title: '解绑成功',
                    icon: 'success'
                })
            }
        }
    })
}

onLoad(() => {
    console.log('学生绑定页加载')
})
</script>

<style lang="scss" scoped>
.bind-page {
    min-height: 100vh;
    background: #F5F7FA;
    padding-bottom: 40rpx;
}

.page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 30rpx;
    background: #FFFFFF;

    .page-title {
        font-size: 36rpx;
        font-weight: 600;
        color: #333333;
    }

    .add-btn {
        padding: 14rpx 28rpx;
        background: linear-gradient(135deg, #1E88E5 0%, #64B5F6 100%);
        border-radius: 30rpx;

        text {
            font-size: 26rpx;
            color: #FFFFFF;
        }
    }
}

.student-list {
    padding: 20rpx 30rpx;
}

.student-item {
    background: #FFFFFF;
    border-radius: 20rpx;
    padding: 30rpx;
    margin-bottom: 20rpx;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.05);

    .student-info {
        display: flex;
        margin-bottom: 20rpx;

        .avatar {
            width: 96rpx;
            height: 96rpx;
            background: #E3F2FD;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 24rpx;
            font-size: 48rpx;
        }

        .info {
            display: flex;
            flex-direction: column;
            justify-content: center;

            .name {
                font-size: 32rpx;
                font-weight: 600;
                color: #333333;
                margin-bottom: 8rpx;
            }

            .school {
                font-size: 26rpx;
                color: #666666;
                margin-bottom: 4rpx;
            }

            .card {
                font-size: 24rpx;
                color: #999999;
            }
        }
    }

    .student-actions {
        display: flex;
        gap: 20rpx;

        .action-btn {
            flex: 1;
            height: 72rpx;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 36rpx;

            text {
                font-size: 28rpx;
            }

            &.edit {
                background: #E3F2FD;
                text { color: #1E88E5; }
            }

            &.delete {
                background: #FFEBEE;
                text { color: #F44336; }
            }
        }
    }
}

.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 120rpx 0;

    .empty-icon {
        font-size: 120rpx;
        margin-bottom: 30rpx;
        opacity: 0.5;
    }

    .empty-text {
        font-size: 30rpx;
        color: #666666;
        margin-bottom: 12rpx;
    }

    .empty-hint {
        font-size: 26rpx;
        color: #999999;
    }
}

.modal-mask {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 999;
}

.modal-content {
    width: 90%;
    background: #FFFFFF;
    border-radius: 24rpx;
    overflow: hidden;
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 30rpx;
    border-bottom: 1rpx solid #F0F0F0;

    .modal-title {
        font-size: 32rpx;
        font-weight: 600;
        color: #333333;
    }

    .close-btn {
        width: 56rpx;
        height: 56rpx;
        display: flex;
        align-items: center;
        justify-content: center;

        text {
            font-size: 36rpx;
            color: #999999;
        }
    }
}

.form-area {
    padding: 30rpx;
}

.form-item {
    margin-bottom: 24rpx;

    .label {
        display: block;
        font-size: 28rpx;
        color: #333333;
        margin-bottom: 12rpx;
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

    .code-input-group {
        display: flex;
        gap: 16rpx;

        .code-input {
            flex: 1;
        }

        .get-code-btn {
            width: 200rpx;
            height: 88rpx;
            background: linear-gradient(135deg, #1E88E5 0%, #64B5F6 100%);
            border-radius: 12rpx;
            display: flex;
            align-items: center;
            justify-content: center;

            text {
                font-size: 26rpx;
                color: #FFFFFF;
            }
        }
    }
}

.modal-footer {
    display: flex;
    border-top: 1rpx solid #F0F0F0;

    .cancel-btn, .confirm-btn {
        flex: 1;
        height: 96rpx;
        display: flex;
        align-items: center;
        justify-content: center;

        text {
            font-size: 30rpx;
        }
    }

    .cancel-btn {
        text { color: #666666; }
    }

    .confirm-btn {
        background: linear-gradient(135deg, #1E88E5 0%, #64B5F6 100%);
        text { color: #FFFFFF; }
    }
}
</style>
