"""
Module for room evaluation
"""
import si.problem.room_planning.geometry as geom

tv_max_angle = 30
intersections_penalty = 5


def punish_intersections(room):
    penalty = 0

    for first_furniture in room.furniture.values():
        for second_furniture in room.furniture.values():
            if first_furniture != second_furniture:
                if geom.intersects(first_furniture.figure,
                                   second_furniture.figure):
                    penalty += intersections_penalty
            else:
                continue

    return penalty


def punish_chairs(room):
    penalty = 0

    table = room.furniture['Table']
    chairs = [
        room.furniture['Chair1'],
        room.furniture['Chair2'],
        room.furniture['Chair3'],
        room.furniture['Chair4']
    ]

    for chair in chairs:
        if not geom.intersects(chair.figure, table.figure):
            penalty += geom.distance((chair.figure.x, chair.figure.y),
                                     (table.figure.x, table.figure.y))

    return penalty


def punish_sofa(room):
    penalty = 0

    tv = room.furniture['TV']
    sofa = room.furniture['Sofa']

    if not geom.intersects(tv.figure, sofa.figure):
        tv_current_angle = geom.angle(tv.figure, sofa.figure)
        if tv_current_angle > tv_max_angle:
            penalty += tv_max_angle - tv_current_angle


def punish_carpet(room):
    pass


def evaluate_room(room):
    """Should take an Room object and calculate the fitness (real number).
    Lower value = better value."""

    fitness = 0
    return fitness

