"""
quick_add.py
-------------
Ye file "AI Quick-Add" feature ka core logic rakhti hai.

Hum ek MOCK parser bana rahe hain (koi real AI/internet use nahi ho raha) —
ye function ek plain English sentence leta hai aur khud se decide karta hai
title, priority, aur due_date_hint kya honge. Bilkul deterministic hai —
same input hamesha same output dega.
"""


# Priority ke liye keyword groups (exact order zaroori hai)
HIGH_PRIORITY_KEYWORDS = ["urgent", "asap"]
LOW_PRIORITY_KEYWORDS = ["whenever", "low priority"]

# Due-date keywords, EXACT order mein check karne hain
SIMPLE_DATE_KEYWORDS = ["today", "tomorrow", "next week"]

NEXT_WEEKDAY_KEYWORDS = [
    "next monday", "next tuesday", "next wednesday", "next thursday",
    "next friday", "next saturday", "next sunday",
]

BARE_WEEKDAY_KEYWORDS = [
    "monday", "tuesday", "wednesday", "thursday",
    "friday", "saturday", "sunday",
]


def build_system_prompt():
    """
    Task 2 ke liye: ye "system" role wala message hai jo batata hai
    AI (ya humare mock) ko uska kaam kya hai.
    Real LLM use karte waqt bhi yehi structure follow karenge.
    """
    return (
        "You are a task-parsing assistant. Given a free-text task "
        "description, extract a clean title, a priority level "
        "(low/medium/high), and a due-date hint if mentioned."
    )


def build_messages(description):
    """
    Task 2: role-based message structure banata hai —
    system message + user message (jisme asli description hai).
    """
    return [
        {"role": "system", "content": build_system_prompt()},
        {"role": "user", "content": description},
    ]


def parse_task_description(description):
    """
    Task 3: Mock parser — ye poora algorithm assignment mein
    diye gaye exact steps follow karta hai.

    Return karta hai: {"title": ..., "priority": ..., "due_date_hint": ...}
    """
    # ---- Step (a): lowercase copy sirf keyword matching ke liye ----
    lower_text = description.lower()
    matched_spans = []  # yahan hum wo saare text spans rakhenge jo title se hatane hain

    # ---- Step (b): Priority decide karo ----
    priority = "medium"  # default

    high_found = [kw for kw in HIGH_PRIORITY_KEYWORDS if kw in lower_text]
    low_found = [kw for kw in LOW_PRIORITY_KEYWORDS if kw in lower_text]

    if high_found:
        priority = "high"
    elif low_found:
        priority = "low"
    # warna priority "medium" hi rahegi

    # Title-stripping note: dono groups ke saare matched keywords hatane hain,
    # sirf jisne priority decide ki wahi nahi
    matched_spans.extend(high_found)
    matched_spans.extend(low_found)

    # ---- Step (c): Due-date hint dhoondo (exact order mein) ----
    due_date_hint = None

    # Pehle simple keywords (today, tomorrow, next week)
    for keyword in SIMPLE_DATE_KEYWORDS:
        if keyword in lower_text:
            due_date_hint = keyword
            matched_spans.append(keyword)
            break

    # Agar upar kuch nahi mila, to "next <weekday>" check karo
    if due_date_hint is None:
        for phrase in NEXT_WEEKDAY_KEYWORDS:
            if phrase in lower_text:
                due_date_hint = phrase
                matched_spans.append(phrase)
                break

    # Agar wo bhi nahi mila, to bare weekday check karo
    if due_date_hint is None:
        for day in BARE_WEEKDAY_KEYWORDS:
            if day in lower_text:
                due_date_hint = day
                matched_spans.append(day)
                break

    # ---- Step (d): Title banao (original-cased text se) ----
    title = description

    # Lambe spans pehle hatao (taaki "next friday" pehle nikle, "friday" baad mein na uljhe)
    matched_spans_sorted = sorted(matched_spans, key=len, reverse=True)

    for span in matched_spans_sorted:
        # Case-insensitive replace: original text mein span ko dhoondh ke hatana hai,
        # chahe original mein wo kisi bhi case mein ho (jaise "ASAP" ya "asap")
        title = _remove_case_insensitive(title, span)

    title = title.strip()

    if not title:
        title = "Untitled task"

    return {
        "title": title,
        "priority": priority,
        "due_date_hint": due_date_hint,
    }


def _remove_case_insensitive(text, phrase):
    """
    Helper function: text mein se 'phrase' ke saare occurrences hatata hai,
    case ignore karke (jaise "ASAP" bhi "asap" bhi match karega),
    lekin original text ka baaki hissa jaisa tha waisa hi rehta hai.
    """
    result = []
    lower_text = text.lower()
    lower_phrase = phrase.lower()
    phrase_len = len(lower_phrase)

    i = 0
    while i < len(text):
        if lower_text[i:i + phrase_len] == lower_phrase:
            i += phrase_len  # is match ko skip karo (hata do)
        else:
            result.append(text[i])
            i += 1

    return "".join(result)