from ctypes import *
from ctypes.wintypes import *

PDH_HQUERY = HANDLE
PDH_HCOUNTER = HANDLE

class PDH_FMT_COUNTERVALUE_U(Union):
    _fields_ = [
        ("longValue", LONG),
        ("doubleValue", c_double),
        ("largeValue", c_longlong),
        ("AnsiStringValue", LPCSTR),
        ("WideStringValue", LPCWSTR),
    ]

    longValue: int
    doubleValue: float
    largeValue: c_longlong
    AnsiStringValue: LPCSTR
    WideStringValue: LPCWSTR

class PDH_FMT_COUNTERVALUE(Structure):
    _anonymous_ = ("u",)
    _fields_ = [
        ("CStatus", DWORD),
        ("u", PDH_FMT_COUNTERVALUE_U),
    ]

    CStatus: DWORD
    u: PDH_FMT_COUNTERVALUE_U
PPDH_FMT_COUNTERVALUE = POINTER(PDH_FMT_COUNTERVALUE)

class PDH_FMT_COUNTERVALUE_ITEM_A(Structure):
    _fields_ = [
        ("szName", LPSTR),
        ("FmtValue", PDH_FMT_COUNTERVALUE),
    ]

    szName: LPSTR
    FmtValue: PDH_FMT_COUNTERVALUE
PPDH_FMT_COUNTERVALUE_ITEM_A = POINTER(PDH_FMT_COUNTERVALUE_ITEM_A)