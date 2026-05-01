<script setup>
import { onLaunch, onShow, onHide } from '@dcloudio/uni-app'

onLaunch(() => {
    console.log('App Launch')
})

onShow(() => {
    console.log('App Show')
})

onHide(() => {
    console.log('App Hide')
})
</script>

<style>
/* 全局样式 */
@import './uni.scss';

page {
    background-color: $bg-color;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    font-size: 28rpx;
    color: $text-primary;
    min-height: 100vh;
}

.container {
    padding: 0 30rpx;
}

.flex {
    display: flex;
}

.flex-center {
    display: flex;
    align-items: center;
    justify-content: center;
}

.flex-between {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.flex-column {
    display: flex;
    flex-direction: column;
}

.text-center {
    text-align: center;
}

.text-primary {
    color: $text-primary;
}

.text-secondary {
    color: $text-secondary;
}

.text-placeholder {
    color: $text-placeholder;
}

.text-primary-color {
    color: $primary-color;
}

.bg-white {
    background-color: #FFFFFF;
}

.bg-primary {
    background-color: $primary-color;
}

.mt-10 { margin-top: 10rpx; }
.mt-20 { margin-top: 20rpx; }
.mt-30 { margin-top: 30rpx; }
.mb-10 { margin-bottom: 10rpx; }
.mb-20 { margin-bottom: 20rpx; }
.mb-30 { margin-bottom: 30rpx; }
.p-20 { padding: 20rpx; }
.p-30 { padding: 30rpx; }

/* 卡片样式 */
.card {
    background-color: #FFFFFF;
    border-radius: 16rpx;
    margin-bottom: 20rpx;
    padding: 30rpx;
    box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.05);
}

/* 按钮样式 */
.btn-primary {
    background: linear-gradient(135deg, $primary-color 0%, $primary-light 100%);
    color: #FFFFFF;
    border-radius: 50rpx;
    height: 88rpx;
    line-height: 88rpx;
    text-align: center;
    font-size: 32rpx;
    font-weight: 500;
    box-shadow: 0 8rpx 20rpx rgba(30, 136, 229, 0.3);
}

.btn-primary:active {
    opacity: 0.9;
}

.btn-outline {
    background-color: #FFFFFF;
    color: $primary-color;
    border: 2rpx solid $primary-color;
    border-radius: 50rpx;
    height: 88rpx;
    line-height: 88rpx;
    text-align: center;
    font-size: 32rpx;
    font-weight: 500;
}

/* 输入框样式 */
.input-group {
    background-color: #FFFFFF;
    border-radius: 16rpx;
    padding: 0 30rpx;
    margin-bottom: 20rpx;
    display: flex;
    align-items: center;
    height: 96rpx;
    box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.03);
}

.input-group input {
    flex: 1;
    height: 100%;
    font-size: 30rpx;
    color: $text-primary;
}

.input-group .input-prefix {
    margin-right: 20rpx;
    color: $text-secondary;
}

.input-group .input-suffix {
    margin-left: 20rpx;
    color: $primary-color;
    font-size: 28rpx;
}

/* 分割线 */
.divider {
    height: 1rpx;
    background-color: $border-color;
    margin: 20rpx 0;
}

/* 列表项 */
.list-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 30rpx;
    background-color: #FFFFFF;
    border-bottom: 1rpx solid $border-color;
}

.list-item:last-child {
    border-bottom: none;
}

.list-item .left {
    display: flex;
    align-items: center;
}

.list-item .icon {
    width: 48rpx;
    height: 48rpx;
    margin-right: 20rpx;
    border-radius: 12rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #F0F7FF;
    color: $primary-color;
}

.list-item .arrow {
    color: $text-placeholder;
    font-size: 32rpx;
}

/* 空状态 */
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 100rpx 0;
}

.empty-state .empty-icon {
    width: 200rpx;
    height: 200rpx;
    margin-bottom: 30rpx;
    opacity: 0.5;
}

.empty-state .empty-text {
    color: $text-placeholder;
    font-size: 28rpx;
}
</style>
