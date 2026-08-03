"""
benchmark.py
-------------
Ye script humare algorithms (Task 5 ke counting versions) ko
teen alag data sizes (10, 500, 3000) pe test karta hai,
aur batata hai ki kitni comparisons lagi.

Isse hum dekh sakte hain ki data size badhne se
comparisons kaise badhti hain (jo README mein likhna hai).
"""

import random
from algorithms import insertion_sort_count, binary_search_count, linear_search_count


def generate_fake_tasks(count):
    """
    Fake task dictionaries banata hai — bilkul waise fields ke saath
    jo humare real Task model mein hain (title, priority, due_date).
    """
    priorities = ["low", "medium", "high"]
    tasks = []

    for i in range(count):
        tasks.append({
            "id": i,
            "title": f"Task {i}",
            "priority": random.choice(priorities),
            "due_date": f"2026-08-{(i % 28) + 1:02d}",
        })

    return tasks


def run_benchmark_for_size(size):
    print(f"\n===== Data size: {size} tasks =====")

    # ---- Insertion Sort Benchmark (priority ke hisaab se) ----
    tasks = generate_fake_tasks(size)
    priority_rank = {"low": 1, "medium": 2, "high": 3}
    for t in tasks:
        t["priority_rank"] = priority_rank[t["priority"]]

    sort_comparisons = insertion_sort_count(tasks, "priority_rank")
    print(f"insertion_sort_count: {sort_comparisons} comparisons")

    # ---- Binary Search Benchmark (ab list sorted hai title ke hisaab se) ----
    # Pehle title ke hisaab se sort karna zaroori hai binary search ke liye
    for t in tasks:
        pass  # title already unique hai "Task 0", "Task 1", etc.

    insertion_sort_count(tasks, "title")  # title se sort karo (comparison count yahan discard)
    target_title = tasks[size // 2]["title"]  # beech ka koi ek title dhoondhenge

    binary_result = binary_search_count(tasks, target_title, "title")
    print(f"binary_search_count: index={binary_result['index']}, "
          f"comparisons={binary_result['comparison_count']}")

    # ---- Linear Search Benchmark (same target, bina sort ke) ----
    unsorted_tasks = generate_fake_tasks(size)  # fresh unsorted list
    target_title_2 = unsorted_tasks[size // 2]["title"]

    linear_result = linear_search_count(unsorted_tasks, target_title_2, "title")
    print(f"linear_search_count: index={linear_result['index']}, "
          f"comparisons={linear_result['comparison_count']}")


if __name__ == "__main__":
    for size in [10, 500, 3000]:
        run_benchmark_for_size(size)