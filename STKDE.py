import math, os, sys, glob
import numpy as np

# Kernel parameters
hs = 25     # spatial bandwidth in meters
ht = 15     # temporal bandwidth in days

hs2 = pow(int(hs), 2)

# regular grid resolution
xRes = 10        # x resolution in meters
yRes = 10        # y resolution in meters
tRes = 10         # t resolution in days

# Read coordinates of point events 
fData = open("pointFiles" + os.sep + "data.txt", "r")

xytList = []
for line in fData:

    x = float(line.split(",")[0])      	# x-coordinate variable
    y = float(line.split(",")[1])      	# y-coordinate variable
    t = float(line.split(",")[2])      	# z-coordinate variable

    xytList.append([x,y,t])
    
fData.close()

# Read subdomain boundaries
fBound = open("boundaryFiles" + os.sep + "data_bds.txt", "rU")              	
inBound = fBound.read()
inBoundList = inBound.split(",")             
fBound.close()

# Create output file  
outFile = open("stkdeFiles" + os.sep + "stkde_data.txt" , "w")       

# number of point events
n = len(xytList)

xmin = int(inBoundList[0])
xmax = int(inBoundList[1])
ymin = int(inBoundList[2])
ymax = int(inBoundList[3])
tmin = int(inBoundList[4])
tmax = int(inBoundList[5])

#constants
const1 = 0.5 * math.pi
const2 = pow(10.0, 10) / (n * pow(hs, 2) * ht)

# loop through all grid points within subdomain
for xC in range(xmin, xmax, xRes):            # for all possible x-coordinates that are within the subdomain (according to xy resolution) 
    for yC in range(ymin, ymax, yRes):            # for all possible y-coordinates that are within the subdomain (according to xy resolution)
        for tC in range(tmin, tmax, tRes):            # for all possible t-coordinates that are within the subdomain (according to t resolution)
            
            density = 0.0           # set initial density to 0
            
            for xyt in xytList:              # for all point events

                xCoord = xyt[0]
                yCoord = xyt[1]
                tCoord = xyt[2]
                
                if hs2 >= pow(xCoord - xC, 2) + pow(yCoord - yC, 2):    # if within spatial bandwidth
                    
                    if ht >= abs(tCoord - tC):          # if within temporal bandwidth

                        u = (xCoord-xC) / hs
                        v = (yCoord-yC) / hs
                        w = (tCoord-tC) / ht

                        Ks = const1 * (1 - pow(u, 2) - pow(v, 2))
                        Kt = 0.75 * (1 - pow(w, 2))
                        
                        density += const2 * Ks * Kt
                        
            outFile.write(str(xC) + "," + str(yC) + "," + str(tC) + "," + str(density) +"\n")
        
outFile.close()



    

        
        
