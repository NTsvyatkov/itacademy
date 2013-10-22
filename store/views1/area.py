class Figure(object):
    def perimeter(self):
        raise NotImplementedError()
 
    def area(self):
        raise NotImplementedError()
 
class Rectangle(Figure):
    sides = 2
 
    def __init__(self, a, b):
        super(Rectangle, self).__init__()
        self.a = a
        self.b = b
 
    def perimeter(self):
        return (self.a + self.b) * 2
 
    def area(self):
        return self.a * self.b
 
 
class Square(Rectangle):
    sides = 1
 
    def __init__(self, a):
        super(Square, self).__init__(a, a)
 
 
class Triangle(Figure):
    sides = 3
 
    def __init__(self, a, b, c):
        super(Triangle, self).__init__()
        self.a = a
        self.b = b
        self.c = c
 
    def perimeter(self):
        return self.a + self.b + self.c
 
    def area(self):
        p = float(self.perimeter()) / 2
        return (p * (p - self.a) * (p - self.b) * (p - self.c)) ** 0.5