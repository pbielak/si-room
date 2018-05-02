import unittest

import si.problem.room_planning.eval as evals
from si.problem.room_planning import furniture as fun
from si.problem.room_planning.geometry import flip
from si.problem.room_planning.room import Room


class TestRoomEvaluator(unittest.TestCase):

    def test_intersections_exist(self):
        """In this test 5 items should intersect."""

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
        test_room = Room(50, 50, 5, furniture_dict=furniture_dict)
        self.assertEqual(evals.punish_for_intersections(test_room), 80)

    def test_no_intersections_exist(self):
        """In this test any item should not intersect."""

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
        test_room = Room(50, 50, 5, furniture_dict=furniture_dict)
        self.assertEqual(evals.punish_for_intersections(test_room), 0)

    def test_chairs_far_from_table(self):
        """In this test two chairs are far from the table."""

        furniture_dict = {
            'Table': fun.Table(-10, 4),
            'Chair1': fun.Chair(-12, 11),
            'Chair2': fun.Chair(-8, 11),
            'Chair3': fun.Chair(1, 1),
            'Chair4': fun.Chair(16, 15)
        }
        test_room = Room(50, 50, 5, furniture_dict=furniture_dict)
        self.assertAlmostEqual(
            evals.punish_for_chairs_placement(test_room), 54.2, delta=0.01)

    def test_chairs_near_table(self):
        """All chairs are near the table center."""

        furniture_dict = {
            'Table': fun.Table(-10, 4),
            'Chair1': fun.Chair(-12, 11),
            'Chair2': fun.Chair(-8, 11),
            'Chair3': fun.Chair(-12, -3),
            'Chair4': fun.Chair(-8, -3)
        }
        test_room = Room(50, 50, 5, furniture_dict=furniture_dict)
        self.assertAlmostEqual(
            evals.punish_for_chairs_placement(test_room), 29.12, delta=0.01)

    def test_correct_spectator_angle(self):
        """In this test spectator angle is smaller than 30 degrees."""

        furniture_dict = {
            'TV': fun.TV(8, 23),
            'Sofa': fun.Sofa(8, 18)
        }

        test_room = Room(50, 50, 5, furniture_dict=furniture_dict)
        self.assertEqual(evals.punish_for_too_big_spectator_angle(test_room), 0)

        flip(furniture_dict['TV'].figure)
        flip(furniture_dict['Sofa'].figure)
        self.assertEqual(evals.punish_for_too_big_spectator_angle(test_room), 0)

    def test_too_big_spectator_angle(self):
        """In this test spectator angle is bigger than 30 degrees."""

        furniture_dict = {
            'TV': fun.TV(4, 14),
            'Sofa': fun.Sofa(8, 18),
        }
        test_room = Room(50, 50, 5, furniture_dict=furniture_dict)
        self.assertEqual(evals.punish_for_too_big_spectator_angle(test_room), 10)

        flip(furniture_dict['TV'].figure)
        flip(furniture_dict['Sofa'].figure)
        self.assertEqual(evals.punish_for_too_big_spectator_angle(test_room), 10)

    def test_carpet_intersection(self):
        """In this test only one item (from 2) is not allowed to intersect
         with carpet."""

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
        test_room = Room(50, 50, 5, furniture_dict=furniture_dict)
        self.assertEqual(evals.punish_for_carpet_intersection(test_room), 10)

    def test_big_carpet(self):
        """In this test we are checking carpet field."""
        test_room = Room(50, 50, 10, furniture_dict={})
        self.assertAlmostEqual(
            evals.reward_for_carpet_size(test_room), 314.16, delta=0.01)


# Test runner
if __name__ == '__main__':
    unittest.main()
