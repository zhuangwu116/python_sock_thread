import threading,time

sema = threading.Semaphore(2)

class MyThread(threading.Thread):
    def __init__(self,name):
        super().__init__()
        self.name = name
    def run(self):
        if sema.acquire():
            print(self.name,'Had got resurce.')
            time.sleep(1)
        sema.release()
        print(self.name,'Had release resource.')
if __name__ == '__main__':
    ths = [MyThread(str(i)+'Sema') for i in range(5)]
    for th in ths:
        th.start()
