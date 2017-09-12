import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
import glob
import sys
import math


def slopes(a,b,i):
    return  np.rad2deg(np.arctan(   np.float64(a[i,0] - b[i,0]) / np.float64(a[i,1] - b[i,1])))

def td(a,adjust = 0):
    n = a.shape[0]
    d = np.zeros((n,1))
    for i in range(0,n):
        d[i] = math.sqrt(a[i,0]*a[i,0] + a[i,1]*a[i,1])+adjust
    return d

def l(a,b):
    n = a.shape[0]
    d = np.zeros((n,1))
    for i in range(0,n):
        d[i] = math.sqrt( (a[i,0]-b[i,0])**2 + (a[i,1]-b[i,1])**2)
    return d

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



        drcslope[i] = slopes(drc1,drc3,i)
        armslope[i] = slopes(drc1arm,drc3arm,i)
        woodslope[i] = slopes(wood1,wood2,i)

    print " mean wood: ", np.mean(woodslope)
    print " mean gripper: ", np.mean(armslope)
    print " std wood: ", np.std(woodslope,ddof=1)
    print " std gripper: ", np.std(armslope,ddof=1)
    print "Wood: \n", wood1
    d = td(wood1,0.130175)
    print "mean d:\n", np.mean(d)
    print "std d:\n", np.std(d,ddof=1)
    print d
    print "L:\n",l(wood1,wood2)
#    print "std d: ", np.std(d,ddof=1)
    return [drc1,drc3,drc1arm,drc3arm,wood1,wood2,drcslope,armslope,woodslope]

def plotdata(data):
    [drc1,drc3,drc1arm,drc3arm,wood1,wood2,drcslope,armslope,woodslope] = data
    fig, axes = plt.subplots(nrows=1, ncols=1) #, figsize=(8, 8) )
    #fig.tight_layout()
    #fig.subplots_adjust(wspace = 2.5)
    #axes.set_title('Positions')
    #axes.set_xlabel('X (m)')
    #axes.set_ylabel('Y (m)')
    
    #w = 0.25
    #h = 0.15
    #c = axes.add_patch(
    # patches.Rectangle(  (-w/2, -h/2+.05), w, h,        hatch='\\',
    #    fill=False
    #)
    #)
    #for i in range(0,drc1.shape[0]):
    #    b, = axes.plot([drc1[i,1],    drc3[i,1]],         [drc1[i,0],     drc3[i,0]],     'g-', label = "Bases")
    #    g, = axes.plot([drc1arm[i,1], drc3arm[i,1]],   [drc1arm[i,0],  drc3arm[i,0]],  'b-',label = 'Grippers')
    #    l, = axes.plot([wood1[i,1],   wood2[i,1]],       [wood1[i,0],    wood2[i,0]],    'k-',label = 'Lumber')
    
    #plt.legend([b,g,l,c],["Body","Grippers",'Lumber','saw'],loc=3)
    #plt.show()
    #plt.plot(drcslope,'go')
    #plt.plot(armslope,'bo')
    #plt.plot(woodslope,'ko')
    #plt.subplot(313)
    
    #axes.set_title('Alignment Angle')
    axes.set_ylabel('Angle (degrees)')
    axes.boxplot([drcslope,armslope,woodslope], labels = ["Body","Grippers",'Lumber'])
  
    plt.show()


def main():
    files = glob.glob('run*.txt')
    files.remove('run1.txt')
    files.remove('run2.txt')
    files.remove('run3.txt')
    #files.remove('run5.txt')
    print files
    #files.remove('run10.txt')
    data = processfiles(files)
    plotdata(data)
    #print data


if __name__ == "__main__":
    sys.exit(int(main() or 0))