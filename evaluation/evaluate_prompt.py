import csv
from pathlib import Path

from evaluation.test_cases import TEST_CASES
from query_engine.services.sql_generator import SQLGenerator


generator = SQLGenerator()


def evaluate_sql(sql: str, expected_view: str, expected_keywords: list[str]):

    sql_lower = sql.lower()

    view_match = expected_view.lower() in sql_lower

    keyword_matches = [
        keyword.lower() in sql_lower
        for keyword in expected_keywords
    ]

    keyword_score = sum(keyword_matches)

    passed = view_match and all(keyword_matches)

    return {
        "passed": passed,
        "view_match": view_match,
        "keyword_score": f"{keyword_score}/{len(expected_keywords)}",
    }


def run_evaluation():

    results = []

    total = len(TEST_CASES)
    passed_count = 0

    print("\nStarting Prompt Evaluation...\n")

    for idx, test in enumerate(TEST_CASES, start=1):

        question = test["question"]
        expected_view = test["expected_view"]
        expected_keywords = test["expected_keywords"]

        try:

            generated_sql = generator.generate_sql(question)

            evaluation = evaluate_sql(
                generated_sql,
                expected_view,
                expected_keywords,
            )

            status = "PASS" if evaluation["passed"] else "FAIL"

            if evaluation["passed"]:
                passed_count += 1

            results.append(
                {
                    "question": question,
                    "status": status,
                    "expected_view": expected_view,
                    "view_match": evaluation["view_match"],
                    "keyword_score": evaluation["keyword_score"],
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
                    "status": "ERROR",
                    "expected_view": expected_view,
                    "view_match": False,
                    "keyword_score": "0/0",
                    "generated_sql": str(e),
                }
            )

            print(
                f"[{idx}/{total}] ERROR - {question}"
            )

    accuracy = round((passed_count / total) * 100, 2)

    print("\nEvaluation Complete")
    print(f"Passed: {passed_count}/{total}")
    print(f"Accuracy: {accuracy}%")

    save_results(results, accuracy)


def save_results(results, accuracy):

    output_dir = Path("evaluation")
    output_dir.mkdir(exist_ok=True)

    csv_file = output_dir / "evaluation_results.csv"

    with open(
        csv_file,
        mode="w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "question",
                "status",
                "expected_view",
                "view_match",
                "keyword_score",
                "generated_sql",
            ],
        )

        writer.writeheader()

        for row in results:
            writer.writerow(row)

    summary_file = output_dir / "evaluation_summary.txt"

    with open(summary_file, "w", encoding="utf-8") as file:

        file.write(
            f"AML Prompt Evaluation Report\n"
        )

        file.write(
            f"Accuracy: {accuracy}%\n"
        )

        file.write(
            f"Total Questions: {len(results)}\n"
        )

        passed = sum(
            1
            for row in results
            if row["status"] == "PASS"
        )

        failed = sum(
            1
            for row in results
            if row["status"] == "FAIL"
        )

        errors = sum(
            1
            for row in results
            if row["status"] == "ERROR"
        )

        file.write(
            f"Passed: {passed}\n"
        )

        file.write(
            f"Failed: {failed}\n"
        )

        file.write(
            f"Errors: {errors}\n"
        )

    print(
        f"\nResults saved to: {csv_file}"
    )

    print(
        f"Summary saved to: {summary_file}"
    )


if __name__ == "__main__":
    run_evaluation()