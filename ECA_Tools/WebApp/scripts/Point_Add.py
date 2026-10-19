#!/usr/bin/python3

"""
"" 26th April 2025 ::: Utpal Kumar Ray
""
"" Point Addition on an Elliptic Curve over GF(p^n) or GF(p).
""
"" Usage : sage Point_Add.py <Base_Field> <Degree> <Choice_of_Coeff> <Coeff_a1> <Coeff_a2> <Coeff_a3> <Coeff_a4> <Coeff_a6> <Point1_x> <Point1_y> <Point2_x> <Point2_y>
""
"" This Program adds two Points on an Elliptic Curve over GF(p^n) or GF(p).
"" The Elliptic Curve Equation being used is :-
"" y^2 + Coeff_a1*xy + Coeff_a3*y = x^3 + Coeff_a2*x^2 + Coeff_a4*x + Coeff_a6
""
"" The argument Choice_of_Coeff tells whether the Coeff's will be taken from Command Line or not.
"" If Choice_of_Coeff is 0: All Coefficients and Points are taken from Command Line Arguments.
"" If Choice_of_Coeff is 1: All Coefficients and Points are set to Random Element taken from the Base Field or Xtended Field
""                         (Depending upon the degree). So, the values of Coefficients and Points are absent in the command
""                         line.
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
"" Point1 = (5,1)
"" Point2 = (6,3)
"" OUTPUT :-
"" P + Q = (x,y) depending upon the curve and points
""
"""

from sage.all import *
import sys


USAGE1 = "Usage : sage Point_Add.py <Base_Field> <Degree> <Choice_of_Coeff(=0)> <Coeff_a1> <Coeff_a2> <Coeff_a3> <Coeff_a4> <Coeff_a6> <Point1_x> <Point1_y> <Point2_x> <Point2_y>"
USAGE2 = "Usage : sage Point_Add.py <Base_Field> <Degree> <Choice_of_Coeff(=1)>"


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


def _make_point(curve, x_coord, y_coord, label):
	try:
		return curve([x_coord, y_coord])
	except Exception:
		print(f"Problem with Argument! {label} is not a point on the selected elliptic curve.")
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

if (choice_of_coeff == 0) and (len(sys.argv) != 13):
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
	# All coefficients and points are taken from the Command Line.
	coeff_a1 = _coerce(K, degree, sys.argv[4])
	coeff_a2 = _coerce(K, degree, sys.argv[5])
	coeff_a3 = _coerce(K, degree, sys.argv[6])
	coeff_a4 = _coerce(K, degree, sys.argv[7])
	coeff_a6 = _coerce(K, degree, sys.argv[8])
	point1_x = _coerce(K, degree, sys.argv[9])
	point1_y = _coerce(K, degree, sys.argv[10])
	point2_x = _coerce(K, degree, sys.argv[11])
	point2_y = _coerce(K, degree, sys.argv[12])

	E = EllipticCurve(K, [coeff_a1, coeff_a2, coeff_a3, coeff_a4, coeff_a6])
	P = _make_point(E, point1_x, point1_y, "Point1")
	Q = _make_point(E, point2_x, point2_y, "Point2")
else:
	# It can be Finite Field or Extended Finite Field.
	# All coefficients and points are set to Random Values coming from the respective field.
	E = _random_curve(K)
	coeff_a1, coeff_a2, coeff_a3, coeff_a4, coeff_a6 = E.a_invariants()
	P = E.random_point()
	Q = E.random_point()

R = P + Q

print(f"Printing Point Addition Result:-\n")
print(f"{E}")
print(f"P = {P}")
print(f"Q = {Q}")
print(f"P + Q = {R}")

print("\n")

exit(0)
