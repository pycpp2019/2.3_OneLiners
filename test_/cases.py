import random


def case_1(expr, glob):
    assert eval(expr, {}, glob) == 562949970198528

def case_2(expr, glob):
    f1000 = int(open("f1000.txt", "r").read())
    assert eval(expr, {}, glob) == f1000

def case_3(expr, glob):
    cases = [
        [],
        [2],
        [1],
        [1, 2],
    ]
    for _ in range(16):
        cases.append([random.randint(-100, 100) for _ in range(100)])
        
    for a in cases:
        b = eval(expr, {"a": a}, glob)
        assert len(a) == len(b), "len({}) != len({})".format(a, b)
        for x, y in zip(a, b):
            if x % 2:
                assert 2*x == y, "2*{} != {}".format(x, y)
            else:
                assert x == y, "{} != {}".format(x, y)

def case_4(expr, glob):
    cases = [
        ([], [], set()),
        ([], [1], set()),
        ([1], [1], set()),
        ([1], [], {1}),
        ([1, 1], [], {1}),
        ([1, 1], [1], set()),
        ([1, 2], [1], {2}),
        ([1, 2], [2], {1}),
        ([1, 2], [1, 2], set()),
        ([1, 2], [1, 1], {2}),
        ([1, 2], [3], {1, 2}),
        ([1, 2], [1, 3], {2}),
        ([()], [], {()}),
        ([()], [()], set()),
        (["", ""], [""], set()),
        (["", ""], [], {""}),
        (["1", 1], [(1,)], {"1", 1}),
        ([1, (1,)], [1], {(1,)}),
        ([1, "abc", (1, 2)], ["bac", (1, 2), 2, 2], {1, "abc"}),
    ]
    for _ in range(16):
        a = []
        b = []
        c = set()
        for k in set([random.randint(-100, 100) for _ in range(random.randrange(0, 100))]):
            xa = random.randint(0, 2)
            xb = random.randint(0, 2)
            if xa:
                for _ in range(random.randint(1, 4)):
                    a.append(k)
            if xb:
                for _ in range(random.randint(1, 4)):
                    b.append(k)
            if xa and not xb:
                c.add(k)
        random.shuffle(a)
        random.shuffle(b)
        cases.append((a, b, c))
        
    for a, b, c in cases:
        d = eval(expr, {"a": a, "b": b}, glob)
        assert c == set(d), "{} != set()".format(c, d)

def case_5(expr, glob):
    cells = [
        ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1', 'J1'],
        ['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2', 'J2'],
        ['A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3', 'I3', 'J3'],
        ['A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4', 'H4', 'I4', 'J4'],
        ['A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5', 'I5', 'J5'],
        ['A6', 'B6', 'C6', 'D6', 'E6', 'F6', 'G6', 'H6', 'I6', 'J6'],
        ['A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7', 'I7', 'J7'],
        ['A8', 'B8', 'C8', 'D8', 'E8', 'F8', 'G8', 'H8', 'I8', 'J8'],
        ['A9', 'B9', 'C9', 'D9', 'E9', 'F9', 'G9', 'H9', 'I9', 'J9'],
        ['A10', 'B10', 'C10', 'D10', 'E10', 'F10', 'G10', 'H10', 'I10', 'J10']
    ]
    assert eval(expr, {}, glob) == cells

def case_6(expr, glob):
    n = 0
    for i in range(2, 10**6 + 1, 2):
        if (i % 7) and str(i).startswith("793"):
            n += 1
    assert eval(expr, {}, glob) == n

def case_7(expr, glob):
    cases = [
        ("", ""),
        ("live", "evil"),
        ("deified", "deified"),
        ("one love", "evol eno"),
    ]
    for _ in range(16):
        a = random.choices("1234567890abcdefghijklmnopqrstuvwxyz ", k=random.randrange(0, 100))
        b = "".join(reversed(a))
        a = "".join(a)
        cases.append((a, b))
    
    for a, b in cases:
        assert eval(expr, {"input": lambda: a}, glob) == b
        assert eval(expr, {"input": lambda: b}, glob) == a

class FileMimic:
    def __init__(self, content):
        self.content = content
        
    def read(self):
        content = self.content
        self.content = ""
        return content
    
    def close(self):
        pass

class OpenMimic:
    def __init__(self, path, content):
        self.path = path
        self.content = content
        
    def __call__(self, path, mode="r", *args, **kwargs):
        if self.path != path:
            raise FileNotFoundError
        if mode != "r":
            raise PermissionError
        return FileMimic(self.content)
    
def case_8(expr, glob):
    cases = [
        ("", 0),
        ("z", 1),
        ("Z", 1),
        ("zzz", 3),
        ("ZZZ", 3),
        ("zZz", 3),
        ("xyz", 1),
        ("XYZ", 1),
        ("abc", 0),
    ]
    for _ in range(16):
        a = random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ", k=random.randrange(0, 1000))
        n = 0
        for c in a:
            if c == "z" or c == "Z":
                n += 1
        cases.append(("".join(a), n))
    
    for i, (a, n) in enumerate(cases):
        p = "text{}.txt".format(i)
        mimic = OpenMimic(p, a)
        m = eval(expr, {"p": p, "open": mimic}, glob)
        assert m == n, "{} != {}".format(m, n)
        
def case_9(expr, glob):
    pi20 = "3.14159265358979323846"
    pi = eval(expr, {}, glob)
    assert pi.startswith(pi20), "\n{}\n{}".format(pi, pi20)


tests = {
    1: case_1,
    2: case_2,
    3: case_3,
    4: case_4,
    5: case_5,
    6: case_6,
    7: case_7,
    8: case_8,
    9: case_9,
}
