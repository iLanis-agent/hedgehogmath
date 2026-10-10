# Hedgehog math

Hedgehog habitat and care planning for the spiky roommate you actually have. A static site with three calculators:

- **Habitat check** - cage length and width become a floor-area verdict against labeled square-foot norms.
- **Wheel check** - wheel diameter becomes a size verdict plus the laps behind a labeled 5 km night.
- **Food plan** - body weight and days become kibble grams, bag counts and leftovers.

Live site: https://ilanis-agent.github.io/hedgehogmath/

## Labeled norms

Labeled community care norms, not veterinary advice - an exotic vet knows your hedgehog, these calculators do not:

- Habitat: 4 sq ft (0.372 m2) is the commonly labeled floor minimum; 8 sq ft (0.743 m2) is roomy.
- Wheels: the commonly labeled band is 28-32 cm so the back stays flat; solid running surface only - wire and bar wheels injure feet.
- Food: roughly 4% of body weight per day, about 1-2 tablespoons of kibble.
- Night runs: a 5 km night is the labeled activity estimate.

## Layout

- `engine.js` - pure arithmetic and text rendering, shared by the page and the tests.
- `index.html` - landing page. `app.html` - the calculators.
- `oracle.py` - independent Python mirror of the engine's exact float operations.
- `expected.json` - 42 oracle-generated cases. `test.js` - runs every case against the engine plus render checks.

## Tests

```
python3 oracle.py   # regenerate expected.json
node test.js        # 126 checks, 0 failures
```
