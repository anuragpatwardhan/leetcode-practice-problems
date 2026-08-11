import random

from daily_temperatures import daily_temperatures


def brute_force(temperatures):
    result = []
    for i, temp in enumerate(temperatures):
        wait = 0
        for j in range(i + 1, len(temperatures)):
            if temperatures[j] > temp:
                wait = j - i
                break
        result.append(wait)
    return result


def test_example():
    assert daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]


def test_empty_input():
    assert daily_temperatures([]) == []


def test_single_day():
    assert daily_temperatures([50]) == [0]


def test_strictly_increasing_resolves_every_day_the_next_morning():
    assert daily_temperatures([1, 2, 3, 4]) == [1, 1, 1, 0]


def test_strictly_decreasing_never_resolves():
    assert daily_temperatures([4, 3, 2, 1]) == [0, 0, 0, 0]


def test_all_equal_never_resolves():
    # The comparison is strict, so an equal temperature does not count as warmer.
    assert daily_temperatures([30, 30, 30]) == [0, 0, 0]


def test_equal_then_warmer():
    assert daily_temperatures([30, 30, 31]) == [2, 1, 0]


def test_one_late_warm_day_resolves_a_long_backlog():
    assert daily_temperatures([50, 40, 30, 20, 60]) == [4, 3, 2, 1, 0]


def test_negative_temperatures():
    assert daily_temperatures([-5, -10, -1]) == [2, 1, 0]


def test_matches_brute_force_on_random_inputs():
    rng = random.Random(7)
    for _ in range(300):
        size = rng.randint(1, 40)
        temps = [rng.randint(-10, 10) for _ in range(size)]
        assert daily_temperatures(temps) == brute_force(temps), temps


def test_matches_brute_force_on_narrow_value_ranges():
    # Heavy duplication stresses the strict-versus-loose comparison.
    rng = random.Random(11)
    for _ in range(300):
        temps = [rng.randint(0, 2) for _ in range(rng.randint(1, 25))]
        assert daily_temperatures(temps) == brute_force(temps), temps
