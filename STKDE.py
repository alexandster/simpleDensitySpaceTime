import math, os

# Kernel parameters
hs = 25     # spatial bandwidth in meters
ht = 15     # temporal bandwidth in days

hs2 = pow(int(hs), 2)   #videogame-trick

# regular grid resolution
xRes = 10       # x resolution
yRes = 10       # y resolution 
tRes = 10       # t resolution 

# Read coordinates of points
fData = open("pointFiles" + os.sep + "data.txt", "r")
xytList = []
for line in fData:
    x = float(line.split(",")[0])      	# x-coordinate variable
    y = float(line.split(",")[1])      	# y-coordinate variable
    t = float(line.split(",")[2])      	# z-coordinate variable
    xytList.append([x,y,t])
fData.close()

# Read domain boundaries
fBound = open("boundaryFiles" + os.sep + "data_bds.txt", "rU")              	
inBound = fBound.read()
inBoundList = inBound.split(",")             
fBound.close()

# Create output file  
outFile = open("stkdeFiles" + os.sep + "stkde_data.txt" , "w")       

xmin = int(inBoundList[0])
xmax = int(inBoundList[1])
ymin = int(inBoundList[2])
ymax = int(inBoundList[3])
tmin = int(inBoundList[4])
tmax = int(inBoundList[5])

# number of point events
n = len(xytList)

#constants
const1 = 0.5 * math.pi
const2 = pow(10.0, 10) / (n * pow(hs, 2) * ht)

# loop through all regular grid points within domain
for xC in range(xmin, xmax, xRes):            # for all possible x-coordinates that are within domain (determined by xy resolution) 
    for yC in range(ymin, ymax, yRes):            # for all possible y-coordinates that are within the subdomain (determined by xy resolution)
        for tC in range(tmin, tmax, tRes):            # for all possible t-coordinates that are within the subdomain (determined by t resolution)
            
            density = 0.0           # set initial density to 0
            
            for xyt in xytList:              # for all points

                xCoord = xyt[0]
                yCoord = xyt[1]
                tCoord = xyt[2]
                
                if hs2 >= pow(xCoord - xC, 2) + pow(yCoord - yC, 2):    # if within spatial bandwidth
                    
                    if ht >= abs(tCoord - tC):          # if within temporal bandwidth

                        u = (xCoord-xC) / hs
                        v = (yCoord-yC) / hs
                        w = (tCoord-tC) / ht

                        #epanechnikov kernel space-time
                        Ks = const1 * (1 - pow(u, 2) - pow(v, 2))
                        Kt = 0.75 * (1 - pow(w, 2))
                        
                        density += const2 * Ks * Kt
                        
            outFile.write(str(xC) + "," + str(yC) + "," + str(tC) + "," + str(density) +"\n")
        
outFile.close()



    

        
        
