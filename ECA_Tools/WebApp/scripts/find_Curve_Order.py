#!/usr/bin/python3   

"""
"" 29th MAY 2025 ::: Utpal Kumar Ray  
"" 
"" Usage : sage find_Curve_Order.py <Base_Field> <Degree> <Choice_of_Coeff> <Coeff_a1> <Coeff_a2> <Coeff_a3> <Coeff_a4> <Coeff_a6>
"" 
"" This Program finds the Curve Order of an Elliptic Curve over GF(p^n) or GF(p).
"" This Program also tries to find the Generator Points [Need to be Verified].                
"" The Elliptic Curve Equation being used is :-
"" y^2 + Coeff_a1*xy + Coeff_a3*y = x^3 + Coeff_a2*x^2 + Coeff_a4*x + Coeff_a6
""
"" The argument Choice_of_Coeff tells whether the Coeff's will be taken from Command Line or not.   
"" If Choice_of_Coeff is 0: All Coefficients are taken from Command Line Arguments.
"" If Choice_of_Coeff is 1: All Coefficients are set to Random Element taken from the Base Field or Xtended Field
""                         (Depending upon the degree). So, the values of Coefficients are absent in the command 
""                         line.
""
""
"" Sample Input/Output Sets                 
""
"" INPUT 1:-
"" Base_Field = 17
"" Degree = 1
"" Choice_of_Coeff = 0
"" Coeff_a1 = 0
"" Coeff_a2 = 0
"" Coeff_a3 = 0
"" Coeff_a4 = 3
"" Coeff_a6 = 14
"" OUTPUT 1:-
"" Elliptic Curve defined by y^2 = x^3 + 3*x + 14 over Finite Field of size 17 :: Curve Order = 12
"" Time Taken = 3 Sec (Macbook Air M2)
"" 
"" INPUT 2:-
"" Base_Field = 43
"" Degree = 1
"" Choice_of_Coeff = 0
"" Coeff_a1 = 4
"" Coeff_a2 = 1
"" Coeff_a3 = 2
"" Coeff_a4 = 3
"" Coeff_a6 = 14
"" OUTPUT 2:-
"" Elliptic Curve defined by y^2 + 4*x*y + 2*y = x^3 + x^2 + 3*x + 14 over Finite Field of size 43 :: Curve Order = 48
"" Time Taken = 3 Sec (Macbook Air M2)
""
"" INPUT 3:-
"" Base_Field = 43
"" Degree = 2
"" Choice_of_Coeff = 1
"" OUTPUT 3:-
"" Elliptic Curve defined by y^2 + (37*a+36)*x*y + (32*a+15)*y = x^3 + (40*a+21)*x^2 + (19*a+9)*x + (9*a+31) over Finite Field in a of size 43^2 :: Curve Order = 1856
"" Time Taken = 3 Sec (Macbook Air M2)
"" 
"" INPUT 4:-
"" Base_Field = 3
"" Degree = 3
"" Choice_of_Coeff = 0
"" Coeff_a1 = 0
"" Coeff_a2 = 0
"" Coeff_a3 = 0
"" Coeff_a4 = a^2+a+2
"" Coeff_a6 = 2*a^2+a
"" OUTPUT 4:-
"" Elliptic Curve defined by y^2 = x^3 + (a^2+a+2)*x + (2*a^2+a) over Finite Field in a of size 3^3 :: Curve Order (It is PRIME) = 37
"" Time Taken = 3 Sec (Macbook Air M2)
""
"" INPUT 5:-
"" Base_Field = 11
"" Degree = 2
"" Choice_of_Coeff = 0
"" Coeff_a1 = 3*a+9
"" Coeff_a2 = 5*a+8
"" Coeff_a3 = 9*a
"" Coeff_a4 = 8
"" Coeff_a6 = 2*a+2
"" OUTPUT 5:-
"" Elliptic Curve defined by y^2 + (3*a+9)*x*y + 9*a*y = x^3 + (5*a+8)*x^2 + 8*x + (2*a+2) over Finite Field in a of size 11^2 :: Curve Order (It is PRIME) = 139
"" Time Taken = 3 Sec (Macbook Air M2)
""
""
"" INPUT 6:-
"" Base_Field = 1019
"" Degree = 1
"" Choice_of_Coeff = 0
"" Coeff_a1 = 0
"" Coeff_a2 = 0
"" Coeff_a3 = 0
"" Coeff_a4 = 19
"" Coeff_a6 = 11
"" OUTPUT 6:-
"" Elliptic Curve defined by y^2 = x^3 + 19*x + 11 over Finite Field of size 1019 :: Curve Order (It is PRIME) = 1031
"" Time Taken = 3 Sec (Macbook Air M2)
"" 
""
"" INPUT 7:-
"" Base_Field = 10111114444444444444444411111111111111777777777333337777722222222222222222222222222211133333333333333333333333333333333333333431
"" Degree = 1
"" Choice_of_Coeff = 1
"" OUTPUT 7:-
"" Elliptic Curve defined by y^2 + 7310212633484731257460566712091507592697467826279193687125171931972942722461742379660297963191143794662253612058843834294288376*x*y + 7828532324393425911978645136452074525160967745938842625461593219076746302939591661382267683714325905545796229092644279674600385*y = x^3 + 698815542549916190575731293140972727057774005714989648863740572618471482066028739601646739398004869993054333936194146258545625*x^2 + 2618253721792796463994512162599124487070790693355896017060777086495483545346640585166227831470186803364010996364782785059356998*x + 1906779653174817023500982560606570365659238447716870029425937995347566040011485085070795682903053544603256240937681370851481400 over Finite Field of size 10111114444444444444444411111111111111777777777333337777722222222222222222222222222211133333333333333333333333333333333333333431 :: Curve Order = 10111114444444444444444411111111111111777777777333337777722222227061286798181158662051962946702981833761611143829917461722040118 (Digits=128 :: Bits=427 :: HEX=107)
"" Time Taken = 21 Sec (Macbook Air M2)
""
"" INPUT 8:-
"" Base_Field = 1011111444444444444444441111111111111177777777733333777837
"" Degree = 4
"" Choice_of_Coeff = 1
"" OUTPUT 8:-
"" Elliptic Curve defined by y^2 + (276879158294675083655138488394279286867069767014567955723*a^3+223583651702665544789604581808931064566848166517632039359*a^2+402890251920259664741231946994859998533635386889742343794*a+88610267354313600946096427367018110915567849472307392960)*x*y + (201867200829452608749419206781009121571032734332574521323*a^3+704299478410913146348527961940787488125547221202495159446*a^2+767440185484982667633125781373057491440840689082442418481*a+296784836818616672882259300823288324717892440550463994339)*y = x^3 + (819940548898192950085218551233794377374242322201507919309*a^3+17232561620610748822320028412997180505759968213965161351*a^2+232927062918053180604478862544398019358107097850440400152*a+858831600009963339635900252991847050051913661231363055631)*x^2 + (129260127774335188757088034091494171027924558959293777436*a^3+23686839759846717715204039696703543843217368917349289117*a^2+453071019890105531605216876930637894406220927916721674579*a+456393442168696082167047622927767634933008386257305474917)*x + (554956449517373399862480588419747010169939005960485911805*a^3+705846314072449520799064738763490071773480588292537420564*a^2+635186662165785317679657355658178959919192141894759383402*a+530873567202243687273342282499074325231772289208163418026) over Finite Field in a of size 1011111444444444444444441111111111111177777777733333777837^4 :: Curve Order = 1045192065669329635876041708945368872477452971793638354091598414551900869443790542727512159389332676254133678322753801881431584918198602651372797273568614840740577464356460373057631851976842425656512705050962297162319758180823412 (Digits=229 :: Bits=764 :: HEX=192)
"" Time Taken = 15 Min (Macbook Air M2)
""
"""

