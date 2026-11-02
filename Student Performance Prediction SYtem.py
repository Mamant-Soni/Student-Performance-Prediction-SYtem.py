# ============================================================
# Student Performance Prediction System
# DSA Mini Project - Python Version
#
# Data Structures / Algorithms:
# 1. Hash Table with Separate Chaining
# 2. Binary Heap
# 3. Merge Sort
# 4. Binary Search
# 5. k-NN Regression
# 6. Weighted Formula Prediction
# 7. CSV File Persistence
# ============================================================

import math
import csv
import os


# ============================================================
# 1. STUDENT DATA MODEL
# ============================================================

class Student:

    def __init__(
        self,
        student_id=0,
        name="",
        attendance=0,
        internals=0,
        assignments=0,
        cgpa=0,
        study_hours=0,
        final_marks=-1
    ):
        self.id = student_id
        self.name = name
        self.attendance = attendance
        self.internals = internals
        self.assignments = assignments
        self.cgpa = cgpa
        self.study_hours = study_hours
        self.final_marks = final_marks
        self.score = 0


# ============================================================
# FEATURES
# ============================================================

def features(student):

    return [
        student.attendance,
        student.internals,
        student.assignments,
        student.cgpa * 10,
        min(student.study_hours * 10, 100)
    ]


# ============================================================
# WEIGHTED FORMULA
# ============================================================

def formula_score(student):

    f = features(student)

    return (
        0.25 * f[0]
        + 0.30 * f[1]
        + 0.20 * f[2]
        + 0.20 * f[3]
        + 0.05 * f[4]
    )


# ============================================================
# CATEGORY
# ============================================================

def category(score):

    if score >= 80:
        return "Excellent"

    if score >= 65:
        return "Good"

    if score >= 50:
        return "Average"

    return "At-Risk"


# ============================================================
# 2. HASH TABLE - SEPARATE CHAINING
# ============================================================

class HashTable:

    class Node:

        def __init__(self, key, value):
            self.key = key
            self.value = value

    def __init__(self, capacity=11):

        self.table = [[] for _ in range(capacity)]
        self.count = 0

    def hash_function(self, key):

        return key % len(self.table)

    def rehash(self):

        old_table = self.table

        self.table = [[] for _ in range(len(old_table) * 2 + 1)]

        for bucket in old_table:

            for node in bucket:

                index = self.hash_function(node.key)

                self.table[index].append(
                    self.Node(node.key, node.value)
                )

    def put(self, key, value):

        index = self.hash_function(key)

        for node in self.table[index]:

            if node.key == key:

                node.value = value
                return

        if self.count + 1 > 0.75 * len(self.table):

            self.rehash()

        index = self.hash_function(key)

        self.table[index].append(
            self.Node(key, value)
        )

        self.count += 1

    def get(self, key):

        index = self.hash_function(key)

        for node in self.table[index]:

            if node.key == key:
                return node.value

        return -1

    def clear(self):

        self.table = [[] for _ in range(11)]
        self.count = 0


# ============================================================
# 3. BINARY HEAP
# ============================================================

class BinaryHeap:

    def __init__(self, higher_priority):

        self.array = []
        self.higher_priority = higher_priority

    def empty(self):

        return len(self.array) == 0

    def size(self):

        return len(self.array)

    def top(self):

        if not self.array:
            return None

        return self.array[0]

    def push(self, item):

        self.array.append(item)

        self.sift_up(len(self.array) - 1)

    def pop(self):

        if not self.array:
            return None

        top = self.array[0]

        self.array[0] = self.array[-1]

        self.array.pop()

        if self.array:

            self.sift_down(0)

        return top

    def sift_up(self, index):

        while index > 0:

            parent = (index - 1) // 2

            if not self.higher_priority(
                self.array[index],
                self.array[parent]
            ):
                break

            self.array[parent], self.array[index] = (
                self.array[index],
                self.array[parent]
            )

            index = parent

    def sift_down(self, index):

        n = len(self.array)

        while True:

            left = 2 * index + 1
            right = 2 * index + 2

            best = index

            if (
                left < n
                and self.higher_priority(
                    self.array[left],
                    self.array[best]
                )
            ):
                best = left

            if (
                right < n
                and self.higher_priority(
                    self.array[right],
                    self.array[best]
                )
            ):
                best = right

            if best == index:
                break

            self.array[index], self.array[best] = (
                self.array[best],
                self.array[index]
            )

            index = best


# ============================================================
# 4. MERGE SORT
# ============================================================

