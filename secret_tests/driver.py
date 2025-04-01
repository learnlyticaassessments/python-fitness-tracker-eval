import importlib.util
import datetime
import os
import numpy as np
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

    edge_cases = [
        {
            "func": "create_step_series",
            "input": [1000, 3000, 5000],
            "expected": np.array([1000, 3000, 5000]),
            "desc": "Hardcoded step array return"
        },
        {
            "func": "validate_steps",
            "input": np.array([-1, 0, 1]),
            "expected": False,
            "desc": "Negative steps not handled"
        },
        {
            "func": "compute_fitness_summary",
            "input": np.array([1, 1, 1]),
            "expected": (3, 1.0, 1),
            "desc": "Hardcoded summary values"
        },
        {
            "func": "apply_bonus_points",
            "input": np.array([7000, 8000, 6500]),
            "expected": np.array([7100, 8100, 6500]),
            "desc": "Bonus logic hardcoded or missing"
        },
        # Pass-only checks
        {
            "func": "create_step_series",
            "input": None,
            "expected": None,
            "desc": "Function contains only 'pass' statement"
        },
        {
            "func": "validate_steps",
            "input": None,
            "expected": None,
            "desc": "Function contains only 'pass' statement"
        },
        {
            "func": "compute_fitness_summary",
            "input": None,
            "expected": None,
            "desc": "Function contains only 'pass' statement"
        },
        {
            "func": "apply_bonus_points",
            "input": None,
            "expected": None,
            "desc": "Function contains only 'pass' statement"
        }
    ]

    for i, case in enumerate(test_cases, 1):
        try:
            func = getattr(student_module, case["func"])
            edge_case_failed = False
            failing_edge_case_desc = None

            for edge_case in edge_cases:
                if edge_case["func"] == case["func"]:
                    edge_func = getattr(student_module, edge_case["func"])
                    src = inspect.getsource(edge_func).replace(" ", "").replace("\n", "").lower()

                    # Fail if only 'pass'
                    if 'pass' in src and len(src) < 80:
                        edge_case_failed = True
                        failing_edge_case_desc = "Function contains only pass statement"
                        break

                    # Run edge case input if applicable
                    if edge_case["input"] is not None:
                        result = edge_func(edge_case["input"])
                        expected = edge_case["expected"]

                        if isinstance(expected, np.ndarray):
                            passed = np.array_equal(result, expected)
                        elif isinstance(expected, tuple):
                            passed = all(round(a, 2) == round(b, 2) for a, b in zip(result, expected))
                        else:
                            passed = result == expected

                        # Check if correct result is returned with no logic
                        if passed:
                            if (
                                "sum" not in src and "mean" not in src and "max" not in src and
                                "np." not in src and "+" not in src and "*" not in src and "/" not in src
                            ):
                                edge_case_failed = True
                                failing_edge_case_desc = edge_case["desc"]
                                break

                            # Additional check for exact hardcoded return line
                            if edge_case["func"] == "create_step_series" and "returnnp.array([1000,3000,5000])" in src:
                                edge_case_failed = True
                                failing_edge_case_desc = "Hardcoded return: np.array with fixed values"
                                break

                            if edge_case["func"] == "compute_fitness_summary" and "return(3,1.0,1)" in src:
                                edge_case_failed = True
                                failing_edge_case_desc = "Hardcoded return: tuple with fixed values"
                                break

                            if edge_case["func"] == "validate_steps" and "returntrue" in src:
                                edge_case_failed = True
                                failing_edge_case_desc = "Hardcoded return: always True"
                                break

            if edge_case_failed:
                msg = (
                    f"❌ Test Case {i} Failed: {case['desc']} "
                    f"| Reason: Edge case validation failed - {failing_edge_case_desc}."
                )
            else:
                result = func(case["input"])
                expected = case["expected"]
                if isinstance(expected, np.ndarray):
                    passed = np.array_equal(result, expected)
                elif isinstance(expected, tuple):
                    passed = all(round(a, 2) == round(b, 2) for a, b in zip(result, expected))
                else:
                    passed = result == expected

                if passed:
                    msg = f"✅ Test Case {i} Passed: {case['desc']} | Actual={result}"
                else:
                    msg = f"❌ Test Case {i} Failed: {case['desc']} | Expected={expected} | Actual={result}"

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
