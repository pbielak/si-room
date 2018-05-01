import unittest

from si.gui.room import RoomGUI
from si.problem.room_planning import furniture as fun
from si.problem.room_planning.eval import punish_for_intersections, \
    punish_for_chairs_placement, punish_for_too_big_spectator_angle, \
    punish_for_carpet_intersection, reward_for_carpet_size, evaluate_room
from si.problem.room_planning.room import Room, load_default_room_furniture


class TestRoomEvaluator(unittest.TestCase):

    def test_intersections_exist(self):
        """Should returns penalty value of prepared room
        (5 items intersect)"""

        furniture_dict = {
            'Wardrobe1': fun.Wardrobe(4, 10),
            'Wardrobe2': fun.Wardrobe(1, 5),
            'TV': fun.TV(6, 23),
            'Sofa': fun.Sofa(7, 16),
            'Table': fun.Table(-10, 4),
            'Chair1': fun.Chair(-12, 11),
            'Chair2': fun.Chair(-8, 11),
            'Chair3': fun.Chair(1, 1),
            'Chair4': fun.Chair(15, 15),
            'Desk': fun.Desk(-20, 5)
        }
        test_room = Room(50, 50, None, 5, furniture_dict)
        self.assertEqual(
            punish_for_intersections(test_room), 80)

    def test_no_intersections_exist(self):
        """Should returns penalty value of prepared room
        (0 items intersect)"""

        furniture_dict = {
            'Wardrobe1': fun.Wardrobe(4, 10),
            'Wardrobe2': fun.Wardrobe(1, -6),
            'TV': fun.TV(6, 23),
            'Sofa': fun.Sofa(7, 18),
            'Table': fun.Table(-10, 4),
            'Chair1': fun.Chair(-12, 11),
            'Chair2': fun.Chair(-8, 12),
            'Chair3': fun.Chair(1, 1),
            'Chair4': fun.Chair(16, 15),
            'Desk': fun.Desk(-20, 5)
        }
        test_room = Room(50, 50, None, 5, furniture_dict)
        self.assertEqual(
            punish_for_intersections(test_room), 0)

    def test_chairs_far_from_table(self):
        """Should returns penalty value of prepared room
        (2 chairs have bigger distances from table)"""

        furniture_dict = {
            'Wardrobe1': fun.Wardrobe(4, 10),
            'Wardrobe2': fun.Wardrobe(1, -6),
            'TV': fun.TV(6, 23),
            'Sofa': fun.Sofa(7, 18),
            'Table': fun.Table(-10, 4),
            'Chair1': fun.Chair(-12, 11),
            'Chair2': fun.Chair(-8, 11),
            'Chair3': fun.Chair(1, 1),
            'Chair4': fun.Chair(16, 15),
            'Desk': fun.Desk(-20, 5)
        }
        test_room = Room(50, 50, None, 5, furniture_dict)
        self.assertAlmostEqual(
            punish_for_chairs_placement(test_room), 54.2, delta=0.01)

    def test_chairs_near_table(self):
        """Should returns penalty value of prepared room
        (all chairs are near table)"""

        furniture_dict = {
            'Wardrobe1': fun.Wardrobe(4, 10),
            'Wardrobe2': fun.Wardrobe(1, -6),
            'TV': fun.TV(6, 23),
            'Sofa': fun.Sofa(7, 18),
            'Table': fun.Table(-10, 4),
            'Chair1': fun.Chair(-12, 11),
            'Chair2': fun.Chair(-8, 11),
            'Chair3': fun.Chair(-12, -3),
            'Chair4': fun.Chair(-8, -3),
            'Desk': fun.Desk(-20, 5)
        }
        test_room = Room(50, 50, None, 5, furniture_dict)
        self.assertAlmostEqual(
            punish_for_chairs_placement(test_room), 29.12, delta=0.01)

    def test_correct_spectator_angle(self):
        """Should returns penalty value of prepared room
        (when angle between TV and sofa is bigger than 30 degrees) """

        furniture_dict = {
            'Wardrobe1': fun.Wardrobe(4, 10),
            'Wardrobe2': fun.Wardrobe(1, -6),
            'TV': fun.TV(8, 14),
            'Sofa': fun.Sofa(8, 18),
            'Table': fun.Table(-10, 4),
            'Chair1': fun.Chair(-12, 11),
            'Chair2': fun.Chair(-8, 11),
            'Chair3': fun.Chair(-12, -3),
            'Chair4': fun.Chair(-8, -3),
            'Desk': fun.Desk(-20, 5)
        }
        test_room = Room(50, 50, None, 5, furniture_dict)
        self.assertEqual(
            punish_for_too_big_spectator_angle(test_room), 0)

    def test_too_big_spectator_angle(self):
        """Should returns penalty value of prepared room
        (when angle between TV and sofa is bigger than 30 degrees) """

        furniture_dict = {
            'Wardrobe1': fun.Wardrobe(4, 10),
            'Wardrobe2': fun.Wardrobe(1, -6),
            'TV': fun.TV(4, 14),
            'Sofa': fun.Sofa(8, 18),
            'Table': fun.Table(-10, 4),
            'Chair1': fun.Chair(-12, 11),
            'Chair2': fun.Chair(-8, 11),
            'Chair3': fun.Chair(-12, -3),
            'Chair4': fun.Chair(-8, -3),
            'Desk': fun.Desk(-20, 5)
        }
        test_room = Room(50, 50, None, 5, furniture_dict)
        self.assertEqual(
            punish_for_too_big_spectator_angle(test_room), 15)

    def test_carpet_intersection(self):
        """Should returns penalty value of prepared room
        (when not expected furniture intersects with carpet rect) """

        furniture_dict = {
            'Wardrobe1': fun.Wardrobe(4, 10),
            'Wardrobe2': fun.Wardrobe(1, -6),
            'TV': fun.TV(4, 14),
            'Sofa': fun.Sofa(8, 18),
            'Table': fun.Table(-10, 4),
            'Chair1': fun.Chair(0, 2),
            'Chair2': fun.Chair(-8, 11),
            'Chair3': fun.Chair(-12, -3),
            'Chair4': fun.Chair(-8, -3),
            'Desk': fun.Desk(-20, 5)
        }
        test_room = Room(50, 50, None, 5, furniture_dict)
        self.assertEqual(
            punish_for_carpet_intersection(test_room), 10)

    def test_big_carpet(self):
        test_room = Room(50, 50, load_default_room_furniture(), 10)
        self.assertAlmostEqual(
            reward_for_carpet_size(test_room), 314.16, delta=0.01)

    def test_full_eval(self):
        """Should returns penalty value of prepared room
        (when angle between TV and sofa is bigger than 30 degrees) """

        furniture_dict = {
            'Wardrobe1': fun.Wardrobe(4, 10),
            'Wardrobe2': fun.Wardrobe(1, -6),
            'TV': fun.TV(4, 14),
            'Sofa': fun.Sofa(8, 18),
            'Table': fun.Table(-10, 4),
            'Chair1': fun.Chair(-12, 11),
            'Chair2': fun.Chair(-8, 11),
            'Chair3': fun.Chair(-12, -3),
            'Chair4': fun.Chair(-8, -3),
            'Desk': fun.Desk(-20, 5)
        }
        test_room = Room(50, 50, None, 5, furniture_dict)
        self.assertAlmostEqual(
            evaluate_room(test_room), 4.42, delta=0.01)


# Test runner
if __name__ == '__main__':
    unittest.main()

