import random

from best_time_to_buy_and_sell_stock import max_profit


def brute_force(prices):
    best = 0
    for buy in range(len(prices)):
        for sell in range(buy + 1, len(prices)):
            best = max(best, prices[sell] - prices[buy])
    return best


def test_example():
    assert max_profit([7, 1, 5, 3, 6, 4]) == 5


def test_example_with_no_profitable_trade():
    assert max_profit([7, 6, 4, 3, 1]) == 0


def test_empty_input():
    assert max_profit([]) == 0


def test_single_price_leaves_no_time_to_sell():
    assert max_profit([5]) == 0


def test_two_prices_rising():
    assert max_profit([1, 5]) == 4


def test_two_prices_falling():
    assert max_profit([5, 1]) == 0


def test_flat_prices():
    assert max_profit([3, 3, 3]) == 0


def test_the_lowest_price_after_the_highest_is_not_a_trade():
    # Selling must come after buying; 1 arriving last cannot pair with 9.
    assert max_profit([9, 2, 8, 1]) == 6


def test_best_buy_is_not_the_global_minimum():
    # Buying at 1 is cheapest but the peak that follows is small; buying at 2
    # captures more. A solution pinned to the global minimum gets this wrong.
    assert max_profit([3, 1, 2, 100]) == 99


def test_monotonically_increasing():
    assert max_profit([1, 2, 3, 4, 5]) == 4


def test_matches_brute_force_on_random_inputs():
    rng = random.Random(31)
    for _ in range(400):
        prices = [rng.randint(0, 50) for _ in range(rng.randint(0, 30))]
        assert max_profit(prices) == brute_force(prices), prices


def test_matches_brute_force_with_heavy_duplication():
    rng = random.Random(37)
    for _ in range(400):
        prices = [rng.randint(0, 3) for _ in range(rng.randint(0, 20))]
        assert max_profit(prices) == brute_force(prices), prices
