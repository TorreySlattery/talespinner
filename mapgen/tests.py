from django.test import TestCase

from mapgen.geometry import Rectangle

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

