import math as m
# ----------------------------------------------------------------------------------------------------------------------
C = 1                   # Chord length [m]
jetPosition = 0.0082*C  # Chord location of the jet [m]
jetHeight = 0.0005*C    # Jet Height [m]
fmrDistance = 0.025*C   # Distance from the chord of the first meshing region  [m]
AoA = 14*m.pi/180       # Angle of Attack [rad]
inletDistance = 15*C    # Distance from the leading edge to the inlet [m]
outletDistance = 20*C   # Distance from the leading edge to the outlet [m]
slopeNodesSJA = 4       # Number of nodes that conform the SJA slope
# ----------------------------------------------------------------------------------------------------------------------
""" Creates a file that will contain all the mesh information """
meshFile = open("SD7003_Mesh.geo", 'w')
# ----------------------------------------------------------------------------------------------------------------------
""" Declares some mesh parameters that allow tuning the mesh directly from this .geo file """
meshFile.write("//=================================================================================\n")
meshFile.write("// Mesh parameters:\n")
meshFile.write("//=================================================================================\n")

""" nSpX define the number of structured cells that bound the different airfoil's sections """
meshFile.write("nSp1 = 160*0.7;\n")
meshFile.write("nSp2 = 150*0.7;\n")
meshFile.write("nSp3 = 150*0.7;\n")
meshFile.write("nSp4 = 12*0.7;\n")
meshFile.write("nSp5 = 40*0.7;\n")
meshFile.write("nSp6 = 34*0.7;\n")
meshFile.write("nSp7 = 100*0.7;\n")
meshFile.write("nSp8 = 300*0.7;\n\n")

""" Parameters defining the progression of the nSpX structured cells """
meshFile.write("xProg1 = 1;\n")
meshFile.write("xProg2 = 0.991;\n")
meshFile.write("xProg3 = 0.995;\n")
meshFile.write("xProg4 = 1;\n")
meshFile.write("xProg5 = 1;\n")
meshFile.write("xProg6 = 1;\n")
meshFile.write("xProg7 = 1.017;\n")
meshFile.write("xProg8 = 1.002;\n\n")

""" Parameters defining the number of structured cells of the jet patch and their progression """
meshFile.write("SJAYdiv = 20;\n")
meshFile.write("SJAYprog = 1;\n\n")

""" Parameters defining the number of vertically structured cells and their progression in the first meshing region """
meshFile.write("firstYdiv = 36;\n")
meshFile.write("firstYprog = 1.15;\n\n")

""" Parameters defining the number of horizontally structured cells and their progression in the trailing edge """
meshFile.write("teXpoints = 40;\n")
meshFile.write("teXprog = 1;\n\n")

""" Parameter that defines the resolution of the transition between the structured and unstructured regions """
meshFile.write("densOut = 1/8;\n\n")

""" Parameter that defines the color of the mesh, just for beauty purposes """
meshFile.write("meshColor = 'DimGray';\n")
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# Section in charge of plotting the airfoil
# ----------------------------------------------------------------------------------------------------------------------
""" Opens the document containing the airfoil discretization """
airfoilPointsFile = open("airfoilPoints", 'r')
X = []
Y = []

""" Jumps the initial commentary """
line = airfoilPointsFile.readline()
line = airfoilPointsFile.readline()
line = airfoilPointsFile.readline()
line = airfoilPointsFile.readline()
line = airfoilPointsFile.readline()
line = airfoilPointsFile.readline()

""" Loop in charge of translating the airfoil document points into tractable X-Y vectors """
while line != "":
    formatLine = line.split("{")
    formatLine2 = formatLine[1].replace(" ", "")
    coordinatesLine = formatLine2.split(",")

    X.append(float(coordinatesLine[0]))
    Y.append(float(coordinatesLine[1]))
    line = airfoilPointsFile.readline()
airfoilPointsFile.close()

""" Variables that characterize the different airfoil's divisions """
leadingEdgeLimitUp2 = 0.4
leadingEdgeLimitUp1 = 0.1
leadingEdgeLimitDown1 = 0.005
leadingEdgeLimitDown2 = 0.1

