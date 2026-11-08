def plan_execution(tasks, dependencies):
    # 1) Unknown task names reject karo
    task_set = set(tasks)
    for a, b in dependencies:
        if a not in task_set or b not in task_set:
            raise ValueError(f"Unknown task in dependency: ({a}, {b})")

    # 2) Graph aur Indegree (kitne tasks pehle complete hone hain) banao
    # adj: A -> [B, C] (A ke baad B aur C aayenge)
    adj = {t: [] for t in tasks}
    in_degree = {t: 0 for t in tasks}

    for a, b in dependencies:
        adj[a].append(b)
        in_degree[b] += 1

    # 3) Un tasks ko queue mein daalo jinka koi prerequisite nahi hai (in_degree == 0)
    # Requirement: "multiple available tasks, select alphabetically first"
    available = [t for t in tasks if in_degree[t] == 0]
    available.sort()  # Alphabetical order

    result = []

    # 4) Kahn's Algorithm
    while available:
        # Alphabetically first task nikalo
        current = available.pop(0)
        result.append(current)

        # Iske aane se jo tasks unlock hue, unki indegree kam karo
        for neighbor in adj[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                available.append(neighbor)
        
        # Naye unlock hue tasks ko dobara sort karo taake alphabetically first aage aaye
        available.sort()

    # 5) Cycle Detection: Agar result mein saare tasks nahi aaye, matlab cycle hai
    if len(result) != len(tasks):
        raise ValueError("Cycle detected: The dependencies contain a circular loop.")

    return result


# ---- Sample Test ----
tasks = ["build", "test", "deploy"]
dependencies = [("build", "test"), ("test", "deploy")]
print(plan_execution(tasks, dependencies))