import numpy as np
import matplotlib.pyplot as plt
import os
import glob
import sys

def processfiles(fileslist):
    numpts = len(fileslist)
    drc1= np.zeros((numpts,3))
    drc3= np.zeros((numpts,3))
    drc1arm= np.zeros((numpts,3))
    drc3arm= np.zeros((numpts,3))
    wood1= np.zeros((numpts,3))
    wood2= np.zeros((numpts,3))
    drcslope = np.zeros((numpts,1))
    armslope = np.zeros((numpts,1))
    woodslope = np.zeros((numpts,1))


    lookup = {"drc1 is":drc1,
              "drc3 is":drc3,
              "drc1 arm is":drc1arm,
              "drc3 arm is":drc3arm,
              "woodmount1 is":wood1,
              "woodmount2 is":wood2,
             }
    for i in range(0,numpts):
        filename = fileslist[i]
        f = file(filename,'r')
        for line in f:
            a = line.rstrip()
            b = a.split(":")
            c = [float(x) for x in b[1].split(',')]
            dataarray = lookup[b[0]]
            dataarray[i,:] = c
        drcslope[i] = np.float64(drc1[i,0] - drc3[i,0])/ np.float64(drc1[i,1] - drc3[i,1]) 
        armslope[i] = np.float64(drc1arm[i,0] - drc3arm[i,0])/ np.float64(drc1arm[i,1] - drc3arm[i,1]) 
        woodslope[i] = np.float64(wood1[i,0] - wood2[i,0])/ np.float64(wood1[i,1] - wood2[i,1]) 

    return [drc1,drc3,drc1arm,drc3arm,wood1,wood2,drcslope,armslope,woodslope]

def plotdata(data):
    [drc1,drc3,drc1arm,drc3arm,wood1,wood2,drcslope,armslope,woodslope] = data
    plt.figure(1)
    plt.subplot(311)
    for i in range(0,drc1.shape[0]):
        plt.plot([drc1[i,1],    drc3[i,1]],         [drc1[i,0],     drc3[i,0]],     'g-')
        plt.plot([drc1arm[i,1], drc3arm[i,1]],   [drc1arm[i,0],  drc3arm[i,0]],  'b-')
        plt.plot([wood1[i,1],   wood2[i,1]],       [wood1[i,0],    wood2[i,0]],    'k-')
    plt.subplot(312)    
    plt.plot(drcslope,'go')
    plt.plot(armslope,'bo')
    plt.plot(woodslope,'ko')
    plt.subplot(313)
    plt.boxplot([drcslope,armslope,woodslope])
  
    plt.show()


def main():
    files = glob.glob('run*.txt')
    data = processfiles(files)
    plotdata(data)
    #print data


if __name__ == "__main__":
    sys.exit(int(main() or 0))