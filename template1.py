import json
from pathlib import Path

m = 840
r = list(range(m))

def f(x, m=m, k=100, amax=6000, bmax=10000, all_=False):
    ns = [x + i * m for i in range(k) if x + i * m >= 2]
    if not ns:
        return "No n>=2 in test range."
    out = []
    for a in range(1, amax):
        c = 4 * a - 1
        if (a * m) % c:
            continue
        b0 = (-a * x) % c
        for j in range(bmax):
            b = b0 + j * c
            if b <= 0:
                continue
            ok = 1
            for n in ns:
                t = a * n + b
                if t % c:
                    ok = 0
                    break
                p = t // c
                if p <= 0:
                    ok = 0
                    break
                u = a * n * p
                if u % b:
                    ok = 0
                    break
                q = u // b
                z = a * n
                if 4 * p * z * q != n * (p * z + z * q + q * p):
                    ok = 0
                    break
            if ok:
                s = (a, b, c)
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

print(len(ok) * 100 // len(r))
print(bad)
print(ok)

def t(n, a, b, c):
    u = a * n + b
    if u % c:
        return 0
    p = u // c
    v = a * n * p
    if v % b:
        return 0
    q = v // b
    z = a * n
    return 4 * p * z * q == n * (p * z + z * q + q * p)

x = 1
for r0, (a, b, c) in ok:
    for n in range(r0, 10**6, m):
        x *= t(n, a, b, c)

print("Works!" if x == 1 else "Didn't work.")

templates_data = {}
for residue, (a, b, c) in ok:
    templates_data[str(residue)] = {
        "template": "template1",
        "a": a,
        "b": b,
        "c": c
    }
with open("templates.json", "w") as f:
    json.dump(templates_data, f, indent=2)

remaining_data = {"remaining_residues": bad}
with open("remaining_residues.json", "w") as f:
    json.dump(remaining_data, f, indent=2)
