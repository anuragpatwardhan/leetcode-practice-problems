# LeetCode Practice Problems

Python solutions to LeetCode problems, organised by the pattern each one exercises
rather than by problem number. The focus is Medium and Hard problems that map onto
recurring interview patterns, and the write-up for each problem matters as much as
the code.

## Language and tooling

- Python 3.11
- `pytest` for tests

Install the test dependency and run the full suite:

```bash
pip install -r requirements-dev.txt
pytest
```

Run a single problem's tests:

```bash
pytest <topic>/<problem_slug>
```

## How solutions are organised

Every problem lives in its own directory under the topic it belongs to:

```
<topic>/<problem_slug>/
├── README.md                  notes, approach and complexity
├── <problem_slug>.py          the solution
└── test_<problem_slug>.py     tests, including edge cases
```

Files are named after the problem slug rather than a generic `solution.py` so that
each module has a unique import name and the whole suite can run in one pytest
session.

The `README.md` for each problem records the title, number, difficulty, pattern and
a link to the original problem, followed by an explanation of the approach in my own
words. Problem statements are not reproduced here — follow the link for those.

## Topics

| Directory | Pattern |
| --- | --- |
| `arrays/` | array traversal, hashing, prefix sums |

Directories are added as new patterns are covered.

## Complexity notation

Complexities are given in Big-O terms. Unless stated otherwise:

- `n` is the size of the primary input.
- Space complexity excludes the memory used to hold the returned result, but
  includes any auxiliary structure the algorithm builds. Where the sort used by a
  solution dominates auxiliary space, that is called out explicitly.

## Progress

| Topic | Solved |
| --- | --- |
| Arrays | 1 |
| **Total** | **1** |

By difficulty: 1 Medium.
