# test.py
from assignment import Assignment
from category import Category
from class_profile import ClassProfile


eecs_348 = ClassProfile(name="EECS 348 - Software Engineering")


try:
    homework_cat = Category(name="Homework", weight=40)  # 40% weight
    exam_cat = Category(name="Exams", weight=60)        # 60% weight
    eecs_348.add_category(homework_cat)
    eecs_348.add_category(exam_cat)
except ValueError as e:
    print(f"Error creating categories: {e}")
    
# Check total declared weight
print(f"Total Declared Weight: {eecs_348.get_total_declared_weight()}%")


# Homework (40% Category)
hw1 = Assignment("HW 1", earned=9.5, possible=10)
hw2 = Assignment("HW 2", earned=18, possible=20)
homework_cat.add_assignment(hw1)
homework_cat.add_assignment(hw2)

# Exams (60% Category)
midterm = Assignment("Midterm Exam", earned=85, possible=100)
exam_cat.add_assignment(midterm)



# Check Category Scores
hw_score = homework_cat.get_category_score()
print(f"\n{homework_cat.name} Score: {hw_score['earned']}/{hw_score['possible']} ({round(hw_score['percentage'], 2)}%)")

exam_score = exam_cat.get_category_score()
print(f"{exam_cat.name} Score: {exam_score['earned']}/{exam_score['possible']} ({round(exam_score['percentage'], 2)}%)")

# Calculate Final Grade
current_grade = eecs_348.calculate_current_grade()

print(f"\n--- {eecs_348.name} ---")
print(f"Current Weighted Grade: {current_grade}%")