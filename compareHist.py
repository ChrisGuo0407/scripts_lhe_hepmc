import json
import pyhepmc_ng as hep
import matplotlib.pyplot as plt
import numpy


def compareHist(arrays,labels, bins, yscale, xtitle, ytitle, filename):
	plt.style.use('fivethirtyeight')
	bin = bins
	plt.yscale(yscale)
	for i, array in enumerate(arrays):
		plt.hist(array, bins=bin, alpha=0.5, label = labels[i])
	plt.legend(loc = 'upper right')
	plt.xlabel(xtitle)
	plt.ylabel(ytitle)
	plt.tight_layout()
	plt.savefig(filename)
	plt.clf()



def comparemasses(dist, lifetime, masses, bins, yscale, xtitle, ytitle, filename):
	arrays = []
	labels = []
	for mass in masses:
		jsonfile = open("SleptonCalc{}_{}.json".format(mass, lifetime))
		data = json.load(jsonfile)
		array = data["{}{}_{}".format(dist, mass, lifetime)]
		arrays.append(array)
		labels.append("{} GeV".format(mass))
	compareHist(arrays, labels, bins, yscale, xtitle, ytitle, filename)


def comparelts(dist, lifetimes, mass, bins, yscale, xtitle, ytitle, filename):
	arrays = []
	labels = []
	for lifetime in lifetimes:
		jsonfile = open("SleptonCalc{}_{}.json".format(mass, lifetime))
		data = json.load(jsonfile)
		array = data["{}{}_{}".format(dist, mass, lifetime)]
		arrays.append(array)
		labels.append("{}".format(lifetime))
	compareHist(arrays, labels, bins, yscale, xtitle, ytitle, filename)



comparemasses("Lxy", "1ns", [100, 400, 600], numpy.linspace(0,2000,30), "log", "Lxy (mm)", "# of Sleptons", 'LxyMassComp.png')
comparemasses("pT", "1ns", [100, 400, 600], numpy.linspace(0,800,30), "linear", "pT (GeV)", "# of Sleptons", 'pTMassComp.png')
comparemasses("phi", "1ns", [100, 400, 600], numpy.linspace(-numpy.pi,numpy.pi,30), "linear", "phi", "# of Sleptons", 'phiMassComp.png')
comparemasses("eta", "1ns", [100, 400, 600], numpy.linspace(-4,4,30), "linear", "eta", "# of Sleptons", 'etaMassComp.png')

comparelts("Lxy", ["0p01ns", "0p1ns", "1ns", "10ns"], 300, numpy.linspace(0,2000,30), "log", "Lxy (mm)", "# of Sleptons", 'LxyLTComp.png')
comparelts("pT", ["0p01ns", "0p1ns", "1ns", "10ns"], 300, numpy.linspace(0,800,30), "linear", "pT (GeV)", "# of Sleptons", 'pTLTComp.png')
comparelts("phi",["0p01ns", "0p1ns", "1ns", "10ns"],300, numpy.linspace(-numpy.pi,numpy.pi,30), "linear", "phi", "# of Sleptons", 'phiLTComp.png')
comparelts("eta", ["0p01ns", "0p1ns", "1ns", "10ns"],300, numpy.linspace(-4,4,30), "linear", "eta", "# of Sleptons", 'etaLTComp.png')


