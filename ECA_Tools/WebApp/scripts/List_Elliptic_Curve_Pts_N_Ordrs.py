#!/usr/bin/python3   

"""
"" 
"" 28th Sept 2025
"" List all Elliptic Curve Points and their Orders. 
"" 
""
"" Usage : sage List_Elliptic_Curve_Pts_N_Ordrs.py <Base_Field> <Degree> <Choice_of_Coeff> <Coeff_a1> <Coeff_a2> <Coeff_a3> <Coeff_a4> <Coeff_a6>
""
"" 
"" Interesting Results out of this program:-
""
"" 1. The coefficients a1 and a3 should be zero so that the resultant curve is 
"" symmetrical accross X-axis. 
""
"" 2. The coefficient a3 has certain effect on the curve.[Use Desmos Graphing Calculator]
"" It shifts the curve up or down depending upon the sign and value of a3.
"" Usually, for a good EC(a1/a3 being 0), the mirror-line is X-axis.
"" But, a3 shifts the mirror-line away from X-axis.
"" if a3 = 6, then the mirror-line is (y=-3). [a1 being 0]
"" if a3 = -16, then the mirror-line is (y=8). [a1 being 0]
""
""
""
"""

from sage.all import *
import sys

"""
age " The following code is for Single Stepping Debugging Process.
"" 
"" import pdb
""
"" pdb.set_trace()
""
"" Important pdb commands:-
"" n: Step to the next line of code.
"" s: Step into a function call.
"" c: Continue execution until the next breakpoint or the end of the program.
"" q: Quit the debugger.
""
"""

USAGE1="Usage : sage List_Elliptic_Curve_Pts_N_Ordrs.py <Base_Field> <Degree> <Choice_of_Coeff(=0)> <Coeff_a1> <Coeff_a2> <Coeff_a3> <Coeff_a4> <Coeff_a6>"
USAGE2="Usage : sage List_Elliptic_Curve_Pts_N_Ordrs.py <Base_Field> <Degree> <Choice_of_Coeff(=1)>"


print("\n")

if (len(sys.argv) < 4):
	print (f"Not Enough Arguments!")
	print (f"\n{USAGE1}")
	print (f"           OR")
	print (f"\n{USAGE2}")
	exit(1)

Choice_of_Coeff = Integer(sys.argv[3])

if (Choice_of_Coeff > 1):
	print (f"Problem with Argument! Choice_of_Coeff should be either 0 or 1.")
	print (f"\n{USAGE1}")
	print (f"           OR")
	print (f"\n{USAGE2}")
	exit(1)

if ((Choice_of_Coeff == 0) and (len(sys.argv)!=9)):
	print (f"Problem with Argument!\n{USAGE1}")
	exit(1)
if ((Choice_of_Coeff == 1) and (len(sys.argv)!=4)):
	print (f"Problem with Argument!\n{USAGE2}")
	exit(1)

# ensuring a proper Base Field. 
Base_Field = Integer(sys.argv[1])
if is_prime(Base_Field) == False:
	print (f"Given Base_Field {Base_Field} is not prime.")
	Base_Field = next_prime(Base_Field)
	print (f"Using the next Prime {Base_Field}.")

Degree = Integer(sys.argv[2])

# Defining the elliptic curve
K = GF((Base_Field,Degree), names=('a',))
(a,) = K._first_ngens(1)

if ((Choice_of_Coeff == 0) and (Degree == 1)):
#It's a Finite Field. All coefficient are integers. They are taken from the Command Line.
	Coeff_a1 = Integer(sys.argv[4])
	Coeff_a2 = Integer(sys.argv[5])
	Coeff_a3 = Integer(sys.argv[6])
	Coeff_a4 = Integer(sys.argv[7])
	Coeff_a6 = Integer(sys.argv[8])

if ((Choice_of_Coeff == 0) and (Degree > 1)):
#It's a Extended Finite Field. All coefficient are Polynomial. They are taken from the Command Line.
	Coeff_a1 = K(sys.argv[4])
	Coeff_a2 = K(sys.argv[5])
	Coeff_a3 = K(sys.argv[6])
	Coeff_a4 = K(sys.argv[7])
	Coeff_a6 = K(sys.argv[8])

if (Choice_of_Coeff == 1):
#It can be Finite Field or Extended Finite Field.
#All coefficient are set to Random Values comming from the respective field..
	Coeff_a1 = K.random_element()
	Coeff_a2 = K.random_element()
	Coeff_a3 = K.random_element()
	Coeff_a4 = K.random_element()
	Coeff_a6 = K.random_element()

E = EllipticCurve(K, [Coeff_a1, Coeff_a2, Coeff_a3, Coeff_a4, Coeff_a6]) 
#The Equation for Elliptic Curve:
#y^2 + Coeff_a1*xy + Coeff_a3*y = x^3 + Coeff_a2*x^2 + Coeff_a4*x + Coeff_a6
#print(f"The Elliptic Curve Parameters ::: Base_Field={Base_Field} :: Degree={Degree} :: Coeff_a1={Coeff_a1} :: Coeff_a2={Coeff_a2} :: Coeff_a3={Coeff_a3} :: Coeff_a4={Coeff_a4} :: Coeff_a6={Coeff_a6}")

#Identify the Elliptic Curve(Whether Symmetrical/Non-Symmetrical accross X-axis)
if (Coeff_a1 == 0) and (Coeff_a3 == 0):
	Symmetric_EC = 1 #(Suitable for Cryptography)
	print(f"{E} [Symmetric accross X-axis]\n")
else:
	Symmetric_EC = 0 #(May not be Suitable for Cryptography)
	print(f"{E} [Non-Symmetric accross X-axis]\n")

Curve_Order = E.order()
Lst_of_Pts = E.points()

print(f"\nNumber of Total Points(including O point) is: {Curve_Order}")

#Print the First Point(Infinity Point).
First_Point = Lst_of_Pts[0]
print(f"{First_Point}\tOrder is::{First_Point.order()}::")

#Print the Second Point(Incase it is a Zero Point).
i=1
Second_Point = Lst_of_Pts[i]
if ((Second_Point.x() == 0) and (Second_Point.y() == 0)):
	print(f"{Second_Point}\tOrder is::{Second_Point.order()}::")
	i=2
else:
	i=1

#Now print Rest of the Points. But first, make sure whether the EC is Symmetrical or Non-Symmetrical.
#For Symmetrical EC (Cryptography Friendly), print the points pair-wise.
#For Non-Symmetrical EC (Not Cryptography Friendly), print a single points in a single row.
if (Symmetric_EC):
	while i < Curve_Order:
		#for every point, check whether it is a point on X-axis. If it is, then print it alone.
		#Otherwise, print in pairs.
		if (Lst_of_Pts[i].y() == 0):
			#Single Point on X-axis.
			Single_Point = Lst_of_Pts[i]
			print(f"{Single_Point}\tOrder is::{Single_Point.order()}::")
			#print(f"{Single_Point} SINGLE")
			i = i + 1
		else:
			#print in pairs.
			Double_Point = Lst_of_Pts[i]
			print(f"{Double_Point}", end='\t')
			i = i + 1
			Double_Point = Lst_of_Pts[i]
			print(f"{Double_Point}\tOrder is::{Double_Point.order()}::")
			i = i + 1
else: #Non_Symmetric EC. Print Single point in a Single row.
	while i < Curve_Order:
		Single_Point = Lst_of_Pts[i]
		print(f"{Single_Point}\tOrder is::{Single_Point.order()}::")
		i = i + 1

print("\n")


