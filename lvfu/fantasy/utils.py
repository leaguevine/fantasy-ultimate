from datetime import datetime

from ..lv.stats import get_player_stats
from models import Player
from rules import STATS_FIELDS, compute_score


def update_player_scores(league, players=None):
    if players is None:
        players = Player.objects.get_for_league(league)
    if not players:
        return

    player_map = dict([(p.lv_player_id, p) for p in players])
    results = get_player_stats([p.lv_player_id for p in players],
                               league.event.type,
                               league.event.lv_id,
                               STATS_FIELDS)
    for player_id, stats in results.iteritems():
        player = player_map[player_id]
        player.score = compute_score(stats)
        player.score_updated = datetime.utcnow()
        player.save()
