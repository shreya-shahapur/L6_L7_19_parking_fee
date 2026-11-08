from hypothesis import given, settings, strategies as st
from parking_fee import minutes_parked, hourly_rate, format_plate

# ---------- Fuzz tests: the functions must NEVER crash ----------

@settings(max_examples=500)
@given(st.text() | st.none())
def test_minutes_parked_no_crash(s):
    try:
        minutes_parked(s)
    except Exception as e:
        assert False, f"minutes_parked crashed on {s!r} with: {type(e).__name__}: {e}"


@settings(max_examples=500)
@given(st.text() | st.none())
def test_hourly_rate_no_crash(s):
    try:
        hourly_rate(s)
    except Exception as e:
        assert False, f"hourly_rate crashed on {s!r} with: {type(e).__name__}: {e}"


@settings(max_examples=500)
@given(st.text() | st.none())
def test_format_plate_no_crash(s):
    try:
        format_plate(s)
    except Exception as e:
        assert False, f"format_plate crashed on {s!r} with: {type(e).__name__}: {e}"


# ---------- Extra fuzz tests: "almost valid" inputs + correctness properties ----------

# Times that look like HH:MM-HH:MM but with any integers (negative, huge, 99, ...)
@given(st.integers(), st.integers(), st.integers(), st.integers())
def test_minutes_parked_weird_numbers(h1, m1, h2, m2):
    result = minutes_parked(f"{h1}:{m1}-{h2}:{m2}")
    # Result is either None (rejected) or a sensible, non-negative duration within a day
    assert result is None or 0 <= result <= 24 * 60


# Valid times must give the exact correct answer
@given(st.integers(0, 23), st.integers(0, 59), st.integers(0, 23), st.integers(0, 59))
def test_minutes_parked_valid_times(h1, m1, h2, m2):
    start, end = h1 * 60 + m1, h2 * 60 + m2
    result = minutes_parked(f"{h1:02d}:{m1:02d}-{h2:02d}:{m2:02d}")
    if end >= start:
        assert result == end - start
    else:
        assert result is None  # exit before entry is invalid


# Vehicle names in any case / with spaces should still work
@given(st.sampled_from(["bike", "car", "truck"]), st.booleans(), st.text(" \t", max_size=3))
def test_hourly_rate_valid_vehicles(vehicle, upper, pad):
    name = vehicle.upper() if upper else vehicle
    assert hourly_rate(pad + name + pad) == {"bike": 10, "car": 30, "truck": 60}[vehicle]


# Rate is always None or one of the known rates
@given(st.text())
def test_hourly_rate_output(s):
    assert hourly_rate(s) in (None, 10, 30, 60)


# Valid plates are formatted as "KA 01 AB 1234"
@given(st.from_regex(r"[a-zA-Z]{2}[0-9]{2}[a-zA-Z]{2}[0-9]{4}", fullmatch=True))
def test_format_plate_valid(plate):
    p = plate.upper()
    assert format_plate(plate) == f"{p[0:2]} {p[2:4]} {p[4:6]} {p[6:10]}"


# Short / wrong-length strings must be rejected, not half-formatted
@given(st.text(max_size=9))
def test_format_plate_short_input(s):
    assert format_plate(s) is None
