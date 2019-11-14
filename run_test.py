from test_.suite import run_tests

if __name__ == "__main__":
    if run_tests("one-liners.ipynb"):
        exit(0)
    else:
        exit(1)
