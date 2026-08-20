#!/usr/bin/env python3
"""
Calculate the split (change) time for a split shift, showing the full working.

Shift start = first brief time - 2.5 hours.
Split time  = exact midpoint between shift start and last land time.

Usage: python calculate_changeover.py <first_brief HH:MM> <last_land HH:MM> [--quiet] [--json]

By default the script prints the full calculation breakdown. Pass --quiet to
print only the final split time (the original behavior). Pass --json for a
machine-readable payload (used by the web UI).
"""

import json
import sys
from datetime import datetime, timedelta, date

SHIFT_LEAD = timedelta(hours=2.5)  # first brief precedes shift start by 2h 30m
BASE = date(2026, 1, 1)            # arbitrary reference day for the arithmetic


def parse_time(t_str):
    try:
        return datetime.strptime(t_str, "%H:%M").time()
    except ValueError:
        raise ValueError(f"Invalid time format: {t_str}. Use HH:MM (24-hour).")


def fmt_hm(td):
    """Format a positive timedelta as 'Xh Ym' (floored to the minute)."""
    total_minutes = int(td.total_seconds() // 60)
    h, m = divmod(total_minutes, 60)
    return f"{h}h {m:02d}m"


def fmt_clock(dt):
    """Format a datetime as HH:MM with a day-offset note relative to BASE."""
    s = dt.strftime("%H:%M")
    if dt.date() > BASE:
        s += " (+1 day)"
    elif dt.date() < BASE:
        s += " (-1 day)"
    return s


def compute(first_brief_str, last_land_str):
    brief_time = parse_time(first_brief_str)
    land_time = parse_time(last_land_str)

    dt_brief = datetime.combine(BASE, brief_time)
    dt_land = datetime.combine(BASE, land_time)

    overnight = dt_land < dt_brief
    if overnight:
        dt_land += timedelta(days=1)

    dt_start = dt_brief - SHIFT_LEAD
    total = dt_land - dt_start

    if total.total_seconds() <= 0:
        raise ValueError("Last land time must occur after the calculated shift start.")

    half = total / 2
    dt_split = dt_start + half

    return {
        "brief": dt_brief,
        "land": dt_land,
        "start": dt_start,
        "total": total,
        "half": half,
        "split": dt_split,
        "overnight": overnight,
    }


def render_breakdown(r):
    land_note = "   (rolled to next day - overnight shift)" if r["overnight"] else ""
    lines = [
        f"First brief:    {fmt_clock(r['brief'])}",
        f"Shift start:    {fmt_clock(r['start'])}   (first brief - 2h 30m)",
        f"Last land:      {fmt_clock(r['land'])}{land_note}",
        f"Total span:     {fmt_hm(r['total'])}   (last land - shift start)",
        f"Half span:      {fmt_hm(r['half'])}   (total span / 2)",
        f"Split time:     {fmt_clock(r['split'])}   (shift start + half span)",
    ]
    return "\n".join(lines)


def split_only(r):
    s = r["split"].strftime("%H:%M")
    if r["split"].date() > BASE:
        s += " (next day)"
    elif r["split"].date() < BASE:
        s += " (previous day)"
    return s


def result_payload(r):
    """JSON-serializable payload consumed by the web UI."""
    split_offset = (r["split"].date() - BASE).days
    return {
        "ok": True,
        "overnight": bool(r["overnight"]),
        "firstBrief": fmt_clock(r["brief"]),
        "shiftStart": fmt_clock(r["start"]),
        "lastLand": fmt_clock(r["land"]),
        "totalSpan": fmt_hm(r["total"]),
        "halfSpan": fmt_hm(r["half"]),
        "splitTime": fmt_clock(r["split"]),
        "splitClock": r["split"].strftime("%H:%M"),
        "splitDayOffset": split_offset,
        "splitQuiet": split_only(r),
        "breakdown": render_breakdown(r),
    }


if __name__ == "__main__":
    raw = sys.argv[1:]
    quiet = "--quiet" in raw
    as_json = "--json" in raw
    args = [a for a in raw if a not in ("--quiet", "--json")]

    if len(args) != 2:
        msg = "Usage: python calculate_changeover.py <first_brief HH:MM> <last_land HH:MM> [--quiet] [--json]"
        if as_json:
            print(json.dumps({"ok": False, "error": msg}))
        else:
            print(msg)
        sys.exit(1)

    try:
        result = compute(args[0], args[1])
    except ValueError as e:
        if as_json:
            print(json.dumps({"ok": False, "error": str(e)}))
        else:
            print(f"Error: {e}")
        sys.exit(1)

    if as_json:
        print(json.dumps(result_payload(result)))
    elif quiet:
        print(split_only(result))
    else:
        print(render_breakdown(result))
