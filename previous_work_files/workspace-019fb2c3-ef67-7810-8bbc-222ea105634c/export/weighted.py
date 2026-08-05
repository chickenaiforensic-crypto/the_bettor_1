"""
USER'S WEIGHTED RESULT SCALE — implemented and tested against plain goal difference.

  draw 0-0                    : +1
  draw 1-1, 2-2, ...          : +2
  win by exactly 1 goal       : +4
  win by 2 or more goals      : +6
  loss by exactly 1 goal      : -4
  loss by 2 or more goals     : -6

Rationale (user): weighs wins, draws and losses on a single scale, and separates
a goalless stalemate from a scoring draw.
"""

def wscore(gf, ga):
    d = gf - ga
    if d == 0:
        return 1 if gf == 0 else 2
    if d == 1:
        return 4
    if d >= 2:
        return 6
    if d == -1:
        return -4
    return -6


def wscore_from_gd_only(gd):
    """When only goal difference is known (no scoreline), 0-0 vs 1-1 is indistinguishable."""
    if gd == 0:
        return 1.5          # midpoint of +1 and +2
    if gd == 1:
        return 4
    if gd >= 2:
        return 6
    if gd == -1:
        return -4
    return -6


SCALE = {"draw_0_0": 1, "draw_scoring": 2, "win_1": 4, "win_2plus": 6,
         "loss_1": -4, "loss_2plus": -6}
