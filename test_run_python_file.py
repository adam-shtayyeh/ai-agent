from functions.run_python_file import run_python_file


def main():
    print("--- Test 1: main.py without args ---")
    print(run_python_file("calculator", "main.py"))

    print("\n--- Test 2: main.py with '3 + 5' ---")
    print(run_python_file("calculator", "main.py", ["3 + 5"]))

    print("\n--- Test 3: tests.py ---")
    print(run_python_file("calculator", "tests.py"))

    print("\n--- Test 4: Path Traversal Check ---")
    print(run_python_file("calculator", "../main.py"))

    print("\n--- Test 5: Nonexistent file ---")
    print(run_python_file("calculator", "nonexistent.py"))

    print("\n--- Test 6: Not a python file ---")
    print(run_python_file("calculator", "lorem.txt"))


if __name__ == "__main__":
    main()