from datetime import datetime

from ..lv.stats import get_player_stats
from models import Player
from rules import STATS_FIELDS, compute_score


def update_player_scores(league):
    all_players = Player.objects.get_for_league(league)
    players = all_players.distinct('lv_player_id')
    # Use len because if it's non-zero we're going to load all the rows anyway
    if len(players) == 0:
        return

    results = get_player_stats([p.lv_player_id for p in players],
                               league.event.type,
                               league.event.lv_id,
                               STATS_FIELDS)
    for player_id, stats in results.iteritems():
        (all_players.filter(lv_player_id=player_id)
                    .update(score=compute_score(stats),
                            score_updated = datetime.utcnow()))
