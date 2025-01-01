import recognition

if __name__ == "__main__":
    try:
        result = recognition.mark_attendance()
        print("Attendance marked:", result)
    except Exception as e:
        print("Error:", e)
