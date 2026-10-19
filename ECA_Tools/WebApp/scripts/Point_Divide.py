#!/usr/bin/python3

"""
Point division by an integer scalar on an elliptic curve over GF(p^n) or GF(p).

Given a point P and a positive integer k, this program finds all points Q on
the same curve such that k*Q = P. There can be zero, one, or several answers.

Usage : sage Point_Divide.py <Base_Field> <Degree> <Choice_of_Coeff> <Coeff_a1> <Coeff_a2> <Coeff_a3> <Coeff_a4> <Coeff_a6> <Point_x> <Point_y> <Scalar>
Choice 1 takes no further arguments and chooses a random curve, point, and
positive scalar.
"""

from sage.all import *
import sys


USAGE1 = "Usage : sage Point_Divide.py <Base_Field> <Degree> <Choice_of_Coeff(=0)> <Coeff_a1> <Coeff_a2> <Coeff_a3> <Coeff_a4> <Coeff_a6> <Point_x> <Point_y> <Scalar>"
USAGE2 = "Usage : sage Point_Divide.py <Base_Field> <Degree> <Choice_of_Coeff(=1)>"


def _coerce(field, degree, value):
	return Integer(value) if degree == 1 else field(value)


def _random_curve(field):
	for _ in range(20):
		coeffs = [field.random_element() for _ in range(5)]
		try:
			return EllipticCurve(field, coeffs)
		except Exception:
			continue
	raise ValueError("Unable to generate a valid random elliptic curve.")


def _make_point(curve, x_coord, y_coord):
	try:
		return curve([x_coord, y_coord])
	except Exception:
		print("Problem with Argument! Point is not a point on the selected elliptic curve.")
		exit(1)


print("\n")

if len(sys.argv) < 4:
	print("Not Enough Arguments!")
	print(f"\n{USAGE1}")
	print("           OR")
	print(f"\n{USAGE2}")
	exit(1)

choice_of_coeff = Integer(sys.argv[3])

if choice_of_coeff not in (0, 1):
	print("Problem with Argument! Choice_of_Coeff should be either 0 or 1.")
	print(f"\n{USAGE1}")
	print("           OR")
	print(f"\n{USAGE2}")
	exit(1)

if (choice_of_coeff == 0) and (len(sys.argv) != 12):
	print(f"Problem with Argument!\n{USAGE1}")
	exit(1)
if (choice_of_coeff == 1) and (len(sys.argv) != 4):
	print(f"Problem with Argument!\n{USAGE2}")
	exit(1)

base_field = Integer(sys.argv[1])
degree = Integer(sys.argv[2])

K = GF((base_field, degree), names=('a',))
(a,) = K._first_ngens(1)

if choice_of_coeff == 0:
	coeffs = [_coerce(K, degree, sys.argv[index]) for index in range(4, 9)]
	point_x = _coerce(K, degree, sys.argv[9])
	point_y = _coerce(K, degree, sys.argv[10])
	scalar = Integer(sys.argv[11])
	E = EllipticCurve(K, coeffs)
	P = _make_point(E, point_x, point_y)
else:
	E = _random_curve(K)
	P = E.random_point()
	scalar = ZZ.random_element(1, 11)

if scalar <= 0:
	print("Problem with Argument! Scalar must be a positive integer.")
	exit(1)

division_points = P.division_points(scalar)

print("Printing Point Division Result:-\n")
print(f"{E}")
print(f"P = {P}")
print(f"Scalar = {scalar}")
if division_points:
	print(f"Points Q satisfying {scalar}*Q = P:")
	for Q in division_points:
		print(f"Q = {Q}")
else:
	print(f"No point Q over the selected field satisfies {scalar}*Q = P.")

print("\n")
exit(0)
