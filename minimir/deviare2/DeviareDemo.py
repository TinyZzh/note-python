# -*- coding:UTF-8 -*-
import logging
import threading
import time

import pythoncom
import win32com

from minimir.deviare2.NktSpyMgrEvents import NktSpyMgrEvents


# def GetPIDByProcessName(aProcessName):
# 	for proc in psutil.process_iter():
# 		if proc.name == aProcessName:
# 			return proc.pid

def _fs():
    pythoncom.CoInitialize()
    try:
        spyManager = win32com.client.DispatchWithEvents('DeviareCOM.NktSpyMgr', NktSpyMgrEvents)
        spyManager.Initialize()

        _pid = spyManager.FindProcessId("game.exe")
        print("PID:{}".format(_pid))
        #
        hook = spyManager.CreateHookForAddress(int("0x005664E0", 0), None, 0)
        hook.Attach(_pid, True)
        hook.Hook(True)
        print("Hook.")
        while True:
            time.sleep(1)
    except Exception as e:
        logging.exception(e)
    finally:
        pythoncom.CoUninitialize()
        pass
    pass


if __name__ == "__main__":
    worker_thread = threading.Thread(target=_fs)
    worker_thread.start()
    while True:
        time.sleep(1)
    pass
