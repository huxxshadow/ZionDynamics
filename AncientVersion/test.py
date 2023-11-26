from threading import Thread
import time


class keepMonitor(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        while True:
            print("1")
            time.sleep(2)


class keepReceiveMsg(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        while True:
            print("2")
            time.sleep(2)

# def keepMonitor():
#     while True:
#         print("1")
#         time.sleep(2)

#
# def keepReceiveMsg():
#     while True:
#         print("2")
#         time.sleep(2)

#
# tMonitor = threading.Thread(target=keepMonitor(), name="Monitor")
# tRec = threading.Thread(target=keepReceiveMsg(), name="Receive_Msg")
#
# # tSend = threading.Thread(target=mainSendMsg(), name="MainSendMsg")
# tRec.start()
# tMonitor.start()
#
# tMonitor.join()
# tRec.join()

if __name__ == "__main__":
    t1 = keepReceiveMsg("ReceiveMsg")
    t2 = keepMonitor("KeepMon")
    t1.start()
    t2.start()

    print("this main thread")
