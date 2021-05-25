import sys
import math

# Code Royal Puzzle Wood League 2 3rd #

num_sites = int(input())
sites, sitesIds = {}, []
queenX, queenY = 1872, 698
ownedStruct = {}
for i in range(num_sites):
    site_id, x, y, radius = [int(j) for j in input().split()]
    sites[site_id] = (x, y, radius)
    sitesIds.append(site_id)
    print("site_id: %s, (%s, %s), r: %s" % (site_id, x, y, radius), file=sys.stderr, flush=True)
# Prepare for game
# Sort site by distance
sites = dict(sorted(sites.items(), key=lambda item: math.dist([item[1][0], item[1][1]], [queenX, queenY])))
print("sites: %s" % (sites.items()), file=sys.stderr, flush=True)

# game loop
while True:
    # touched_site: -1 if none
    gold, touched_site = [int(i) for i in input().split()]
    barKnight, barArcher = 0, 0
    inTrainKnight, inTrainArcher = 0, 0
    # Structure info
    for i in range(num_sites):
        # structure_type: -1 = No structure, 2 = Barracks
        # owner: -1 = No structure, 0 = Friendly, 1 = Enemy
        site_id, ignore_1, ignore_2, structure_type, owner, param_1, param_2 = [int(j) for j in input().split()]
        sites[site_id] = (
            sites[site_id][0], sites[site_id][1], sites[site_id][2], structure_type, owner, param_1, param_2)
        if owner == 0: ownedStruct[site_id] = sites[site_id]
        if owner == 0 and structure_type == 2 and param_2 == 0: barKnight += 1
        if owner == 0 and structure_type == 2 and param_2 == 1: barArcher += 1
        if owner == 0 and structure_type == 2 and param_2 == 0 and param_1 > 0: inTrainKnight += 1
        if owner == 0 and structure_type == 2 and param_2 == 1 and param_1 > 0: inTrainArcher += 1

    # Unit info
    num_units = int(input())
    knight, archer = 0, 0
    for i in range(num_units):
        # unit_type: -1 = QUEEN, 0 = KNIGHT, 1 = ARCHER
        x, y, owner, unit_type, health = [int(j) for j in input().split()]
        if owner == 0 and unit_type == 0: knight += 1
        if owner == 0 and unit_type == 1: archer += 1
        if unit_type == -1 and owner == 0: queenX, queenY = x, y
        print("unit: %s" % (unit_type == -1 and owner == 0), file=sys.stderr, flush=True)

    # sort sites base on distance 
    sites = dict(sorted(sites.items(), key=lambda item: math.dist([item[1][0], item[1][1]], [queenX, queenY])))

    # Queen action
    print("sites: %s" % (sites.items()), file=sys.stderr, flush=True)
    if barKnight + barArcher < 2:
        goTo = [[y[0], y[1]] for x, y in sites.items() if y[3] == -1][0]
        move = 'MOVE ' + str(goTo[0]) + ' ' + str(goTo[1])
        build = 'BUILD ' + str(touched_site) + ' BARRACKS-' + ['KNIGHT', 'ARCHER'][barKnight > 0]
        print([move, build][touched_site > -1 and sites[touched_site][3] == -1])
    else:
        goTo = [[y[0], y[1]] for x, y in sites.items() if y[3] == -1]
        if len(goTo) > 0:
            goTo = goTo[0]
            move = 'MOVE ' + str(goTo[0]) + ' ' + str(goTo[1])
            build = 'BUILD ' + str(touched_site) + ' TOWER'
            print([move, build][touched_site > -1 and sites[touched_site][3] == -1])
        else:
            print('WAIT')
    # Second line: A set of training instructions
    training = []
    if gold >= 100 and knight >= 8:
        s = [[x] for x, y in ownedStruct.items() if y[6] == 1]
        if len(s) > 0: training.append(s[0][0])
        gold = gold - 100
    if gold >= 80 and inTrainKnight == 0 and knight < 8:
        s = [[x] for x, y in ownedStruct.items() if y[6] == 0]
        print(*s, file=sys.stderr, flush=True)
        if len(s) > 0: training.append(s[0][0])
        gold = gold - 80

    print("TRAIN", *list(training))
