import ctypes
import math


class DynamicArray:
    def __init__(self, resize_strategy, capacity=8):
        self._resize_counter = 0
        self._n = 0 
        self._capacity = capacity 
        self._array = self._make_array(self._capacity)
        self._resize_strategy = resize_strategy

    def len(self):
        return self._n

    def resizecounter(self):
        return self._resize_counter

    def getitem(self, index):
        if not 0 <= index < self._n:
            raise IndexError("index out of range")
        return self._array[index]

    def fixed_coefficient(self):
        return self._capacity * 2

    def fixed_by_number_coefficient(self):
        growth_factor = 1 + 10/10
        return int(self._capacity * growth_factor)

    def dynamic_coefficient(self):
        growth_factor = 1 + 1 / math.log2(self._capacity + 2)
        return int(self._capacity * growth_factor)

    def append(self, value):
        if self._n == self._capacity:
            self._resize(self._resize_strategy(self))
        self._array[self._n] = value
        self._n += 1

    def _resize(self, new_cap):
        new_array = self._make_array(new_cap)

        for i in range(self._n):
            new_array[i] = self._array[i]

        self._array = new_array
        self._capacity = new_cap
        self._resize_counter += 1

    def _make_array(self, capacity):
        return (capacity * ctypes.py_object)()

    def capacity(self):
        return self._capacity


arr1 = DynamicArray(DynamicArray.fixed_coefficient, 8)
arr2 = DynamicArray(DynamicArray.fixed_by_number_coefficient, 16)
arr3 = DynamicArray(DynamicArray.dynamic_coefficient, 32)

for i in range(10000):
    arr1.append(i)
    arr2.append(i)
    arr3.append(i)

print(arr1.resizecounter())
print(arr2.resizecounter())
print(arr3.resizecounter())