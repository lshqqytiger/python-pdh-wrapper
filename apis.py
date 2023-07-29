from ctypes import *
from ctypes.wintypes import *
from typing import Callable

from .structures import *
from .defines import *

pdh = CDLL("pdh.dll")

PdhOpenQueryA: Callable = pdh.PdhOpenQueryA
PdhOpenQueryA.restype = PDH_FUNCTION
PdhOpenQueryA.argtypes = [LPCSTR, DWORD_PTR, POINTER(PDH_HQUERY)]

PdhAddEnglishCounterA: Callable = pdh.PdhAddCounterA
PdhAddEnglishCounterA.restype = PDH_FUNCTION
PdhAddEnglishCounterA.argtypes = [PDH_HQUERY, LPCSTR, DWORD_PTR, POINTER(PDH_HCOUNTER)]

PdhCollectQueryData: Callable = pdh.PdhCollectQueryData
PdhCollectQueryData.restype = PDH_FUNCTION
PdhCollectQueryData.argtypes = [PDH_HQUERY]

PdhGetFormattedCounterValue: Callable = pdh.PdhGetFormattedCounterValue
PdhGetFormattedCounterValue.restype = PDH_FUNCTION
PdhGetFormattedCounterValue.argtypes = [PDH_HCOUNTER, DWORD, LPDWORD, PPDH_FMT_COUNTERVALUE]

PdhGetFormattedCounterArrayA: Callable = pdh.PdhGetFormattedCounterArrayA
PdhGetFormattedCounterArrayA.restype = PDH_FUNCTION
PdhGetFormattedCounterArrayA.argtypes = [PDH_HCOUNTER, DWORD, LPDWORD, LPDWORD, PPDH_FMT_COUNTERVALUE_ITEM_A]

PdhCloseQuery: Callable = pdh.PdhCloseQuery
PdhCloseQuery.restype = PDH_FUNCTION
PdhCloseQuery.argtypes = [PDH_HQUERY]