""" Initializers to perform the loop properly """
leadingEdgeDist = [1, 1, 1, 1, 1]
leIndex = [0, 0, 0, 0, 0]
jetPosDist = 1
jetPositionIndex = 0
points = 1

""" Loop in charge of defining the different airfoil sections """
meshFile.write("//=================================================================================\n")
meshFile.write("// Airfoil Points:\n")
meshFile.write("//=================================================================================\n")
while points < len(X):
    if leadingEdgeLimitUp2 < X[points - 1] < leadingEdgeDist[0]:
        leadingEdgeDist[0] = X[points - 1]
        leIndex[0] = points
    else:
        if leadingEdgeLimitUp1 < X[points - 1] < leadingEdgeDist[1]:
            leadingEdgeDist[1] = X[points - 1]
            leIndex[1] = points
        else:
            if jetPosition < X[points - 1] < jetPosDist and Y[points - 1] > 0:
                jetPosDist = X[points - 1]
                jetPositionIndex = points
            else:
                if X[points - 1] < leadingEdgeDist[2]:
                    leadingEdgeDist[2] = X[points - 1]
                    leIndex[2] = points
                else:
                    if leadingEdgeLimitDown1 < X[points - 1] < leadingEdgeDist[3]:
                        leadingEdgeDist[3] = X[points - 1]
                        leIndex[3] = points
                    else:
                        if leadingEdgeLimitDown2 < X[points - 1] < leadingEdgeDist[4]:
                            leadingEdgeDist[4] = X[points - 1]
                            leIndex[4] = points
    points = points + 1

""" Ordering the airfoil divisions breakpoints anti-clockwise """
airfoilBreakPoints = [leIndex[0], leIndex[1], leIndex[2], leIndex[3], leIndex[4], jetPositionIndex, jetPositionIndex
                      - slopeNodesSJA]
airfoilOrder = sorted(airfoilBreakPoints)

""" Loop in charge of rotating the airfoil profile's points AoA degrees and writing them into the mesh file """
points = 1
while points < len(X)+1:
    """ Rotation with respect to the leading edge"""
    xN = (X[points - 1] - 0.00006100) * m.cos(AoA) + (Y[points - 1] + 0.00039600) * m.sin(AoA)
    yN = -(X[points - 1] - 0.00006100) * m.sin(AoA) + (Y[points - 1] + 0.00039600) * m.cos(AoA)

    X[points - 1] = xN
    Y[points - 1] = yN

    """ Writing the rotated airfoil points into the mesh file """
    meshFile.write("Point(" + str(points) + ") = {" + str(X[points - 1]) + ", " + str(Y[points - 1]) + ", 0.0, 1};\n")
    points = points + 1

""" Writing the different airfoil divisions into the mesh file"""
meshFile.write("//=================================================================================\n")
meshFile.write("// Airfoil Contour Lines:\n")
meshFile.write("//=================================================================================\n")
meshFile.write("Spline(1) = {1:" + str(airfoilOrder[0]) + "};" + "\n")
meshFile.write("Spline(2) = {" + str(airfoilOrder[0]) + ":" + str(airfoilOrder[1]) + "};\n")
meshFile.write("Spline(3) = {" + str(airfoilOrder[1]) + ":" + str(airfoilOrder[2]) + "};\n")
meshFile.write("Spline(4) = {" + str(airfoilOrder[2]) + ":" + str(airfoilOrder[3]) + "};\n")
meshFile.write("Spline(5) = {" + str(airfoilOrder[3]) + ":" + str(airfoilOrder[4]) + "};\n")
meshFile.write("Spline(6) = {" + str(airfoilOrder[4]) + ":" + str(airfoilOrder[5]) + "};\n")
meshFile.write("Spline(7) = {" + str(airfoilOrder[5]) + ":" + str(airfoilOrder[6]) + "};\n")
meshFile.write("Spline(8) = {" + str(airfoilOrder[6]) + ":" + str(points - 2) + ", 1};\n")
meshFile.write("//=================================================================================\n")
# ----------------------------------------------------------------------------------------------------------------------
# Section in charge of creating the tangential jet points
# ----------------------------------------------------------------------------------------------------------------------
""" Creating the normal jet limiting point """
tangAng = m.atan2(Y[jetPositionIndex] - Y[jetPositionIndex - 2], X[jetPositionIndex] - X[jetPositionIndex - 2])
normAng = tangAng - m.pi / 2
meshFile.write("Point(" + str(points) + ") = {" + str(X[jetPositionIndex - 1] - jetHeight * m.cos(normAng)) + ", "
               + str(Y[jetPositionIndex - 1] - jetHeight * m.sin(normAng)) + ", 0.0, 1.0};\n")

