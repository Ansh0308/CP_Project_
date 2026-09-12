# Phase 7 — Concepts

1. **What unit testing means** — testing the smallest independent piece of logic (a function, a class method) in isolation, with all its inputs controlled and its dependencies replaced, so a test failure points at exactly one thing that's broken.

2. **Why validation and unit testing are different** — Phase 6's CI layers (syntax check, DAG import, lint rules) validate that a DAG file is *well-formed*: it parses, it follows naming/tagging conventions. None of that proves the DAG's *logic* is correct. Unit tests go one level deeper: they call `clean_data()` with a crafted input and assert the output is exactly right. Validation asks "is this a legal DAG?"; unit testing asks "does this DAG's code actually do what it's supposed to do?"

3. **Why Airflow DAGs need tests** — a DAG is still just Python. Its task callables contain real business logic that can have real bugs (an off-by-one, a wrong aggregation, a broken edge case) that no amount of "does it parse" checking will catch. DAG *structure* also needs testing: a dependency wired backwards, a task silently deleted, a cycle introduced by a bad merge — unit tests catch these regressions in milliseconds, long before anyone waits for a real Airflow run.

4. **What pytest is** — a Python testing framework: plain functions prefixed `test_`, plain `assert` statements, automatic test discovery, and clear per-assertion failure reporting.

5. **What mocking means** — replacing a real dependency (a function, an API client, a database connection) with a fake stand-in that returns controlled, predictable data instead of doing the real thing.

6. **Why external APIs/databases should be mocked during unit tests** — a unit test must be fast, deterministic, and runnable anywhere with zero side effects. A real API call could be slow, fail for unrelated reasons (network blip, rate limit), cost money, or write real data somewhere. Mocking removes all of that: the same test produces the same result every time, in milliseconds, with nothing outside the process ever touched.

## Note on Mocking Scope in This Project

This project's DAGs do not yet call a real external API or database — `fetch_data` simulates a source system with a hardcoded list, by deliberate design since Phase 3. The nearest real dependency the task callables have is Airflow's own TaskInstance/XCom mechanism, which in production is backed by the metadata database. That is what Phase 7 mocks (`MockTaskInstance` in `tests/conftest.py`), and `store_result`'s `print()` (standing in for a future real destination) is also mocked in one test to demonstrate the technique idiomatically. If a real external API or database call is ever added to a DAG, it would be mocked the same way: with `unittest.mock.patch` targeted at that specific call, never by letting a test reach the real network or database.
