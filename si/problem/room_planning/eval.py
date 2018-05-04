"""
Module for room evaluation
"""
import math

import si.problem.room_planning.geometry as geom

# ROOM PARAMETERS
spectator_max_angle = 30

# PENALTIES MULTIPLIERS VALUES
penalty_multiplier = 20


# REWARDS METHODS
def reward_for_intersections(room):
    reward = 0.0
    for f in room.furniture.values():
        for ff in room.furniture.values():
            if f != ff:
                if geom.intersects(f.figure, ff.figure):
                    reward -= penalty_multiplier * geom.overlapping_area(
                        f.figure, ff.figure)
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

    reward = 0.0
    tv = room.furniture['TV']
    sofa = room.furniture['Sofa']

    if not geom.intersects(tv.figure, sofa.figure):
        current_angle = abs(geom.angle(tv.figure, sofa.figure))
        if current_angle >= ROT_ANGLE + spectator_max_angle / 2 \
                or current_angle <= ROT_ANGLE - spectator_max_angle / 2:
            reward -= penalty_multiplier * current_angle
    return reward


def reward_for_furniture_inside_room(room):
    reward = 0.0

    bb = room.bounding_box
    for f in room.furniture.values():
        if not geom.inside(f.figure, bb):
            reward -= penalty_multiplier * (
                geom.area(f.figure) - geom.overlapping_area(f.figure, bb))

    return reward


def reward_for_carpet_size(room):
    return math.pi * room.carpet_radius ** 2


# FINAL EVAL
def evaluate_room(room):
    """Should take an Room object and calculate the fitness (real number).
    Bigger value = better value."""
    total_reward = 0.0
    total_reward += reward_for_intersections(room)
    total_reward += reward_for_chairs_placement(room)
    total_reward += reward_for_tv_sofa_angle(room)
    total_reward += reward_for_furniture_inside_room(room)
    total_reward += reward_for_carpet_size(room)
    return total_reward
