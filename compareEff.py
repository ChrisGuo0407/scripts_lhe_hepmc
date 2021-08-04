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
    Errors = data["{}Errors{}_{}".format(dist, mass, lifetime)]
    Cuts = data["{}Cuts{}_{}".format(dist,mass, lifetime)]
    Effs = data["{}Efficiencies{}_{}".format(dist,mass, lifetime)]
        
    return Cuts[i], Effs[i], Errors[i]

def getStauOk(dist, i, mass, lifetime):
    jsonfile = open("SleptonCalc{}_{}.json".format(mass, lifetime))
    data = json.load(jsonfile)
    SOL = data["{}SOL{}_{}".format(dist,mass, lifetime)]
    Cuts = data["{}Cuts{}_{}".format(dist,mass, lifetime)]

    return SOL[i], Cuts[i]

def getEventOk(dist, i, mass, lifetime):
    jsonfile = open("SleptonCalc{}_{}.json".format(mass, lifetime))
    data = json.load(jsonfile)
    Eol = data["nEvent{}SOL{}_{}".format(dist,mass, lifetime)]
    Cuts = data["{}Cuts{}_{}".format(dist,mass, lifetime)]

    return Eol[i], Cuts[i]

def mass(dist, masses, lifetime):
       
    Effi_versus_mass = []
    Cuti_versus_mass = []
    errorbars = []

    for mass in masses:
        cutVal,Eff,errors = getEff(dist, i, mass, lifetime) #Calls the values from getEff function
        Effi_versus_mass.append(Eff)
        Cuti_versus_mass.append(cutVal)
        errorbars.append(errors)
 
    #print(Effi_versus_lt)
    #print(Cuti_versus_lt)
    #cutVal = Cuti_versus_lt[0]#Never change this value!
    plt.title("Efficiency Over Multiple Masses")
    lab = dist + " > "  + str(cutVal)+ "mm"
    fig = plt.figure()
    plt.style.use('fivethirtyeight')
    plt.ylim(0,1.4)
    plt.errorbar(masses, Effi_versus_mass, yerr = errorbars, label = lab, marker = "o", alpha = 0.5)
    plt.legend(loc = "upper right", fontsize = 'small', frameon = False)
    plt.xlabel("masses")
    plt.ylabel("Efficiency")
    plt.tight_layout()
    plt.savefig(filename)
    #plt.clf()

    return masses, Effi_versus_mass, lab, errorbars


def compmass(dist, masses,lifetime):
    nCuts = nLxyCuts 

    fig = plt.figure()
    for cut in range(0,len(nCuts)):
        masses, effs, label, errorbars = mass(dist, cut, masses, lifetime, "{}MassCuts{}Gev{}.png".format(dist,mass,cut))
        plt.figure(1)
        plt.errorbar(masses, effs, label = label, yerr = errorbars)
    plt.title("Efficiency Over Multiple Masses")
    plt.legend(loc = "upper right", fontsize = 'small', frameon = False)
    plt.ylim(0,1.4)
    plt.xlabel("Masses")
    plt.ylabel("Efficiency")
    plt.tight_layout()
    plt.savefig("{}LTCuts{}GeV_All.png".format(dist,mass))
    plt.clf()

def lt(dist, i, lifetimes, mass, filename):
    
    Effi_versus_lt = []
    Cuti_versus_lt = []
    errorbars = []

    for lifetime in lifetimes:
        cutVal,Eff,errors = getEff(dist, i, mass, lifetime) #Calls the values from getEff function
        Effi_versus_lt.append(Eff)
        Cuti_versus_lt.append(cutVal)
        errorbars.append(errors)
 
    #print(Effi_versus_lt)
    #print(Cuti_versus_lt)
    #cutVal = Cuti_versus_lt[0]#Never change this value!
    plt.title("Efficiency Over Multiple Lifetimes")
    lab = dist + " > "  + str(cutVal)+ "mm"
    fig = plt.figure()
    plt.style.use('fivethirtyeight')
    plt.ylim(0,1.4)
    plt.errorbar(lifetimes, Effi_versus_lt, yerr = errorbars, label = lab, marker = "o", alpha = 0.5)
    plt.legend(loc = "upper right", fontsize = 'small', frameon = False)
    plt.xlabel("Lifetimes")
    plt.ylabel("Efficiency")
    plt.tight_layout()
    plt.savefig(filename)
    #plt.clf()

    return lifetimes, Effi_versus_lt, lab, errorbars

