
import ctypes
import os

# 定义 DLL 路径
DM_DLL_PATH = "xd47243.dll"
CRACK_DLL_PATH = "Go.dll"
# 全局变量
g_dm_hmodule = None

# 加载大漠插件
def LoadDm(path):
    global g_dm_hmodule
    if g_dm_hmodule:
        return g_dm_hmodule

    hmod = ctypes.windll.kernel32.LoadLibraryA(path.encode('utf-8'))
    if not hmod:
        print(f"LoadLibraryA 加载失败，路径: {path}, 错误码: {ctypes.windll.kernel32.GetLastError()}")
        return None
    g_dm_hmodule = hmod
    return hmod

# 手动偏移调用类
class DmSoft:
    def __init__(self):
        # 偏移 98304 创建对象
        CreateObj = ctypes.CFUNCTYPE(ctypes.c_long)(g_dm_hmodule + 98304)
        self.obj = CreateObj()

    def __del__(self):
        # 偏移 98400 释放对象
        ReleaseObj = ctypes.CFUNCTYPE(None, ctypes.c_long)(g_dm_hmodule + 98400)
        ReleaseObj(self.obj)

    def Reg(self, code, ver):
        # 偏移 104160 注册
        RegFunc = ctypes.CFUNCTYPE(ctypes.c_long, ctypes.c_long, ctypes.c_char_p, ctypes.c_char_p)(g_dm_hmodule + 121344)
        return RegFunc(self.obj, code.encode('utf-8'), ver.encode('utf-8'))

    def BindWindow(self, hwnd, display, mouse, keypad, mode):
        # 偏移 120080 绑定窗口
        BindFunc = ctypes.CFUNCTYPE(ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_long)(g_dm_hmodule + 120080)
        return BindFunc(self.obj, hwnd, display.encode('utf-8'), mouse.encode('utf-8'), keypad.encode('utf-8'), mode)

    def MoveTo(self, x, y):
        # 偏移 109088 移动鼠标
        MoveFunc = ctypes.CFUNCTYPE(ctypes.c_long, ctypes.c_long, ctypes.c_long, ctypes.c_long)(g_dm_hmodule + 109088)
        return MoveFunc(self.obj, x, y)

    def LeftClick(self):
        # 偏移 118096 左键点击
        ClickFunc = ctypes.CFUNCTYPE(ctypes.c_long, ctypes.c_long)(g_dm_hmodule + 118096)
        return ClickFunc(self.obj)

# 调用主逻辑
def main():
    dm_hmodule = LoadDm(DM_DLL_PATH)
    if not dm_hmodule:
        return

    # 加载破解 DLL 并执行 Go(dm)
    crack_dll = ctypes.windll.kernel32.LoadLibraryA(CRACK_DLL_PATH.encode('utf-8'))
    if not crack_dll:
        print("破解DLL加载失败")
        return

    GoFuncAddr = ctypes.windll.kernel32.GetProcAddress(crack_dll, b"Go")
    if not GoFuncAddr:
        print("破解Go函数获取失败")
        return

    GoFunc = ctypes.CFUNCTYPE(None, ctypes.c_long)(GoFuncAddr)
    GoFunc(dm_hmodule)

    # 创建大漠对象并注册
    dm1 = DmSoft()
    ret = dm1.Reg("", "")
    if ret == 1:
        print("大漠注册成功")
    else:
        print("大漠注册失败")

    hwnd = 920690  # 你的目标窗口句柄
    res = dm1.BindWindow(hwnd, "gdi", "dx", "normal", 0)
    print(f"绑定窗口返回: {res}")
    dm1.MoveTo(684,509)
    dm1.LeftClick()

    dm2 = DmSoft()
    ret = dm2.Reg("", "")
    if ret == 1:
        print("大漠注册成功")
    else:
        print("大漠注册失败")

    hwnd = 200256  # 你的目标窗口句柄
    res = dm2.BindWindow(hwnd, "gdi", "dx", "normal", 0)
    print(f"绑定窗口返回: {res}")
    dm2.MoveTo(684,509)
    dm2.LeftClick()

    print("Hello World!")

if __name__ == "__main__":
    main()
