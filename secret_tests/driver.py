import importlib.util
import datetime
import os
import numpy as np
import random
import inspect

def test_student_code(solution_path):
    report_dir = os.path.join(os.path.dirname(__file__), "..", "student_workspace")
    report_path = os.path.join(report_dir, "report.txt")
    os.makedirs(report_dir, exist_ok=True)

    spec = importlib.util.spec_from_file_location("student_module", solution_path)
    student_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(student_module)

    report_lines = [f"\n=== Fitness Tracker Test Run at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ==="]

    test_cases = [
        {
            "desc": "Create Step Series",
            "func": "create_step_series",
            "input": [1000, 3000, 5000],
            "expected": np.array([1000, 3000, 5000])
        },
        {
            "desc": "Validate Step Data - Valid",
            "func": "validate_steps",
            "input": np.array([1000, 3000, 5000]),
            "expected": True
        },
        {
            "desc": "Compute Fitness Summary",
            "func": "compute_fitness_summary",
            "input": np.array([3000, 7000, 9000]),
            "expected": (19000, 6333.33, 9000)
        },
        {
            "desc": "Apply Bonus Points",
            "func": "apply_bonus_points",
            "input": np.array([2000, 7000, 8000]),
            "expected": np.array([2000, 7100, 8100])
        },
        {
            "desc": "Validate Step Data - Invalid",
            "func": "validate_steps",
            "input": np.array([3000, -500, 4000]),
            "expected": False
        }
    ]

    # Run all tests
    for i, case in enumerate(test_cases, 1):
        try:
            func = getattr(student_module, case["func"])
            result = func(case["input"])

            if isinstance(case["expected"], np.ndarray):
                passed = np.array_equal(result, case["expected"])
            elif isinstance(case["expected"], tuple):
                passed = all(round(a, 2) == round(b, 2) for a, b in zip(result, case["expected"]))
            else:
                passed = result == case["expected"]

            # --- Randomized logic test (anti-hardcoding)
            random_failed = False
            try:
                rand_func = getattr(student_module, case["func"])
                if case["func"] == "create_step_series":
                    rand_input = [random.randint(1000, 10000) for _ in range(5)]
                    expected = np.array(rand_input)
                    output = rand_func(rand_input)
                    random_failed = not np.array_equal(output, expected)

                elif case["func"] == "validate_steps":
                    valid_input = np.array([random.randint(0, 10000) for _ in range(5)])
                    invalid_input = np.array([1000, -1])
                    if not rand_func(valid_input):
                        random_failed = True
                    if rand_func(invalid_input):
                        random_failed = True

                elif case["func"] == "compute_fitness_summary":
                    steps = np.array([random.randint(1000, 10000) for _ in range(3)])
                    total = int(np.sum(steps))
                    avg = round(np.mean(steps), 2)
                    max_val = int(np.max(steps))
                    expected = (total, avg, max_val)
                    result = rand_func(steps)
                    random_failed = not all(round(a, 2) == round(b, 2) for a, b in zip(result, expected))

                elif case["func"] == "apply_bonus_points":
                    steps = np.array([random.randint(2000, 8000) for _ in range(3)])
                    expected = steps.copy()
                    for i in range(len(expected)):
                        if expected[i] >= 7000:
                            expected[i] += 100
                    output = rand_func(steps)
                    random_failed = not np.array_equal(output, expected)

            except Exception:
                random_failed = True

            if random_failed:
                msg = f"❌ Test Case {i} Failed: {case['desc']} | Reason: Randomized logic failure for {case['func']}"
            elif passed:
                msg = f"✅ Test Case {i} Passed: {case['desc']}"
            else:
                msg = f"❌ Test Case {i} Failed: {case['desc']} | Expected={case['expected']} | Actual={result}"

            print(msg)
            report_lines.append(msg)

        except Exception as e:
            msg = f"❌ Test Case {i} Crashed: {case['desc']} | Error={str(e)}"
            print(msg)
            report_lines.append(msg)

    with open(report_path, "a", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")

if __name__ == "__main__":
    solution_file = os.path.join(os.path.dirname(__file__), "..", "student_workspace", "solution.py")
    test_student_code(solution_file)