""" Creating an auxiliary point that helps with the structured meshing """
tangAng = m.atan2(Y[jetPositionIndex - slopeNodesSJA] - Y[jetPositionIndex - 2 - slopeNodesSJA],
                  X[jetPositionIndex - slopeNodesSJA] - X[jetPositionIndex - 2 - slopeNodesSJA])
normAng = tangAng - m.pi / 2
meshFile.write("Point(" + str(points+1) + ") = {" + str(X[jetPositionIndex - 1 - slopeNodesSJA]
               + jetHeight * m.cos(normAng)) + ", " + str(Y[jetPositionIndex - 1 - slopeNodesSJA]
               + jetHeight * m.sin(normAng)) + ", 0.0, 1.0};\n")
points = points+2

""" Writing the different tangential jet sections"""
meshFile.write("Line(9) = {" + str(points-2) + ", " + str(jetPositionIndex) + "};\n")
meshFile.write("Line(10) = {" + str(points-2) + ", " + str(jetPositionIndex-slopeNodesSJA) + "};\n")
meshFile.write("Line(11) = {" + str(jetPositionIndex - slopeNodesSJA) + ", " + str(points-1) + "};\n")
meshFile.write("Line(12) = {" + str(points-1) + ", " + str(jetPositionIndex) + "};\n")
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# Section in charge of meshing the first region
# ----------------------------------------------------------------------------------------------------------------------
meshFile.write("//·················································································\n")
meshFile.write("//·················································································\n")
meshFile.write("//·················································································\n")
meshFile.write("//=================================================================================\n")
meshFile.write("// First Meshing Region Points:\n")
meshFile.write("//=================================================================================\n")

""" Initializers to perform the loop properly """
i = jetPositionIndex-slopeNodesSJA-2
c = 0
firstoffOrder = [1, 1]

""" Loop in charge of creating an auxiliary meshing region that helps to mesh the jet structured """
while i > 0:
    """ Creates a resembling airfoil's profile at a jetHeight distance from the airfoil's surface """
    tangAng = m.atan2(Y[i + 1] - Y[i - 1], X[i + 1] - X[i - 1])
    normAng = tangAng - m.pi / 2
    xOff = X[i] + jetHeight * m.cos(normAng)
    yOff = Y[i] + jetHeight * m.sin(normAng)

    """ Writes the surrounding auxiliary points """
    meshFile.write("Point(" + str(points) + ") = {" + str(xOff) + ", " + str(yOff) + ", 0.0, 1.0};\n")
    points = points + 1

    """ Conditions that help with the points indexing so that the loop can be performed correctly """
    if i == 1:
        meshFile.write("Point(" + str(points) + ") = {" + str(X[i-1] + jetHeight * m.cos(normAng)) + ", " +
                       str(Y[i-1] + jetHeight * m.sin(normAng)) + ", 0.0, 1.0};\n")
        points = points + 1
    if c < 2:
        if i == (airfoilOrder[1-c]):
            firstoffOrder[1-c] = points
            c = c + 1
    i = i - 1

""" Initializers to perform the loop properly """
offLim = len(X) - 1
i = 1
c = 0
offsetOrder = [1, 1, 1, 1, 1, 1, 1, 1, 1]

