import json
import numpy
import matplotlib.pyplot as plt

pTEff = []
pTCuts = []
df = open("SleptonCalc400_1ns.json")
nLxyCuts = df("LxyCuts400_1ns")

def getEff(dist, i , mass, lifetime):
    jsonfile = open("SleptonCalc{}_{}.json".format(mass, lifetime))
    data = json.load(jsonfile)
    Cuts = data["{}Cuts{}_{}".format(dist,mass, lifetime)]
    Effs = data["{}Eff{}_{}".format(dist,mass, lifetime)]
        
    return Cuts[i], Effs[i]

def compmass ():
    i = 0
    lifetime = "1ns"
    masses = [100,400,600]
    LxyEffi_versus_mass = []
    LxyCuti_versus_mass = []

    for mass in masses: 
        jsonfile = open("SleptonCalc{}_{}.json".format(mass, lifetime))
        data = json.load(jsonfile)
        LxyCuts = data["LxyCuts{}_{}".format(mass, lifetime)]
        LxyEffs = data["LxyEff{}_{}".format(mass, lifetime)]
        print("Eff ", LxyEffs)
        LxyEffi_versus_mass.append( LxyEffs[i] )
        print("Eff i ", LxyEffs[i])
        LxyCuti_versus_mass.append(LxyCuts[i])

   # print(LxyEffi_versus_mass)
   # print(LxyCuti_versus_mass)
    
    plt.style.use('fivethirtyeight')
    plt.ylim(0,100)
    plt.errorbar(masses, LxyEffi_versus_mass, label = "Lxy > {} mm".format( LxyCuti_versus_mass[0]))
    plt.legend(loc = "upper right")
    plt.xlabel("GeV")
    plt.ylabel("Efficiency %")
    plt.tight_layout()
    plt.savefig("LxyCut1200mm.png")
    plt.clf()
    
    #pTEff = data["pTEff400_1ns"]



def lt(dist, i, lifetimes, mass, filename):
    
    Effi_versus_lt = []
    Cuti_versus_lt = []

    for lifetime in lifetimes:
        cutVal,Eff = getEff(dist, i, mass, lifetime)
        Effi_versus_lt.append(Eff)
        Cuti_versus_lt.append(cutVal)
 
    print(Effi_versus_lt)
    print(Cuti_versus_lt)
    #cutVal = Cuti_versus_lt[0]#Never change this value!
    lab = dist + " > "  + str(cutVal)+ "mm"
    fig = plt.figure()
    plt.style.use('fivethirtyeight')
    plt.ylim(0,100)
    plt.errorbar(lifetimes, Effi_versus_lt, label = lab )
    plt.legend(loc = "upper right")
    plt.xlabel("Lifetimes")
    plt.ylabel("Efficiency %")
    plt.tight_layout()
    plt.savefig(filename)
    #plt.clf()

    return lifetimes, Effi_versus_lt, lab

def complt(dist, lifetimes, mass)
    nCuts = nLxyCuts 

    fig = plt.figure()
    for cut in range (0, nCuts):
        lifetimes, effs, label = lt(dist, cut, lifetimes, mass, "LxyLTCuts300Gev{}.png".format(cut))
        plt.figure(1)
        plt.errorbar(lifetimes, effs, label = label)

    plt.legend(loc = "upper left")
    plt.xlabel("Lifetimes")
    plt.ylabel("Efficiency %")
    plt.tight_layout()
    plt.savefig("LxyLTCuts300GeV_All.png")
    plt.clf()

