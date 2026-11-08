def analyze_transactions(transactions):
    # 1) Duplicate transaction IDs reject karo (pehli occurrence rakho)
    seen_ids = set()
    unique_txns = []
    for t in transactions:
        if t["id"] not in seen_ids:
            seen_ids.add(t["id"])
            unique_txns.append(t)

    # 2) Saare customers ki list (chahe unka koi successful txn na ho)
    all_customers = sorted({t["customer"] for t in unique_txns})

    # 3) Sirf successful transactions
    successful = [t for t in unique_txns if t["status"] == "success"]

    # 4) Per-customer: total spending + category-wise spending
    totals = {c: 0 for c in all_customers}
    cat_spend = {c: {} for c in all_customers}

    for t in successful:
        c = t["customer"]
        totals[c] += t["amount"]
        cat_spend[c][t["category"]] = cat_spend[c].get(t["category"], 0) + t["amount"]

    # 5) Har customer ka top category (highest spend; tie ho to category name ascending)
    top_category = {}
    for c in all_customers:
        if cat_spend[c]:
            top_category[c] = sorted(
                cat_spend[c].items(),
                key=lambda kv: (-kv[1], kv[0])
            )[0][0]
        else:
            top_category[c] = None   # koi successful txn nahi

    # 6) Spending ke descending order mein rank (ties ko same rank)
    ranked_customers = sorted(all_customers, key=lambda c: -totals[c])
    rank_map = {}
    for i, c in enumerate(ranked_customers):
        if i > 0 and totals[c] == totals[ranked_customers[i - 1]]:
            rank_map[c] = rank_map[ranked_customers[i - 1]]   # same rank
        else:
            rank_map[c] = i + 1

    # 7) Final report: spending desc, phir customer name asc
    report = [
        {
            "customer": c,
            "total_spending": totals[c],
            "top_category": top_category[c],
            "rank": rank_map[c],
        }
        for c in sorted(all_customers, key=lambda c: (-totals[c], c))
    ]
    return report


# ---- Sample test ----
transactions = [
    {"id": 1, "customer": "Ali",  "category": "Food",   "amount": 500, "status": "success"},
    {"id": 2, "customer": "Ali",  "category": "Travel", "amount": 200, "status": "failed"},
    {"id": 3, "customer": "Sara", "category": "Food",   "amount": 700, "status": "success"},
]

for row in analyze_transactions(transactions):
    print(row)