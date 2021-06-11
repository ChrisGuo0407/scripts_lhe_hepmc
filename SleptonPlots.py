import json
import numpy
import pyhepmc_ng as hep
import matplotlib.pyplot as plt

f = open('SleptonCalc.json')
data = json.load(f)


Lxy = data["Lxy"]
pT = data["pT"]
phi = data["phi"]
eta = data["eta"]

  # Create a histogram for Lxy.
plt.style.use('fivethirtyeight')
bin = numpy.linspace(0,7000,30)
  # Creates the histogram that will display the x and y position
plt.hist(Lxy, bins = bin, edgecolor = 'black')
plt.title('X and Y decay position of Slepton')
plt.xlabel('Lxy')
plt.ylabel('# of Sleptons')
plt.tight_layout()
plt.savefig('LxyPlot.png')
plt.clf()

  # Create a histogram for pT.
plt.style.use('fivethirtyeight')
bin = numpy.linspace(0,800,30)
  # Creates the histogram that will display the x and y position
plt.hist(pT, bins = bin, edgecolor = 'black')
plt.title('X and Y decay position of Slepton')
#plt.ylim(0,75)
plt.xlabel('pT (GeV)')
plt.ylabel('# of Sleptons')
plt.tight_layout()
plt.savefig('pTPlot.png')
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
plt.savefig('phiPlot.png')
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
plt.savefig('etaPlot.png')
plt.clf()
