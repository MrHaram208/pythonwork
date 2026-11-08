import json
import os
import uuid
import unittest

# ==========================================
# 1. OOP Classes & Composition
# ==========================================
class Product:
    def __init__(self, p_id, name, price, stock):
        self.p_id = p_id
        self.name = name
        self.price = price
        self.stock = stock

class Inventory:
    def __init__(self):
        self.products = {} # {p_id: Product object}

    def load_from_dict(self, data):
        for p in data:
            self.products[p['id']] = Product(p['id'], p['name'], p['price'], p['stock'])

class Cart:
    def __init__(self):
        self.items = [] # List of (p_id, quantity)
        self.discount_percent = 0

    def add_item(self, p_id, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        self.items.append((p_id, quantity))

    def apply_discount(self, percent):
        if not (0 <= percent <= 100):
            raise ValueError("Discount must be between 0 and 100.")
        self.discount_percent = percent

class Order:
    def __init__(self, cart, inventory):
        self.order_id = f"ORD-{uuid.uuid4().hex[:6].upper()}"
        self.items = cart.items
        self.discount = cart.discount_percent
        self.total = 0.0
        self.inventory = inventory

    def validate_and_calculate(self):
        """Validates stock and calculates total without changing inventory yet."""
        subtotal = 0.0
        
        # 1. Validate all items first
        for p_id, qty in self.items:
            if p_id not in self.inventory.products:
                raise ValueError(f"Product {p_id} not found in inventory.")
            product = self.inventory.products[p_id]
            if product.stock < qty:
                raise ValueError(f"Insufficient stock for {product.name}. Available: {product.stock}, Requested: {qty}")
            subtotal += product.price * qty

        # 2. Calculate total with discount
        discount_amount = subtotal * (self.discount / 100.0)
        self.total = subtotal - discount_amount

    def process_order(self, filepath):
        """Updates stock and persists order with rollback on failure."""
        self.validate_and_calculate() # Throws error if invalid

        # --- SNAPSHOT for Rollback ---
        # Agar save fail ho jaye, toh stock wapis original par lane ke liye
        original_stocks = {p_id: self.inventory.products[p_id].stock for p_id, _ in self.items}

        try:
            # 1. Update Inventory (Stock Deduct)
            for p_id, qty in self.items:
                self.inventory.products[p_id].stock -= qty

            # 2. Persist Order to JSON
            order_data = {
                "order_id": self.order_id,
                "items": [{"product_id": p_id, "quantity": qty} for p_id, qty in self.items],
                "discount_percent": self.discount,
                "total_amount": round(self.total, 2)
            }

            # Load existing orders if file exists
            existing_orders = []
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    existing_orders = json.load(f)
            
            existing_orders.append(order_data)

            with open(filepath, 'w') as f:
                json.dump(existing_orders, f, indent=4)

            return True, self.order_id

        except Exception as e:
            # --- ROLLBACK INVENTORY IF FAILURE OCCURS ---
            for p_id, original_qty in original_stocks.items():
                self.inventory.products[p_id].stock = original_qty
            raise RuntimeError(f"Order processing failed. Inventory rolled back. Error: {e}")


# ==========================================
# 2. Unit Tests (unittest)
# ==========================================
class TestOrderSystem(unittest.TestCase):
    def setUp(self):
        """Har test se pehle fresh inventory setup."""
        self.inventory = Inventory()
        self.inventory.load_from_dict([
            {"id": "P1", "name": "Laptop", "price": 100, "stock": 5}
        ])
        self.order_file = "test_orders.json"
        if os.path.exists(self.order_file):
            os.remove(self.order_file)

    def tearDown(self):
        if os.path.exists(self.order_file):
            os.remove(self.order_file)

    def test_successful_order_with_discount(self):
        """Test 1: Valid order with 10% discount, stock deduction."""
        cart = Cart()
        cart.add_item("P1", 2)
        cart.apply_discount(10)

        order = Order(cart, self.inventory)
        success, order_id = order.process_order(self.order_file)

        # Check total: (100*2) - 10% = 200 - 20 = 180
        self.assertTrue(success)
        self.assertEqual(order.total, 180.0)
        
        # Check stock: 5 - 2 = 3
        self.assertEqual(self.inventory.products["P1"].stock, 3)

    def test_invalid_quantity(self):
        """Test 2: Quantity <= 0 raises ValueError."""
        cart = Cart()
        with self.assertRaises(ValueError):
            cart.add_item("P1", -1)

    def test_insufficient_stock_rollback(self):
        """Test 3: Out-of-stock order raises error and does NOT change stock."""
        cart = Cart()
        cart.add_item("P1", 10) # Only 5 available
        order = Order(cart, self.inventory)

        with self.assertRaises(ValueError):
            order.process_order(self.order_file)
            
        # Verify stock remains unchanged
        self.assertEqual(self.inventory.products["P1"].stock, 5)


# ==========================================
# 3. Execution
# ==========================================
if __name__ == "__main__":
    # Sample behavior demonstration
    print("--- Running Sample Behavior ---")
    inv = Inventory()
    inv.load_from_dict([{"id": "P1", "name": "Laptop", "price": 100, "stock": 5}])
    
    c = Cart()
    c.add_item("P1", 2)
    c.apply_discount(10)
    
    o = Order(c, inv)
    success, o_id = o.process_order("orders.json")
    
    print(f"Order {o_id} Success: {success}")
    print(f"Total Calculated: {o.total}")
    print(f"Stock Remaining: {inv.products['P1'].stock}")
    
    if os.path.exists("orders.json"):
        os.remove("orders.json")

    print("\n--- Running Unit Tests ---")
    # Unittest run karne ke liye
    unittest.main(argv=['first-arg-is-ignored'], exit=False)