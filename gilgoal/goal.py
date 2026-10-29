"""Goal math for the FFXIV gil savings tracker."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GoalProgress:
    goal_amount: float
    total_earned: float
    total_spent: float
    balance: float
    remaining: float
    percent_complete: float
    is_complete: bool

    @classmethod
    def compute(cls, goal_amount: float, total_earned: float, total_spent: float) -> "GoalProgress":
        balance = total_earned - total_spent
        remaining = max(goal_amount - balance, 0.0)
        if goal_amount > 0:
            percent = max(0.0, min(balance / goal_amount * 100.0, 100.0))
        else:
            percent = 100.0 if balance >= 0 else 0.0
        return cls(
            goal_amount=goal_amount,
            total_earned=total_earned,
            total_spent=total_spent,
            balance=balance,
            remaining=remaining,
            percent_complete=percent,
            is_complete=balance >= goal_amount,
        )


def can_afford(balance: float, cost: float) -> bool:
    """Return True if the current balance covers a purchase of cost gil."""
    return balance >= cost
