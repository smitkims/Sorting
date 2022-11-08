
import argparse
import random
from abc import ABC, abstractmethod
from time import perf_counter
from typing import List


class AbstractSortingAlgorithm(ABC):
    @abstractmethod
    def sort(self, a: List[int]) -> None:
        raise NotImplementedError("Please implement your sorting algorithm")

    @classmethod
    def name(cls) -> str:
        raise NotImplementedError

    """
    Helper method for timing the sort algorithms
    """
    def time_sort(self, list_size=4 ** 1, num_repeat=10, seed=0) -> float:
        random.seed(seed)
        unsorted_arr_list = [list(range(list_size)) for _ in range(num_repeat)]
        for arr in unsorted_arr_list:
            random.shuffle(arr)
        start_time = perf_counter()
        for arr in unsorted_arr_list:
            self.sort(arr)
        delta = perf_counter() - start_time
        avg_delta = delta / num_repeat
        print(f"- List size: {list_size}")
        print(f"- Num repeats: {num_repeat}")
        print(f"- Avg. time per sort for {self.name()}: {avg_delta}s")
        return avg_delta


class BubbleSort(AbstractSortingAlgorithm):
    """
    Implement BubbleSort
    """

    def sort(self, a: List[int]) -> None:
        isSwap = False

        for m in range(len(a) - 1):
            for n in range(0, len(a)-m-1):
                if(a[n] > a[n+1]):
                    isSwap = True
                    temp = a[n]
                    a[n]= a[n + 1]
                    a[n + 1] = temp
                if not isSwap:
                    return
        return

    @classmethod
    def name(cls) -> str:
        return "Bubble Sort"

class QuickSort(AbstractSortingAlgorithm):
    """
    Implement QuickSort
    """

    def sort(self, a: List[int]) -> None:
        left = 0
        right = len(a) - 1

        def partition(left, right, a: List[int]) -> int:
            temp = left - 1
            pivot = a[right]

            for n in range(left, right - 1):
                if a[n] <= pivot:
                    temp += 1
                    holder = a[temp]
                    a[temp]= a[n]
                    a[n] = holder

                holder = a[right]
                a[temp + 1] = a[right]
                a[right] = holder

                return temp + 1

        def quicksort(left, right, a: List[int]) -> List[int]:
            if left < right:
                pivot = partition(left, right, a)
                quicksort(left, pivot - 1, a)
                quicksort(pivot + 1, right, a)
            return a
        return

    @classmethod
    def name(cls) -> str:
        return "QuickSort"


class MergeSort(AbstractSortingAlgorithm):
    """
    Implement MergeSort
    """

    def sort(self, a: List[int]) -> None:
        left = 0
        right = len(a)-1

        def crossing(left, right, mid, a: List[int]) -> List[int]:
            leftsize = mid - 1 + 1
            rightsize = right - mid

            # temporary arrays
            templeft = [0] * leftsize
            tempright = [0] * rightsize

            for m in range(0, leftsize):
                templeft = a[left + m]

            for n in range(0, rightsize):
                tempright = a[mid + 1 + n]

            firstindex = 0
            secondindex = 0
            mergeindex = left

            while firstindex < leftsize and secondindex < rightsize:
                if templeft[firstindex] >= tempright[secondindex]:
                    a[mergeindex] = tempright[secondindex]
                    secondindex += 1
                    mergeindex += 1
                else:
                    a[mergeindex] = templeft[firstindex]
                    firstindex += 1
                    mergeindex += 1

            while firstindex < leftsize:
                a[mergeindex] = templeft[firstindex]
                firstindex += 1
                mergeindex += 1

            while secondindex < rightsize:
                a[mergeindex] = tempright[secondindex]
                secondindex += 1
                mergeindex += 1

            return a

        def mergesort(left, right, a: List[int]) -> List[int]:
            if left < right:
                mid = (left + right) / 2
                mergesort(left, mid, a)
                mergesort(mid + 1, right, a)
                crossing(left, right, mid, a)
        return

    @classmethod
    def name(cls) -> str:
        return "MergeSort"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sort_type", type=str, default="bubble_sort",
                        choices=["bubble_sort", "merge_sort", "quick_sort"], help="Choose sorting algorithm.")
    parser.add_argument("--list_size", type=int, default=2, help="List size (power of 4. e.g., input=2 --> output= 4^2")
    parser.add_argument("--num_repeat", type=int, default=10, help="Number of times to repeat for timing")
    args = parser.parse_args()

    algos_dict = {"bubble_sort": BubbleSort(),
                  "merge_sort": MergeSort(),
                  "quick_sort": QuickSort()}

    sort_algorithm = algos_dict[args.sort_type]
    sort_algorithm.time_sort(list_size=4 ** args.list_size, num_repeat=args.num_repeat)

