import threading
import logging.config


def set_interval(func, sec, argum):
    def func_wrapper():
        set_interval(func, sec, argum)
        func(argum)

    t = threading.Timer(sec, func_wrapper)

    t.setDaemon(True)
    t.start()

    return t
