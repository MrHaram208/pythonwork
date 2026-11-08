from datetime import datetime
import itertools

# ==========================================
# 1. Immutable Transaction Record Class
# ==========================================
class Transaction:
    def __init__(self, txn_id, action, amount, resulting_balance):
        self._txn_id = txn_id
        self._action = action
        self._amount = amount
        self._resulting_balance = resulting_balance
        self._timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Immutability enforce karne ke liye sirf getters diye hain (koi setters nahi)
    @property
    def txn_id(self): return self._txn_id
    @property
    def action(self): return self._action
    @property
    def amount(self): return self._amount
    @property
    def resulting_balance(self): return self._resulting_balance
    
    def __repr__(self):
        return f"[{self.txn_id}] {self.action}: {self.amount} -> Bal: {self.resulting_balance}"


# ==========================================
# 2. Account Class
# ==========================================
class Account:
    def __init__(self, account_number):
        self._account_number = account_number
        self._balance = 0
        self._transactions = []

    # Read-only properties (Encapsulation)
    @property
    def account_number(self): return self._account_number
    @property
    def balance(self): return self._balance
    @property
    def transactions(self): return tuple(self._transactions) # return copy as tuple

    def _add_transaction(self, action, amount):
        """Private method: record add karne ke liye"""
        txn_id = f"TXN-{next(self._txn_counter)}"
        record = Transaction(txn_id, action, amount, self._balance)
        self._transactions.append(record)

    # Transaction ID generator
    _txn_counter = itertools.count(1001)

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self._balance += amount
        self._add_transaction("Deposit", amount)

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self._balance:
            raise ValueError("Insufficient funds.")
        self._balance -= amount
        self._add_transaction("Withdrawal", -amount)

    # Internal methods for Bank transfer (bypassing external checks but keeping logic same)
    def _internal_deduct(self, amount):
        if amount > self._balance:
            raise ValueError("Insufficient funds.")
        self._balance -= amount

    def _internal_add(self, amount):
        self._balance += amount

    def get_statement(self):
        print(f"--- Statement for Account {self._account_number} ---")
        for txn in self._transactions:
            print(txn)
        print(f"Current Balance: {self._balance}\n")


# ==========================================
# 3. Bank Class
# ==========================================
class Bank:
    def __init__(self):
        self._accounts = {} # {account_number: Account_object}

    def create_account(self, account_number):
        if account_number in self._accounts:
            raise ValueError("Account already exists.")
        self._accounts[account_number] = Account(account_number)

    def _get_account(self, account_number):
        if account_number not in self._accounts:
            raise ValueError(f"Account {account_number} does not exist.")
        return self._accounts[account_number]

    def deposit(self, account_number, amount):
        acc = self._get_account(account_number)
        acc.deposit(amount)

    def withdraw(self, account_number, amount):
        acc = self._get_account(account_number)
        acc.withdraw(amount)

    def transfer(self, from_acc, to_acc, amount):
        if amount <= 0:
            raise ValueError("Transfer amount must be positive.")
        
        sender = self._get_account(from_acc)
        receiver = self._get_account(to_acc)

        if sender.balance < amount:
            raise ValueError("Insufficient funds for transfer.")

        # --- ATOMICITY LOGIC ---
        # Dono accounts par pehle dry-run jaisa check kar liya.
        # Ab hum temporarily dono ko update karenge. Agar beech mein error aaye, 
        # toh rollback karna padega. (Yahan simple error handling hai kyunki
        # sender.balance already check ho chuka hai.)
        try:
            sender._internal_deduct(amount)
            receiver._internal_add(amount)
            
            # Record transactions (Resulting balances ab update ho chuke hain)
            sender._add_transaction("Transfer Out", -amount)
            receiver._add_transaction("Transfer In", amount)
            
        except Exception as e:
            # Rollback (though upar ka check isko prevent karega)
            sender._internal_add(amount)
            receiver._internal_deduct(amount)
            raise RuntimeError(f"Transfer failed. Reverting. Error: {e}")


# ==========================================
# Sample Test
# ==========================================
if __name__ == "__main__":
    bank = Bank()
    bank.create_account("A")
    bank.create_account("B")

    bank.deposit("A", 1000)
    bank.deposit("B", 200)

    print(f"Before Transfer -> A: {bank._get_account('A').balance}, B: {bank._get_account('B').balance}")

    # Transfer 350 from A to B
    bank.transfer("A", "B", 350)

    print(f"After Transfer  -> A: {bank._get_account('A').balance}, B: {bank._get_account('B').balance}")
    
    # Statements
    bank._get_account("A").get_statement()
    bank._get_account("B").get_statement()