def complt(dist, lifetimes, mass):
    nCuts = nLxyCuts 

    fig = plt.figure()
    for cut in range(0,len(nCuts)):
        lifetimes, effs, label, errorbars = lt(dist, cut, lifetimes, mass, "{}LTCuts{}Gev{}.png".format(dist,mass,cut))
        plt.figure(1)
        plt.errorbar(lifetimes, effs, label = label, yerr = errorbars)
    plt.title("Efficiency Over Multiple Lifetimes")
    plt.legend(loc = "upper right", fontsize = 'small', frameon = False)
    plt.ylim(0,1.4)
    plt.xlabel("Lifetimes")
    plt.ylabel("Efficiency")
    plt.tight_layout()
    plt.savefig("{}LTCuts{}GeV_All.png".format(dist,mass))
    plt.clf()

def SOLmass(dist, i, masses, lifetime, filename):
    SOLi_vs_mass = []
    Cuti_vs_mass = []
    
    for mass in masses:
        SOL, cutVal = getStauOk(dist, i, mass, lifetime) #Calls both values from getStauOk function
        SOLi_vs_mass.append(SOL)
        Cuti_vs_mass.append(cutVal)

    #print(SOLi_vs_mass)
    #print(cutVal)
    lab = "Staus past"  + str(cutVal)+ "mm"
    fig = plt.figure()
    plt.style.use('fivethirtyeight')
    plt.ylim(0,100)
    plt.errorbar(masses, SOLi_vs_mass, label = lab )
    plt.legend(loc = "upper right")
    plt.xlabel("Masses")
    plt.ylabel("# of Stau")
    plt.tight_layout()
    plt.savefig(filename)
    return masses, SOLi_vs_mass, lab

def compSOL(dist, masses, lifetime):
    nCuts = nLxyCuts #Should be 600, 800, 1000, 1200

    fig = plt.figure()
    for cut in range(0,len(nCuts)):
        masses, SOLi_vs_mass, label = SOLmass(dist, cut, masses, lifetime, "LxySOL{}Cut.png".format(cut))
        plt.figure(1)
        plt.errorbar(masses, SOLi_vs_mass, label = label)

    plt.legend(loc = "upper right")
    plt.xlabel("Masses")
    plt.ylabel("# of Stau")
    plt.tight_layout()
    plt.savefig("LxySOL_All.png")
    plt.clf()

def Eol(dist, i, masses, lifetime, filename):
    Eol_vs_mass = []
    Cuti_vs_mass = []
    
    for mass in masses:
        Eol, cutVal = getEventOk(dist, i, mass, lifetime) #Calls both values from getEventOk function
        Eol_vs_mass.append(Eol)
        Cuti_vs_mass.append(cutVal)

    #print(Eol_vs_mass)
    #print(cutVal)
    lab = str(cutVal)+ "mm"
    fig = plt.figure()
    plt.style.use('fivethirtyeight')
    plt.ylim(0,100)
    plt.errorbar(masses, Eol_vs_mass, label = lab )
    plt.legend(loc = "upper right")
    plt.xlabel("Masses")
    plt.ylabel("# Events per Cut")
    plt.tight_layout()
    plt.savefig(filename)
    return masses, Eol_vs_mass, lab

def compEol(dist, masses, lifetime):
    nCuts = nLxyCuts #Should be 600, 800, 1000, 1200

    fig = plt.figure()
    for cut in range(0,len(nCuts)):
        masses, Eol_vs_mass, label = Eol(dist, cut, masses, lifetime, "{}Eol{}Cut.png".format(dist,cut))
        plt.figure(1)
        plt.errorbar(masses, Eol_vs_mass, label = label)

    plt.legend(loc = "upper right")
    plt.xlabel("Masses")
    plt.ylabel("# Events per Cut")
    plt.tight_layout()
    plt.savefig("{}Eol_All.png".format(dist))
    plt.clf()


complt("Lxy", ["0p001ns","0p01ns","0p1ns","1ns","10ns"], "300")
complt("pT", ["100","300","400","600"], "1ns")
compSOL("Lxy",[100,300,400,600],"1ns")
compEol("Lxy",[100,300,400,600],"1ns")
