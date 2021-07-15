import json
import numpy
import matplotlib.pyplot as plt

pTEff = []
pTCuts = []
df = open("SleptonCalc400_1ns.json")
data = json.load(df)
nLxyCuts = data["LxyCuts400_1ns"]

def getEff(dist, i , mass, lifetime):
    jsonfile = open("SleptonCalc{}_{}.json".format(mass, lifetime))
    data = json.load(jsonfile)
    Cuts = data["{}Cuts{}_{}".format(dist,mass, lifetime)]
    Effs = data["{}Eff{}_{}".format(dist,mass, lifetime)]
        
    return Cuts[i], Effs[i]

def getStauOk(dist, i, mass, lifetime):
    jsonfile = open("SleptonCalc{}_{}.json".format(mass, lifetime))
    data = json.load(jsonfile)
    SOL = data["{}SOL{}_{}".format(dist,mass, lifetime)]
    Cuts = data["{}Cuts{}_{}".format(dist,mass, lifetime)]

    return SOL[i], Cuts[i]

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
        cutVal,Eff = getEff(dist, i, mass, lifetime) #Calls the values from getEff function
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

def complt(dist, lifetimes, mass):
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

def SOLmass(dist, i, masses, lifetime, filename):
    SOLi_vs_mass = []
    Cuti_vs_mass = []
    
    for mass in masses:
        SOL, cutVal = getStauOk(dist, i, mass, lifetime) #Calls both values from getStauOk function
        SOLi_vs_mass.append(SOL)
        Cuti_vs_mass.append(cutVal)

    print(SOLi_vs_mass)
    print(Cuti_vs_mass)
    lab = "Stau that passed"  + str(Cuti_vs_mass)+ "mm"
    fig = plt.figure()
    plt.style.use('fivethirtyeight')
    plt.ylim(0,100)
    plt.errorbar(masses, SOLi_vs_mass, label = lab )
    plt.legend(loc = "upper right")
    plt.xlabel("Masses")
    plt.ylabel("# of Stau")
    plt.tight_layout()
    plt.savefig(filename)
    return masses, SOLi_vs_mass

def compSOL(dist, masses, lifetime):
    nCuts = nLxyCuts #Should be 600, 800, 1000, 1200

    fig = plt.figure()
    for i in nCuts:
        print(i)
        masses, SOLi_vs_mass, label = SOLmass(dist, i, masses, lifetime, "LxySOL{}Cut.png".format(i))
        plt.figure(1)
        plt.errorbar(masses, SOLi_vs_mass, label = label)

    plt.legend(loc = "upper left")
    plt.xlabel("Masses")
    plt.ylabel("# of Stau")
    plt.tight_layout()
    plt.savefig("LxySOL_All.png")
    plt.clf()

#complt(Lxy, [
compSOL("Lxy",[100,300,400,600],"1ns")
