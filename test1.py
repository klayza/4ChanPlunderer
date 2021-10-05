import subprocess
import time
from subprocess import *
import subprocess
import psutil

def checkIfProcessRunning(processName):
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False;

def startorstopDownload(command):
    global proc
    if command == "start":
        proc = subprocess.Popen("console.pyw", shell=True)
    if command == "stop":
        process = psutil.Process(proc.pid)
        for proc in process.children(recursive=True):
            proc.kill()
        process.kill()

print(checkIfProcessRunning("pythonw.exe"))
startorstopDownload("start")
time.sleep(3)
print(checkIfProcessRunning("pythonw.exe"))
startorstopDownload("stop")
print(checkIfProcessRunning("pythonw.exe"))




#subprocess.run("console.py", shell=True)

#p1 = subprocess.Popen("taskmgr", shell=True)
#print(p1.poll())
#time.sleep(4)
#p1.terminate()
#print("stopped")
#print(p1.poll())