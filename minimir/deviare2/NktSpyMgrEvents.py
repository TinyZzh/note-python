# -*- coding:UTF-8 -*-
# Event Handlers ======================================================================

import win32com.client


class NktSpyMgrEvents:

    def OnAgentLoad(self, proc, errorCode):
        if not errorCode == 0:
            print("OnAgenLoad error code: %d" % (errorCode,))

    def OnProcessStarted(self, nktProcessAsPyIDispatch):
        print("OnProcessStarted;{}".format(nktProcessAsPyIDispatch))
        nktProcess = win32com.client.Dispatch(nktProcessAsPyIDispatch)
        if (nktProcess.Name == "notepad.exe"):
            print("Notepad was started.")

    def OnProcessTerminated(self, nktProcessAsPyIDispatch):
        print("OnProcessTerminated;{}".format(nktProcessAsPyIDispatch))
        nktProcess = win32com.client.Dispatch(nktProcessAsPyIDispatch)
        if (nktProcess.Name == "notepad.exe"):
            print("Notepad was terminated.")

    def OnFunctionCalled(self, nktHookAsPyIDispatch, nktProcessAsPyIDispatch, nktHookCallInfoAsPyIDispatch):
        print("OnFunctionCalled;{}".format(nktProcessAsPyIDispatch))
        nktHookCallInfo = win32com.client.Dispatch(nktHookCallInfoAsPyIDispatch)
        nktProcess = win32com.client.Dispatch(nktProcessAsPyIDispatch)
        if (nktHookCallInfo.IsPreCall):
            fileName = self.GetFileNameParam(nktHookCallInfo.Params())
            if (fileName.endswith(".txt")):
                self.SkipCall(nktHookCallInfo, nktProcess)

    # Aux Functions =========================================================================

    def SkipCall(self, nktHookCallInfo, nktProcess):
        nktHookCallInfo.SkipCall()
        if (nktProcess.PlatformBits == 64):
            nktHookCallInfo.Result().LongLongVal = -1
        else:
            nktHookCallInfo.Result().LongVal = -1
        nktHookCallInfo.LastError = 5

    def GetFileNameParam(self, nktParamsEnum):
        nktParam = nktParamsEnum.First()
        return nktParam.Value
