# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import time

import paramiko


class ProxyServer(object):
    def __init__(self, ip, port, username, password):
        self._ip = ip
        self._port = port
        self._username = username
        self._password = password

        self._min_time_interval = 3  # 最短拨号间隔3-5s
        self._last_request_time = -1

        pass

    def _set_last_request_time(self):
        now = time.time()
        if now - self._last_request_time < self._min_time_interval:
            sleep = self._min_time_interval - (now - self._last_request_time)
            if sleep > 0:
                time.sleep(sleep)
            pass
        self._last_request_time = time.time()
        pass

    def get_current_ip(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        stdin, stdout, stderr = ssh.exec_command("curl http://123.206.6.251:8888/test_ip")
        ip = stdout.readline()
        ssh.close()
        return ip

    def restart_adsl(self):
        self._set_last_request_time()
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self._ip, self._port, self._username, self._password)
        stdin, stdout, stderr = ssh.exec_command("adsl-stop")
        stdin, stdout, stderr = ssh.exec_command("adsl-start")
        ssh.close()
