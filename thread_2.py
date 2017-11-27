import threading,time

def dmn():
    print('dmn start...')
    time.sleep(2)
    print('dmn end.')


def ndmn():
    print('ndmn start...')
    time.sleep(1)
    print('ndmn end.')

d = threading.Thread(target=dmn)
# d.daemon = True
n = threading.Thread(target=ndmn)
print('start....')
d.start()
n.start()
print('end.')