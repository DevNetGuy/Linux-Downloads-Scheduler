#!/usr/bin/python3

import paramiko
import time
import os
import sys
from pathlib import Path


class MountServer:

    def __init__(self, host, user, password):

        self.__host = host
        self.__user = user
        self.__password = password

        os.system("modprobe fuse")
        home = str(Path.home())

        if not (os.path.exists(f"{home}/{self.__host}")):
            os.system(f"mkdir ~/{self.__host}")

        self.connectToServer()
        self.runTorrentClient()

    def connectToServer(self):
        os.system(
            "echo '{p}' | sshfs {u}@{h}:/ ~/{h} -o nonempty -o password_stdin".format(h=self.__host, u=self.__user, p=self.__password))

    def runTorrentClient(self):
        os.system("transmission-gtk &")

    def unMountServer(self):
        os.system(f"fusermount -u ~/{self.__host}")

        os.system(f"rm -r {self.__host}")

    def sendShutdownSignal(self):

        self.unMountServer()

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(f"{self.__host}", username="USER",
                    password=f"{self.__password}")
        ssh.exec_command("shutdown /s")
        ssh.close()
        time.sleep(15)
        os.system("poweroff")


scheduledTime = sys.argv[1]

currentTime = time.strftime("%H:%M")

s1 = MountServer("HOST", "USER", "PASSWORD")

while(currentTime < scheduledTime):
    time.sleep(30)
    currentTime = time.strftime("%H:%M")

s1.sendShutdownSignal()
