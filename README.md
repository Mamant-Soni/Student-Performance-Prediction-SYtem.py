# Student Performance Prediction System (DSA Mini Project)

A menu-driven C++ program that stores student records, ranks them, flags at-risk students and
predicts the performance of a new student, using **only hand-written data structures and algorithms**.

## Build & run
```
g++ -std=c++17 -O2 main.cpp -o spps
./spps
```
Data is saved to `students.csv` (auto-loaded next run; sample data is used if the file is missing).

## Problem statement
Given attendance, internal marks, assignment score, previous CGPA and daily study hours,
predict a student's final performance (Excellent / Good / Average / At-Risk) so teachers can
spot weak students early.

## DSA used

| Feature | Data structure / algorithm | Complexity |
|---|---|---|
| Find student by ID | Hash table, separate chaining, auto-rehash at load factor 0.75 | O(1) average |
| Ranked list of all students | Merge sort (score desc, ties by ID) | O(n log n) |
| Top-K performers | Min-heap of size K | O(n log K) |
| At-risk students | Filter + merge sort | O(n log n) |
| Rank of any score | Binary search on ranked list | O(log n) after sort |
| Prediction (data driven) | k-Nearest Neighbours; max-heap keeps K closest | O(n log K) |
| Prediction (rule based) | Weighted formula | O(1) |

## Prediction model
**Weighted formula** (all features scaled to 0-100):

`score = 0.25*attendance + 0.30*internals + 0.20*assignments + 0.20*(CGPA*10) + 0.05*(study hrs*10)`

**k-NN (k = 3):** Euclidean distance over the 5 scaled features against past students with known
final marks; the prediction is the inverse-distance-weighted average of the 3 nearest students' final marks.
Final output shows both plus their average.

| Score | Category |
|---|---|
| >= 80 | Excellent |
| 65 - 79 | Good |
| 50 - 64 | Average |
| < 50 | At-Risk |

## Possible viva questions
- Why a hash table instead of a vector scan? -> O(1) vs O(n) lookup.
- Why a min-heap for Top-K instead of sorting? -> O(n log K) and only K items in memory.
- Why merge sort? -> Stable and guaranteed O(n log n).
- What happens on hash collisions? -> Chaining with linked lists, rehash when load factor > 0.75.
- Limitations? -> Weights are hand-picked; k-NN needs enough past data.

## Future scope
Linear regression for learned weights, BST/AVL index for range queries, GUI or web front end,
graph-based study-group suggestions.

