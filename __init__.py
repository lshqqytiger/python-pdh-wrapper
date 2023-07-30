from ctypes import *
from ctypes.wintypes import *

from .apis import PdhOpenQueryW, PdhAddEnglishCounterW, PdhCollectQueryData, PdhGetFormattedCounterValue, PdhGetFormattedCounterArrayW, PdhCloseQuery
from .structures import PDH_HQUERY, PDH_HCOUNTER, PDH_FMT_COUNTERVALUE, PPDH_FMT_COUNTERVALUE_ITEM_W
from .defines import *
from .msvcrt import malloc
from .errors import PDHError

class HCounter(PDH_HCOUNTER):
    def get_double(self) -> float:
        value = PDH_FMT_COUNTERVALUE()
        if PdhGetFormattedCounterValue(self, DWORD(PDH_FMT_DOUBLE | PDH_FMT_NOSCALE), None, byref(value)) != PDH_OK:
            raise PDHError("Couldn't get formatted counter value.")
        return value.u.doubleValue

    def get_long_ints(self) -> dict[str, int]:
        bufferSize = DWORD(0)
        itemCount = DWORD(0)
        if PdhGetFormattedCounterArrayW(self, DWORD(PDH_FMT_LONG | PDH_FMT_NOSCALE), byref(bufferSize), byref(itemCount), None) != PDH_MORE_DATA:
            raise PDHError("Something went wrong.")
        itemBuffer = cast(malloc(c_size_t(bufferSize.value)), PPDH_FMT_COUNTERVALUE_ITEM_W)
        if PdhGetFormattedCounterArrayW(self, DWORD(PDH_FMT_LONG | PDH_FMT_NOSCALE), byref(bufferSize), byref(itemCount), itemBuffer) != PDH_OK:
            raise PDHError("Couldn't get formatted counter array.")
        result: dict[str, int] = dict()
        for i in range(0, itemCount.value):
            item = itemBuffer[i]
            result[item.szName] = item.FmtValue.u.longValue
        return result

class HQuery(PDH_HQUERY):
    def __init__(self):
        super(HQuery, self).__init__()
        if PdhOpenQueryW(None, None, byref(self)) != PDH_OK:
            raise PDHError("Couldn't open PDH query.")

    def add_counter(self, path: str) -> HCounter:
        hCounter = HCounter()
        if PdhAddEnglishCounterW(self, LPCWSTR(path), None, byref(hCounter)) != PDH_OK:
            raise PDHError("Couldn't add counter query.")
        return hCounter

    def collect_data(self):
        if PdhCollectQueryData(self) != PDH_OK:
            raise PDHError("Couldn't collect query data.")

    def close(self):
        if PdhCloseQuery(self) != PDH_OK:
            raise PDHError("Couldn't close PDH query.")
