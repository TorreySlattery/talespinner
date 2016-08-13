from django.test import TestCase

from mapgen.geometry import Rectangle
from mapgen.utils import Room, Maze, Cave
from mapgen.models import RoomData

class GeometryTestCase(TestCase):
    def setUp(self):
        self.rect = Rectangle(x1=0, y1=0, x2=10, y2=5)

    def test_rectangle_defauts(self):
        rect = Rectangle()
        self.assertEquals(rect.x1, 0)
        self.assertEquals(rect.y1, 0)
        self.assertEquals(rect.x2, 1)
        self.assertEquals(rect.y2, 1)

    def test_rectangle_constructs(self):
        self.assertEquals(self.rect.x1, 0)
        self.assertEquals(self.rect.y1, 0)
        self.assertEquals(self.rect.x2, 10)
        self.assertEquals(self.rect.y2, 5)

    def test_rectangle_height(self):
        self.assertEquals(self.rect.height, 5)

    def test_rectangle_width(self):
        self.assertEquals(self.rect.width, 10)

    def test_rectangle_contains(self):
        vertex = (1, 1)
        self.assertTrue(self.rect.contains(vertex))

    def test_rectangle_intersects(self):
        rect = Rectangle()
        self.assertTrue(self.rect.intersects(rect))
        self.assertTrue(rect.intersects(self.rect))


class RoomTestCase(TestCase):
    def setUp(self):
        self.room = Room()

    def test_width(self):
        for row in self.room.room:
            self.assertEqual(self.room.width, len(row))

    def test_height(self):
        self.assertEqual(self.room.height, len(self.room.room))

    def test_save(self):
        room_objs = RoomData.objects.all()
        self.assertEqual(len(room_objs), 0)

        room_data = self.room.save()
        room_objs = RoomData.objects.all()
        self.assertEqual(len(room_objs), 1)

        room_obj = room_objs[0]

        self.assertEqual(self.room.width, room_obj.width)
        self.assertEqual(self.room.height, room_obj.height)

class MazeTestCase(TestCase):
    def setUp(self):
        self.maze = Maze()

    def test_get_dirs(self):
        directions  = self.maze.get_dirs()

        for direction in directions:
            self.assertIn(direction, [(1,0), (-1,0), (0,1), (0,-1)])

    def test_get_quad_cardinals(self):
        self.maze.room = [[1,2,3],
                          [4,5,6],
                          [7,8,9]] # North 
        center = (1,1)
        quad = self.maze.get_quad(center)
        self.assertEqual(quad[(0,1)], 8)
        self.assertEqual(quad[(1,0)], 6)
        self.assertEqual(quad[(0,-1)], 2)
        self.assertEqual(quad[(-1,0)], 4)

    def test_seedable(self):
        seed = self.maze.seed
        clone_maze = Maze(seed=seed)
        self.assertEqual(self.maze.room, clone_maze.room)
        new_seed = seed + "This is a really unremarkable seed"
        new_maze = Maze(seed=new_seed)
        self.assertNotEqual(self.maze.room, new_maze.room)

    def test_recreate_from_db(self):
        room_data = self.maze.save()
        room_data.refresh_from_db()
        clone_maze = Maze(seed=room_data.seed)
        self.assertEqual(self.maze.room, clone_maze.room)

class CaveTestCase(TestCase):

    def setUp(self):
        pass

    def test_reset(self):
        pass

    def test_lifespan(self):
        pass

    def test_seedable(self):
        pass

    def test_recreate_from_db(self):
        pass

    def test_min_area(self):
        pass

    def test_area(self):
        pass