""" Loop in charge of creating the surrounding first meshing region resembling the airfoil's profile """
while i < offLim:
    """ Creates a resembling airfoil's profile at fmrDistance distance from the airfoil's surface """
    tangAng = m.atan2(Y[i + 1] - Y[i - 1], X[i + 1] - X[i - 1])
    normAng = tangAng - m.pi / 2
    xOff = X[i] + fmrDistance * m.cos(normAng)
    yOff = Y[i] + fmrDistance * m.sin(normAng)

    """ Condition that helps with the points indexing so that the loop can be performed correctly """
    if i == 1:
        meshFile.write("Point(" + str(points) + ") = {" + str(X[i - 1] + fmrDistance * m.cos(normAng)) + ", " +
                       str(Y[i - 1] + fmrDistance * m.sin(normAng)) + ", 0.0, 1.0};\n")
        points = points + 1

    """ Writes the surrounding first meshing region points """
    X.append(xOff)
    Y.append(yOff)
    meshFile.write("Point(" + str(points) + ") = {" + str(xOff) + ", " + str(yOff) + ", 0.0, 1.0};\n")
    points = points + 1

    """ Condition that helps with the points indexing so that the loop can be performed correctly """
    if c < 7:
        if i == (airfoilOrder[c]-2):
            offsetOrder[c] = points
            c = c + 1

    i = i + 1
# ----------------------------------------------------------------------------------------------------------------------
# Section in charge of creating a small trailing edge meshing region
# ----------------------------------------------------------------------------------------------------------------------
""" Variable that defines the horizontal length of the trailing edge meshing region """
trailingEdgeDistance = 1.05

""" Writing the different trailing edge meshing region sections"""
meshFile.write("Point(" + str(points) + ") = {" + str(X[i] + fmrDistance * m.cos(normAng)) + ", "
               + str(Y[i] + fmrDistance * m.sin(normAng)) + ", 0.0, 1.0};\n")
meshFile.write("Point(" + str(points+1) + ") = {" + str(trailingEdgeDistance * m.cos(AoA) + fmrDistance * m.sin(AoA))
               + ", " + str(fmrDistance * m.cos(AoA) - trailingEdgeDistance * m.sin(AoA)) + ", 0.0, 1.0};\n")
meshFile.write("Point(" + str(points+2) + ") = {" + str(trailingEdgeDistance * m.cos(AoA) + 5*jetHeight * m.sin(AoA))
               + ", " + str(5*jetHeight * m.cos(AoA) - trailingEdgeDistance * m.sin(AoA)) + ", 0.0, 1.0};\n")
meshFile.write("Point(" + str(points+3) + ") = {" + str(trailingEdgeDistance * m.cos(AoA)) + ", "
               + str(- trailingEdgeDistance * m.sin(AoA)) + ", 0.0, 1.0};\n")
meshFile.write("Point(" + str(points+4) + ") = {" + str(trailingEdgeDistance * m.cos(AoA) - fmrDistance * m.sin(AoA))
               + ", " + str(-fmrDistance * m.cos(AoA) - trailingEdgeDistance * m.sin(AoA)) + ", 0.0, 1.0};\n")
points = points+5

""" Writing the different first meshing region divisions into the mesh file"""
meshFile.write("//=================================================================================\n")
meshFile.write("// First Meshing Region Contour Lines:\n")
meshFile.write("//=================================================================================\n")

""" Auxiliary jet meshing region """
meshFile.write("Spline(13) = {" + str(points - offLim - 6) + ":" + str(firstoffOrder[0]) + "};\n")
meshFile.write("Spline(14) = {" + str(firstoffOrder[0]) + ":" + str(firstoffOrder[1]) + "};\n")
meshFile.write("Spline(15) = {" + str(firstoffOrder[1]) + ":" + str(points - jetPositionIndex
                                                                    + slopeNodesSJA - offLim - 5) + "};\n")

""" Surrounding first meshing region """
meshFile.write("Spline(16) = {" + str(points-offLim-5) + ":" + str(offsetOrder[0]) + "};\n")
meshFile.write("Spline(17) = {" + str(offsetOrder[0]) + ":" + str(offsetOrder[1]) + "};\n")
meshFile.write("Spline(18) = {" + str(offsetOrder[1]) + ":" + str(offsetOrder[2]) + "};\n")
meshFile.write("Spline(19) = {" + str(offsetOrder[2]) + ":" + str(offsetOrder[3]) + "};\n")
meshFile.write("Spline(20) = {" + str(offsetOrder[3]) + ":" + str(offsetOrder[4]) + "};\n")
meshFile.write("Spline(21) = {" + str(offsetOrder[4]) + ":" + str(offsetOrder[5]) + "};\n")
meshFile.write("Spline(22) = {" + str(offsetOrder[5]) + ":" + str(offsetOrder[6]) + "};\n")
meshFile.write("Spline(23) = {" + str(offsetOrder[6]) + ":" + str(points - 5) + "};\n")

