import _thread
import time


shared_var = 0
lock = _thread.allocate_lock()


def th_func():
    global shared_var
    while True:
        with lock:
            shared_var += 1
        print('In thread')
        time.sleep(2)

_thread.start_new_thread(th_func, ())

while True:
    with lock:
        print(shared_var)
    time.sleep(2)
