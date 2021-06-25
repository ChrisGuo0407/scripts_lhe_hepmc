import json
import pyhepmc_ng as hep
import matplotlib.pyplot as plt
import numpy
import argparse

parser = argparse.ArgumentParser(description='Runs configuration for Slepton files')
parser.add_argument('--mass1', type=str, default = '400', help = 'Default mass for Slepton ')
parser.add_argument('--lifetime1', type=str, default = '1ns', help = 'Default lifetime for Slepton')
parser.add_argument('--mass2', type=str, default = '400', help = 'Default mass for Slepton ')
parser.add_argument('--lifetime2', type=str, default = '1ns', help = 'Default lifetime for Slepton')

parser.add_argument('dotest', type=bool, default = False, help = 'Set to false so no test is run, change to True to run test')

args = parser.parse_args()

f1 = open('SleptonCalc{}_{}.json'.format(args.mass1, args.lifetime1))
data1 = json.load(f1)

f2 = open('SleptonCalc{}_{}.json'.format(args.mass2, args.lifetime2))
data2 = json.load(f2)

#fnames = ['LxyPlot{}_{}.png'.format(args.mass1, args.lifetime1),'LxyPlot{}_{}.png'.format(args.mass2, args.lifetime2),
 #'etaPlot{}_{}.png'.format(args.mass1, args.lifetime1),'etaPlot{}_{}.png'.format(args.mass2, args.lifetime2), 
 #'phiPlot{}_{}.png'.format(args.mass1, args.lifetime1),'phiPlot{}_{}.png'.format(args.mass2, args.lifetime2),
 #'pTPlot{}_{}.png'.format(args.mass1, args.lifetime1),'pTPlot{}_{}.png'.format(args.mass2, args.lifetime2)]


Lxy1 = data1["Lxy{}_{}".format(args.mass1, args.lifetime1)]
Lxy2 = data2["Lxy{}_{}".format(args.mass2, args.lifetime2)]

pT1 = data1["pT{}_{}".format(args.mass1, args.lifetime1)]
pT2 = data2["pT{}_{}".format(args.mass2, args.lifetime2)]

phi1 = data1["phi{}_{}".format(args.mass1, args.lifetime1)]
phi2 = data2["phi{}_{}".format(args.mass2, args.lifetime2)]

eta1 = data1["eta{}_{}".format(args.mass1, args.lifetime1)]
eta2 = data2["eta{}_{}".format(args.mass2, args.lifetime2)]

LxyEff1 = data1["LxyEff{}_{}".format(args.mass1, args.lifetime1)]
LxyEff2 = data2["LxyEff{}_{}".format(args.mass2, args.lifetime2)]

#Checks to see if code works
print('Code is working')
	
doTest = args.dotest

plt.title("Line Graph")
plt.xlabel("Cut")
plt.ylabel("Efficiency %")
plt.plot(LxyEff1,  alpha=0.5, label='{} GeV'.format(args.mass1))
plt.plot(LxyEff2,  alpha=0.5, label='{} GeV'.format(args.mass2))
plt.tight_layout()
plt.savefig("LxyEffComp.png")
plt.clf()

#plt.style.use('fivethirtyeight')
#bin = numpy.linspace(0,2000,30)
#plt.yscale("log")
#plt.hist(Lxy1, bins=bin, alpha=0.5, label='{} GeV'.format(args.mass1))
#plt.hist(Lxy2, bins=bin, alpha=0.5, label='{} GeV'.format(args.mass2))
#plt.legend(loc = 'upper right')
#plt.xlabel('Lxy(mm)')
#plt.ylabel('# of Sleptons')
#plt.tight_layout()
#plt.savefig('LxyPlotComp{}_{}vs{}_{}.png'.format(args.mass1, args.lifetime1, args.mass2, args.lifetime2))
#plt.clf()


#  # Create a histogram for pT.
#plt.style.use('fivethirtyeight')
#bin = numpy.linspace(0,800,30)
#  # Creates the histogram that will display the x and y position
##plt.hist([pT1, pT2], bins = bin, 
#	#label=['{}_{}'.format(args.mass1, args.lifetime1),'{}_{}'.format(args.mass2, args.lifetime2)])
#plt.hist(pT1, bins=bin, alpha=0.5, label='{} GeV'.format(args.mass1))
#plt.hist(pT2, bins=bin, alpha=0.5, label='{} Gev'.format(args.mass2))
##plt.title('X and Y decay position of Slepton')
#plt.yscale("linear")
#plt.legend(loc = 'upper right')
#plt.xlabel('pT (GeV)')
#plt.ylabel('# of Sleptons')
#plt.tight_layout()
#plt.savefig('pTPlot{}_{}vs{}_{}.png'.format(args.mass1, args.lifetime1, args.mass2, args.lifetime2))
#plt.clf()
#
#  #Histogram for phi
#plt.style.use('fivethirtyeight')
#bin = numpy.linspace(-5,5,30)
#plt.hist(phi1, bins=bin, alpha=0.5, label='{} GeV'.format(args.mass1))
#plt.hist(phi2, bins=bin, alpha=0.5, label='{} GeV'.format(args.mass2))
#plt.legend(loc = 'upper right')
#plt.xlabel('phi')
#plt.ylabel('# of Sleptons')
#plt.tight_layout()
#plt.savefig('phiPlotComp{}_{}vs{}_{}.png'.format(args.mass1, args.lifetime1, args.mass2, args.lifetime2))
#plt.clf()
#
#  #Histogram for eta
#plt.style.use('fivethirtyeight')
#bin = numpy.linspace(-4,4,30)
#plt.hist(eta1, bins=bin, alpha=0.5, label='{} GeV'.format(args.mass1))
#plt.hist(eta2, bins=bin, alpha=0.5, label='{} GeV'.format(args.mass2))
#plt.legend(loc = 'upper right')
#plt.xlabel('eta')
#plt.ylabel('# of Sleptons')
#plt.tight_layout()
#plt.savefig('eta{}_{}vs{}_{}.png'.format(args.mass1, args.lifetime1, args.mass2, args.lifetime2))
#plt.clf()
#