""" Auxiliary jet meshing region """
meshFile.write("Line(24) = {1, " + str(points - offLim - 6) + "};\n")
meshFile.write("Line(25) = {" + str(airfoilOrder[0]) + ", " + str(firstoffOrder[0]) + "};\n")
meshFile.write("Line(26) = {" + str(airfoilOrder[1]) + ", " + str(firstoffOrder[1]) + "};\n")

""" Surrounding first meshing region """
meshFile.write("Line(27) = {" + str(points - offLim - 6) + ", " + str(points-offLim-5) + "};\n")
meshFile.write("Line(28) = {" + str(firstoffOrder[0]) + ", " + str(offsetOrder[0]) + "};\n")
meshFile.write("Line(29) = {" + str(firstoffOrder[1]) + ", " + str(offsetOrder[1]) + "};\n")
meshFile.write("Line(30) = {" + str(points - jetPositionIndex + slopeNodesSJA - offLim - 5) + ", "
               + str(offsetOrder[2]) + "};\n")
meshFile.write("Line(31) = {" + str(airfoilOrder[3]) + ", " + str(offsetOrder[3]) + "};\n")
meshFile.write("Line(32) = {" + str(airfoilOrder[4]) + ", " + str(offsetOrder[4]) + "};\n")
meshFile.write("Line(33) = {" + str(airfoilOrder[5]) + ", " + str(offsetOrder[5]) + "};\n")
meshFile.write("Line(34) = {" + str(airfoilOrder[6]) + ", " + str(offsetOrder[6]) + "};\n")
meshFile.write("Line(35) = {1, " + str(points - 5) + "};\n")

""" Trailing edge small meshing region """
meshFile.write("Line(36) = {" + str(points-offLim-5) + ", " + str(points-4) + "};\n")
meshFile.write("Line(37) = {" + str(points-offLim-6) + ", " + str(points - 3) + "};\n")
meshFile.write("Line(38) = {1, " + str(points-2) + "};\n")
meshFile.write("Line(39) = {" + str(points-5) + ", " + str(points-1) + "};\n")
meshFile.write("Line(40) = {" + str(points-3) + ", " + str(points-4) + "};\n")
meshFile.write("Line(41) = {" + str(points - 3) + ", " + str(points - 2) + "};\n")
meshFile.write("Line(42) = {" + str(points - 2) + ", " + str(points - 1) + "};\n")

# ----------------------------------------------------------------------------------------------------------------------
# Section in charge of writing the actual structured mesh commands
# ----------------------------------------------------------------------------------------------------------------------
meshFile.write("//=================================================================================\n")
meshFile.write("// First region mesh:\n")
meshFile.write("//=================================================================================\n")

""" Loop that allows saving code lines """
i = 0
while i < 2:
    meshFile.write("Curve Loop(" + str(i + 1) + ") = {" + str(24 + i) + "," + str(13 + i) + "," + str(
        -(25 + i)) + "," + str(-(1 + i)) + "};\n")
    meshFile.write("Plane Surface(" + str(i + 1) + ") = {" + str(i + 1) + "};\n")
    meshFile.write("Transfinite Surface {" + str(i + 1) + "};\n")
    meshFile.write("Transfinite Curve {" + str(24 + i) + "," + str(25 + i)
                   + "} = SJAYdiv Using Progression SJAYprog;\n")
    meshFile.write("Transfinite Curve {" + str(13 + i) + "," + str(1 + i) + "} = nSp" + str(i + 1)
                   + " Using Progression xProg" + str(i + 1) + ";\n")
    meshFile.write("Recombine Surface {" + str(i + 1) + "};\n")
    meshFile.write("Color meshColor {Surface{" + str(i + 1) + "}; }\n\n")
    i = i + 1

