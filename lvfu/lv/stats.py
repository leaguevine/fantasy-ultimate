from . import GetListRequest


def get_player_stats(player_ids, event_type, event_id, fields=None):
    extra_args = {
        'player_ids': player_ids,
        event_type + 'ids': [event_id]
    }
    if fields is not None:
        request_fields = []
        request_fields.extend(fields)
        if not 'player_id' in request_fields:
            request_fields.append('player_id')
    else:
        request_fields = None

    results = GetListRequest("/stats/ultimate/player_stats_per_" + event_type,
                             fields=request_fields, **extra_args).get_all()
    return dict([(r['player_id'], dict([(k, r[k]) for k in fields])) for r in results])
