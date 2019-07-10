import unittest
from autopew.transform import CoordinateTransform

stream_log("autopew.transform")

a = CoordinateTransform("A", "B")

b = CoordinateTransform("B", "C")

c = CoordinateTransform("B", "C")

str(a.library[0])
CoordinateTransform.library