meshFile.write("Curve Loop(3) = {26,15,-11,-3};\n")
meshFile.write("Plane Surface(3) = {3};\n")
meshFile.write("Transfinite Surface {3};\n")
meshFile.write("Transfinite Curve {26,11} = SJAYdiv Using Progression SJAYprog;\n")
meshFile.write("Transfinite Curve {15,3} = nSp3 Using Progression xProg3;\n")
meshFile.write("Recombine Surface {3};\n")
meshFile.write("Color meshColor {Surface{3}; }\n\n")

meshFile.write("Curve Loop(4) = {-9,10,11,12};\n")
meshFile.write("Plane Surface(4) = {4};\n")
meshFile.write("Transfinite Surface {4};\n")
meshFile.write("Transfinite Curve {9,11} = SJAYdiv Using Progression SJAYprog;\n")
meshFile.write("Transfinite Curve {10,12} = nSp4 Using Progression xProg4;\n")
meshFile.write("Recombine Surface {4};\n")
meshFile.write("Color meshColor {Surface{4}; }\n\n")

""" Loop that allows saving code lines """
i = 0
while i < 3:
    meshFile.write("Curve Loop(" + str(i + 5) + ") = {" + str(27 + i) + "," + str(16 + i) + "," + str(
        -(28 + i)) + "," + str(-(13 + i)) + "};\n")
    meshFile.write("Plane Surface(" + str(i + 5) + ") = {" + str(i + 5) + "};\n")
    meshFile.write("Transfinite Surface {" + str(i + 5) + "};\n")
    meshFile.write("Transfinite Curve {" + str(27 + i) + "," + str(28 + i)
                   + "} = firstYdiv Using Progression firstYprog;\n")
    meshFile.write("Transfinite Curve {" + str(16 + i) + "," + str(13 + i)
                   + "} = nSp" + str(i+1) + " Using Progression xProg" + str(i+1) + ";\n")
    meshFile.write("Recombine Surface {" + str(i + 5) + "};\n")
    meshFile.write("Color meshColor {Surface{" + str(i + 5) + "}; }\n\n")
    i = i + 1

meshFile.write("Curve Loop(8) = {30,19,-31,-12};\n")
meshFile.write("Plane Surface(8) = {8};\n")
meshFile.write("Transfinite Surface {8};\n")
meshFile.write("Transfinite Curve {30,31} = firstYdiv Using Progression firstYprog;\n")
meshFile.write("Transfinite Curve {19,12} = nSp4 Using Progression xProg4;\n")
meshFile.write("Recombine Surface {8};\n")
meshFile.write("Color meshColor {Surface{8}; }\n\n")

""" Loop that allows saving code lines """
i = 0
while i < 4:
    meshFile.write("Curve Loop(" + str(i + 9) + ") = {" + str(31 + i) + "," + str(20 + i) + "," + str(
        -(32 + i)) + "," + str(-(5 + i)) + "};\n")
    meshFile.write("Plane Surface(" + str(i + 9) + ") = {" + str(i + 9) + "};\n")
    meshFile.write("Transfinite Surface {" + str(i + 9) + "};\n")
    meshFile.write(
        "Transfinite Curve {" + str(31 + i) + "," + str(32 + i) + "} = firstYdiv Using Progression firstYprog;\n")
    meshFile.write("Transfinite Curve {" + str(20 + i) + "," + str(5 + i) + "} = nSp" + str(
        i + 5) + " Using Progression xProg" + str(i + 5) + ";\n")
    meshFile.write("Recombine Surface {" + str(i + 9) + "};\n")
    meshFile.write("Color meshColor {Surface{" + str(i + 9) + "}; }\n\n")
    i = i + 1

meshFile.write("Curve Loop(13) = {40,37,-27,-36};\n")
meshFile.write("Plane Surface(13) = {13};\n")
meshFile.write("Transfinite Surface {13};\n")
meshFile.write("Transfinite Curve {27} = firstYdiv Using Progression firstYprog;\n")
meshFile.write("Transfinite Curve {40} = firstYdiv Using Progression firstYprog-0.07;\n")
meshFile.write("Transfinite Curve {37,36} = teXpoints Using Progression teXprog;\n")
meshFile.write("Recombine Surface {13};\n")
meshFile.write("Color meshColor {Surface{13}; }\n\n")

