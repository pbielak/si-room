import unittest

import si.problem.room_planning.eval as evals
from si.problem.room_planning import furniture as fun
from si.problem.room_planning.geometry import flip
from si.problem.room_planning.room import Room


class TestRoomEvaluator(unittest.TestCase):

    def setUp(self):
        self.room = Room(50, 50)

    def set_furniture(self, furniture_dict):
        self.room.furniture = furniture_dict
        self.room.update_carpet_size()

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
        self.set_furniture(furniture_dict)
        actual_reward = evals.reward_for_intersections(self.room)
        self.assertAlmostEqual(actual_reward, -892.5, delta=0.01)

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
        self.set_furniture(furniture_dict)
        actual_reward = evals.reward_for_intersections(self.room)
        self.assertAlmostEqual(actual_reward, 0, delta=0.01)

    def test_chairs_far_from_table(self):
        """In this test two chairs are far from the table."""

        furniture_dict = {
            'Table': fun.Table(-10, 4),
            'Chair1': fun.Chair(-12, 11),
            'Chair2': fun.Chair(-8, 11),
            'Chair3': fun.Chair(1, 1),
            'Chair4': fun.Chair(16, 15)
        }
        self.set_furniture(furniture_dict)
        actual_reward = evals.reward_for_chairs_placement(self.room)
        self.assertAlmostEqual(actual_reward, -54.2, delta=0.01)

    def test_chairs_near_table(self):
        """All chairs are near the table center."""

        furniture_dict = {
            'Table': fun.Table(-10, 4),
            'Chair1': fun.Chair(-12, 11),
            'Chair2': fun.Chair(-8, 11),
            'Chair3': fun.Chair(-12, -3),
            'Chair4': fun.Chair(-8, -3)
        }
        self.set_furniture(furniture_dict)
        actual_reward = evals.reward_for_chairs_placement(self.room)
        self.assertAlmostEqual(actual_reward, -29.12, delta=0.01)

    def test_correct_spectator_angle(self):
        """In this test spectator angle is smaller than 30 degrees."""

        furniture_dict = {
            'TV': fun.TV(8, 23),
            'Sofa': fun.Sofa(8, 18)
        }

        self.set_furniture(furniture_dict)
        actual_reward = evals.reward_for_tv_sofa_angle(self.room)
        self.assertAlmostEqual(actual_reward, 0, delta=0.01)

        flip(furniture_dict['TV'].figure)
        flip(furniture_dict['Sofa'].figure)
        actual_reward = evals.reward_for_tv_sofa_angle(self.room)
        self.assertAlmostEqual(actual_reward, 0, delta=0.01)

    def test_too_big_spectator_angle(self):
        """In this test spectator angle is bigger than 30 degrees."""

        furniture_dict = {
            'TV': fun.TV(4, 14),
            'Sofa': fun.Sofa(8, 18)
        }
        self.set_furniture(furniture_dict)
        actual_reward = evals.reward_for_tv_sofa_angle(self.room)
        self.assertAlmostEqual(actual_reward, -900.0, delta=0.01)

        flip(furniture_dict['TV'].figure)
        flip(furniture_dict['Sofa'].figure)
        actual_reward = evals.reward_for_tv_sofa_angle(self.room)
        self.assertAlmostEqual(actual_reward, -900.0, delta=0.01)

    def test_reward_for_furniture_outside_room(self):
        """Test if there is an appropriate reward/penalty for furniture
           that doesn't fit into the room.
        """

        furniture_dict = {
            'Sofa': fun.Sofa(30, 0)
        }
        self.set_furniture(furniture_dict)

        actual_reward = evals.reward_for_furniture_inside_room(self.room)
        self.assertEqual(actual_reward, -50)


# Test runner
if __name__ == '__main__':
    unittest.main()
