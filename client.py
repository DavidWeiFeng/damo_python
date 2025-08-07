
import json
import sys

import requests


class dm_client:

    def __init__(self,ip,prot):
        self.ip = ip
        self.prot = prot

    def __getattribute__(self,item):
        ret = super().__getattribute__(item)
        if str(type(ret))=="<class 'function'>" or str(type(ret))=="<class 'method'>":
            global  temp
            temp = ret
            def res(*args):
                data = {
                    "hwnd":args[0],# 如果不写默认使用序号0
                    "func":str(temp.__name__),
                    "args":args[1:],
                }
                return requests.post(f'http://{self.ip}:{self.prot}/login', json=data).json()
            return res
        else:
            return ret

    @staticmethod
    def BindWindow(hwnd, display="gdi", mouse="dx", keypad="normal", mode=0):
        pass

    @staticmethod
    def MoveTo(hwnd,x, y):
        pass

    @staticmethod
    def LeftClick(hwnd):
        pass




if __name__ == '__main__':
    dm = dm_client("127.0.0.1","9000")
    hwnd=3608184
    dm.MoveTo(hwnd,704,502)
    print(dm.LeftClick(hwnd))