meshFile.write("Curve Loop(14) = {38,-41,-24,-37};\n")
meshFile.write("Plane Surface(14) = {14};\n")
meshFile.write("Transfinite Surface {14};\n")
meshFile.write("Transfinite Curve {41} = SJAYdiv Using Progression SJAYprog;\n")
meshFile.write("Transfinite Curve {24} = SJAYdiv Using Progression SJAYprog;\n")
meshFile.write("Transfinite Curve {38,37} = teXpoints Using Progression teXprog;\n")
meshFile.write("Recombine Surface {14};\n")
meshFile.write("Color meshColor {Surface{14}; }\n\n")

meshFile.write("Curve Loop(15) = {35,39,-42,-38};\n")
meshFile.write("Plane Surface(15) = {15};\n")
meshFile.write("Transfinite Surface {15};\n")
meshFile.write("Transfinite Curve {42} = firstYdiv Using Progression firstYprog-0.07;\n")
meshFile.write("Transfinite Curve {35} = firstYdiv Using Progression firstYprog;\n")
meshFile.write("Transfinite Curve {39,38} = teXpoints Using Progression teXprog;\n")
meshFile.write("Recombine Surface {15};\n")
meshFile.write("Color meshColor {Surface{15}; }\n\n")
meshFile.write("//=================================================================================\n")
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# Section in charge of meshing the limiting mesh region
# ----------------------------------------------------------------------------------------------------------------------
meshFile.write("//·················································································\n")
meshFile.write("//·················································································\n")
meshFile.write("//·················································································\n")
meshFile.write("//=================================================================================\n")
meshFile.write("// Limit Meshing Region Points:\n")
meshFile.write("//=================================================================================\n")

""" Writing the computational domain boundary points """
meshFile.write("Point(" + str(points) + ") = {" + str(outletDistance) + ", " + str(inletDistance) + ", 0.0, 1.0};\n")
meshFile.write("Point(" + str(points + 1) + ") = {0.0, " + str(inletDistance) + ", 0.0, 1.0};\n")
meshFile.write("Point(" + str(points + 2) + ") = {" + str(-inletDistance) + ", 0.0, 0.0, 1.0};\n")
meshFile.write("Point(" + str(points + 3) + ") = {0.0, " + str(-inletDistance) + ", 0.0, 1.0};\n")
meshFile.write("Point(" + str(points + 4) + ") = {" + str(outletDistance) + ", " +
               str(-inletDistance) + ", 0.0, 1.0};\n")
# ----------------------------------------------------------------------------------------------------------------------
# Section in charge of developing a special trailing edge region that helps solve meshing issues
# ----------------------------------------------------------------------------------------------------------------------
""" Variables that characterize some auxiliary parameters for this auxiliary meshing region """
teh1 = 30
teh2 = 10
teb1 = 0.25
teb2 = 5

""" Writing the auxiliary trailing edge meshing region points """
meshFile.write("Point(" + str(points+5) + ") = {" + str(
    -trailingEdgeDistance * teb1 * m.cos(AoA) + fmrDistance * teh1 * m.sin(AoA)) + ", " + str(
    fmrDistance * teh1 * m.cos(AoA) + trailingEdgeDistance * teb1 * m.sin(AoA)) + ", 0.0, densOut};\n")
meshFile.write("Point(" + str(points + 6) + ") = {" + str(
    -trailingEdgeDistance * teb1 * m.cos(AoA) - fmrDistance * teh1 * m.sin(AoA)) + ", " + str(
    -fmrDistance * teh1 * m.cos(AoA) + trailingEdgeDistance * teb1 * m.sin(AoA)) + ", 0.0, densOut};\n")
meshFile.write("Point(" + str(points + 7) + ") = {" + str(
    trailingEdgeDistance * teb2 * m.cos(AoA) + fmrDistance * teh2 * m.sin(AoA)) + ", " + str(
    fmrDistance * teh1 * m.cos(AoA) + trailingEdgeDistance * teb1 * m.sin(AoA)) + ", 0.0, densOut};\n")
meshFile.write("Point(" + str(points + 8) + ") = {" + str(
    trailingEdgeDistance * teb2 * m.cos(AoA) - fmrDistance * teh2 * m.sin(AoA)) + ", " + str(
    -fmrDistance * teh2 * m.cos(AoA) - trailingEdgeDistance * teb2 * m.sin(AoA)) + ", 0.0, densOut};\n")
