def read_errors(path):
    """
    Generator jo file ko line-by-line read karta hai.
    Sirf ERROR level wali valid lines yield karta hai.
    """
    malformed_count = 0
    
    try:
        # File ko lazily open karo (memory mein load nahi hogi)
        with open(path, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()
                
                # Khali lines ko skip karo
                if not line:
                    continue
                
                # Format check: YYYY-MM-DD HH:MM:SS | LEVEL | message
                parts = line.split('|')
                
                # Agar parts 3 nahi hain, toh line malformed hai
                if len(parts) != 3:
                    malformed_count += 1
                    continue
                
                timestamp_str = parts[0].strip()
                level = parts[1].strip()
                message = parts[2].strip()
                
                # Timestamp format ko basic validate karo
                # (Asal scenario mein datetime.strptime use kar sakte hain, 
                # par yahan simple length check kaafi hai)
                if len(timestamp_str) < 19:
                    malformed_count += 1
                    continue

                # Sirf ERROR lines yield karo
                if level == "ERROR":
                    yield (line_number, timestamp_str, message)
                    
    except FileNotFoundError:
        print(f"Error: File '{path}' not found.")
    
    # Generator end hone par malformed count ko expose karna
    # (Real world mein isko yield kiya ja sakta hai ya global rakha ja sakta hai)
    global LAST_MALFORMED_COUNT
    LAST_MALFORMED_COUNT = malformed_count


def summarize_errors(path):
    """
    Errors ko date (YYYY-MM-DD) ke hisaab se count karta hai.
    """
    error_summary = {}
    
    # read_errors generator ko consume karo
    for line_num, timestamp, message in read_errors(path):
        # Timestamp se sirf date nikalo (YYYY-MM-DD)
        date = timestamp.split(' ')[0]
        
        if date in error_summary:
            error_summary[date] += 1
        else:
            error_summary[date] = 1
            
    return error_summary


# ==========================================
# Sample Test
# ==========================================
if __name__ == "__main__":
    # Ek dummy log file banate hain test ke liye
    sample_log_content = """2026-11-07 10:30:00 | ERROR | Connection lost
2026-11-07 10:31:00 | INFO | User logged in
2026-11-07 10:32:00 | ERROR | Database timeout
Malformed line without pipes
2026-11-08 09:00:00 | ERROR | Disk full
2026-11-08 09:05:00 | WARNING | Memory high
2026-11-08 09:10:00 | ERROR | CPU spike
2026-11-07 11:00:00 | ERROR | Server crash
"""
    
    # File likho
    with open("test_log.txt", "w") as f:
        f.write(sample_log_content)

    print("--- 1. Testing read_errors() ---")
    for error in read_errors("test_log.txt"):
        print(error)
        
    print(f"\n[Malformed lines skipped: {LAST_MALFORMED_COUNT}]")

    print("\n--- 2. Testing summarize_errors() ---")
    summary = summarize_errors("test_log.txt")
    print(summary)
    
    # Clean up
    import os
    os.remove("test_log.txt")