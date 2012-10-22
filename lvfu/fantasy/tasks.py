from celery.task import task

from utils import update_player_scores as update_player_scores_impl


@task(ignore_result=True)
def update_player_scores(league_ids):
    if isinstance(league_ids, int):
        league_ids = [league_ids]

    from models import League
    for id in league_ids:
        league = League.objects.select_related('event').get(id)
        update_player_scores_impl(league)