points = points + 9
# ----------------------------------------------------------------------------------------------------------------------
# Section in charge of writing the computational domain boundaries into the mesh file
# ----------------------------------------------------------------------------------------------------------------------
meshFile.write("//=================================================================================\n")
meshFile.write("// Limit Meshing Region Contour Lines:\n")
meshFile.write("//=================================================================================\n")

""" Computational domain boundaries """
meshFile.write("Line(43) = {" + str(points - 9) + ", " + str(points - 8) + "};\n")
meshFile.write("Circle(44) = {" + str(points - 8) + ", 484, " + str(points - 7) + "};\n")
meshFile.write("Circle(45) = {" + str(points - 7) + ", 484, " + str(points - 6) + "};\n")
meshFile.write("Line(46) = {" + str(points - 6) + ", " + str(points - 5) + "};\n")
meshFile.write("Line(47) = {" + str(points - 5) + ", " + str(points - 9) + "};\n")
meshFile.write("Spline(48) = {" + str(points - 3) + "," + str(points - 4) + "," + str(points - 2) + "," + str(
    points - 1) + "," + str(points - 3) + "};" + "\n")
# ----------------------------------------------------------------------------------------------------------------------
# Section in charge of writing the meshing commands for the computational domain boundaries into the mesh file
# ----------------------------------------------------------------------------------------------------------------------
meshFile.write("//=================================================================================\n")
meshFile.write("// Limit region mesh:\n")
meshFile.write("//=================================================================================\n")

""" First meshing region  """
meshFile.write("Curve Loop(16) = {-41, 40, -36, 16, 17, 18, 19, 20, 21, 22, 23, 39, -42};\n")
meshFile.write("Curve Loop(17) = {48};\n")
meshFile.write("Plane Surface(16) = {16,17};\n")
meshFile.write("Color meshColor {Surface{16}; }\n\n")

""" Computational domain boundary region  """
meshFile.write("Curve Loop(18) = {43, 44, 45, 46, 47};\n")
meshFile.write("Curve Loop(19) = {48};\n")
meshFile.write("Plane Surface(17) = {18,19};\n")
meshFile.write("Color meshColor {Surface{17}; }\n\n")
meshFile.write("//=================================================================================\n")
# ----------------------------------------------------------------------------------------------------------------------
# Section in charge of writing the different patches where boundary conditions are applied
# ----------------------------------------------------------------------------------------------------------------------
meshFile.write("//·················································································\n")
meshFile.write("//·················································································\n")
meshFile.write("//·················································································\n")
meshFile.write("//=================================================================================\n")
meshFile.write("// CFD boundary regions definitions:\n")
meshFile.write("//=================================================================================\n")

""" Extruding the 2D mesh one cell depth, it is related with OpenFOAM being FVM """
meshFile.write("Extrude {0, 0, -0.1} {\n")

""" Extruding all the surfaces that construct the 2D mesh """
i = 1
while i < 18:
    meshFile.write("   Surface{" + str(i) + "};\n")
    i = i + 1
meshFile.write("   Layers {1};\n")
meshFile.write("   Recombine;\n")
meshFile.write("}\n\n")

""" Writing the different patches definitions into the mesh file """
meshFile.write("Physical Surface('inlet') = {469, 465};\n")
meshFile.write("Physical Surface('outlet') = {477};\n")
meshFile.write("Physical Surface('up') = {461};\n")
meshFile.write("Physical Surface('down') = {473};\n")
meshFile.write("Physical Surface('front') = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17};\n")
meshFile.write("Physical Surface('back') = {482, 450, 378, 312, 290, 268, 246, 224, 136, 202, 114, 92, 180, 70, 158, "
               "356, 334};\n")
meshFile.write("Physical Surface('wallUp') = {69, 91, 113, 127, 245};\n")
meshFile.write("Physical Surface('jet') = {123};\n")
meshFile.write("Physical Surface('wallDown') = {289, 311, 267};\n")
meshFile.write("Physical Volume('fluid') = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17};\n")
meshFile.write("//=================================================================================\n")
meshFile.close()
# ----------------------------------------------------------------------------------------------------------------------
