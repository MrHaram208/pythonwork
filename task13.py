from datetime import datetime

class Booking:
    def __init__(self, booking_id, room, start, end):
        self.booking_id = booking_id
        self.room = room
        self.start = start
        self.end = end

    def overlaps_with(self, other):
        """Check karta hai ke kya do bookings overlap karti hain"""
        # Standard interval overlap logic: start1 < end2 AND start2 < end1
        return self.start < other.end and other.start < self.end

    def __repr__(self):
        return f"Booking({self.booking_id}, {self.room}, {self.start.strftime('%H:%M')}-{self.end.strftime('%H:%M')})"


class Scheduler:
    def __init__(self):
        self.accepted_bookings = []  # List of valid bookings
        self.rejected_conflicts = [] # List of (booking_request, reason)
        self.seen_ids = set()        # Duplicate ID check ke liye

    def add_booking(self, booking_id, room, start_str, end_str, fmt="%H:%M"):
        try:
            start = datetime.strptime(start_str, fmt)
            end = datetime.strptime(end_str, fmt)
        except ValueError:
            self.rejected_conflicts.append((booking_id, "Invalid date/time format"))
            return False

        # Validation 1: Duplicate ID
        if booking_id in self.seen_ids:
            self.rejected_conflicts.append((booking_id, "Duplicate booking ID"))
            return False

        # Validation 2: End time start time se pehle ya barabar ho
        if end <= start:
            self.rejected_conflicts.append((booking_id, "End time must be greater than start time"))
            return False

        new_booking = Booking(booking_id, room, start, end)

        # Validation 3: Conflict check for the SAME room
        for existing in self.accepted_bookings:
            if existing.room == room and existing.overlaps_with(new_booking):
                self.rejected_conflicts.append((booking_id, f"Overlaps with existing booking {existing.booking_id}"))
                return False

        # Sab validations pass -> Accept booking
        self.accepted_bookings.append(new_booking)
        self.seen_ids.add(booking_id)
        return True

    def get_accepted_schedule(self):
        # Time ke hisaab se sorted schedule return karta hai
        return sorted(self.accepted_bookings, key=lambda b: (b.room, b.start))

    def get_rejected_conflicts(self):
        return self.rejected_conflicts


# ==========================================
# Sample Test
# ==========================================
if __name__ == "__main__":
    scheduler = Scheduler()

    # Test Case 1: 09:00–10:00 (Accepted)
    print("Book 1:", scheduler.add_booking("B1", "Room A", "09:00", "10:00"))

    # Test Case 2: 10:00–11:00 (Accepted - Adjacent)
    print("Book 2:", scheduler.add_booking("B2", "Room A", "10:00", "11:00"))

    # Test Case 3: 09:30–10:30 (Rejected - Overlap)
    print("Book 3:", scheduler.add_booking("B3", "Room A", "09:30", "10:30"))

    # Test Case 4: Different Room (Accepted)
    print("Book 4:", scheduler.add_booking("B4", "Room B", "09:30", "10:30"))

    # Test Case 5: Invalid Time (Rejected)
    print("Book 5:", scheduler.add_booking("B5", "Room A", "12:00", "11:00"))

    # Test Case 6: Duplicate ID (Rejected)
    print("Book 6:", scheduler.add_booking("B1", "Room A", "14:00", "15:00"))

    print("\n--- ACCEPTED SCHEDULE ---")
    for b in scheduler.get_accepted_schedule():
        print(b)

    print("\n--- REJECTED CONFLICTS ---")
    for b_id, reason in scheduler.get_rejected_conflicts():
        print(f"ID: {b_id} | Reason: {reason}")