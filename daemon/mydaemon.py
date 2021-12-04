#!/usr/bin/env python3

import sys
import time

from daemon3x import Daemon
from api import CheckUpdate, username, token


class MyDaemon(Daemon):
    def run(self):
        while 1:
            time.sleep(2)
            print('mydaemon!')
            moscow = CheckUpdate(username=username, token=token)
            moscow.get_update_repo()  # скачиваем инфу по апдейту с репозитория


if __name__ == "__main__":
    # dd = MyDaemon('/tmp/dd-example.pid')
    daemon = MyDaemon('/home/nanku/PycharmProjects/Daemon3x/daemon/mydaemon.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)
