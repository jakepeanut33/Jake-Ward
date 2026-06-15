"""Auction arbitrage MVP package.

Surfaces auction listings where (estimated resale value - all-in cost) clears a
target profit margin, then ranks and alerts on the best opportunities.

The package is intentionally config-driven and source-pluggable so new
categories and auction sources can be added without rewriting core logic.
"""

__version__ = "0.1.0"
