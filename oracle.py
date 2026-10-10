#!/usr/bin/env python3
"""Independent oracle for Hedgehog math. Mirrors engine.js float ops exactly."""
import json, math

def r1(x): return math.floor(x * 10 + 0.5) / 10
def r2(x): return math.floor(x * 100 + 0.5) / 100

def num(x):
    if x == int(x) and abs(x) < 1e15:
        return str(int(x))
    return repr(x)

def habitat_check(len_cm, wid_cm):
    if not all(isinstance(v, (int, float)) and math.isfinite(v) and v > 0 for v in (len_cm, wid_cm)):
        return {"error": "habitat dimensions must be positive"}
    area_cm2 = len_cm * wid_cm
    area_m2 = r2(area_cm2 / 10000)
    sqft = r1(area_cm2 / 929.0304)
    if area_m2 < 0.372:
        verdict = "under the commonly labeled 4 sq ft floor - more room is the usual advice"
    elif area_m2 <= 0.743:
        verdict = "inside the commonly labeled 4-8 sq ft band"
    else:
        verdict = "roomier than the commonly labeled 8 sq ft"
    return {"lenCm": r1(len_cm), "widCm": r1(wid_cm), "areaM2": area_m2, "sqft": sqft, "verdict": verdict}

def render_habitat(r):
    if "error" in r: return r["error"]
    return (f"A {num(r['lenCm'])} x {num(r['widCm'])} cm habitat: {num(r['areaM2'])} m2 ({num(r['sqft'])}"
            f" sq ft) - {r['verdict']}. Labeled community norms, not veterinary advice.")

def wheel_check(d_cm):
    if not (isinstance(d_cm, (int, float)) and math.isfinite(d_cm) and d_cm > 0):
        return {"error": "wheel diameter must be positive"}
    if d_cm < 28:
        verdict = "under the commonly labeled 28 cm minimum - backs arch on small wheels"
    elif d_cm <= 32:
        verdict = "inside the commonly labeled 28-32 cm band"
    else:
        verdict = "over the commonly labeled 32 cm - fine if it fits the habitat"
    circ_m = math.pi * d_cm / 100
    laps = math.floor(5000 / circ_m)
    return {"dCm": r1(d_cm), "verdict": verdict, "laps": laps}

def render_wheel(r):
    if "error" in r: return r["error"]
    return (f"A {num(r['dCm'])} cm wheel: {r['verdict']}; about {r['laps']}"
            " laps covers a labeled 5 km night. Solid running surface only - wire and bar wheels injure feet (labeled care norms).")

def food_plan(weight_g, days, bag_g):
    if not all(isinstance(v, (int, float)) and math.isfinite(v) and v > 0 for v in (weight_g, days, bag_g)):
        return {"error": "weight, days and bag size must be positive"}
    daily_g = r1(weight_g * 0.04)
    total_g = r1(daily_g * days)
    bags = math.ceil(total_g / bag_g)
    left_g = r1(bags * bag_g - total_g)
    return {"weightG": r1(weight_g), "days": days, "bagG": r1(bag_g),
            "dailyG": daily_g, "totalG": total_g, "bags": bags, "leftG": left_g}

def render_food(r):
    if "error" in r: return r["error"]
    ds = "" if r["days"] == 1 else "s"
    bs = "" if r["bags"] == 1 else "s"
    return (f"A {num(r['weightG'])} g hedgehog eats about {num(r['dailyG'])} g/day (labeled ~4% of body weight); "
            f"{r['days']} day{ds} needs {num(r['totalG'])} g - {r['bags']} bag{bs} of {num(r['bagG'])} g, "
            f"{num(r['leftG'])} g left over. Labeled feeding norms, not veterinary advice.")

cases = []
for l, w in [(100, 50), (60, 60), (120, 80), (40, 40), (50, 75), (90, 45), (150, 100),
             (61, 61), (86.1, 86.1), (30, 30), (0, 50), (100, -5), (200, 60), (75.5, 49.5), (110, 67)]:
    res = habitat_check(l, w)
    cases.append({"fn": "habitatCheck", "args": [l, w], "result": res, "render": render_habitat(res)})
for d in [30, 28, 32, 25, 20, 35, 40, 27.9, 32.1, 28.5, 0, -10, 50, 12]:
    res = wheel_check(d)
    cases.append({"fn": "wheelCheck", "args": [d], "result": res, "render": render_wheel(res)})
for wt, dy, bg in [(450, 30, 1000), (350, 7, 500), (600, 30, 1000), (400, 14, 750), (500, 1, 250),
                   (250, 60, 1000), (550, 90, 1500), (450, 30, 250), (0, 30, 1000), (450, 0, 1000),
                   (450, 30, 0), (-100, 30, 1000), (700, 365, 2000)]:
    res = food_plan(wt, dy, bg)
    cases.append({"fn": "foodPlan", "args": [wt, dy, bg], "result": res, "render": render_food(res)})

with open("expected.json", "w") as f:
    json.dump(cases, f, separators=(",", ":"))
    f.write("\n")
print(len(cases), "cases written")
