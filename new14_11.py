import ctypes
import math
import time
import matplotlib.pyplot as plt

class DynamicArray:
    def __init__(self, resize_strategy, capacity=8):
        self._resize_counter = 0
        self._n = 0  # actual elements in array
        self._capacity = capacity  # initial capacity
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


#тест щоб візуалізувати
growth_types = ["fixed", "fixed_by_number", "dynamic"]
sizes = [100, 1000, 5000, 10000, 50000, 100000]
results = {gt: [] for gt in growth_types}

for gt_name, strategy in [
    ("fixed", DynamicArray.fixed_coefficient),
    ("fixed_by_number", DynamicArray.fixed_by_number_coefficient),
    ("dynamic", DynamicArray.dynamic_coefficient)
]:
    
    times = []
    for num in sizes:
        arr = DynamicArray(strategy, 128)
        t0 = time.time()

        for i in range(num):
            arr.append(i)

        t1 = time.time()
        times.append((t1 - t0) * 1000) 
        print(f"{gt_name}: {num} елементів - {times[-1]:.2f} мс")

    results[gt_name] = times

# сам графік
plt.figure(figsize=(12, 7))

for gt_name in growth_types:
    plt.plot(sizes, results[gt_name], marker='o', linewidth=2, label=gt_name)

plt.xlabel('Кількість елементів')
plt.ylabel('Час додавання (мс)')
plt.title('Порівняння швидкості DynamicArray для різних стратегій росту')
plt.legend()

plt.grid(True, alpha=0.3)
plt.yscale('log')
plt.xscale('log')

plt.xticks(sizes, [f'{s:,}' for s in sizes])
plt.tight_layout()
plt.show()