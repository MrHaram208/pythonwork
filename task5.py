def evaluate_expression(expr):
    if not expr or not expr.strip():
        raise ValueError("Malformed expression: Empty string.")

    def apply_op(ops, vals):
        op = ops.pop()
        b = vals.pop()
        a = vals.pop()
        if op == '+': vals.append(a + b)
        elif op == '-': vals.append(a - b)
        elif op == '*': vals.append(a * b)
        elif op == '/':
            if b == 0:
                raise ZeroDivisionError("Division by zero is not allowed.")
            vals.append(a / b)

    def precedence(op):
        if op in ('+', '-'): return 1
        if op in ('*', '/'): return 2
        return 0

    values = []
    ops = []
    i = 0
    n = len(expr)
    prev_char = None # Unary minus detect karne ke liye

    while i < n:
        ch = expr[i]

        # 1. Whitespace skip karo
        if ch == ' ':
            i += 1
            continue

        # 2. Number parse karo (multi-digit support ke liye)
        if ch.isdigit():
            num = 0
            while i < n and expr[i].isdigit():
                num = num * 10 + int(expr[i])
                i += 1
            values.append(num)
            prev_char = 'num'
            continue

        # 3. Opening bracket
        elif ch == '(':
            ops.append(ch)
            prev_char = '('

        # 4. Closing bracket
        elif ch == ')':
            while ops and ops[-1] != '(':
                apply_op(ops, values)
            if not ops:
                raise ValueError("Malformed expression: Unmatched ')'.")
            ops.pop() # '(' ko pop karo
            prev_char = ')'

        # 5. Operators (+ - * /)
        elif ch in '+-*/':
            # Unary minus / plus handle karna
            if (ch == '-' or ch == '+') and (prev_char is None or prev_char in '+-*/('):
                if ch == '-':
                    values.append(0) # Unary minus ko 0 - x bana diya
                # Unary plus ke liye kuch nahi karna, bas ignore karo
                ops.append(ch)
                prev_char = ch
                i += 1
                continue

            # Standard precedence logic
            while ops and ops[-1] != '(' and precedence(ops[-1]) >= precedence(ch):
                apply_op(ops, values)
            ops.append(ch)
            prev_char = ch

        else:
            raise ValueError(f"Malformed expression: Invalid character '{ch}'.")

        i += 1

    # 6. Bache hue operators apply karo
    while ops:
        if ops[-1] == '(':
            raise ValueError("Malformed expression: Unmatched '('.")
        apply_op(ops, values)

    if len(values) != 1:
        raise ValueError("Malformed expression: Invalid sequence of numbers/operators.")

    # Return float (e.g. 18/3 = 6.0)
    return float(values[0])


# ---- Sample Test ----
expr = "-(3 + 2) * 4 + 18 / 3"
print(f"Result: {evaluate_expression(expr)}")  # Output: -14.0