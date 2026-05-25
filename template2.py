import json
from pathlib import Path

m = 840

with open("remaining_residues.json", "r") as f:
    remaining_data = json.load(f)
r = remaining_data["remaining_residues"]

def f(x, m=m, k=100, Amax=20, Bmax=5, Cmax=30, Dmax=20, Emax=5, Fmax=30, all_=False):
    ns = [x + i * m for i in range(k) if x + i * m >= 2]
    if not ns:
        return "No n>=2 in test range."
    out = []
    for A in range(1, Amax):
        for B in range(0, Bmax):
            for C in range(1, Cmax):
                for D in range(1, Dmax):
                    for E in range(0, Emax):
                        for F in range(1, Fmax):
                            ok = 1
                            for n in ns:
                                if (A * n + B) % C:
                                    ok = 0
                                    break
                                a = (A * n + B) // C
                                if a <= 0:
                                    ok = 0
                                    break
                                if (D * n + E) % F:
                                    ok = 0
                                    break
                                b = (D * n + E) // F
                                if b <= 0:
                                    ok = 0
                                    break
                                denom = 4 * a * b - n * (a + b)
                                if denom <= 0:
                                    ok = 0
                                    break
                                if (a * b * n) % denom:
                                    ok = 0
                                    break
                                c = (a * b * n) // denom
                                if c <= 0:
                                    ok = 0
                                    break
                                if 4 * a * b * c != n * (b * c + a * c + a * b):
                                    ok = 0
                                    break
                            if ok:
                                s = (A, B, C, D, E, F)
                                if all_:
                                    out.append(s)
                                else:
                                    return s
    return out if all_ and out else ("Nothing worked." if not all_ else [])

ok = []
bad = []
for x in r:
    s = f(x, m)
    print(x, s)
    if s == "Nothing worked.":
        bad.append(x)
    else:
        ok.append((x, s))

print(len(ok) * 100 // len(r) if r else 0)
print(bad)
print(ok)

def t(n, A, B, C, D, E, F):
    if (A * n + B) % C:
        return 0
    a = (A * n + B) // C
    if a <= 0:
        return 0
    if (D * n + E) % F:
        return 0
    b = (D * n + E) // F
    if b <= 0:
        return 0
    denom = 4 * a * b - n * (a + b)
    if denom <= 0:
        return 0
    if (a * b * n) % denom:
        return 0
    c = (a * b * n) // denom
    if c <= 0:
        return 0
    return 4 * a * b * c == n * (b * c + a * c + a * b)

x = 1
for r0, (A, B, C, D, E, F) in ok:
    for n in range(r0, 10**6, m):
        x *= t(n, A, B, C, D, E, F)

print("Works!" if x == 1 else "Didn't work.")

templates_data = {}
for residue, (A, B, C, D, E, F) in ok:
    templates_data[str(residue)] = {
        "template": "template2",
        "A": A,
        "B": B,
        "C": C,
        "D": D,
        "E": E,
        "F": F
    }
with open("templates_template2.json", "w") as f:
    json.dump(templates_data, f, indent=2)

remaining_data = {"remaining_residues": bad}
with open("remaining_residues_template2.json", "w") as f:
    json.dump(remaining_data, f, indent=2)
