import json

DEFAULT_RANK = 1000

MAX_DELTA_PART = 0.1

SUPER_RATIO = 2
WEAK_RATIO = 1 / SUPER_RATIO


def normalize_scores(scores):
    s = sum(scores)
    if s == 0:
        return [1 / len(scores) for x in scores]
    return [x / s for x in scores]

def count_bets(ranks):
    s, n = sum(ranks), len(ranks)
    bets = []
    for x in ranks:
        op_av = (s - x) / (n - 1)
        ratio = max(min(x / op_av, SUPER_RATIO), WEAK_RATIO)
        part = MAX_DELTA_PART * (ratio - WEAK_RATIO) / (SUPER_RATIO - WEAK_RATIO)
        bets.append(part * x)
    return bets

def count_ranks_change_list(ranks, scores):
    scores = normalize_scores(scores)
    bets = count_bets(ranks)
    bets_sum = sum(bets)
    return [
        bets_sum * score - bet
        for score, bet in zip(scores, bets)
    ]

def count_ranks_change(ranks, scores):
    ids = ranks.keys()
    ranks_list = [ranks[id] for id in ids]
    scores_list = [scores[id] for id in ids]
    ranks_change_list = count_ranks_change_list(ranks_list, scores_list)
    return {
        id: rank for id, rank in zip(ids, ranks_change_list)
    }
