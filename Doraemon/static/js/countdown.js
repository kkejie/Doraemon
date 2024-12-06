// 获取时间差的小时、分钟、秒
function getTimeDiff(targetTime, flg = true) {
    let diff;
    if (!flg) {
        diff = new Date() - targetTime;
    } else {
        diff = targetTime - new Date();
    }
    const days = Math.floor(diff / (24 * 60 * 60 * 1000));
    const hours = Math.floor((diff % (24 * 60 * 60 * 1000)) / (60 * 60 * 1000));
    const minutes = Math.floor((diff % (60 * 60 * 1000)) / (60 * 1000));
    const seconds = Math.floor((diff % (60 * 1000)) / 1000);
    return {days, hours, minutes, seconds};
}

// 设置元素内容
function updateTimeElement(message, timeString) {
    document.getElementById("status-message").textContent = message;
    document.getElementById("time-left").textContent = timeString;
}
function updateWeekEndElement(message, timeString) {
    document.getElementById("weekend-text").textContent = message;
    document.getElementById("weekend-time").textContent = timeString;
}

// 更新倒计时
function updateCountdown() {
    const now = new Date();
    const workEndTime = new Date(now);
    workEndTime.setHours(17, 30, 0, 0); // 设置晚餐时间

    // 判断是否是周末，如果是周末，直接显示“周末剩余时间”
    const dayOfWeek = now.getDay(); // 获取当前星期几，0是周日，6是周六
    if (dayOfWeek === 0 || dayOfWeek === 6 || dayOfWeek === 5 && now > workEndTime) {
        // 如果是周末，显示当前时间距离周末结束（星期天24:00）的剩余时间
        const weekendEndTime = new Date(now);

        // 判断是周六还是周日
        if (dayOfWeek === 6) {
            // 如果是周六，设置周末结束时间为周日24:00
            weekendEndTime.setDate(weekendEndTime.getDate() + 1);
        } else if (dayOfWeek === 5 ) {
            // 如果是周六，设置周末结束时间为周日24:00
            weekendEndTime.setDate(weekendEndTime.getDate() + 2);
        }

        weekendEndTime.setHours(23, 59, 59, 999); // 设置为周末结束时间（周日的24:00）

        // 转换为天、小时、分钟和秒
        const {days, hours, minutes, seconds} = getTimeDiff(weekendEndTime);
        updateWeekEndElement("周末余额 ", `${days}天${hours}时${minutes}分${seconds}秒`);
        updateTimeElement("", "快乐时间！！！");
    } else {
        // 周末倒计时：假设周五18:00
        const weekendTime = new Date(now);
        weekendTime.setHours(17, 30, 0, 0);
        weekendTime.setDate(weekendTime.getDate() + ((5 - weekendTime.getDay() + 7) % 7)); // 本周五

        // 转换为天、小时、分钟和秒
        const {days, hours, minutes, seconds} = getTimeDiff(weekendTime);
        updateWeekEndElement("距离 周末 还有 ", `${days}天${hours}时${minutes}分${seconds}秒`);
        // 定义固定的时间点
        // 每次修改时间时，创建新的 Date 对象
        const LunchStartTime = new Date(now);  // 创建 now 的副本
        LunchStartTime.setHours(11, 45, 0, 0); // 设置午餐开始时间

        const LunchBreakEndTime = new Date(now);
        LunchBreakEndTime.setHours(14, 0, 0, 0); // 设置午休结束时间

        const workEndTime = new Date(now);
        workEndTime.setHours(17, 30, 0, 0); // 设置晚餐时间

        const overtimeStartTime = new Date(now);
        overtimeStartTime.setHours(18, 30, 0, 0); // 设置加班开始时间

        // 判断当前时间并更新
        if (now < LunchStartTime) {
            const {hours, minutes, seconds} = getTimeDiff(LunchStartTime);
            updateTimeElement("距离午餐还有 ", `${hours}时${minutes}分${seconds}秒`);
        } else if (now >= LunchStartTime && now < LunchBreakEndTime) {
            updateTimeElement("滚去", "吃饭睡觉！！！");
        } else if (now >= LunchBreakEndTime && now < workEndTime) {
            const {hours, minutes, seconds} = getTimeDiff(workEndTime);
            updateTimeElement("距离晚餐还有 ", `${hours}时${minutes}分${seconds}秒`);
        } else if (now >= workEndTime && now < overtimeStartTime) {
            updateTimeElement("滚去", "吃饭！！！");
        } else {
            const {hours, minutes, seconds} = getTimeDiff(overtimeStartTime, false);
            updateTimeElement("你已加班 ", `${hours}时${minutes}分${seconds}秒`);
        }

    }
}

// 获取下一个节假日
function getNextHoliday() {
    return fetch('/next-holiday')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => data)
        .catch(error => {
            console.error('Error fetching holiday:', error);
            return {date: '只要胆子大', name: '天天都放假'}; // 默认值
        });
}

// 倒计时
function startCountdown(targetDate) {
    const countdownFunction = setInterval(function () {
        const now = new Date().getTime();
        const countDownDate = new Date(targetDate).getTime();
        const distance = countDownDate - now;

        if (distance < 0) {
            clearInterval(countdownFunction);
            updateHolidayCountdown(0, 0, 0, 0);  // 时间到时设置为0
            return;
        }

        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);

        updateHolidayCountdown(days, hours, minutes, seconds);
    }, 1000);
}

// 更新节假日倒计时
function updateHolidayCountdown(days, hours, minutes, seconds) {
    document.getElementById('remaining-days').innerText = days;
    document.getElementById('remaining-hours').innerText = hours;
    document.getElementById('remaining-minutes').innerText = minutes;
    document.getElementById('remaining-seconds').innerText = seconds;
}

// 页面初始化
function init() {
    updateCountdown();  // 初次调用
    setInterval(updateCountdown, 1000);  // 每秒更新

    // 获取并处理下一个节假日
    getNextHoliday().then(holiday => {
        document.getElementById('holiday-date').innerText = holiday.date;
        document.getElementById('holiday-name').innerText = holiday.name;
        document.getElementById('holiday-name2').innerText = holiday.name;

        const date = new Date(holiday.date);
        date.setDate(date.getDate() - 1); // 前一天
        date.setHours(17, 30, 0, 0); // 设置时间为17:30

        const formatter = new Intl.DateTimeFormat('en-US', {
            year: 'numeric',
            month: 'short',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: false
        });

        const formattedDate = formatter.format(date);
        startCountdown(formattedDate);
    }).catch(error => {
        console.error('Error fetching holiday:', error);
        document.getElementById('holiday-date').innerText = '只要胆子大';
        document.getElementById('holiday-name').innerText = '天天都放假';
        document.getElementById('holiday-name2').innerText = '放假';
    });
}

// 初始化
init();
