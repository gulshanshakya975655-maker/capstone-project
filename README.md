# TaskFlow

> A full-stack task management system built as a capstone project.

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

## Section 3 — AI Quick-Add

### Prompting Technique

Humara system message aur mock parser **zero-shot prompting** technique pe based hain — matlab hum AI (ya mock) ko sirf ek clear instruction dete hain (system message mein) ki usse kya extract karna hai (title, priority, due-date hint), lekin koi worked example andar nahi dete jaisa few-shot mein hota hai. Ye choice isliye ki gayi kyunki task simple aur rule-based hai — priority sirf 3 fixed values mein se ek hoti hai, aur due-date hints ek chhoti si fixed list se aate hain, isliye complex reasoning (jaisa chain-of-thought mein hota hai) ki zarurat nahi. Zero-shot approach token usage ko kam rakhta hai (kyunki extra examples nahi bhejne padte), jo real LLM use karte waqt cost aur speed dono behtar banata hai. Reliability ke liye, humne isi wajah se ek **deterministic mock parser** banaya — jo humesha same input pe same output deta hai, bina kisi AI ki randomness ke, taaki grading exact match ho sake.

### Worked Examples (verified against running mock)

**Example 1:**
Input: `"This is urgent, mark it ASAP please"`
```json
{"title": "This is , mark it  please", "priority": "high", "due_date": null}
```

**Example 2:**
Input: `" "` (whitespace only)
```json
{"title": "Untitled task", "priority": "medium", "due_date": null}
```

**Example 3:**
Input: `"Finish the report next Friday, it's urgent"`
```json
{"title": "Finish the report , it's", "priority": "high", "due_date": "next friday"}
```

**Example 4:**
Input: `"tomorrow review tomorrow"`
```json
{"title": "review", "priority": "medium", "due_date": "tomorrow"}
```

**Example 5:**
Input: `"Buy groceries whenever you get time"`
```json
{"title": "Buy groceries  you get time", "priority": "low", "due_date": null}
```

### How to Run

Quick-Add endpoint: `POST /tasks/quick-add` with body `{"description": "...", "project_id": <int>}`. No API key or environment variable is required — the deterministic mock parser is the default behavior.

## Author
Built by Gulshan as part of the Masai capstone project.