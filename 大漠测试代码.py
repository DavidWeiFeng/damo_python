import ctypes
import os

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
        print("大漠插件加载并破解完成")

    def __init__(self):
        if not DmSoft._initialized:
            raise RuntimeError("请先调用 DmSoft.load_and_crack_dm() 进行初始化")

        # 创建大漠对象（偏移 98304）
        CreateObj = ctypes.CFUNCTYPE(ctypes.c_long)(DmSoft._dm_hmodule + 98304)
        self.obj = CreateObj()

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

    def BindWindow(self, hwnd, display, mouse, keypad, mode):
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
    DmSoft.load_and_crack_dm()
    hwnds = [920690, 200256]  # 示例窗口句柄

    for hwnd in hwnds:
        dm = DmSoft()
        dm.Reg("", "")
        dm.BindWindow(hwnd, "gdi", "dx", "normal", 0)
        dm_classes[hwnd] = dm


if __name__ == "__main__":
    main()