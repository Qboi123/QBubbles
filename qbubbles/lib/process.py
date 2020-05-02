import wx
import threading
import time, sys


class Process(wx.App):
    def __init__(self):
        wx.App.__init__(self, True)

        # We can either derive from wx.Process and override OnTerminate
        # or we can let wx.Process send this window an event that is
        # caught in the normal way...
        self.Bind(wx.EVT_END_PROCESS, self.OnProcessEnded)

        self.process: wx.Process = None
        self.MainLoop()

    def OnExecuteBtn(self, cmd):

        self.process = wx.Process(self)
        self.process.Redirect()
        pid = wx.Execute(cmd, wx.EXEC_ASYNC, self.process)
        print('OnExecuteBtn: "%s" pid: %s\n' % (cmd, pid))
        #
        # self.inp.Enable(True)
        # self.sndBtn.Enable(True)
        # self.termBtn.Enable(True)
        # self.cmd.Enable(False)
        # self.exBtn.Enable(False)
        # self.inp.SetFocus()

    def Execute(self, command):
        self.OnExecuteBtn(command)
        print("Starting Process Update")
        threading.Thread(None, self.Update, "ProcessUpdate").start()

    def OnSendText(self, text):
        print('OnSendText: "%s"\n' % text)
        text += '\n'
        self.process.GetOutputStream().write(text.encode('utf-8'))

    def Send(self, text):
        self.OnSendText(text)

    def OnCloseStream(self):
        print('OnCloseStream\n')
        self.process.CloseOutput()

    def Close(self):
        self.OnCloseStream()

    def Update(self):
        while self.process is not None:
            self.OnIdle()

    def OnIdle(self):
        if self.process is not None:
            try:
                stream = self.process.GetInputStream()
                stream2 = self.process.GetErrorStream()
                if stream.CanRead():
                    text = stream.read()
                    print("[Game]: "+text.decode()[:-1])
                if stream2.CanRead():
                    text2 = stream2.read()
                    print(text2.decode()[:-1], file=sys.stderr)
            except RuntimeError:
                pass

    def OnProcessEnded(self, evt):
        print('OnProcessEnded, pid:%s,  exitCode: %s\n' %
              (evt.GetPid(), evt.GetExitCode()))
        stream = self.process.GetInputStream()
        stream2 = self.process.GetErrorStream()

        if stream.CanRead():
            text = stream.read()
            print("[Game]: "+text.decode()[:-1])
        if stream2.CanRead():
            text2 = stream2.read()
            print(text2.decode()[:-1], file=sys.stderr)
        #
        # if evt.GetExitCode() == 1:
        #     self.OnIdle()
        #     self.process.Destroy()
        #     self.process = None
        self.process.Destroy()
        self.process = None

    def ShutdownDemo(self):
        # Called when the demo application is switching to a new sample. Tell
        # the process to close (by closign its output stream) and then wait
        # for the termination signals to be received and processed.
        if self.process is not None:
            self.process.CloseOutput()
            wx.MilliSleep(250)
            wx.Yield()
            self.process = None
