from django.test import TestCase

from mapgen.geometry import Rectangle
from mapgen.utils import Maze

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

class MazeTestCase(TestCase):
    def setUp(self):
        self.maze = Maze()

    def test_get_dirs(self):
        directions  = self.maze.get_dirs()

        for direction in directions:
            self.assertIn(direction, [(1,0), (-1,0), (0,1), (0,-1)])

    def test_get_quad(self):
        tl,tr,bl,br = ((0,0), (39, 0), (0, 19), (39, 19))

        from_top_left = self.maze.get_quad(tl)
        self.assertEqual(from_top_left['N'], None)
        self.assertEqual(from_top_left['E'], 0)
        self.assertEqual(from_top_left['S'], 0)
        self.assertEqual(from_top_left['W'], None)

        from_top_right = self.maze.get_quad(tr)
        self.assertEqual(from_top_right['N'], None)
        self.assertEqual(from_top_right['E'], None)
        self.assertEqual(from_top_right['S'], 0)
        self.assertEqual(from_top_right['W'], 0)

        from_bottom_left = self.maze.get_quad(bl)
        self.assertEqual(from_bottom_left['N'], 0)
        self.assertEqual(from_bottom_left['E'], 0)
        self.assertEqual(from_bottom_left['S'], None)
        self.assertEqual(from_bottom_left['W'], None)

        from_bottom_right = self.maze.get_quad(br)
        self.assertEqual(from_bottom_right['N'], 0)
        self.assertEqual(from_bottom_right['E'], None)
        self.assertEqual(from_bottom_right['S'], None)
        self.assertEqual(from_bottom_right['W'], 0)
