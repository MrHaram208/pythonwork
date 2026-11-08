def find_paths(data, target):
    results = []

    def _match(value):
        # bool True/False ko numeric 1/0 ke saath equal mat maano
        if isinstance(value, bool) or isinstance(target, bool):
            return type(value) is type(target) and value == target
        return value == target

    def _walk(node, path):
        # Agar current value target ke barabar hai to path record karo
        if _match(node):
            results.append(path)

        # Dictionary -> dot notation
        if isinstance(node, dict):
            for key, value in node.items():
                new_path = f"{path}.{key}" if path else f"{key}"
                _walk(value, new_path)

        # List -> [index] notation
        elif isinstance(node, list):
            for i, value in enumerate(node):
                _walk(value, f"{path}[{i}]")

    # Root ka path "" hai
    _walk(data, "")
    return results
def find_paths(data, target):
    results = []

    def _match(value):
        if isinstance(value, bool) or isinstance(target, bool):
            return type(value) is type(target) and value == target
        return value == target

    def _walk(node, path):
        if _match(node):
            results.append(path)

        if isinstance(node, dict):
            for key, value in node.items():
                new_path = f"{path}.{key}" if path else f"{key}"
                _walk(value, new_path)

        elif isinstance(node, list):
            for i, value in enumerate(node):
                _walk(value, f"{path}[{i}]")

    _walk(data, "")
    return results
data = {"a": [{"x": 5}, 5], "b": {"y": 5}}
print(find_paths(data, 5))