# Student Record Management System

**Week 8 Programming Assignment — Debug, Fix, and Refactor**
Course: Programming Fundamentals
Author: Stavion Colquitt

Part 1 finds and fixes ten planted bugs in a flat, top-down program. Part 2
refactors that working program into an object-oriented design with binary
search, while keeping the external behaviour identical.

## Files

| File | Description |
|---|---|
| `student_records_fixed.py` | The original program with all 10 bugs corrected |
| `student_records_refactored.py` | Object-oriented version with binary search |
| `bug_report.txt` | Each bug: line, type, original code, fix, symptom, explanation |
| `students.csv` | The provided data file, unmodified |

## Running either version

```
python student_records_fixed.py
python student_records_refactored.py
```

Both present the same menu. Choose option 1 and enter `students.csv` to load
the data, then use options 2 and 3.

## Part 1 — the ten bugs

| # | Type | Problem |
|---|---|---|
| 1 | Crash | File closed before `DictReader` iterated over it |
| 2 | Crash | Dictionary key `Student_ID` instead of `StudentID` |
| 3 | Logic | `csv_loaded` never set to `True` after a successful load |
| 4 | Logic | Record list never cleared, so reloading duplicated every row |
| 5 | Logic | Table separator was 80 characters while the others were 82 |
| 6 | Logic | Row counter never incremented, so every row printed as `1` |
| 7 | Logic | Menu compared input to the integer `4` instead of the string `"4"` |
| 8 | Logic | Previous search result never cleared between searches |
| 9 | Subtle | Loop condition ran one index past the end of the list |
| 10 | Subtle | Only the stored ID was uppercased, not the user's input |

Full details are in `bug_report.txt`.

## Part 2 — the refactor

**Classes**

- `Student` — one record, with `__str__` and a detail view
- `GraduateStudent(Student)` — bonus subclass adding `thesis_topic`
- `StudentRoster` — owns the list and provides every menu action

**`StudentRoster` methods:** `load_csv()`, `list_students()`,
`binary_search()`, `search_by_id()`, `run()`

**Binary search.** The linear scan is replaced with binary search. Records are
sorted by ID when loaded, since binary search requires ordered data. No
`list.index()` or `in` operator is used.

**Error handling.** File operations use `with open()` inside `try/except`.
A missing file prints a message and returns to the menu rather than crashing.
Malformed CSV rows are skipped individually instead of aborting the load.

**No global state.** Everything lives in instance attributes.

## Behavioural equivalence

The refactored version produces output identical to the fixed version. Both
were run against test cases T1 through T9 and the output matched line for line,
including the menu text, column widths, and search result formatting.

| Test | Input | Result |
|---|---|---|
| T1 | Load `students.csv` | 10 records loaded |
| T2 | Load again | Still 10, not duplicated |
| T3 | Option 2 before loading | Reports no data loaded |
| T4 | Option 2 after loading | Rows numbered 1–10, columns aligned |
| T5 | Search `s1005` lowercase | Finds Emily Chen |
| T6 | Search `S9999` | Reports no match |
| T7 | Search `S1001` then `S9999` | Second search reports no match |
| T8 | Search `S1010`, the last record | Found without an index error |
| T9 | Option 4 | Goodbye message, program exits |
