import ctypes
import os
import flask
import json


dm_classes = {}
# 手动偏移调用类
class DmSoft:
    _dm_hmodule = None  # 类变量，保存 DLL 句柄
    _initialized = False  # 是否已经破解

    @classmethod
    def load_and_crack_dm(cls, dll_path="xd47243.dll", crack_path="Go.dll"):
        if cls._initialized:
            return

        if not cls._dm_hmodule:
            hmod = ctypes.windll.kernel32.LoadLibraryA(dll_path.encode('utf-8'))
            if not hmod:
                print(f"LoadLibraryA 加载失败，路径: {dll_path}, 错误码: {ctypes.windll.kernel32.GetLastError()}")
                return
            cls._dm_hmodule = hmod

        # 加载破解 DLL 并执行 Go(hmod)
        crack_dll = ctypes.windll.kernel32.LoadLibraryA(crack_path.encode('utf-8'))
        if not crack_dll:
            print("破解DLL加载失败")
            return

        GoFuncAddr = ctypes.windll.kernel32.GetProcAddress(crack_dll, b"Go")
        if not GoFuncAddr:
            print("破解Go函数获取失败")
            return

        GoFunc = ctypes.CFUNCTYPE(None, ctypes.c_long)(GoFuncAddr)
        GoFunc(cls._dm_hmodule)
        cls._initialized = True

    def __init__(self):
        if not DmSoft._initialized:
            raise RuntimeError("请先调用 DmSoft.load_and_crack_dm() 进行初始化")

        # 创建大漠对象（偏移 98304）
        CreateObj = ctypes.CFUNCTYPE(ctypes.c_long)(DmSoft._dm_hmodule + 98304)
        self.obj = CreateObj()
        self.Reg("","")

    def __del__(self):
        ReleaseObj = ctypes.CFUNCTYPE(None, ctypes.c_long)(DmSoft._dm_hmodule + 98400)
        ReleaseObj(self.obj)

    def Reg(self, code, ver):
        RegFunc = ctypes.CFUNCTYPE(ctypes.c_long, ctypes.c_long, ctypes.c_char_p, ctypes.c_char_p)(
            DmSoft._dm_hmodule + 121344)
        res = RegFunc(self.obj, code.encode('utf-8'), ver.encode('utf-8'))
        if res != 1:
            print(f"注册失败，错误码: {res}")
        return res

    def BindWindow(self, hwnd, display="gdi", mouse="dx", keypad="normal", mode=0):
        BindFunc = ctypes.CFUNCTYPE(ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_char_p, ctypes.c_char_p,
                                    ctypes.c_char_p, ctypes.c_long)(DmSoft._dm_hmodule + 120080)
        return BindFunc(self.obj, hwnd, display.encode('utf-8'), mouse.encode('utf-8'), keypad.encode('utf-8'), mode)

    def MoveTo(self, x, y):
        MoveFunc = ctypes.CFUNCTYPE(ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long)(
            DmSoft._dm_hmodule + 109088)
        return MoveFunc(self.obj, x, y)

    def LeftClick(self):
        ClickFunc = ctypes.CFUNCTYPE(ctypes.c_long, ctypes.c_long)(DmSoft._dm_hmodule + 118096)
        return ClickFunc(self.obj)


# 调用主逻辑
def main():
    api = flask.Flask(__name__)
    debug=True
    @api.route('/login', methods=['post'])
    def login():
        try:
            hwnd = int(flask.request.json.get("hwnd", 0))
            func = flask.request.json["func"]
            args = flask.request.json.get("args", ())

            #如果还没有初始化对应 hwnd 的实例，则创建并绑定
            if hwnd not in dm_classes:
                dm = DmSoft()
                bind_result = dm.BindWindow(hwnd)
                if bind_result != 1:
                    return json.dumps({"state": False, "value": f"BindWindow 失败: {bind_result}"})
                dm_classes[hwnd] = dm
                if debug:
                    print(f"[info] 新建并绑定 hwnd: {hwnd}")
            if debug:
                print(f"func:{func}\nargs:{args}")
            if hasattr(dm_classes[hwnd], func):
                func = getattr(dm_classes[hwnd], func)
                res = {"state": True, "value": func(*args)}
            else:
                res = {"state": False, "value": "请检查大漠函数名称"}
            return json.dumps(res)
        except Exception as e:
            res = {"state": False, "value": str(e)}
            return json.dumps(res)
    DmSoft.load_and_crack_dm()
    api.run(threaded=True, port=9000, debug=True, host='127.0.0.1')


if __name__ == "__main__":
    main()