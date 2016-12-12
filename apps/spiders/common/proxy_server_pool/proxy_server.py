# -*- coding:utf-8 -*-
__author__ = 'zhaojm'

import time

import paramiko

from ssh_config import proxy_ip_url

class ProxyServer(object):
    def __init__(self, ssh_ip, ssh_port, ssh_username, ssh_password, proxy_port):
        self._ssh_ip = ssh_ip
        self._ssh_port = ssh_port
        self._ssh_username = ssh_username
        self._ssh_password = ssh_password

        self._proxy_port = proxy_port
        self._proxy_ip = None

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

    def get_current_proxy(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self._ssh_ip, self._ssh_port, self._ssh_username, self._ssh_password)
        stdin, stdout, stderr = ssh.exec_command("curl %s" % proxy_ip_url)
        self._proxy_ip = stdout.readline()
        ssh.close()
        return self._proxy_ip, self._proxy_port

    def restart_adsl(self):
        self._set_last_request_time()
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self._ssh_ip, self._ssh_port, self._ssh_username, self._ssh_password)
        stdin, stdout, stderr = ssh.exec_command("adsl-stop")
        stdin, stdout, stderr = ssh.exec_command("adsl-start")
        ssh.close()
