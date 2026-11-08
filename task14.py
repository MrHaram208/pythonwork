import json
import os
import re

DB_FILE = "contacts.json"

# ==========================================
# 1. Storage Layer (JSON Handling)
# ==========================================
def load_contacts():
    """JSON file se data safely load karta hai."""
    if not os.path.exists(DB_FILE):
        return {} # Agar file nahi hai, toh khali dictionary return karo
    
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if not isinstance(data, dict):
                raise ValueError("Root element is not a dictionary")
            return data
    except (json.JSONDecodeError, ValueError) as e:
        print(f"\n[WARNING] Data file '{DB_FILE}' is corrupt or invalid: {e}")
        print("[WARNING] A backup has been created. Starting with empty contacts.\n")
        # Safe fallback: Corrupt file ko delete mat karo, balke rename karke backup banao
        os.rename(DB_FILE, DB_FILE + ".corrupt_backup")
        return {}

def save_contacts(contacts):
    """Data ko JSON file mein save karta hai."""
    try:
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(contacts, f, indent=4)
    except Exception as e:
        print(f"[ERROR] Could not save data: {e}")

# ==========================================
# 2. Business Logic Layer (CRUD & Validation)
# ==========================================
def validate_email(email):
    """Basic email regex validation."""
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None

def add_contact(contacts, c_id, name, phone, email):
    if c_id in contacts:
        return False, "Contact ID already exists."
    if not name.strip():
        return False, "Name cannot be empty."
    if not validate_email(email):
        return False, "Invalid email format."
    
    contacts[c_id] = {"name": name.strip(), "phone": phone.strip(), "email": email.strip()}
    save_contacts(contacts)
    return True, "Contact added successfully."

def search_contacts(contacts, query):
    """Case-insensitive name search."""
    query = query.lower()
    results = {}
    for c_id, data in contacts.items():
        if query in data["name"].lower():
            results[c_id] = data
    return results

def update_contact(contacts, c_id, name=None, phone=None, email=None):
    if c_id not in contacts:
        return False, "Contact not found."
    
    if name is not None and name.strip():
        contacts[c_id]["name"] = name.strip()
    if phone is not None:
        contacts[c_id]["phone"] = phone.strip()
    if email is not None:
        if not validate_email(email):
            return False, "Invalid email format."
        contacts[c_id]["email"] = email.strip()
        
    save_contacts(contacts)
    return True, "Contact updated successfully."

def delete_contact(contacts, c_id):
    if c_id not in contacts:
        return False, "Contact not found."
    del contacts[c_id]
    save_contacts(contacts)
    return True, "Contact deleted successfully."

# ==========================================
# 3. Presentation Layer (CLI Menu)
# ==========================================
def print_contact(c_id, data):
    print(f"  ID: {c_id} | Name: {data['name']:<15} | Phone: {data['phone']:<12} | Email: {data['email']}")

def main():
    contacts = load_contacts()
    
    while True:
        print("\n" + "="*40)
        print("      CONTACT MANAGER CLI")
        print("="*40)
        print("1. Add Contact")
        print("2. Search Contact (by Name)")
        print("3. Update Contact")
        print("4. Delete Contact")
        print("5. List All Contacts")
        print("6. Exit")
        print("="*40)
        
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == '1':
            c_id = input("Enter unique ID: ").strip()
            name = input("Enter Name: ").strip()
            phone = input("Enter Phone: ").strip()
            email = input("Enter Email: ").strip()
            
            success, msg = add_contact(contacts, c_id, name, phone, email)
            print(f"[{'OK' if success else 'FAILED'}] {msg}")
            
        elif choice == '2':
            query = input("Enter name to search: ").strip()
            results = search_contacts(contacts, query)
            if results:
                print(f"\nFound {len(results)} contact(s):")
                for c_id, data in results.items():
                    print_contact(c_id, data)
            else:
                print("No contacts found matching that name.")
                
        elif choice == '3':
            c_id = input("Enter ID to update: ").strip()
            if c_id not in contacts:
                print("[FAILED] Contact not found.")
                continue
            print("Leave blank to keep existing value.")
            name = input(f"New Name [{contacts[c_id]['name']}]: ").strip() or None
            phone = input(f"New Phone [{contacts[c_id]['phone']}]: ").strip() or None
            email = input(f"New Email [{contacts[c_id]['email']}]: ").strip() or None
            
            success, msg = update_contact(contacts, c_id, name, phone, email)
            print(f"[{'OK' if success else 'FAILED'}] {msg}")
            
        elif choice == '4':
            c_id = input("Enter ID to delete: ").strip()
            confirm = input(f"Are you sure you want to delete ID {c_id}? (y/n): ").strip().lower()
            if confirm == 'y':
                success, msg = delete_contact(contacts, c_id)
                print(f"[{'OK' if success else 'FAILED'}] {msg}")
            else:
                print("Deletion cancelled.")
                
        elif choice == '5':
            if not contacts:
                print("Contact list is empty.")
            else:
                print(f"\nTotal Contacts: {len(contacts)}")
                for c_id, data in contacts.items():
                    print_contact(c_id, data)
                    
        elif choice == '6':
            print("Exiting Contact Manager. Goodbye!")
            break
        else:
            print("[FAILED] Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()