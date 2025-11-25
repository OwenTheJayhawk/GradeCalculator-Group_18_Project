# Grade Calculator Application

A **Python/PyQt** application that lets students calculate grades based on assignments and assignment categories that have corresponding weights. The application also allows students to calculate the percentage grade needed on an upcoming assignment to achieve a specified letter grade.

## 📥 Download

### **Windows**
Simply download **GradeCalculator.exe** and run it.

Download Link:  
https://drive.google.com/file/d/1pPxCmmotGKJOFxo-b6LduTVmBkOPoOh0/view?usp=sharing

### **Linux**
Download the project folder and ensure **Python** and **PyQt5** are installed. Then run:

```bash
./run.sh
```

If you get a permissions error:

```bash
chmod +x run.sh
```

## ⭐ Features

### **Classes**
Add your academic classes that contain:
- Class categories  
- Assignments  
- Letter grade thresholds  

### **Categories**
- Each category has a weight.
- Add assignments into categories.  
- Category weights must not exceed **100%**.

### **Assignments**
- Define total possible points.
- Enter points earned.
- Must belong to a category.

### **Grade Thresholds**
- Percentage required to earn each letter grade.
- Fully customizable.
- Thresholds must not overlap.

## 📊 Hypothetical Grades

Create a hypothetical assignment and calculate what score you must earn to achieve a specific letter grade.

## 💾 Save / Load

Class data can be saved and loaded for later use.
