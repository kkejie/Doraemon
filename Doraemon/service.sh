#!/bin/bash

# 使用gunicorn部署服务
## shellcheck disable=SC2120
status() {
  GUNiCORN_STATUS=$(ps -ef |grep -E 'gunicorn.*5001' |grep -v grep|awk '{print $2}')
  # 判断是否为空
  if [ -n "$GUNiCORN_STATUS" ]; then
    if [ "$1" == "print" ]; then
      echo "service [running]"
    fi
    return 0
  else

    if [ "$1" == "print" ]; then
      echo "service [not running]"
    fi
    return 1
  fi
}

start() {
  status
  if [ $? -ne 0 ]; then

    # 后台启动服务
    # pip install gevent==1.4
    # pip install gunicorn
    nohup gunicorn -w 7 -b 0.0.0.0:5001 --daemon --worker-class=gevent manage:app  >/dev/null 2>&1 &
    sleep 3
    status
    if [ $? -ne 0 ]; then
      echo "start service failed"
      return 1
    else
      echo "start service success"
      return 0
    fi
  fi
  echo "service is already [running]"
  return 0
}

stop() {
  status
  if [ $? -ne 0 ]; then
    echo "service is already [not running]"
    return 0
  else
    # pkill gunicorn
    ps -ef |grep -E 'gunicorn.*5001' |grep -v grep|awk '{print $2}'|xargs kill -9
    sleep 3
    status
    if [ $? -ne 0 ]; then
      echo "stop service success"
      return 0
    else
      echo "start service failed"
      return 1
    fi
  fi
}

main() {
  case $1 in
  status)
    status "print"
    ;;
  start)
    start
    ;;
  stop)
    stop
    ;;
  restart)
    stop
    sleep 3
    start
    ;;
  *) echo "usage: $0 [start|stop|restart|status]" ;;
  esac
}

main "$1"

