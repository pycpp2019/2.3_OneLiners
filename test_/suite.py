import json
import re
import traceback
import random

from test_.cases import tests


def run_tests(notebook):
    with open("one-liners.ipynb", "r") as f:
        notebook = json.loads(f.read())

    oneliners = {}
    imports = []
    reexpr = re.compile(r"^#expr\((\d+)\)$")
    reimp = re.compile(r"^import\s+(\S+)")
    refrimp = re.compile(r"^from\s+(\S+)\s+import\s+")

    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            nf = None
            for l in cell["source"]:
                sl = l.strip()

                imp = re.match(reimp, sl)
                frimp = re.search(refrimp, sl)
                imp = frimp if imp is None else imp
                if imp:
                    if not imp.group(1).startswith("test_"):
                        imports.append(sl)

                m = re.search(reexpr, l)
                if m:
                    nf = int(m.group(1))
                    continue

                if nf is not None:
                    oneliners[nf] = sl.split("#")[0].strip()
                    nf = None

    print("found imports:")
    for s in imports:
        print(s)
    print()


    if 0 in oneliners:
        del oneliners[0]

    for k in list(oneliners.keys()):
        #if k not in tests.keys():
        #    del oneliners[k]
        assert k in tests.keys(), "unexpected expr number {}".format(k)
    
    for k in tests.keys():
        if k not in list(oneliners.keys()):
            oneliners[k] = "pass"

    skip = "skipped"
    ok = "ok"
    fail = "failed"
    results = {k: skip for k in oneliners.keys()}

    random.seed(0xDEADBEEF)
    for (k, v) in sorted(oneliners.items()):
        if k > 1:
            print()

        print("[{}]:\nexpr: {}".format(k, "(hidden)"))
        if v == "pass":
            print("[SKIP] task is not implemented, skipping")
            continue

        print("length: {}".format(len(v)))
        if len(v) > 80:
            print("[FAIL] length is greater than 80")
            results[k] = fail
            continue

        glob = {}
        exec("\n".join(imports), glob)
        try:
            tests[k](v, glob)
        except:
            print()
            print(traceback.format_exc())
            print("[FAIL] test failed")
            results[k] = fail
        else:
            print("[OK] test passed")
            results[k] = ok

    print()
    count = {skip: 0, ok: 0, fail: 0}
    print("Results:")
    for k, v in results.items():
        print("{}: {}".format(k, v))
        count[v] += 1

    print()
    print("ok: {}, failed: {}, skipped: {}".format(count[ok], count[fail], count[skip]))

    print()
    if count[ok] < 5:
        print("You need to solve at least 5 tasks")
        return False
    elif count[ok] <= 9:
        print("You solved 5 or more tasks, good")
        return True
    else:
        print("You solved all tasks, awesome!")
        return True
