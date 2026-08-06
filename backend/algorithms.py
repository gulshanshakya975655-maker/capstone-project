"""
algorithms.py
--------------
Ye file mein hum khud se sorting aur searching likh rahe hain
(Python ka built-in sorted() ya list.sort() use NAHI kar rahe,
jaisa assignment mein clearly mana kiya gaya hai).
"""


def insertion_sort(arr, key):
    """
    Insertion Sort:
    Dictionaries ki list ko 'key' field ke hisaab se sort karta hai.
    List ko seedhe modify karta hai (in-place) — kuch return nahi karta.

    Kaise kaam karta hai:
    - Doosre element se shuru karte hain (index 1)
    - Usse peeche wale elements se compare karte hain
    - Jab tak peeche wala bada hai, usko ek position aage shift karte hain
    - Jahan sahi jagah mile, wahan current element ko insert kar dete hain
    """
    n = len(arr)
    for i in range(1, n):
        current = arr[i]
        j = i - 1

        # Jab tak peeche wala element current se bada hai, usko shift karo
        while j >= 0 and arr[j][key] > current[key]:
            arr[j + 1] = arr[j]
            j -= 1

        # Sahi jagah pe current element ko rakh do
        arr[j + 1] = current


def binary_search(arr, target_value, key):
    """
    Binary Search:
    Sirf SORTED list pe kaam karta hai.
    target_value dhoondhta hai arr[key] mein, aur uska index deta hai.
    Agar nahi milta to -1 return karta hai.
    """
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = (low + high) // 2
        mid_value = arr[mid][key]

        if mid_value == target_value:
            return mid
        elif mid_value < target_value:
            low = mid + 1
        else:
            high = mid - 1

    return -1  # Nahi mila


def linear_search(arr, target_value, key):
    """
    Linear Search:
    List ko shuru se end tak ek-ek karke check karta hai.
    Sorting ki koi zarurat nahi hai isme.
    """
    for index, record in enumerate(arr):
        if record[key] == target_value:
            return index

    return -1  # Nahi mila


def insertion_sort_count(arr, key):
    """
    Insertion Sort ka counting version.
    Same logic hai jaise insertion_sort, bas ye batata hai
    kitni comparisons hui — sirf ek number (int) return karta hai.
    """
    comparisons = 0
    n = len(arr)
    for i in range(1, n):
        current = arr[i]
        j = i - 1

        while j >= 0:
            comparisons += 1  # har baar comparison hone pe ginti badhao
            if arr[j][key] > current[key]:
                arr[j + 1] = arr[j]
                j -= 1
            else:
                break

        arr[j + 1] = current

    return comparisons


def binary_search_count(arr, target_value, key):
    """
    Binary Search ka counting version.
    Dictionary return karta hai: {"index": ..., "comparison_count": ...}
    """
    comparisons = 0
    low = 0
    high = len(arr) - 1
    result_index = -1

    while low <= high:
        mid = (low + high) // 2
        mid_value = arr[mid][key]

        comparisons += 1  # comparison ginti

        if mid_value == target_value:
            result_index = mid
            break
        elif mid_value < target_value:
            low = mid + 1
        else:
            high = mid - 1

    return {"index": result_index, "comparison_count": comparisons}


def linear_search_count(arr, target_value, key):
    """
    Linear Search ka counting version.
    Dictionary return karta hai: {"index": ..., "comparison_count": ...}
    """
    comparisons = 0
    result_index = -1

    for index, record in enumerate(arr):
        comparisons += 1  # comparison ginti
        if record[key] == target_value:
            result_index = index
            break

    return {"index": result_index, "comparison_count": comparisons}