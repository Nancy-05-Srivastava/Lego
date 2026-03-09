import ast
import subprocess
import tempfile


def detect_inefficient_patterns(code):
    suggestions = []

    if "range(len(" in code:
        suggestions.append(
            "Avoid using range(len(list)). Use direct iteration instead."
        )

    if "==" in code and "None" in code:
        suggestions.append(
            "Use 'is None' instead of '== None'."
        )

    return suggestions


def analyze_ast(code):
    suggestions = []

    try:
        tree = ast.parse(code)

        for node in ast.walk(tree):

            if isinstance(node, ast.For):
                if isinstance(node.iter, ast.Call):
                    if getattr(node.iter.func, "id", "") == "range":
                        suggestions.append(
                            "Loop using range detected. Consider iterating directly over the collection."
                        )

    except Exception as e:
        suggestions.append(f"AST analysis error: {e}")

    return suggestions


def run_pyflakes(code):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as f:
        f.write(code.encode())
        temp_file = f.name

    result = subprocess.run(
        ["pyflakes", temp_file],
        capture_output=True,
        text=True
    )

    return result.stdout


def format_code(code):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as f:
        f.write(code.encode())
        temp_file = f.name

    result = subprocess.run(
        ["autopep8", temp_file],
        capture_output=True,
        text=True
    )

    return result.stdout


def optimize_code(code):

    suggestions = []

    suggestions.extend(detect_inefficient_patterns(code))
    suggestions.extend(analyze_ast(code))

    errors = run_pyflakes(code)

    optimized = format_code(code)

    return suggestions, errors, optimized


if __name__ == "__main__":

    print("Paste your code below. Press Enter twice to finish:\n")

    lines = []

    while True:
        line = input()
        if line == "":
            break
        lines.append(line)

    code = "\n".join(lines)

    suggestions, errors, optimized = optimize_code(code)

    print("\n--- Suggestions ---\n")
    for s in suggestions:
        print("-", s)

    print("\n--- Possible Errors ---\n")
    print(errors if errors else "No issues detected.")

    print("\n--- Optimized Code ---\n")
    print(optimized)