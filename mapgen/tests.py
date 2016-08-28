import sys

from django.test import TestCase

from mapgen.geometry import Rectangle
from mapgen.utils import Room, Maze, Cave, Map
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
        self.sroom = Room(width=3, height=3)

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

    def test_is_path_clear_between(self):
        bl = (0, 0)
        tr = (2, 2)
        # A completely dug out room, thus, multiple shortests paths.
        self.sroom.room = [[1, 1, 1],
                           [1, 1, 1],
                           [1, 1, 1]]
        dist, prev = self.sroom.is_path_clear_between(bl, tr)
        print(dist)
        print(prev)
        self.assertTrue(self.sroom.is_path_clear_between(bl, tr))

        # A wall runs the full height of the room, making the destination unreachable.
        self.sroom.room = [[1, 0, 1],
                           [1, 0, 1],
                           [1, 0, 1]]
        self.assertFalse(self.sroom.is_path_clear_between(bl, tr))

        # A wall runs most of the height of the room, eliminating all but one path
        self.sroom.room = [[1, 0, 1],
                           [1, 0, 1],
                           [1, 1, 1]]

        br = (2, 0)
        self.assertTrue(self.sroom.is_path_clear_between(bl, br))

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
        self.cave = Cave()

    def test_reset(self):
        self.cave.reset((0,0))
        self.assertEqual(self.cave.area, 1)

    def test_lifespan(self):
        new_cave = Cave(lifespan=0)
        self.assertEqual(new_cave.area, 1)  # We always have the start location

        newer_cave = Cave(lifespan=-1)
        self.assertEqual(new_cave.area, 1)

    def test_seedable(self):
        seed = self.cave.seed
        clone_cave = Cave(seed=seed)
        self.assertEqual(self.cave.room, clone_cave.room)
        new_seed = seed + "This is a really unremarkable seed"
        new_cave = Cave(seed=new_seed)
        # This, like the Maze one, isn't airtight because of possible hash collisions
        self.assertNotEqual(self.cave.room, new_cave.room)

    def test_recreate_from_db(self):
        room_data = self.cave.save()
        room_data.refresh_from_db()
        clone_cave = Cave(seed=room_data.seed)
        self.assertEqual(self.cave.room, clone_cave.room)

    def test_min_area(self):
        min_cave = Cave(min_area = 15)
        self.assertGreaterEqual(min_cave.area, 15)

        too_high_min_cave = Cave(width=10, height=10, min_area=sys.maxsize)
        self.assertNotEqual(too_high_min_cave.min_area, sys.maxsize)

    def test_area(self):
        seed = "A rather unremarkable seed"
        cave1 = Cave(lifespan=0, seed=seed)
        area1 = cave1.area
        self.assertEqual(area1, 1)
        cave2 = Cave(seed=seed)
        area2 = cave2.area
        self.assertNotEqual(area1, area2)
        # Same deal. Potential to get a false negative, but I just want a basic check

    def test_get_shrinkwrapped(self):
        self.cave.room =  [[0, 0, 0],
                           [0, 1, 0],
                           [0, 0, 0]] # <-North end

        self.assertEqual(self.cave.get_shrinkwrapped(), [[1]])

    def test_set_shrinkwrapped(self):
        self.cave.room =  [[0, 0, 0],
                           [0, 1, 0],
                           [0, 0, 0]] # <-North end

        self.cave.set_shrinkwrapped()
        self.assertEqual(self.cave.room, [[1]])
        self.assertEqual(self.cave.height, 1)
        self.assertEqual(self.cave.width, 1)


class MapTestCase(TestCase):

    def setUp(self):
        self.map =  Map(width=3, height=3)
        self.map.room = [[0, 0, 0],
                         [0, 0, 0],
                         [0, 0, 0]] # <-North end

    def test_populate(self):
        placed_coordinates = self.map.populate(large=1, medium=0, small=0)
        self.assertNotEqual(placed_coordinates, [])

    def test_place(self):
        tiny_room = [[1]]
        x,y = self.map.place(tiny_room)
        self.assertEqual(self.map.room[y][x], 1)

    def test_check_available(self):
        room1 = [[1, 2],
                 [3, 4]]

        self.assertTrue(self.map.check_available((1,1), room1))
        self.assertFalse(self.map.check_available((2,0), room1))
        self.assertFalse(self.map.check_available((0, 2), room1))

        map2 = Map(width=3, height=3)
        map2.room = [[0, 0, 0],
                     [0, 1, 0],
                     [0, 0, 0]]

        self.assertFalse(map2.check_available((0,0), room1))
        self.assertFalse(map2.check_available((0,1), room1))
        self.assertFalse(map2.check_available((0,2), room1))
        self.assertFalse(map2.check_available((1,0), room1))
        self.assertFalse(map2.check_available((1,1), room1))
        self.assertFalse(map2.check_available((1,2), room1))
        self.assertFalse(map2.check_available((2,0), room1))
        self.assertFalse(map2.check_available((2,1), room1))
        self.assertFalse(map2.check_available((2,2), room1))

