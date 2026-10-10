import unittest

from gym.data.hall_repository import HallRepository
from gym.manager.hall_manager import HallManager
from gym.models.gym_hall import GymHall


class RepositoryTests(unittest.TestCase):
    def setUp(self):
        self.repo = HallRepository()

    def test_duplicate_is_not_overwritten(self):
        self.repo.add(GymHall("Main Hall", 20))
        message = self.repo.add(GymHall("Main Hall", 99))
        self.assertIn("already exists", message)
        self.assertEqual(self.repo.get_by_name("Main Hall").capacity, 20)

    def test_unknown_name_returns_message(self):
        self.assertEqual(self.repo.get_by_name("Ghost"), "Hall 'Ghost' was not found.")

    def test_update_does_not_create(self):
        self.repo.update(GymHall("Ghost", 10))
        self.assertEqual(self.repo.get_all(), [])


class ManagerTests(unittest.TestCase):
    def setUp(self):
        self.manager = HallManager(HallRepository())
        self.manager.create_hall("Main Hall", 20, ["Treadmill"])

    def test_create_and_get(self):
        hall = self.manager.get_hall("Main Hall")
        self.assertEqual(hall.capacity, 20)
        self.assertEqual(hall.equipment, ["Treadmill"])
        self.assertTrue(hall.is_active)

    def test_reject_bad_name(self):
        for name in ("", "   "):
            self.assertFalse(self.manager.create_hall(name, 20).success)

    def test_reject_bad_capacity(self):
        for capacity in (0, -1, 2.5, "20"):
            self.assertFalse(self.manager.create_hall("Yoga Room", capacity).success)
        self.assertEqual(len(self.manager.list_halls()), 1)

    def test_reject_duplicate_name(self):
        self.assertFalse(self.manager.create_hall("Main Hall", 50).success)

    def test_unknown_hall(self):
        self.assertIsNone(self.manager.get_hall("Ghost"))
        self.assertFalse(self.manager.update_hall("Ghost", 5).success)
        self.assertFalse(self.manager.deactivate_hall("Ghost").success)
        self.assertFalse(self.manager.activate_hall("Ghost").success)

    def test_update(self):
        self.assertTrue(self.manager.update_hall("Main Hall", 35, ["Bike"]).success)
        hall = self.manager.get_hall("Main Hall")
        self.assertEqual((hall.capacity, hall.equipment), (35, ["Bike"]))

    def test_invalid_update_changes_nothing(self):
        self.assertFalse(self.manager.update_hall("Main Hall", -5, ["Bike"]).success)
        hall = self.manager.get_hall("Main Hall")
        self.assertEqual((hall.capacity, hall.equipment), (20, ["Treadmill"]))

    def test_deactivate_and_reactivate(self):
        self.manager.deactivate_hall("Main Hall")
        self.assertFalse(self.manager.get_hall("Main Hall").is_active)
        self.assertEqual(len(self.manager.list_halls()), 1)
        self.manager.activate_hall("Main Hall")
        self.assertTrue(self.manager.get_hall("Main Hall").is_active)


if __name__ == "__main__":
    unittest.main()
