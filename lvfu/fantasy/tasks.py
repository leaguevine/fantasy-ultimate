from datetime import datetime

from celery.task import task

from ..lv.stats import get_player_stats
from rules import STATS_FIELDS, compute_score


@task(ignore_result=True)
def update_player_scores(league_ids):
    if isinstance(league_ids, int):
        league_ids = [league_ids]

    from models import League, Player
    for id in league_ids:
        league = League.objects.get(id)
        players = Player.objects.get_for_league(league)
        player_map = dict([(p.lv_player_id, p) for p in players])
        results = get_player_stats([p.lv_player_id for p in players],
                                   league.event_type,
                                   league.lv_event_id,
                                   STATS_FIELDS)
        for player_id, stats in results.iteritems():
            player = player_map[player_id]
            player.score = compute_score(stats)
            player.score_updated = datetime.utcnow()
            player.save()
