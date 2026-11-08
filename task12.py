class ReversibleRange:
    def __init__(self, start, stop, step=1):
        if step == 0:
            raise ValueError("ReversibleRange() arg 3 must not be zero")
        
        self.start = start
        self.stop = stop
        self.step = step
        
        # Python range() semantics ke mutabiq length calculate karo
        self._len = max(0, (stop - start + (step - (1 if step > 0 else -1))) // step)

    def __iter__(self):
        """Generator jo forward direction mein values yield karta hai"""
        current = self.start
        if self.step > 0:
            while current < self.stop:
                yield current
                current += self.step
        else:
            while current > self.stop:
                yield current
                current += self.step

    def __reversed__(self):
        """Generator jo reverse direction mein values yield karta hai"""
        if self._len == 0:
            return
            
        # Reverse iteration ke liye last element se start karo
        # Last element = start + (len - 1) * step
        current = self.start + (self._len - 1) * self.step
        
        if self.step > 0:
            while current >= self.start:
                yield current
                current -= self.step
        else:
            while current <= self.start:
                yield current
                current -= self.step

    def __len__(self):
        """Range mein kitne elements hain wo return karta hai (O(1))"""
        return self._len

    def __contains__(self, value):
        """Membership test bina list banaye (O(1))"""
        if self._len == 0:
            return False
            
        # 1. Check karo ke value range ke bounds ke andar hai ya nahi
        if self.step > 0:
            if value < self.start or value >= self.stop:
                return False
        else:
            if value > self.start or value <= self.stop:
                return False
                
        # 2. Check karo ke value step ka multiple hai ya nahi (start se)
        return (value - self.start) % self.step == 0

    def __repr__(self):
        return f"ReversibleRange({self.start}, {self.stop}, {self.step})"


# ==========================================
# Sample Test
# ==========================================
if __name__ == "__main__":
    r = ReversibleRange(2, 11, 3)
    
    print("--- Forward Iteration ---")
    print(list(r)) # Output: [2, 5, 8]
    
    print("\n--- Reversed Iteration ---")
    print(list(reversed(r))) # Output: [8, 5, 2]
    
    print("\n--- Membership Test ---")
    print("5 in r:", 5 in r)   # True
    print("6 in r:", 6 in r)   # False
    print("11 in r:", 11 in r) # False (stop exclusive)
    
    print("\n--- Length ---")
    print("len(r):", len(r))   # 3
    
    # Negative Step test
    print("\n--- Negative Step Test ---")
    r_neg = ReversibleRange(10, 0, -3)
    print(list(r_neg))          # [10, 7, 4, 1]
    print(list(reversed(r_neg))) # [1, 4, 7, 10]
    print("7 in r_neg:", 7 in r_neg) # True