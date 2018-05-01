"""
Module for room evaluation
"""
import si.problem.room_planning.geometry as geom
from math import pi

spec_angle = 30
intersections_penalty = 10
angle_penalty = 15
carpet_penalty = 10


# PENALTIES METHODS
def punish_for_intersections(room):
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
        if sofa.figure.width >= sofa.figure.height:
            if not ((-90 - spec_angle / 2 <= current_angle <= -90 + spec_angle / 2)
                    or (90 - spec_angle / 2 <= current_angle <= 90 + spec_angle / 2)):
                penalty += angle_penalty
        else:
            pass
            # TODO: implement vertical approach

    return penalty


def punish_for_carpet_intersection(room):
    penalty = 0
    carpet_rectangle = geom.Rectangle(
        0, 0, room.carpet_radius, room.carpet_radius)
    for f in room.furniture.values():
        if not f.carpet and geom.intersects(f.figure, carpet_rectangle):
            penalty += carpet_penalty

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
    fitness -= punish_for_carpet_intersection(room)
    fitness -= punish_for_too_big_spectator_angle(room)
    fitness += reward_for_carpet_size(room)
    return fitness
