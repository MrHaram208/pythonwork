def longest_unique_window(text):
    last_seen = {}      # char -> last index
    start = 0           # window ka left pointer
    best_start = 0
    best_len = 0

    for end, ch in enumerate(text):
        # Agar char pehle aaya hai aur current window ke andar hai
        if ch in last_seen and last_seen[ch] >= start:
            start = last_seen[ch] + 1

        last_seen[ch] = end

        curr_len = end - start + 1
        # Strictly ">" taake equal length par EARLIEST window rahe
        if curr_len > best_len:
            best_len = curr_len
            best_start = start

    return (text[best_start:best_start + best_len], best_start, best_len)
print(longest_unique_window("abcabcbb"))   # Output: ('abc', 0, 3)
print(longest_unique_window(""))           # Output: ('', 0, 0)