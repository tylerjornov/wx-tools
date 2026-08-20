# wx-tools

Aviation / MWO utilities.

## Split Shift Changeover Calculator

Live: [tylerjornov.github.io/wx-tools/mwo-changeover-calculator](https://tylerjornov.github.io/wx-tools/mwo-changeover-calculator/)

Shift start = first brief − 2h 30m. Split time = the exact midpoint between that start and last land.

The page runs `mwo-changeover-calculator/calculate_changeover.py` in the browser (Pyodide). If Python cannot load, it uses a JS port of the same math.

### CLI

```bash
python3 mwo-changeover-calculator/calculate_changeover.py 06:00 22:00
python3 mwo-changeover-calculator/calculate_changeover.py 23:00 03:00 --quiet
python3 mwo-changeover-calculator/calculate_changeover.py 09:30 17:45 --json
```
