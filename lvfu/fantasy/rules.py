RULES = {
    'goals_caught': 1,
    'goals_thrown': 1,
    'ds': 1,
    'turnovers': -1
}

STATS_FIELDS = RULES.keys()


def compute_score(stats):
    return reduce(lambda accum, (k, v): accum + RULES.get(k, 0) * v, stats.iteritems())
