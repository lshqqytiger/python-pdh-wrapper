from ctypes import *
from ctypes.wintypes import *
from typing import Iterable

from .apis import PdhOpenQueryA, PdhAddEnglishCounterA, PdhCollectQueryData, PdhGetFormattedCounterValue, PdhGetFormattedCounterArrayA, PdhCloseQuery
from .structures import PDH_HQUERY, PDH_HCOUNTER, PDH_FMT_COUNTERVALUE, PDH_FMT_COUNTERVALUE_ITEM_A
from .defines import *
from .errors import PDHError

class HCounter(PDH_HCOUNTER):
    def get_double(self) -> float:
        value = PDH_FMT_COUNTERVALUE()
        if PdhGetFormattedCounterValue(self, DWORD(PDH_FMT_DOUBLE | PDH_FMT_NOSCALE), None, byref(value)) != PDH_OK:
            raise PDHError("Couldn't get formatted counter value.")
        return value.u.doubleValue

    def get_array(self) -> Iterable[PDH_FMT_COUNTERVALUE_ITEM_A]:
        bufferSize = DWORD(0)
        itemCount = DWORD(0)
        if PdhGetFormattedCounterArrayA(self, DWORD(PDH_FMT_LONG | PDH_FMT_NOSCALE), byref(bufferSize), byref(itemCount), None) != PDH_MORE_DATA:
            raise PDHError("Something went wrong.")
        itemBuffer = (PDH_FMT_COUNTERVALUE_ITEM_A * itemCount.value)()
        if PdhGetFormattedCounterArrayA(self, DWORD(PDH_FMT_LONG | PDH_FMT_NOSCALE), byref(bufferSize), byref(itemCount), itemBuffer) != PDH_OK:
            raise PDHError("Couldn't get formatted counter array.")
        return itemBuffer

class HQuery(PDH_HQUERY):
    def __init__(self):
        super(HQuery, self).__init__()
        if PdhOpenQueryA(None, None, byref(self)) != PDH_OK:
            raise PDHError("Couldn't open PDH query.")

    def add_counter(self, path: str) -> HCounter:
        hCounter = HCounter()
        if PdhAddEnglishCounterA(self, path.encode("utf-8"), None, byref(hCounter)) != PDH_OK:
            raise PDHError("Couldn't add counter query.")
        return hCounter

    def collect_data(self):
        if PdhCollectQueryData(self) != PDH_OK:
            raise PDHError("Couldn't collect query data.")

    def close(self):
        if PdhCloseQuery(self) != PDH_OK:
            raise PDHError("Couldn't close PDH query.")
