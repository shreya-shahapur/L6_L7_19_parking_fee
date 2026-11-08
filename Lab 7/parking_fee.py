import re

RATES = {"bike": 10, "car": 30, "truck": 60}

# re.ASCII so \d only matches 0-9 (not Arabic/Devanagari digits etc.)
TIME_RE = re.compile(r"(\d{1,2}):(\d{2})\s*-\s*(\d{1,2}):(\d{2})", re.ASCII)
PLATE_RE = re.compile(r"[A-Z]{2}\d{2}[A-Z]{2}\d{4}", re.ASCII)


def minutes_parked(times):
    """Return minutes between entry and exit ("HH:MM-HH:MM"), or None if invalid."""
    if not isinstance(times, str):
        return None
    match = TIME_RE.fullmatch(times.strip())
    if not match:
        return None
    h1, m1, h2, m2 = (int(x) for x in match.groups())
    if not (0 <= h1 <= 23 and 0 <= h2 <= 23 and 0 <= m1 <= 59 and 0 <= m2 <= 59):
        return None
    duration = (h2 * 60 + m2) - (h1 * 60 + m1)
    if duration < 0:          # exit before entry
        return None
    return duration


def hourly_rate(vehicle):
    """Return hourly rate for bike/car/truck, or None if unknown."""
    if not isinstance(vehicle, str):
        return None
    return RATES.get(vehicle.strip().lower())


def format_plate(plate):
    """Format 'ka01ab1234' as 'KA 01 AB 1234', or return None if invalid."""
    if not isinstance(plate, str):
        return None
    p = plate.strip().upper()
    if not PLATE_RE.fullmatch(p):
        return None
    return f"{p[0:2]} {p[2:4]} {p[4:6]} {p[6:10]}"


def main():
    print("==== Running minutes_parked ====")
    user_input = input("Enter entry and exit time (e.g. 09:30-11:45): ")
    result = minutes_parked(user_input)
    print("Minutes Parked:", result if result is not None else "Invalid time input")

    print("\n==== Running hourly_rate ====")
    user_input = input("Enter vehicle type (bike/car/truck): ")
    result = hourly_rate(user_input)
    print("Hourly Rate:", result if result is not None else "Invalid vehicle type")

    print("\n==== Running format_plate ====")
    user_input = input("Enter a number plate (e.g. ka01ab1234): ")
    result = format_plate(user_input)
    print("Formatted Plate:", result if result is not None else "Invalid number plate")


if __name__ == "__main__":
    main()