def merge_sort(array, key_function, reverse=False):

    if len(array) <= 1:
        return array

    mid = len(array) // 2

    left = merge_sort(
        array[:mid],
        key_function,
        reverse
    )

    right = merge_sort(
        array[mid:],
        key_function,
        reverse
    )

    result = []

    i = 0
    j = 0

    while i < len(left) and j < len(right):

        left_key = key_function(left[i])
        right_key = key_function(right[j])

        if reverse:

            if left_key >= right_key:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        else:

            if left_key <= right_key:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result


# ============================================================
# NEIGHBOR
# ============================================================

class Neighbor:

    def __init__(self, distance, index):

        self.distance = distance
        self.index = index


# ============================================================
# STUDENT DATABASE
# ============================================================

class StudentDB:

    def __init__(self):

        self.data = []

        # ID -> index
        self.index = HashTable()

    def size(self):

        return len(self.data)

    # --------------------------------------------------------
    # ADD STUDENT
    # --------------------------------------------------------

    def add(self, student):

        if self.index.get(student.id) != -1:

            return False

        student.score = formula_score(student)

        self.index.put(
            student.id,
            len(self.data)
        )

        self.data.append(student)

        return True

    # --------------------------------------------------------
    # FIND STUDENT
    # --------------------------------------------------------

    def find(self, student_id):

        position = self.index.get(student_id)

        if position == -1:
            return None

        return self.data[position]

    # --------------------------------------------------------
    # RANKED STUDENTS
    # --------------------------------------------------------

    def ranked(self):

        students = self.data.copy()

        students = merge_sort(
            students,
            lambda student: (
                student.score,
                -student.id
            ),
            reverse=True
        )

        return students

    # --------------------------------------------------------
    # TOP K
    # --------------------------------------------------------

    def top_k(self, k):

        # Min heap:
        # student with smallest score has highest priority

        def min_score_priority(a, b):

            return a[0] < b[0]

        heap = BinaryHeap(min_score_priority)

        for i, student in enumerate(self.data):

            heap.push(
                (student.score, i)
            )

            if heap.size() > k:

                heap.pop()

        result = []

        while not heap.empty():

            score, index = heap.pop()

            result.append(
                self.data[index]
            )

        result.reverse()

        return result

    # --------------------------------------------------------
    # AT-RISK STUDENTS
    # --------------------------------------------------------

    def at_risk(self, threshold=50):

        students = []

        for student in self.data:

            if student.score < threshold:

                students.append(student)

        return merge_sort(
            students,
            lambda student: student.score
        )

    # --------------------------------------------------------
    # BINARY SEARCH RANK
    # --------------------------------------------------------

    def rank_of_score(self, score):

        ranked_students = self.ranked()

        low = 0
        high = len(ranked_students)

        while low < high:

            mid = (low + high) // 2

            if ranked_students[mid].score > score:

                low = mid + 1

            else:

                high = mid

        return low + 1

    # --------------------------------------------------------
    # K-NN PREDICTION
    # --------------------------------------------------------

    def knn_predict(
        self,
        query_student,
        k
    ):

        query_features = features(query_student)

        # Max heap based on distance
        # Farthest neighbor stays at top

        def max_distance_priority(a, b):

            return a.distance > b.distance

        heap = BinaryHeap(max_distance_priority)

        for i, student in enumerate(self.data):

            if student.final_marks < 0:

                continue

            student_features = features(student)

            distance = 0

            for j in range(5):

                difference = (
                    student_features[j]
                    - query_features[j]
                )

                distance += difference * difference

            distance = math.sqrt(distance)

            neighbor = Neighbor(
                distance,
                i
            )

            heap.push(neighbor)

            if heap.size() > k:

                heap.pop()

        if heap.empty():

            return -1, []

        numerator = 0
        denominator = 0

        neighbors = []

        while not heap.empty():

            neighbor = heap.pop()

            weight = 1 / (
                neighbor.distance + 0.000001
            )

            student = self.data[
                neighbor.index
            ]

            numerator += (
                weight * student.final_marks
            )

            denominator += weight

            neighbors.append(neighbor)

        prediction = numerator / denominator

        return prediction, neighbors

    def save(self, path):

        try:

            with open(
                path,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.writer(file)

                for student in self.data:

                    writer.writerow([
                        student.id,
                        student.name,
                        student.attendance,
                        student.internals,
                        student.assignments,
                        student.cgpa,
                        student.study_hours,
                        student.final_marks
                    ])

            return True

        except Exception:

            return False

    # --------------------------------------------------------
    # LOAD CSV
    # --------------------------------------------------------

    def load(self, path):

        if not os.path.exists(path):

            return False

        self.data.clear()
        self.index.clear()

        try:

            with open(
                path,
                "r",
                encoding="utf-8"
            ) as file:

                reader = csv.reader(file)

                for row in reader:

                    if len(row) != 8:
                        continue

                    try:

                        student = Student(
                            int(row[0]),
                            row[1],
                            float(row[2]),
                            float(row[3]),
                            float(row[4]),
                            float(row[5]),
                            float(row[6]),
                            float(row[7])
                        )

                        self.add(student)

                    except ValueError:

                        continue

            return len(self.data) > 0

        except Exception:

            return False


# ============================================================
# INPUT FUNCTIONS
# ============================================================

def read_num(prompt, minimum, maximum):

    while True:

        try:

            value = float(
                input(
                    f"{prompt} ({minimum}-{maximum}): "
                )
            )

            if minimum <= value <= maximum:

                return value

            print("Invalid input, try again.")

        except ValueError:

            print("Please enter a valid number.")


# ============================================================
# READ STUDENT
# ============================================================

def read_student(ask_id=True, ask_final=True):

    student = Student()

    if ask_id:

        student.id = int(
            read_num(
                "Student ID",
                1,
                999999
            )
        )

        student.name = input("Name: ").strip()

        student.name = student.name.replace(",", " ")

        if not student.name:

            student.name = "Unnamed"

    student.attendance = read_num(
        "Attendance %",
        0,
        100
    )

    student.internals = read_num(
        "Internal marks",
        0,
        100
    )

    student.assignments = read_num(
        "Assignment score",
        0,
        100
    )

    student.cgpa = read_num(
        "Previous CGPA",
        0,
        10
    )

    student.study_hours = read_num(
        "Study hours per day",
        0,
        10
    )

    if ask_final:

        student.final_marks = read_num(
            "Final marks (-1 if not known yet)",
            -1,
            100
        )

    return student


# ============================================================
# PRINT HEADER
# ============================================================

def print_header():

    print(
        f"{'ID':<8}"
        f"{'Name':<18}"
        f"{'Att%':>7}"
        f"{'Int':>7}"
        f"{'Asg':>7}"
        f"{'CGPA':>7}"
        f"{'Hrs':>6}"
        f"{'Score':>9}"
        f"  {'Category'}"
    )

    print("-" * 78)


# ============================================================
# PRINT STUDENT
# ============================================================

def print_row(student):

    print(
        f"{student.id:<8}"
        f"{student.name[:17]:<18}"
        f"{student.attendance:>7.1f}"
        f"{student.internals:>7.1f}"
        f"{student.assignments:>7.1f}"
        f"{student.cgpa:>7.1f}"
        f"{student.study_hours:>6.1f}"
        f"{student.score:>9.1f}"
        f"  {category(student.score)}"
    )


# ============================================================
# PRINT LIST
# ============================================================

def print_list(students):

    if not students:

        print("(none)")
        return

    print_header()

    for student in students:

        print_row(student)


# ============================================================
# SAMPLE DATA
# ============================================================

def seed(db):

    rows = [

        (101, "Aarav Sharma", 92, 88, 90, 9.1, 4, 91),
        (102, "Diya Verma", 85, 79, 82, 8.4, 3, 83),
        (103, "Rohan Gupta", 60, 55, 58, 6.2, 1.5, 57),
        (104, "Simran Kaur", 96, 94, 95, 9.5, 5, 95),
        (105, "Kabir Singh", 72, 65, 70, 7.1, 2, 68),
        (106, "Ananya Rao", 40, 35, 42, 5.0, 1, 38),
        (107, "Vikram Yadav", 78, 74, 71, 7.6, 2.5, 74),
        (108, "Neha Joshi", 88, 90, 86, 8.8, 4, 89),
        (109, "Arjun Mehta", 55, 48, 50, 5.8, 1, 49),
        (110, "Priya Nair", 81, 77, 80, 8.0, 3, 80),
        (111, "Manav Malik", 67, 62, 60, 6.9, 2, 63),
        (112, "Ishita Bansal", 93, 85, 91, 8.9, 4.5, 88),
        (113, "Karan Chopra", 48, 52, 45, 5.4, 0.5, 46),
        (114, "Tanvi Arora", 75, 80, 78, 7.8, 3, 77),
        (115, "Sahil Dahiya", 64, 58, 66, 6.5, 2, 60)

    ]

    for row in rows:

        student = Student(
            student_id=row[0],
            name=row[1],
            attendance=row[2],
            internals=row[3],
            assignments=row[4],
            cgpa=row[5],
            study_hours=row[6],
            final_marks=row[7]
        )

        db.add(student)


# ============================================================
# MENU
# ============================================================

def menu():

    print(
        "\n===== Student Performance Prediction System ====="
    )

    print(" 1. Add student")
    print(" 2. View all students (ranked)")
    print(" 3. Search student by ID")
    print(" 4. Top-K performers")
    print(" 5. At-risk students")
    print(" 6. Predict performance for a new student")
    print(" 7. Rank a given score (binary search)")
    print(" 8. Save data")
    print(" 0. Exit")


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    FILE = "students.csv"

    db = StudentDB()

    if db.load(FILE):

        print(
            f"Loaded {db.size()} students from {FILE}."
        )

    else:

        seed(db)

        print(
            f"No saved data found - "
            f"loaded {db.size()} sample students."
        )

    while True:

        menu()

        try:

            choice = int(
                input("Choice: ")
            )

        except ValueError:

            print(
                "Enter a number from the menu."
            )

            continue

        # ----------------------------------------------------
        # EXIT
        # ----------------------------------------------------

        if choice == 0:

            db.save(FILE)

            print("Data saved. Bye!")

            break

        # ----------------------------------------------------
        # ADD STUDENT
        # ----------------------------------------------------

        elif choice == 1:

            student = read_student(
                True,
                True
            )

            if db.add(student):

                found = db.find(
                    student.id
                )

                print(
                    f"Added. Predicted score: "
                    f"{found.score:.1f} "
                    f"({category(found.score)})"
                )

            else:

                print(
                    "A student with this ID already exists."
                )

        # ----------------------------------------------------
        # VIEW RANKING
        # ----------------------------------------------------

        elif choice == 2:

            print_list(
                db.ranked()
            )

        # ----------------------------------------------------
        # SEARCH
        # ----------------------------------------------------

        elif choice == 3:

            student_id = int(
                read_num(
                    "Student ID",
                    1,
                    999999
                )
            )

            student = db.find(student_id)

            if student is None:

                print("Not found.")

            else:

                print_header()

                print_row(student)

                if student.final_marks >= 0:

                    print(
                        f"Actual final marks: "
                        f"{student.final_marks:.1f}"
                    )

        # ----------------------------------------------------
        # TOP K
        # ----------------------------------------------------

        elif choice == 4:

            k = int(
                read_num(
                    "How many top students (K)",
                    1,
                    100
                )
            )

            print_list(
                db.top_k(k)
            )

        # ----------------------------------------------------
        # AT RISK
        # ----------------------------------------------------

        elif choice == 5:

            students = db.at_risk(50)

            print(
                "Students predicted below 50:"
            )

            print_list(students)

        # ----------------------------------------------------
        # PREDICT NEW STUDENT
        # ----------------------------------------------------

        elif choice == 6:

            query_student = read_student(
                False,
                False
            )

            formula = formula_score(
                query_student
            )

            knn, neighbors = db.knn_predict(
                query_student,
                3
            )

            print(
                f"\n[Weighted formula] "
                f"predicted score: "
                f"{formula:.1f} "
                f"-> {category(formula)}"
            )

            if knn < 0:

                print(
                    "[k-NN] no training data available."
                )

            else:

                print(
                    f"[k-NN, k=3] "
                    f"predicted marks: "
                    f"{knn:.1f} "
                    f"-> {category(knn)}"
                )

                print(
                    "   Similar past students:",
                    end=""
                )

                for neighbor in neighbors:

                    student = db.data[
                        neighbor.index
                    ]

                    print(
                        f"  {student.name} "
                        f"({student.final_marks})",
                        end=""
                    )

                print()

                combined = (
                    formula + knn
                ) / 2

                print(
                    f"[Combined] "
                    f"{combined:.1f} "
                    f"-> {category(combined)}"
                )

        # ----------------------------------------------------
        # BINARY SEARCH RANK
        # ----------------------------------------------------

        elif choice == 7:

            score = read_num(
                "Score",
                0,
                100
            )

            rank = db.rank_of_score(
                score
            )

            print(
                f"A score of {score:.1f} "
                f"would rank #{rank} "
                f"out of {db.size() + 1}."
            )

        # ----------------------------------------------------
        # SAVE
        # ----------------------------------------------------

        elif choice == 8:

            if db.save(FILE):

                print(
                    f"Saved to {FILE}"
                )

            else:

                print(
                    "Could not save file."
                )

        # ----------------------------------------------------
        # INVALID
        # ----------------------------------------------------

        else:

            print("Invalid choice.")


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":

    main()