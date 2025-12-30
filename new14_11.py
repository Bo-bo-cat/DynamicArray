import ctypes
import math
import pandas as pd
import matplotlib.pyplot as plt

class DynamicArray:
    def init(self, resize_strategy, capacity=8):
        self._resize_counter = 0
        self._n = 0  # actual elements in array
        self._capacity = capacity  # initial capacity
        self._array = self._make_array(self._capacity)
        self._resize_strategy = resize_strategy

        self._initial_capacity = capacity
        self.unused_space_log = []
        self.unused_count_log = []
        self.size_log = []

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
        unused_count = self._capacity - self._n
        self.unused_count_log.append(unused_count)

        unused_percent = (self._capacity - self._n) / self._capacity
        self.unused_space_log.append(unused_percent)

        self.size_log.append(self._n)

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

    def stats(self, name):
        return {
            "Name": name,
            "Strategy": self._resize_strategy.name,
            "Initial capacity": self._initial_capacity,
            "Final size": self._n,
            "Final capacity": self._capacity,
            "Reallocations": self.resizecounter(),
            "Avg unused (elements)": round(self.get_unused_count_average(), 2),
            "Avg unused (%)": round(self.get_unused_average(), 2),
            "Final unused (elements)": self._capacity - self._n
        }

    def get_unused_count_average(self):
        if not self.unused_count_log:
            return 0
        return sum(self.unused_count_log) / len(self.unused_count_log)

    def get_unused_average(self):
        if not self.unused_space_log:
            return 0.0
        return sum(self.unused_space_log) / len(self.unused_space_log) * 100
    
arr_fix1 = DynamicArray(DynamicArray.fixed_coefficient, 8)
arr_fix2 = DynamicArray(DynamicArray.fixed_coefficient, 32)
arr_fix3 = DynamicArray(DynamicArray.fixed_coefficient, 128)
arr_dyn1 = DynamicArray(DynamicArray.dynamic_coefficient, 8)
arr_dyn2 = DynamicArray(DynamicArray.dynamic_coefficient, 32)
arr_dyn3 = DynamicArray(DynamicArray.dynamic_coefficient, 128)

arrays = [
    ("fix_8", arr_fix1),
    ("fix_32", arr_fix2),
    ("fix_128", arr_fix3),
    ("dyn_8", arr_dyn1),
    ("dyn_32", arr_dyn2),
    ("dyn_128", arr_dyn3),
]
results = []

for i in range(100000):
    for _, arr in arrays:
        arr.append(i)

for name, arr in arrays:
    results.append(arr.stats(name))

df = pd.DataFrame(results)
print(df.to_string(index=False))
df.to_csv("results.csv", index=False)

for name, arr in arrays:
    plt.plot(arr.size_log, arr.unused_space_log, label=name)

plt.xlabel("Кількість елементів")
plt.ylabel("Невикористана памʼять (%)")
plt.title("Частка невикористаної памʼяті")
plt.legend()
plt.grid()
plt.show()

realloc_table = df[[
    "Name",
    "Strategy",
    "Initial capacity",
    "Final size",
    "Reallocations"
]]
plt.figure(figsize=(10, 5))
plt.bar(
    realloc_table["Name"],
    realloc_table["Reallocations"],
)
plt.xlabel("Стратегія та ємність при 100000 елементів")
plt.ylabel("Кількість операцій виділення памʼяті")
plt.title("Кількість операцій виділення памʼяті для різних стратегій росту")
plt.grid(axis="y")
plt.tight_layout()
plt.show()
