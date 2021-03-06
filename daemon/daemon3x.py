"""Generic linux dd base class for python 3.x."""

import atexit
import os
import signal
import sys
import time


class Daemon:
    """A generic dd class.

    Usage: subclass the dd class and override the run() method."""

    def __init__(self, pidfile):
        self.pidfile = pidfile

    def daemonize(self):
        """Deamonize class. UNIX double fork mechanism."""

        try:
            pid = os.fork()  # создаем дочерний процесс
            if pid > 0:  # если pid > 0, то все ок, тк exit(0) - это ОК
                # exit first parent
                sys.exit(0)
        except OSError as err:
            sys.stderr.write('fork #1 failed: {0}\n'.format(err))
            sys.exit(1)

        # decouple from parent environment
        # https://fooobar.com/questions/6811245/why-use-ossetsid-in-python
        os.chdir('/')  # меняем директорию на /
        # при выходе из терминала (или при убийстве родителя?)
        # дочерний процесс созданный нами продолжит работу.
        os.setsid()
        # https://handynotes.ru/2010/02/umask.html
        os.umask(0)  # оставить по умолчанию, т.е 777 (rwx-rwx-rwx)

        # do second fork
        try:
            pid = os.fork()
            if pid > 0:
                # exit from second parent
                sys.exit(0)
        except OSError as err:
            sys.stderr.write('fork #2 failed: {0}\n'.format(err))
            sys.exit(1)

        # redirect standard file descriptors
        # показывать сразу в терминал, без буферизации(т.е без задержки)
        sys.stdout.flush()
        sys.stderr.flush()
        # si = open(os.devnull, 'r')
        # so = open(os.devnull, 'a+')
        # se = open(os.devnull, 'a+')
        # делаем дубликат дескриптора. dup2(fd,fd2)
        # os.dup2(si.fileno(), sys.stdin.fileno())
        # os.dup2(so.fileno(), sys.stdout.fileno())
        # os.dup2(se.fileno(), sys.stderr.fileno())

        # write pidfile
        # регистрируем функцию, которая будет выполняться при нормальном завершении программы
        atexit.register(self.delpid)

        # получаем текущий pid процесса и дописываем его в pidfile
        pid = str(os.getpid())
        with open(self.pidfile, 'w+') as f:
            f.write(pid + '\n')

    def delpid(self):
        os.remove(self.pidfile)

    def start(self):
        """Start the dd."""

        # Check for a pidfile to see if the dd already runs
        try:
            with open(self.pidfile, 'r') as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None

        if pid:
            message = "pidfile {0} already exist. " + \
                      "Daemon already running?\n"
            sys.stderr.write(message.format(self.pidfile))
            sys.exit(1)

        # Start the dd
        self.daemonize()
        self.run()

    def stop(self):
        """Stop the dd."""

        # Get the pid from the pidfile
        try:
            with open(self.pidfile, 'r') as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None

        if not pid:
            message = "pidfile {0} does not exist. " + \
                      "Daemon not running?\n"
            sys.stderr.write(message.format(self.pidfile))
            return  # not an error in a restart

        # Try killing the dd process
        try:
            while 1:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)
        except OSError as err:
            e = str(err.args)
            if e.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print(str(err.args))
                sys.exit(1)

        print('IM STOP!')

    def restart(self):
        """Restart the dd."""
        self.stop()
        self.start()

    def run(self):
        """You should override this method when you subclass Daemon.

        It will be called after the process has been daemonized by
        start() or restart()."""
