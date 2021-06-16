#!/usr/bin/env python
import json
import pyhepmc_ng as hep
import matplotlib.pyplot as plt
import numpy
import argparse

parser = argparse.ArgumentParser(description='Runs configuration for Slepton files')
parser.add_argument('--mass', type=str, default = '400', help = 'Default mass for Slepton ')
parser.add_argument('--lifetime', type=str, default = '1ns', help = 'Default lifetime for Slepton')
parser.add_argument('dotest', type=bool, default = False, help = 'Set to false so no test is run, change to True to run test')

args = parser.parse_args()
	
infile = "/eos/user/k/kdipetri/Snowmass_HepMC/run_staus/stau_{}_0_{}/events.hepmc".format(args.mass,args.lifetime)

#Checks to see if the file works
print('Works')

# If this is true, stop after 10 events
doTest = args.dotest

#initializes array
Lxyarray = []
pTarray = []
phiarray = []
etaarray = []

# Reads the file
with hep.open(infile) as f:
  # Just keeps looping
  while True :

    # Try to get an event
    evt = f.read()
    # If it doesn't work, we're at the end of the file. 
    # Just stop.
    if not evt : break

    # Stop if this is just a test
    if doTest and evt.event_number > 500 :
      break
 
    # From here on, do things with the event!
    print("In event",evt.event_number)
 
    # Get particles with evt.particles
    # Get vertices with evt.vertices
    # Various classes link the two together

    for particle in evt.particles :
    # This is what's in the "particle" class: http://hepmc.web.cern.ch/hepmc/classHepMC3_1_1GenParticle.html
      #if(abs(particle.pid)>=10000) : print(particle.id," ",particle.pid)
      if (abs(particle.pid)==2000015 and particle.status==62) :
        #print("This is a Slepton particle")
        #print(particle.status)

        # Get the particle four vector
        particlemom = particle.momentum
        thispT = particlemom.pt()/1000.
        thisphi = particlemom.phi()
        thiseta = particlemom.eta()
        #print(thispT)

        # Get the vertex where it decays and print its properties
        decayvtx = particle.end_vertex
        #print(decayvtx)

        # If decayvtx isn't None, it exists and we can look at it.
        if(decayvtx) :

          # Access some of the vertex properties.
          # These are the methods available for the GenVertex class:
          # http://hepmc.web.cern.ch/hepmc/classHepMC3_1_1GenVertex.html
          status = decayvtx.status
          fourvec = decayvtx.position
          products = decayvtx.particles_out
          #print(status,fourvec,"number of decay products is",len(products)) 
 
          # And let's try doing something with the
          # vertex, like assessing its location.
          # The FourVector class is here: 
          # http://hepmc.web.cern.ch/hepmc/classHepMC3_1_1FourVector.html
          #print("Decay location is: x",fourvec.x,", y",fourvec.y,", z",fourvec.z,", t",fourvec.t)
          Lxy = (fourvec.x**2+fourvec.y**2)**0.5
          #print("Lxy value is ", Lxy)

          # Puts particle information into arrays
          Lxyarray.append(Lxy)
          pTarray.append(thispT)
          phiarray.append(thisphi)
          etaarray.append(thiseta)


        # Otherwise, this particle isn't decaying
        else :
          print("This particle is stable!")

#Tests to see if values are properly placed into array
#print("test array", pTarray)


data = {"Lxy{}_{}".format(args.mass, args.lifetime): Lxyarray,
 "pT{}_{}".format(args.mass, args.lifetime): pTarray,
 "phi{}_{}".format(args.mass, args.lifetime): phiarray,
 "eta{}_{}".format(args.mass, args.lifetime): etaarray}


with open('SleptonCalc{}_{}.json'.format(args.mass, args.lifetime), 'w') as fp:
  json.dump(data, fp)