from sage.all import *
import sys

"""
"" The following code is for Single Stepping Debugging Process.
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

USAGE1="Usage : sage find_Curve_Order.py <Base_Field> <Degree> <Choice_of_Coeff(=0)> <Coeff_a1> <Coeff_a2> <Coeff_a3> <Coeff_a4> <Coeff_a6>"
USAGE2="Usage : sage find_Curve_Order.py <Base_Field> <Degree> <Choice_of_Coeff(=1)>"

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

Base_Field = Integer(sys.argv[1])
Degree = Integer(sys.argv[2])

# Defining the Given Field.
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
	Coeff_a4 = K(sys.argv[7]) #K(a**2+a+2)  
	Coeff_a6 = K(sys.argv[8]) #K(2*a**2+a)  

if (Choice_of_Coeff == 1):
#It can be Finite Field or Extended Finite Field.
#All coefficient are set to Random Values comming from the respective field..
	Coeff_a1 = K.random_element()  
	Coeff_a2 = K.random_element()  
	Coeff_a3 = K.random_element()  
	Coeff_a4 = K.random_element()  
	Coeff_a6 = K.random_element()  
	
#Define the Elliptic Curve.
E = EllipticCurve(K, [Coeff_a1, Coeff_a2, Coeff_a3, Coeff_a4, Coeff_a6]) 
#The Equation for Elliptic Curve:
#y^2 + Coeff_a1*xy + Coeff_a3*y = x^3 + Coeff_a2*x^2 + Coeff_a4*x + Coeff_a6

Curve_Order = E.order()
Generator_Point = E.gens()

#Print the Elliptic Curve Details and the Curve Order.
print(f"Printing the Curve Order:-\n")
if is_prime(Curve_Order) == True:
	print(f"{E} :: Curve Order (It is Prime) = {Curve_Order} :: Generator_Point = {Generator_Point}")
else:
	print(f"{E} :: Curve Order = {Curve_Order} :: Generator_Point = {Generator_Point}")

print("\n")

exit(0)

"""
"""
