// Hedgehog math engine - pure arithmetic, shared by the page and the tests.
// Every borrowed number is a labeled hedgehog care norm, not veterinary advice.
(function (root) {
"use strict";

// Labeled norms (common hedgehog care references):
// - Habitat floor: 4 sq ft (0.372 m2) is the commonly labeled minimum; 8 sq ft (0.743 m2) is roomy.
// - Wheel: 28-32 cm diameter is the commonly labeled band so the back stays flat; solid surface only.
// - Food: roughly 4% of body weight per day, about 1-2 tablespoons of kibble.
// - Night runs: several kilometers per night is the commonly labeled activity level; 5 km is the estimate here.

function r1(x) { return Math.round(x * 10) / 10; }
function r2(x) { return Math.round(x * 100) / 100; }
function positive() {
  for (var i = 0; i < arguments.length; i++) {
    var v = arguments[i];
    if (typeof v !== "number" || !isFinite(v) || v <= 0) return false;
  }
  return true;
}

function habitatCheck(lenCm, widCm) {
  if (!positive(lenCm, widCm)) return { error: "habitat dimensions must be positive" };
  var areaCm2 = lenCm * widCm;
  var areaM2 = r2(areaCm2 / 10000);
  var sqft = r1(areaCm2 / 929.0304);
  var verdict;
  if (areaM2 < 0.372) {
    verdict = "under the commonly labeled 4 sq ft floor - more room is the usual advice";
  } else if (areaM2 <= 0.743) {
    verdict = "inside the commonly labeled 4-8 sq ft band";
  } else {
    verdict = "roomier than the commonly labeled 8 sq ft";
  }
  return { lenCm: r1(lenCm), widCm: r1(widCm), areaM2: areaM2, sqft: sqft, verdict: verdict };
}

function renderHabitat(r) {
  if (r.error) return r.error;
  return "A " + r.lenCm + " x " + r.widCm + " cm habitat: " + r.areaM2 + " m2 (" + r.sqft +
    " sq ft) - " + r.verdict + ". Labeled community norms, not veterinary advice.";
}

function wheelCheck(dCm) {
  if (!positive(dCm)) return { error: "wheel diameter must be positive" };
  var verdict;
  if (dCm < 28) {
    verdict = "under the commonly labeled 28 cm minimum - backs arch on small wheels";
  } else if (dCm <= 32) {
    verdict = "inside the commonly labeled 28-32 cm band";
  } else {
    verdict = "over the commonly labeled 32 cm - fine if it fits the habitat";
  }
  var circM = Math.PI * dCm / 100;
  var laps = Math.floor(5000 / circM);
  return { dCm: r1(dCm), verdict: verdict, laps: laps };
}

function renderWheel(r) {
  if (r.error) return r.error;
  return "A " + r.dCm + " cm wheel: " + r.verdict + "; about " + r.laps +
    " laps covers a labeled 5 km night. Solid running surface only - wire and bar wheels injure feet (labeled care norms).";
}

function foodPlan(weightG, days, bagG) {
  if (!positive(weightG, days, bagG)) return { error: "weight, days and bag size must be positive" };
  var dailyG = r1(weightG * 0.04);
  var totalG = r1(dailyG * days);
  var bags = Math.ceil(totalG / bagG);
  var leftG = r1(bags * bagG - totalG);
  return { weightG: r1(weightG), days: days, bagG: r1(bagG), dailyG: dailyG, totalG: totalG, bags: bags, leftG: leftG };
}

function renderFood(r) {
  if (r.error) return r.error;
  return "A " + r.weightG + " g hedgehog eats about " + r.dailyG + " g/day (labeled ~4% of body weight); " +
    r.days + " day" + (r.days === 1 ? "" : "s") + " needs " + r.totalG + " g - " + r.bags +
    " bag" + (r.bags === 1 ? "" : "s") + " of " + r.bagG + " g, " + r.leftG + " g left over. Labeled feeding norms, not veterinary advice.";
}

var api = {
  habitatCheck: habitatCheck,
  wheelCheck: wheelCheck,
  foodPlan: foodPlan,
  renderHabitat: renderHabitat,
  renderWheel: renderWheel,
  renderFood: renderFood
};
if (typeof module !== "undefined" && module.exports) module.exports = api;
root.HedgehogMath = api;
})(typeof window !== "undefined" ? window : globalThis);
