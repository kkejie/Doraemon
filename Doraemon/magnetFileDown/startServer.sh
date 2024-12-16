#!/bin/bash

# 任务名称
TASK_NAME="autoDownMagnet.py"
TASK_CMD="sudo python3 $TASK_NAME"

# 获取任务进程ID (PID)
get_pid() {
    echo $(pgrep -f "$TASK_NAME")
}

# 查询任务状态
task_status() {
    PID=$(get_pid)
    if [ -z "$PID" ]; then
        echo "$TASK_NAME is not running."
    else
        echo "$TASK_NAME is running with PID(s): $PID"
    fi
}

# 启动任务
start_task() {
    PID=$(get_pid)
    if [ -z "$PID" ]; then
        echo "Starting $TASK_NAME..."
        nohup $TASK_CMD > output.log 2>&1 &
        echo "$TASK_NAME started."
    else
        echo "$TASK_NAME is already running."
    fi
}

# 重启任务
restart_task() {
    PID=$(get_pid)
    if [ -n "$PID" ]; then
        echo "Stopping $TASK_NAME..."
        kill $PID
        sleep 2
    fi
    echo "Restarting $TASK_NAME..."
    nohup $TASK_CMD > output.log 2>&1 &
    echo "$TASK_NAME restarted."
}

# 结束任务
stop_task() {
    PID=$(get_pid)
    if [ -n "$PID" ]; then
        echo "Stopping $TASK_NAME..."
        kill $PID
        echo "$TASK_NAME stopped."
    else
        echo "$TASK_NAME is not running."
    fi
}

# 主菜单
menu() {
    echo "Task Management for $TASK_NAME"
    echo "1. Check Task Status"
    echo "2. Start Task"
    echo "3. Restart Task"
    echo "4. Stop Task"
    echo "5. Exit"
    read -p "Enter your choice: " choice

    case $choice in
        1)
            task_status
            ;;
        2)
            start_task
            ;;
        3)
            restart_task
            ;;
        4)
            stop_task
            ;;
        5)
            exit 0
            ;;
        *)
            echo "Invalid choice, please try again."
            ;;
    esac
}

# 无限循环显示菜单
while true; do
    menu
done
