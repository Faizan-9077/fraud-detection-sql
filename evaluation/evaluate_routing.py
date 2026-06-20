import csv
from pathlib import Path

from evaluation.routing_tests import ROUTING_TESTS
from query_engine.services.sql_generator import SQLGenerator


generator = SQLGenerator()


def run_routing_evaluation():

    results = []

    total = len(ROUTING_TESTS)
    passed = 0

    print("\nStarting View Routing Evaluation...\n")

    for idx, test in enumerate(ROUTING_TESTS, start=1):

        question = test["question"]
        expected_view = test["expected_view"]

        try:

            generated_sql = generator.generate_sql(question)

            is_correct = (
                expected_view.lower()
                in generated_sql.lower()
            )

            status = "PASS" if is_correct else "FAIL"

            if is_correct:
                passed += 1

            results.append(
                {
                    "question": question,
                    "expected_view": expected_view,
                    "status": status,
                    "generated_sql": generated_sql,
                }
            )

            print(
                f"[{idx}/{total}] {status} - {question}"
            )

        except Exception as e:

            results.append(
                {
                    "question": question,
                    "expected_view": expected_view,
                    "status": "ERROR",
                    "generated_sql": str(e),
                }
            )

            print(
                f"[{idx}/{total}] ERROR - {question}"
            )

    accuracy = round(
        (passed / total) * 100,
        2
    )

    print("\nRouting Evaluation Complete")
    print(f"Passed: {passed}/{total}")
    print(f"Accuracy: {accuracy}%")

    save_results(
        results,
        passed,
        total,
        accuracy
    )


def save_results(
    results,
    passed,
    total,
    accuracy
):

    output_dir = Path("evaluation")
    output_dir.mkdir(exist_ok=True)

    csv_file = output_dir / "routing_results.csv"

    with open(
        csv_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "question",
                "expected_view",
                "status",
                "generated_sql",
            ]
        )

        writer.writeheader()

        writer.writerows(results)

    summary_file = (
        output_dir /
        "routing_summary.txt"
    )

    with open(
        summary_file,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "AML View Routing Evaluation\n\n"
        )

        file.write(
            f"Total Questions: {total}\n"
        )

        file.write(
            f"Passed: {passed}\n"
        )

        file.write(
            f"Failed: {total - passed}\n"
        )

        file.write(
            f"Accuracy: {accuracy}%\n"
        )

    print(
        f"\nResults saved to: {csv_file}"
    )

    print(
        f"Summary saved to: {summary_file}"
    )


if __name__ == "__main__":
    run_routing_evaluation()