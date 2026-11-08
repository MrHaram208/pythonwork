import time
import functools

def ttl_cache(seconds):
    def decorator(func):
        cache = {}
        stats = {"hits": 0, "misses": 0}

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 1. Handle Unhashable Inputs (e.g., lists, dicts)
            try:
                # Equivalent keyword argument order ko handle karne ke liye sort karo
                sorted_kwargs = tuple(sorted(kwargs.items()))
                # Cache key: function arguments ka combination
                key = (args, sorted_kwargs)
                hash(key) # Check karo ke hashable hai ya nahi
            except TypeError:
                # Agar unhashable input aaya (jaise list), toh cache bypass karo
                stats["misses"] += 1
                return func(*args, **kwargs)

            # 2. Check Cache & Expiration
            current_time = time.monotonic()
            
            if key in cache:
                result, timestamp = cache[key]
                # Agar time expire nahi hua hai
                if current_time - timestamp < seconds:
                    stats["hits"] += 1
                    return result
                else:
                    # Expire ho gaya, delete karo
                    del cache[key]

            # 3. Cache Miss (Recompute)
            stats["misses"] += 1
            result = func(*args, **kwargs)
            
            # Result ko cache mein save karo current time ke sath
            cache[key] = (result, current_time)
            
            return result

        # Stats view karne ke liye helper method attach karo (testing ke liye)
        wrapper.cache_info = lambda: f"Cache Hits: {stats['hits']}, Misses: {stats['misses']}"
        wrapper.cache_clear = lambda: cache.clear()
        
        return wrapper
    return decorator


# ==========================================
# Sample Test
# ==========================================
if __name__ == "__main__":
    call_count = 0

    @ttl_cache(seconds=2) # 2 second ka TTL
    def slow_add(x, y):
        global call_count
        call_count += 1
        time.sleep(1) # Fake delay (heavy computation simulate karne ke liye)
        return x + y

    print("--- Testing Keyword Argument Order ---")
    print("Result 1:", slow_add(x=2, y=3)) # Miss -> 3 sec lagenge
    print("Result 2:", slow_add(y=3, x=2)) # Hit -> 0 sec lagenge (Order change hone ke bawajood)
    print(slow_add.cache_info())          # Output: Hits: 1, Misses: 1

    print("\n--- Testing Expiration (Wait for 2.5s) ---")
    time.sleep(2.5)
    print("Result 3:", slow_add(x=2, y=3)) # Miss -> Expire ho chuka hai
    print(slow_add.cache_info())          # Output: Hits: 1, Misses: 2

    print("\n--- Testing Unhashable Input (List) ---")
    @ttl_cache(seconds=2)
    def process_list(lst):
        return sum(lst)
    
    # List unhashable hoti hai, isliye yeh hamesha miss hoga aur cache bypass karega
    print("List Result 1:", process_list([1, 2, 3])) 
    print("List Result 2:", process_list([1, 2, 3])) 