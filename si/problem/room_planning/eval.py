"""
Module for room evaluation
"""
import math

import si.problem.room_planning.geometry as geom


# REWARDS METHODS
def reward_for_intersections(room):
    reward = 0.0
    for f in room.furniture.values():
        for ff in room.furniture.values():
            if f != ff:
                if geom.intersects(f.figure, ff.figure):
                    reward -= geom.overlapping_area(f.figure, ff.figure)
            else:
                continue

    return reward


def reward_for_chairs_placement(room):
    reward = 0.0
    table = room.furniture['Table']
    chairs = [
        room.furniture['Chair1'],
        room.furniture['Chair2'],
        room.furniture['Chair3'],
        room.furniture['Chair4']
    ]

    for chair in chairs:
        if not geom.intersects(chair.figure, table.figure):
            reward -= geom.distance((chair.figure.x, chair.figure.y),
                                    (table.figure.x, table.figure.y))

    return reward


def reward_for_tv_sofa_angle(room):
    ROT_ANGLE = 90
    spectator_max_angle = 30

    reward = 0.0
    tv = room.furniture['TV']
    sofa = room.furniture['Sofa']

    if not geom.intersects(tv.figure, sofa.figure):
        current_angle = abs(geom.angle(tv.figure, sofa.figure))
        if current_angle >= ROT_ANGLE + spectator_max_angle / 2 \
                or current_angle <= ROT_ANGLE - spectator_max_angle / 2:
            reward -= current_angle
    return reward


def reward_for_furniture_inside_room(room):
    reward = 0.0

    bb = room.bounding_box
    for f in room.furniture.values():
        if not geom.inside(f.figure, bb):
            reward -= geom.area(f.figure) - geom.overlapping_area(f.figure, bb)

    return reward


def reward_for_carpet_size(room):
    carpet_area = math.pi * room.carpet_radius ** 2
    room_area = geom.area(room.bounding_box)
    return carpet_area / room_area


# FINAL EVAL
def evaluate_room(room,
                  intersections_weight=0.3,
                  chairs_table_weight=0.1,
                  tv_sofa_weight=0.1,
                  inside_room_weight=0.4,
                  carpet_weight=0.1):
    """Should take an Room object and calculate the fitness (real number).
    Bigger value = better value."""
    total_reward = 0.0
    total_reward += intersections_weight * reward_for_intersections(room)
    total_reward += chairs_table_weight * reward_for_chairs_placement(room)
    total_reward += tv_sofa_weight * reward_for_tv_sofa_angle(room)
    total_reward += inside_room_weight * reward_for_furniture_inside_room(room)
    total_reward += carpet_weight * reward_for_carpet_size(room)
    return total_reward
