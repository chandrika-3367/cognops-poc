from crew.run_cognops_crew import run_cognops_crew

if __name__ == "__main__":
    issue_description = "Database timeout when user submits form"
    all_issues = [
        ("Login fails", "500 errors after login, traced to Redis"),
        ("Payment timeout", "Stripe failed to respond after 3 retries"),
        ("Database overload", "Too many connections causing MySQL timeout"),
        ("Service crash", "OOM error due to recursive loop in worker")
    ]

    result = run_cognops_crew(issue_description, all_issues)
    print("Final Output:")
    print(result)
