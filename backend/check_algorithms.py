"""
check_algorithms.py
---------------------
Ye script humare algorithms (Section 2) ko test karta hai.
pytest ya unittest use nahi kiya — sirf simple if/else se
check kiya jaa raha hai, jaisa assignment mein maanga gaya hai.

Chalane ke liye: python check_algorithms.py
"""

from algorithms import (
    insertion_sort,
    binary_search,
    linear_search,
    insertion_sort_count,
    binary_search_count,
    linear_search_count,
)


def check(case_name, result, expected):
    """Helper function — har test case ke liye PASS/FAIL print karta hai."""
    if result == expected:
        print(f"PASS: {case_name}")
    else:
        print(f"FAIL: {case_name} — expected {expected}, got {result}")


# ---------------------------------------------------------------
# Case 1: insertion_sort khaali list pe — khaali hi rehni chahiye
# ---------------------------------------------------------------
empty_list = []
insertion_sort(empty_list, "value")
check("insertion_sort on empty list", empty_list, [])


# ---------------------------------------------------------------
# Case 2: insertion_sort single-element list pe — wahi rehna chahiye
# ---------------------------------------------------------------
single_list = [{"value": 5}]
insertion_sort(single_list, "value")
check("insertion_sort on single-element list", single_list, [{"value": 5}])


# ---------------------------------------------------------------
# Case 3: binary_search — first, last, aur middle index pe value dhoondhna
# ---------------------------------------------------------------
sorted_data = [{"value": 10}, {"value": 20}, {"value": 30}, {"value": 40}, {"value": 50}]

result_first = binary_search(sorted_data, 10, "value")
check("binary_search finds first index", result_first, 0)

result_last = binary_search(sorted_data, 50, "value")
check("binary_search finds last index", result_last, 4)

result_middle = binary_search(sorted_data, 30, "value")
check("binary_search finds middle index", result_middle, 2)


# ---------------------------------------------------------------
# Case 4: binary_search — jab value list mein nahi hai
# ---------------------------------------------------------------
result_not_found = binary_search(sorted_data, 999, "value")
check("binary_search returns -1 when not found", result_not_found, -1)


# ---------------------------------------------------------------
# Case 5: insertion_sort_count — sahi sort ho, aur comparisons int ho
# ---------------------------------------------------------------
count_test_data = [{"value": 3}, {"value": 1}, {"value": 2}]
comparisons = insertion_sort_count(count_test_data, "value")

sorted_correctly = count_test_data == [{"value": 1}, {"value": 2}, {"value": 3}]
check("insertion_sort_count sorts correctly", sorted_correctly, True)

is_int_and_positive = isinstance(comparisons, int) and comparisons > 0
check("insertion_sort_count returns positive int", is_int_and_positive, True)


# ---------------------------------------------------------------
# Case 6: binary_search_count — sahi index aur comparison_count > 0
# ---------------------------------------------------------------
sorted_for_count = [{"value": 10}, {"value": 20}, {"value": 30}, {"value": 40}]
binary_count_result = binary_search_count(sorted_for_count, 30, "value")

check("binary_search_count returns correct index", binary_count_result["index"], 2)

comparison_count_positive = binary_count_result["comparison_count"] > 0
check("binary_search_count comparison_count > 0", comparison_count_positive, True)


# ---------------------------------------------------------------
# Case 7: linear_search_count — value absent, comparison_count == list length
# ---------------------------------------------------------------
absent_test_data = [{"value": 1}, {"value": 2}, {"value": 3}]
linear_count_result = linear_search_count(absent_test_data, 999, "value")

check("linear_search_count index when not found", linear_count_result["index"], -1)
check(
    "linear_search_count comparison_count equals list length",
    linear_count_result["comparison_count"],
    len(absent_test_data),
)


print("\nAll checks completed.")