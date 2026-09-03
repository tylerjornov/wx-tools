# wx-tools

Small aviation / weather-support utilities, published as static pages via GitHub Pages.

Home: [tylerjornov.github.io/wx-tools](https://tylerjornov.github.io/wx-tools/)

## Tools

### Split Shift Changeover Calculator (`mwo-changeover-calculator/`)

Computes the changeover ("split") time for a split shift. Shift start is derived as the first brief time minus 2h30m, and the split time is the exact midpoint between shift start and last land time.

- Live: [tylerjornov.github.io/wx-tools/mwo-changeover-calculator](https://tylerjornov.github.io/wx-tools/mwo-changeover-calculator/)
- CLI:
  ```
  python mwo-changeover-calculator/calculate_changeover.py <first_brief HH:MM> <last_land HH:MM> [--quiet] [--json]
  ```
  - default: prints the full step-by-step breakdown
  - `--quiet`: prints only the final split time
  - `--json`: prints a machine-readable payload (used by the web UI)

### Standby Dashboard (`weather-standby/`)

A weather standby console: METAR/TAF board, mission threshold checks, a WWA (Watch/Warning/Advisory) log, and a brief builder. Pulls live data from the Aviation Weather Center API, with NWS/IEM fallbacks for stations it can't reach directly.

- Live: [tylerjornov.github.io/wx-tools/weather-standby](https://tylerjornov.github.io/wx-tools/weather-standby/)

## License

MIT — see [LICENSE](LICENSE).
