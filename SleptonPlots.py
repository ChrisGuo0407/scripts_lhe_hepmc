import json
import numpy
import pyhepmc_ng as hep
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(description='Runs configuration for Slepton files')
parser.add_argument('--mass', type=str, default = '400', help = 'Default mass for Slepton ')
parser.add_argument('--lifetime', type=str, default = '1ns', help = 'Default lifetime for Slepton')
parser.add_argument('dotest', type=bool, default = False, help = 'Set to false so no test is run, change to True to run test')

args = parser.parse_args()

f = open('SleptonCalc{}_{}.json'.format(args.mass, args.lifetime))
data = json.load(f)

doTest = args.dotest

Lxy = data["Lxy"]
pT = data["pT"]
phi = data["phi"]
eta = data["eta"]

  # Create a histogram for Lxy.
plt.style.use('fivethirtyeight')
bin = numpy.linspace(0,2000,30)
  # Creates the histogram that will display the x and y position
plt.hist(Lxy, bins = bin, edgecolor = 'black')
plt.yscale("log")
plt.title('X and Y decay position of Slepton')
plt.xlabel('Lxy')
plt.ylabel('# of Sleptons')
plt.tight_layout()
plt.savefig('LxyPlot{}_{}.png'.format(args.mass, args.lifetime))
plt.clf()

  # Create a histogram for pT.
plt.style.use('fivethirtyeight')
bin = numpy.linspace(0,800,30)
  # Creates the histogram that will display the x and y position
plt.hist(pT, bins = bin, edgecolor = 'black')
plt.title('X and Y decay position of Slepton')
plt.yscale("linear")
plt.xlabel('pT (GeV)')
plt.ylabel('# of Sleptons')
plt.tight_layout()
plt.savefig('pTPlot{}_{}.png'.format(args.mass, args.lifetime))
plt.clf()

  # Create a histogram for phi.
plt.style.use('fivethirtyeight')
bin = numpy.linspace(-5,5,30)
  # Creates the histogram that will display the x and y position
plt.hist(phi, bins = bin, edgecolor = 'black')
#plt.ylim(0,100)
plt.title('X and Y decay position of Slepton')
plt.xlabel('phi')
plt.ylabel('# of Sleptons')
plt.tight_layout()
plt.savefig('phiPlot{}_{}.png'.format(args.mass, args.lifetime))
plt.clf()

  # Create a histogram for eta.
plt.style.use('fivethirtyeight')
bin = numpy.linspace(-4,4,30)
  # Creates the histogram that will display the x and y position
plt.hist(eta, bins = bin, edgecolor = 'black')
plt.title('X and Y decay position of Slepton')
#plt.ylim(0,75)
plt.xlabel('eta')
plt.ylabel('# of Sleptons')
plt.tight_layout()
plt.savefig('etaPlot{}_{}.png'.format(args.mass, args.lifetime))
plt.clf()
