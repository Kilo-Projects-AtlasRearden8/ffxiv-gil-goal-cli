"""Tests for goal math in the FFXIV gil savings tracker."""

from gilgoal.goal import GoalProgress, can_afford


def test_progress_no_goal() -> None:
    progress = GoalProgress.compute(0.0, 1000.0, 200.0)
    assert progress.balance == 800.0
    assert progress.remaining == 0.0
    assert progress.percent_complete == 100.0
    assert progress.is_complete is True


def test_progress_halfway() -> None:
    progress = GoalProgress.compute(10000.0, 6000.0, 1000.0)
    assert progress.balance == 5000.0
    assert progress.remaining == 5000.0
    assert progress.percent_complete == 50.0
    assert progress.is_complete is False


def test_progress_over_goal_caps_at_100() -> None:
    progress = GoalProgress.compute(5000.0, 9000.0, 1000.0)
    assert progress.balance == 8000.0
    assert progress.remaining == 0.0
    assert progress.percent_complete == 100.0
    assert progress.is_complete is True


def test_progress_overspend() -> None:
    progress = GoalProgress.compute(10000.0, 1000.0, 3000.0)
    assert progress.balance == -2000.0
    assert progress.remaining == 12000.0
    assert progress.percent_complete == 0.0
    assert progress.is_complete is False


def test_can_afford() -> None:
    assert can_afford(5000.0, 5000.0) is True
    assert can_afford(5000.0, 5001.0) is False
    assert can_afford(0.0, 0.0) is True
    assert can_afford(-100.0, 1.0) is False
