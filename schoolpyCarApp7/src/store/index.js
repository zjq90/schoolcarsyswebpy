import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useUserStore = defineStore('user', () => {
    const userType = ref('')
    const token = ref('')
    const userInfo = ref({})

    const isLoggedIn = computed(() => !!token.value)

    function setUserType(type) {
        userType.value = type
    }

    function login(data) {
        token.value = 'mock_token_' + Date.now()
        userInfo.value = data
    }

    function logout() {
        token.value = ''
        userInfo.value = {}
        userType.value = ''
    }

    return {
        userType,
        token,
        userInfo,
        isLoggedIn,
        setUserType,
        login,
        logout
    }
})

export const useStudentStore = defineStore('student', () => {
    const students = ref([
        {
            id: 1,
            name: '张三',
            school: '实验一小',
            className: '三年级二班',
            avatar: '',
            cardNo: 'STU20240001',
            status: 'onway',
            route: '路线A',
            busNo: '京A12345'
        },
        {
            id: 2,
            name: '李四',
            school: '实验一小',
            className: '四年级一班',
            avatar: '',
            cardNo: 'STU20240002',
            status: 'atschool',
            route: '路线A',
            busNo: '京A12345'
        }
    ])

    const currentStudent = ref(students.value[0])

    function addStudent(student) {
        students.value.push({
            id: Date.now(),
            ...student,
            status: 'normal',
            route: '待分配',
            busNo: '待分配'
        })
    }

    function removeStudent(id) {
        const index = students.value.findIndex(s => s.id === id)
        if (index > -1) {
            students.value.splice(index, 1)
        }
    }

    function setCurrentStudent(student) {
        currentStudent.value = student
    }

    return {
        students,
        currentStudent,
        addStudent,
        removeStudent,
        setCurrentStudent
    }
})

export const useMessageStore = defineStore('message', () => {
    const parentMessages = ref([
        {
            id: 1,
            type: 'violation',
            typeName: '学生违规消息',
            title: '学生行为提醒',
            content: '您的孩子张三今日在校期间出现打闹行为，请关注孩子行为。',
            time: '2024-01-15 14:30',
            read: false,
            studentName: '张三'
        },
        {
            id: 2,
            type: 'school',
            typeName: '学生上下学消息',
            title: '上学打卡通知',
            content: '您的孩子张三已安全到校，打卡时间：08:15。',
            time: '2024-01-15 08:15',
            read: true,
            studentName: '张三'
        },
        {
            id: 3,
            type: 'school',
            typeName: '学生上下学消息',
            title: '放学打卡通知',
            content: '您的孩子张三已安全离校，打卡时间：17:00。',
            time: '2024-01-14 17:00',
            read: true,
            studentName: '张三'
        },
        {
            id: 4,
            type: 'vehicle',
            typeName: '车辆状况提醒',
            title: '车辆延误通知',
            content: '接学生的车辆京A12345因道路拥堵预计延误15分钟，请耐心等待。',
            time: '2024-01-14 07:30',
            read: true,
            studentName: '张三、李四'
        },
        {
            id: 5,
            type: 'violation',
            typeName: '学生违规消息',
            title: '迟到提醒',
            content: '您的孩子李四今日迟到10分钟，请提醒孩子准时到校。',
            time: '2024-01-13 08:20',
            read: true,
            studentName: '李四'
        }
    ])

    const driverMessages = ref([
        {
            id: 1,
            type: 'violation',
            typeName: '学生违规提醒',
            title: '学生行为提醒',
            content: '学生张三今日在校期间出现打闹行为，请协助关注。',
            time: '2024-01-15 14:30',
            read: false
        },
        {
            id: 2,
            type: 'emergency',
            typeName: '紧急状况提醒',
            title: '突发情况通知',
            content: '路线A今日有临时交通管制，请提前规划路线。',
            time: '2024-01-15 06:00',
            read: true
        },
        {
            id: 3,
            type: 'route',
            typeName: '路线规划系统',
            title: '今日路线安排',
            content: '今日路线：学校→幸福小区→阳光花园→金色家园。',
            time: '2024-01-15 05:30',
            read: true
        },
        {
            id: 4,
            type: 'violation',
            typeName: '违章提醒',
            title: '交通违章提醒',
            content: '车辆京A12345在2024-01-12有超速记录，请安全驾驶。',
            time: '2024-01-14 10:00',
            read: true
        },
        {
            id: 5,
            type: 'dispatch',
            typeName: '调度消息',
            title: '临时调度通知',
            content: '请于今日18:00前往火车站接送新入学学生。',
            time: '2024-01-14 16:00',
            read: true
        }
    ])

    const messageCategories = {
        parent: [
            { type: 'all', name: '全部', count: 5 },
            { type: 'violation', name: '学生违规', count: 2 },
            { type: 'school', name: '上下学', count: 2 },
            { type: 'vehicle', name: '车辆状况', count: 1 }
        ],
        driver: [
            { type: 'all', name: '全部', count: 5 },
            { type: 'violation', name: '学生违规', count: 1 },
            { type: 'emergency', name: '紧急状况', count: 1 },
            { type: 'route', name: '路线规划', count: 1 },
            { type: 'violation', name: '违章提醒', count: 1 },
            { type: 'dispatch', name: '调度消息', count: 1 }
        ]
    }

    const unreadCount = computed(() => {
        return parentMessages.value.filter(m => !m.read).length
    })

    function markAsRead(id) {
        const msg = parentMessages.value.find(m => m.id === id)
        if (msg) {
            msg.read = true
        }
    }

    function getMessagesByType(type, userType = 'parent') {
        const messages = userType === 'parent' ? parentMessages : driverMessages
        if (type === 'all') {
            return messages.value
        }
        return messages.value.filter(m => m.type === type)
    }

    return {
        parentMessages,
        driverMessages,
        messageCategories,
        unreadCount,
        markAsRead,
        getMessagesByType
    }
})
