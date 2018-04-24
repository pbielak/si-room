"""
Module for room evaluation
"""
import si.problem.room_planning.geometry as geom

sofa_tv_max_angle = 30

# TODO: need to adjust params
intersections_penalty = 2


def evaluate_room(room):
    """Should take an Room object and calculate the fitness (real number).
    Lower value = better value."""

    fitness = 0.0

    # intersections
    for first_furniture in room.furniture:
        for second_furniture in room.furniture:
            if first_furniture != second_furniture:
                if geom.intersects(first_furniture.figure, second_furniture.figure):
                    fitness += intersections_penalty
            else:
                continue

    # how far from table are chairs
    table = room.furniture['Table']
    # TODO:
    table = list(filter(lambda f: type(f).__name__ == 'Table',
                        room.furniture))[0]
    chairs = list(filter(lambda f: type(f).__name__ == 'Chair', room.furniture))

    for chair in chairs:
        # penalty was assigned earlier
        if not geom.intersects(chair.figure, table.figure):
            fitness += geom.distance(chair.figure, table.figure)

    # sofa and tv angle
    sofa = list(filter(lambda f: type(f).__name__ == 'Sofa', room.furniture))[0]
    tv = list(filter(lambda f: type(f).__name__ == 'TV', room.furniture))[0]

    if not geom.intersects(sofa.figure, tv.figure):
        sofa_tv_angle = geom.angle(sofa.figure, tv.figure)
        if sofa_tv_angle > sofa_tv_max_angle:
            fitness += sofa_tv_angle - sofa_tv_max_angle

    # TODO: spaces between furniture

    return fitness
