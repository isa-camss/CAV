from collections import defaultdict


def get_criterion(key) -> (str, str):
    cid = key['cid']['value'].split('#')[1]
    return cid, key['criterion']['value']


def jw(key) -> (str, str, str, str, str, int, int):
    """
    Sets whether a > a', a = a' or a < a' and calculates the individual P(a, a')
    :param key: all the data relative to one criterion per tender lot
    :return: a tuple with the source, target, winner, J sign, agent, the value and the weight
    """
    source = key['source']['value']
    target = key['target']['value']
    winner = key['winner']['value']
    maxscore = int(key['maxscore']['value'])
    agent = key['agent']['value']
    value = int(key['value']['value'])
    weight = round(value / maxscore, 2)

    if value > 1:
        return source, target, winner, '+', agent, value, weight
    elif value == 1:
        return source, target, winner, '=', agent, value, weight
    else:
        return source, target, winner, '-', maxscore, agent, value, weight


def get_j(r) -> {}:
    """
    Extracts the list of individual individual Js and Ps of the ELECTRE Phase I algorithm (see documentation).
    :param r: the SPARQL result-set as a JSON object
    :return: the list of individual Js and Ps
    """
    j = {}
    jwl = []

    for key in r['results']['bindings']:
        cid, cv = get_criterion(key)
        jwl.append(jw(key))
        maxscore = int(key['maxscore']['value'])
        j[cid] = {'max_score': maxscore, 'jw': jwl}

    return j


def pop_dic(dic: {}) -> {}:
    tr = {}
    for criterion in dic:
        for t in dic[criterion]:
            winner = dic[criterion][t][2]
            tr[winner] = 0
    return tr


def get_p(j: {}) -> ({}, {}, {}):
    """
    Calculates the Summation of the individual Ps per a S a'
    :param j: the individual Js and Ps
    :return: a tuple with the summations of the P+, P= and P-
    """
    p_plus = defaultdict(dict)
    p_equal = defaultdict(dict)
    p_minus = defaultdict(dict)
    p_plus_winners = defaultdict(dict)
    p_equal_winners = defaultdict(dict)
    p_minus_winners = defaultdict(dict)

    for criterion in j:
        swp = 0
        swe = 0
        swm = 0
        for source, target, winner, sign, agent, value, weight in j[criterion]['jw']:
            if sign == '+':
                p_plus[criterion][source+'-'+target] = (source, target, winner, weight)
            elif sign == '=':
                p_equal[criterion][source+'-'+target] = (source, target, winner, weight)
            elif sign == '-':
                p_minus[criterion][source+'-'+target] = (source, target, winner, weight)

    ppw = pop_dic(p_plus)
    ppe = pop_dic(p_equal)
    ppm = pop_dic(p_minus)

    for criterion in p_plus:
        for t in p_plus[criterion]:
            winner = p_plus[criterion][t][2]
            weight = p_plus[criterion][t][3] / len(t) / len(p_plus) / 3
            ppw[winner] += weight

    # This is absurd -> the IT method uses value 1 for even values
    for criterion in p_equal:
        for t in p_equal[criterion]:
            winner = p_equal[criterion][t][2]
            weight = p_equal[criterion][t][3] / len(t) / len(p_plus) / 3
            ppe[winner] += weight

    # This is absurd -> no veto is applied at all (no division by lent(t) nor len(p_minus) since they are 0 lengthy)
    for criterion in p_minus:
        for t in p_minus[criterion]:
            winner = p_minus[criterion][t][2]
            weight = p_minus[criterion][t][3]
            ppm[winner] += weight

    return ppw, ppe, ppm


def get_c(p, c):
    pc = {}
    for key in p:
        disc = (p[key] / c) >= c
        pc[key] = p[key], disc
    return pc


def rank(k: {}) -> {}:
    return sorted(k.items(), key=lambda x: x[1][0], reverse=True)


def phase_one(r):
    """
    Calculates phase I of the ELECTRE method
    :param r: the SPARQL result-set
    :return:
    """
    j = get_j(r)    # collects the J+, J= and J- of the ELECTRE phase 1
    p = get_p(j)    # collects the P+, P= and P- of the ELECTRE phase 1
    # collects the concordance indices c(a, a') = P+(a, a') / P=(a, a') >= c, where c = 3/4 ('natural threshold')
    # or c = 2/3 ('strong threshold')
    # The decision of choosing 3/4 or 2/3 is set in the call for tenders.
    c = 2/3
    # p[0] = p_plus
    k = get_c(p[0], c)
    r = rank(k)
    return j, p, r


def run(r):
    return phase_one(r)

