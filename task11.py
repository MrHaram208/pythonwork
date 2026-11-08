import csv
import os

def generate_gradebook(students_file, scores_file, report_file):
    students = {}
    scores = {} # format: {student_id: [marks1, marks2, ...]}
    
    # 1. Read Students File (Handle FileNotFound)
    try:
        with open(students_file, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                s_id = row['student_id'].strip()
                name = row['name'].strip()
                students[s_id] = name
                scores[s_id] = [] # Initialize empty list for scores
    except FileNotFoundError:
        print(f"Error: {students_file} not found.")
        return

    # 2. Read Scores File & Validate
    seen_pairs = set() # To track duplicate student-subject entries
    
    try:
        with open(scores_file, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                s_id = row.get('student_id', '').strip()
                subject = row.get('subject', '').strip()
                marks_str = row.get('marks', '').strip()
                
                # Validation 1: Unknown ID
                if s_id not in students:
                    continue
                    
                # Validation 2: Duplicate entry
                pair = (s_id, subject)
                if pair in seen_pairs:
                    continue
                seen_pairs.add(pair)
                
                # Validation 3: Marks between 0 and 100
                try:
                    marks = float(marks_str)
                    if not (0 <= marks <= 100):
                        continue
                except ValueError:
                    continue # Invalid number (e.g., "abc")
                
                # Valid score add karo
                scores[s_id].append(marks)
                
    except FileNotFoundError:
        print(f"Error: {scores_file} not found.")
        return

    # 3. Calculate Average & Grade for each student
    report_data = []
    
    for s_id, name in students.items():
        student_scores = scores[s_id]
        
        if student_scores:
            average = sum(student_scores) / len(student_scores)
        else:
            average = 0.0 # Koi valid score nahi mila
            
        # Grade logic
        if average >= 85: grade = 'A'
        elif average >= 70: grade = 'B'
        elif average >= 55: grade = 'C'
        elif average >= 40: grade = 'D'
        else: grade = 'F'
        
        report_data.append({
            'student_id': s_id,
            'name': name,
            'average': average,
            'grade': grade
        })

    # 4. Rank calculate karo (Average descending, then ID ascending for ties)
    # Sorting criteria: (-average, student_id)
    report_data.sort(key=lambda x: (-x['average'], int(x['student_id']) if x['student_id'].isdigit() else x['student_id']))
    
    # Rank assign karo (ties get same rank)
    for i, student in enumerate(report_data):
        if i > 0 and student['average'] == report_data[i-1]['average']:
            student['rank'] = report_data[i-1]['rank']
        else:
            student['rank'] = i + 1

    # 5. Write Output to CSV
    with open(report_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['student_id', 'name', 'average', 'grade', 'rank']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in report_data:
            # Average ko 2 decimal places par format karo file mein likhne ke liye
            row['average'] = round(row['average'], 2)
            writer.writerow(row)
            
    print(f"Report successfully generated at {report_file}")


# ==========================================
# Sample Test
# ==========================================
if __name__ == "__main__":
    # Dummy files banate hain
    with open("students.csv", "w", newline="") as f:
        f.write("student_id,name\n101,Alice\n102,Bob\n103,Charlie\n")
        
    with open("scores.csv", "w", newline="") as f:
        f.write("student_id,subject,marks\n")
        f.write("101,Math,90\n")
        f.write("101,Science,80\n")
        f.write("101,English,85\n")   # Alice avg = 85.0 (Grade A)
        f.write("102,Math,70\n")
        f.write("102,Science,65\n")   # Bob avg = 67.5 (Grade C)
        f.write("103,Math,105\n")     # Rejected: > 100
        f.write("103,Science,50\n")   # Charlie avg = 50.0 (Grade D)
        f.write("101,Math,95\n")      # Rejected: Duplicate subject
        f.write("999,Math,90\n")      # Rejected: Unknown ID
        
    # Run function
    generate_gradebook("students.csv", "scores.csv", "report.csv")

    # Output print karke verify karo
    print("\n--- report.csv ---")
    if os.path.exists("report.csv"):
        with open("report.csv", "r") as f:
            print(f.read().strip())

    # Clean up
    for file in ["students.csv", "scores.csv", "report.csv"]:
        if os.path.exists(file):
            os.remove(file)