import unittest

from si.problem.room_planning import furniture as fun
from si.problem.room_planning.eval import punish_intersections, punish_chairs
from si.problem.room_planning.room import Room


class TestRoomEvaluator(unittest.TestCase):

    def test_punish_intersections(self):
        """Should returns penalty value of prepared room (5 items intersect) """

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
        self.assertEqual(punish_intersections(test_room), 40)

    def test_no_punish_intersections(self):
        """Should returns penalty value of prepared room (0 items intersect) """

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
        self.assertEqual(punish_intersections(test_room), 0)

    def test_far_punish_chairs(self):
        """Should returns penalty value of prepared room
        (2 chairs have bigger distance from table) """

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
        # TODO: check distances...
        self.assertAlmostEqual(punish_chairs(test_room), 55.15, delta=0.01)


# Test runner
if __name__ == '__main__':
    unittest.main()
