#!/usr/bin/python3

"""
"" 26th April 2025 ::: Utpal Kumar Ray
""
"" Point Multiplication on an Elliptic Curve over GF(p^n) or GF(p).
""
"" Usage : sage Point_Multiply.py <Base_Field> <Degree> <Choice_of_Coeff> <Coeff_a1> <Coeff_a2> <Coeff_a3> <Coeff_a4> <Coeff_a6> <Point_x> <Point_y> <Scalar>
""
"" This Program multiplies a Point on an Elliptic Curve by an Integer Scalar.
"" The Elliptic Curve Equation being used is :-
"" y^2 + Coeff_a1*xy + Coeff_a3*y = x^3 + Coeff_a2*x^2 + Coeff_a4*x + Coeff_a6
""
"" The argument Choice_of_Coeff tells whether the Coeff's will be taken from Command Line or not.
"" If Choice_of_Coeff is 0: All Coefficients, Point and Scalar are taken from Command Line Arguments.
"" If Choice_of_Coeff is 1: All Coefficients and Point are set to Random Element taken from the Base Field or Xtended Field
""                         (Depending upon the degree). The Scalar is also chosen randomly.
""
""
""
"" Sample Input/Output Set
""
"" INPUT :-
"" Base_Field = 17
"" Degree = 1
"" Choice_of_Coeff = 0
"" Coeff_a1 = 0
"" Coeff_a2 = 0
"" Coeff_a3 = 0
"" Coeff_a4 = 3
"" Coeff_a6 = 14
"" Point = (5,1)
"" Scalar = 7
"" OUTPUT :-
"" 7*P = (x,y) depending upon the curve and point
""
"""

from sage.all import *
import sys


USAGE1 = "Usage : sage Point_Multiply.py <Base_Field> <Degree> <Choice_of_Coeff(=0)> <Coeff_a1> <Coeff_a2> <Coeff_a3> <Coeff_a4> <Coeff_a6> <Point_x> <Point_y> <Scalar>"
USAGE2 = "Usage : sage Point_Multiply.py <Base_Field> <Degree> <Choice_of_Coeff(=1)>"


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

if choice_of_coeff > 1:
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
	# It's a Finite Field or Extended Finite Field.
	# All coefficients, point and scalar are taken from the Command Line.
	coeff_a1 = _coerce(K, degree, sys.argv[4])
	coeff_a2 = _coerce(K, degree, sys.argv[5])
	coeff_a3 = _coerce(K, degree, sys.argv[6])
	coeff_a4 = _coerce(K, degree, sys.argv[7])
	coeff_a6 = _coerce(K, degree, sys.argv[8])
	point_x = _coerce(K, degree, sys.argv[9])
	point_y = _coerce(K, degree, sys.argv[10])
	scalar = Integer(sys.argv[11])

	E = EllipticCurve(K, [coeff_a1, coeff_a2, coeff_a3, coeff_a4, coeff_a6])
	P = _make_point(E, point_x, point_y)
else:
	# It can be Finite Field or Extended Finite Field.
	# All coefficients and point are set to Random Values coming from the respective field.
	E = _random_curve(K)
	coeff_a1, coeff_a2, coeff_a3, coeff_a4, coeff_a6 = E.a_invariants()
	P = E.random_point()
	scalar = ZZ.random_element(-10, 11)

R = scalar * P

print(f"Printing Point Multiplication Result:-\n")
print(f"{E}")
print(f"P = {P}")
print(f"Scalar = {scalar}")
print(f"Scalar * P = {R}")

print("\n")

exit(0)
