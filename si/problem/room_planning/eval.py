"""
Module for room evaluation
"""
import si.problem.room_planning.geometry as geom
from math import pi

# ROOM PARAMETERS
spectator_max_angle = 30

# PENALTIES VALUES
# TODO: add other penalties values
penalty_value = 100


# PENALTIES METHODS
def punish_for_intersections(room):
    penalty = 0
    for first_furniture in room.furniture.values():
        for second_furniture in room.furniture.values():
            if first_furniture != second_furniture:
                if geom.intersects(first_furniture.figure,
                                   second_furniture.figure):
                    penalty += penalty_value
            else:
                continue

    return penalty


def punish_for_chairs_placement(room):
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


def punish_for_too_big_spectator_angle(room):
    penalty = 0
    tv = room.furniture['TV']
    sofa = room.furniture['Sofa']
    if not geom.intersects(tv.figure, sofa.figure):
        current_angle = geom.angle(tv.figure, sofa.figure)
        if abs(current_angle) >= 90 + spectator_max_angle / 2 \
                or abs(current_angle) <= 90 - spectator_max_angle / 2:
            penalty += penalty_value
    return penalty


# REWARDS METHODS
def reward_for_carpet_size(room):
    return pi * room.carpet_radius ** 2


# FINAL EVAL
def evaluate_room(room):
    """Should take an Room object and calculate the fitness (real number).
    Bigger value = better value."""
    fitness = 0.0
    fitness -= punish_for_intersections(room)
    fitness -= punish_for_chairs_placement(room)
    fitness -= punish_for_too_big_spectator_angle(room)
    fitness += reward_for_carpet_size(room)
    return fitness
