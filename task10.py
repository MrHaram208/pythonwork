import csv
import os

def process_inventory(inventory_path, movements_path, updated_out_path, rejected_out_path):
    # 1. Inventory ko memory mein load karo (kyunki humein latest stock track karna hai)
    inventory = {} # format: { 'SKU': {'name': '...', 'quantity': int} }
    
    # Read Inventory
    try:
        with open(inventory_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                sku = row['sku'].strip()
                name = row['name'].strip()
                quantity = int(row['quantity'])
                inventory[sku] = {'name': name, 'quantity': quantity}
    except FileNotFoundError:
        print(f"Error: {inventory_path} not found. Creating empty inventory.")
    
    rejected_movements = []
    
    # 2. Movements apply karo (line by line to avoid loading huge file)
    if os.path.exists(movements_path):
        with open(movements_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                sku = row.get('sku', '').strip()
                move_type = row.get('type', '').strip().upper()
                units_str = row.get('units', '').strip()
                
                # Validation 1: Unknown SKU
                if sku not in inventory:
                    rejected_movements.append(row)
                    continue
                    
                # Validation 2: Invalid units (must be positive integer)
                try:
                    units = int(units_str)
                    if units <= 0:
                        rejected_movements.append(row)
                        continue
                except ValueError:
                    rejected_movements.append(row)
                    continue
                    
                # Validation 3: Invalid movement type
                if move_type not in ('IN', 'OUT'):
                    rejected_movements.append(row)
                    continue
                    
                # Validation 4: OUT causing negative stock
                current_qty = inventory[sku]['quantity']
                if move_type == 'OUT' and (current_qty - units) < 0:
                    rejected_movements.append(row)
                    continue
                    
                # Apply movement (If all validations pass)
                if move_type == 'IN':
                    inventory[sku]['quantity'] += units
                elif move_type == 'OUT':
                    inventory[sku]['quantity'] -= units

    # 3. Write Updated Inventory
    with open(updated_out_path, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['sku', 'name', 'quantity']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for sku, data in inventory.items():
            writer.writerow({
                'sku': sku,
                'name': data['name'],
                'quantity': data['quantity']
            })

    # 4. Write Rejected Movements
    with open(rejected_out_path, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['sku', 'type', 'units']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rejected_movements:
            writer.writerow({
                'sku': row.get('sku', ''),
                'type': row.get('type', ''),
                'units': row.get('units', '')
            })
            
    print(f"Processing complete. Updated: {updated_out_path}, Rejected: {rejected_out_path}")

# ==========================================
# Sample Test
# ==========================================
if __name__ == "__main__":
    # Dummy test files banate hain
    with open("inventory.csv", "w", newline="") as f:
        f.write("sku,name,quantity\nP01,Widget,10\nP02,Gadget,5\n")
        
    with open("movements.csv", "w", newline="") as f:
        f.write("sku,type,units\n")
        f.write("P01,OUT,4\n")   # Valid (10-4=6)
        f.write("P01,OUT,9\n")   # Invalid (6-9 = -3)
        f.write("P01,IN,2\n")    # Valid (6+2=8)
        f.write("P02,IN,0\n")    # Invalid (0 units)
        f.write("P99,IN,5\n")    # Invalid (Unknown SKU)
        f.write("P02,TRANSFER,2\n") # Invalid type

    # Process karo
    process_inventory("inventory.csv", "movements.csv", "updated_inventory.csv", "rejected_movements.csv")

    # Output verify karo
    print("\n--- Updated Inventory ---")
    with open("updated_inventory.csv", "r") as f:
        print(f.read().strip())

    print("\n--- Rejected Movements ---")
    with open("rejected_movements.csv", "r") as f:
        print(f.read().strip())

    # Clean up
    for filename in ["inventory.csv", "movements.csv", "updated_inventory.csv", "rejected_movements.csv"]:
        if os.path.exists(filename):
            os.remove(filename)