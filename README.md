# TaskFlow

Full-stack task management app built with FastAPI, SQLAlchemy, and vanilla JavaScript.

## Setup

1. Backend: `cd backend`, create venv, `pip install -r requirements.txt`, then `uvicorn main:app --reload`
2. Frontend: `cd backend/frontend`, then `python -m http.server 5500`
3. Open `http://127.0.0.1:5500` in your browser

## Features

- Full CRUD for tasks (create, read, update, delete)
- Projects and users management
- Per-project task statistics
- Custom middleware for request logging
- CORS configured for local frontend
- Responsive dashboard with localStorage caching


## Section 2 — Algorithms Engine

### Time Complexity

| Algorithm | Best Case | Worst Case |
|---|---|---|
| insertion_sort | O(n) — jab list already sorted ho | O(n²) — jab list reverse-sorted ho |
| binary_search | O(1) — jab target beech mein mil jaye | O(log n) — jab list ke end tak dhoondhna pade |
| linear_search | O(1) — jab target pehle hi index pe ho | O(n) — jab target end mein ho ya na mile |

### Benchmark Results (real comparison counts)

| Data Size | insertion_sort_count | binary_search_count | linear_search_count |
|---|---|---|---|
| 10 tasks | 23 comparisons | 3 comparisons | 6 comparisons |
| 500 tasks | 44,091 comparisons | 8 comparisons | 251 comparisons |
| 3,000 tasks | 1,507,194 comparisons | 11 comparisons | 1,501 comparisons |

### Is Sorting Worth It?

Humare numbers saaf dikhate hain ki `insertion_sort` ki cost data size ke saath bahut tezi se badhti hai — 10 se 3000 tasks tak jaate hi comparisons **23 se 1,507,194** ho gayi, jabki `binary_search` sirf 3 se 11 comparisons tak hi badha. TaskFlow jaisi app mein team apni task list ko din mein baar-baar dekhti/sort karti hai, lekin naye tasks add ya rename kam karti hai — is usage pattern ko dekhte hue, **sort karke rakhna worth hai**, kyunki ek baar sort hone ke baad, `binary_search` se dhoondhna bahut fast ho jata hai (log n), jabki `linear_search` ki cost list size ke barabar hi rehti hai. Agar team bahut zyada tasks add/rename karti (jisse baar-baar re-sort karna padta), tab shayad linear approach better hota — lekin read-heavy usage mein sorting ka upfront cost, baad ki fast searches se recover ho jata hai.

### How to Run

Benchmark script chalane ke liye:
```bash
cd backend
python benchmark.py
```

Checks script chalane ke liye:
```bash
cd backend
python check_algorithms.py
```