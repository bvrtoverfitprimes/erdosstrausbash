import json

m = 840

with open("remaining_residues.json", "r") as f:
    remaining_data = json.load(f)
r = remaining_data["remaining_residues"]

with open("templates.json", "r") as f:
    existing_templates = json.load(f)

def build_family1_candidates(umax=60, vmax=60, betamax=240):
    out = []
    for u in range(1, umax + 1):
        for v in range(1, vmax + 1):
            target = 4 * u * v
            for d in range(1, target + 1):
                if target % d:
                    continue
                alpha = 2 * u + d
                gamma = 2 * v + target // d
                for beta in range(1, betamax + 1):
                    den = 3 * beta - u
                    if den <= 0:
                        continue
                    num = v * beta
                    if num % den:
                        continue
                    delta = num // den
                    left = u * (gamma + 6 * delta) + v * (alpha + 6 * beta)
                    right = 3 * (alpha * delta + beta * gamma)
                    if left == right:
                        out.append((u, v, alpha, beta, gamma, delta))
    return out

family1_candidates = build_family1_candidates()

def family1_value(n, u, v, alpha, beta, gamma, delta):
    if n < 2 or (n - 1) % 24:
        return None
    if (n + 3) % 4:
        return None
    t = (n - 1) // 24
    a = (n + 3) // 4
    num_b = n * (alpha * t + beta)
    num_c = n * (gamma * t + delta)
    if num_b % u or num_c % v:
        return None
    b = num_b // u
    c = num_c // v
    if a <= 0 or b <= 0 or c <= 0:
        return None
    if 4 * a * b * c != n * (b * c + a * c + a * b):
        return None
    return a, b, c

def family2_value(n, v, d):
    if d == 0 or n < 2:
        return None
    if n + d <= 0 or (n + d) % 4:
        return None
    a = (n + d) // 4
    den_b = v * d
    den_c = (4 - v) * d
    if den_b == 0 or den_c == 0:
        return None
    num = n * (n + d)
    if num % den_b or num % den_c:
        return None
    b = num // den_b
    c = num // den_c
    if a <= 0 or b <= 0 or c <= 0:
        return None
    if 4 * a * b * c != n * (b * c + a * c + a * b):
        return None
    return a, b, c

def family3_value(n, x, u, d, A, B, C):
    if n < 2:
        return None
    if n + d <= 0 or (n + d) % u:
        return None
    a = (n + d) // u
    if a <= 0:
        return None
    t = (n - x) // m
    num_b = n * (A * t + B)
    if num_b % C:
        return None
    b = num_b // C
    if b <= 0:
        return None
    den = 4 * a * b - n * (a + b)
    if den <= 0:
        return None
    num_c = a * b * n
    if num_c % den:
        return None
    c = num_c // den
    if c <= 0:
        return None
    if 4 * a * b * c != n * (b * c + a * c + a * b):
        return None
    return a, b, c

def f(x, m=m, k=100, all_=False):
    ns = [x + i * m for i in range(k) if x + i * m >= 2]
    if not ns:
        return "No n>=2 in test range."
    out = []
    if x % 24 == 1:
        for u, v, alpha, beta, gamma, delta in family1_candidates:
            ok = 1
            for n in ns:
                if family1_value(n, u, v, alpha, beta, gamma, delta) is None:
                    ok = 0
                    break
            if ok:
                s = ("template3a", u, v, alpha, beta, gamma, delta)
                if all_:
                    out.append(s)
                else:
                    return s
        for v in range(1, 4):
            for d in range(-5000, 5001):
                if d == 0:
                    continue
                ok = 1
                for n in ns:
                    if family2_value(n, v, d) is None:
                        ok = 0
                        break
                if ok:
                    s = ("template3b", v, d)
                    if all_:
                        out.append(s)
                    else:
                        return s
    mods = [2, 3, 4, 5, 6, 7, 8, 10, 12]
    for u in mods:
        for d in range(-120, 121):
            if any((n + d) <= 0 or (n + d) % u for n in ns[:3]):
                continue
            for A in range(1, 21):
                for B in range(0, 21):
                    for C in range(1, 21):
                        ok = 1
                        for n in ns:
                            if family3_value(n, x, u, d, A, B, C) is None:
                                ok = 0
                                break
                        if ok:
                            s = ("template3c", u, d, A, B, C)
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

def t(n, r0, s):
    name = s[0]
    if name == "template3a":
        value = family1_value(n, s[1], s[2], s[3], s[4], s[5], s[6])
        return 0 if value is None else 1
    if name == "template3b":
        value = family2_value(n, s[1], s[2])
        return 0 if value is None else 1
    value = family3_value(n, r0, s[1], s[2], s[3], s[4], s[5])
    return 0 if value is None else 1

x = 1
for r0, s in ok:
    for n in range(r0, 10**6, m):
        x *= t(n, r0, s)

print("Works!" if x == 1 else "Didn't work.")

templates_data = existing_templates.copy()
for residue, s in ok:
    if s[0] == "template3a":
        templates_data[str(residue)] = {
            "template": "template3a",
            "u": s[1],
            "v": s[2],
            "alpha": s[3],
            "beta": s[4],
            "gamma": s[5],
            "delta": s[6]
        }
    elif s[0] == "template3b":
        templates_data[str(residue)] = {
            "template": "template3b",
            "v": s[1],
            "d": s[2]
        }
    else:
        templates_data[str(residue)] = {
            "template": "template3c",
            "u": s[1],
            "d": s[2],
            "A": s[3],
            "B": s[4],
            "C": s[5]
        }
with open("templates.json", "w") as f:
    json.dump(templates_data, f, indent=2)

remaining_data = {"remaining_residues": bad}
with open("remaining_residues.json", "w") as f:
    json.dump(remaining_data, f, indent=2)