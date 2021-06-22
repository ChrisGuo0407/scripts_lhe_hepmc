#!/usr/bin/env python
import json
import pyhepmc_ng as hep
import matplotlib.pyplot as plt
import numpy
import argparse
import math
from func.get_iso import *  #grabs functions from get_iso.py


parser = argparse.ArgumentParser(description='Runs configuration for Slepton files')
parser.add_argument('--mass', type=str, default = '400', help = 'Default mass for Slepton ')
parser.add_argument('--lifetime', type=str, default = '1ns', help = 'Default lifetime for Slepton')
parser.add_argument('dotest', type=bool, default = False, help = 'Set to false so no test is run, change to True to run test')

args = parser.parse_args()
    
read_infile = "/eos/user/k/kdipetri/Snowmass_HepMC/run_staus/stau_{}_0_{}/events.hepmc".format(args.mass,args.lifetime)

#Checks to see if the file works
print('Works')

# If this is true, stop after 10 events
doTest = args.dotest

#initializes array
Lxyarray = []
pTarray = []
phiarray = []
etaarray = []
Staus = [2000015, 1000015]

seen_event_count_total = 0
events = 0
n = 0

Lxy_pass_check = [600, 800, 1000, 1200]
pT_pass_check = [10, 20, 30, 50]
eta_pass_check = [1.0, 2.5]
track_low_cut = 1

event_counts = 0 
Stau_counts = 0
event_pass_lxy_cuts = []
cutflow_list = []
Lxy_cuts = []
pT_cuts = []
#-------------------------------------------------------------------------------------------------------------------------


def passTrackTrigger(Lxy, Lxy_cuts, pT, pT_cuts):
    passCounts = [0, 0, 0]
    if Lxy > Lxy_cuts:
        passCounts [0] = 1
    if pT > pT_cuts:
        passCounts[1] = 1
#   if abs(eta) < eta_cuts:
#       passcounts[2] = 1
    if (Lxy>Lxy_cuts and pT>pT_cuts):
        passCounts[2] = 1
    return passCounts


#-------------------------------------------------------------------------------------------------------------------------
#read file start
#for m in range(len(read_infile)):
  #infile = read_infile[m]
  #n += 1
seen_event_count = 0
event_count = 0
  #dotest = False

Lxy_ok_list = numpy.zeros(len(Lxy_pass_check))
pT_ok_list = numpy.zeros(len(pT_pass_check))

event_passes = numpy.zeros([len(Lxy_pass_check), len(pT_pass_check)])



#------------------------------------------------------------------------------------------------------------
#event start

# reads the file
with hep.open(read_infile) as f:
  # just keeps looping
  while True :

    # try to get an event
    evt = f.read()
    # if it doesn't work, we're at the end of the file. 
    # just stop.
    if not evt : break

    # stop if this is just a test
    if doTest and evt.event_number > 100 :
      break
     

    tracks = 0


    if evt.event_number % 1000 == 0:
    #now = datetime.now()
    #current_time = now.strftime("%H:%M:%S")
        print("On file:", m+1, " Event:", evt.event_number)
    event_Lxy_ok_list = numpy.zeros(len(Lxy_pass_check))
    event_pT_ok_list = numpy.zeros(len(pT_pass_check))
    event_num_good_tracks = numpy.zeros([len(Lxy_pass_check), len(pT_pass_check)])
    track_ids = []
    for i in range(len(Lxy_pass_check)):
        track_ids.append([])
        for j in range(len(pT_pass_check)):
            track_ids[i].append([])
    event_count += 1

 
#----------------------------------------------------------------------------------------------------------------------
    # Get particles with evt.particles
    # Get vertices with evt.vertices
    # Various classes link the two together

    for particle in evt.particles :
    # This is what's in the "particle" class: http://hepmc.web.cern.ch/hepmc/classHepMC3_1_1GenParticle.html
      #if(abs(particle.pid)>=10000) : print(particle.id," ",particle.pid)
      if (abs(particle.pid) in Staus and particle.status==62) :
        tracks +=1
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

          #checks if track passes the Lxy / pT
          for i in range(len(Lxy_pass_check)):
            for j in range(len(pT_pass_check)):
                tracker = passTrackTrigger(Lxy, Lxy_pass_check[i], thispT, pT_pass_check[j])
                if tracker[0] == 1 and j == 0:
                    event_Lxy_ok_list[i] += 1
                if tracker[1] == 1 and i == 1:
                    event_pT_ok_list[j] += 1
                if tracker[2] == 1:
                    event_num_good_tracks[i][j] += 1
#keep track ids so we can do other things later
                    track_ids[i][j].append(particle.id)


          # Puts particle information into arrays
          Lxyarray.append(Lxy)
          pTarray.append(thispT)
          phiarray.append(thisphi)
          etaarray.append(thiseta)
          #stau_isolation.append()

        # Otherwise, this particle isn't decaying
        else :
          print("This particle is stable!")

#Tests to see if values are properly placed into array
#print("test array", pTarray)
    
    
    #print(event_Lxy_ok_list, " ", event_pT_ok_list) #Checks to see if it properly loops over the ok_lists
    if tracks > 0:
        seen_event_count += 1
    for i in range(len(event_Lxy_ok_list)):
        if event_Lxy_ok_list[i] >= track_low_cut:
            Lxy_ok_list[i] += 1
    for i in range (len(event_pT_ok_list)):
        if event_pT_ok_list[i] >= track_low_cut:
            pT_ok_list[i] += 1
    for i in range(len(event_num_good_tracks)):
        for j in range(len(event_num_good_tracks[i])):
            if event_num_good_tracks[i][j] >= track_low_cut:
                event_passes[i][j] += 1



events += event_count    
seen_event_count_total += seen_event_count

efficiencies = numpy.empty([len(event_passes), len(event_passes[0])])
errors = numpy.empty([len(event_passes), len(event_passes[0])])
for i in range(len(event_passes)):
    for j in range(len(event_passes[i])):
        efficiencies[i][j] = (event_passes[i][j] / seen_event_count)
        errors[i][j] = (math.sqrt((event_passes[i][j] / seen_event_count) * (1 - (event_passes[i][j] / seen_event_count)) / seen_event_count))


cf_dict = {"events": event_count, "seen": seen_event_count}
for i in range(len(Lxy_cuts)):
    cf_dict[Lxy_cuts[i]] = Lxy_ok_list[i]
for i in range(len(pT_cuts)):
    cf_dict[pT_cuts[i]] = pT_ok_list[i]
cutflow_list.append(cf_dict)


data = {"Lxy{}_{}".format(args.mass, args.lifetime): Lxyarray,
 "pT{}_{}".format(args.mass, args.lifetime): pTarray,
 "phi{}_{}".format(args.mass, args.lifetime): phiarray,
 "eta{}_{}".format(args.mass, args.lifetime): etaarray,
 "cf_list{}_{}".format(args.mass, args.lifetime): cutflow_list,
 "LxyEff{}_{}".format(args.mass, args.lifetime): Lxy_cuts,
 "pTEff{}_{}".format(args.mass, args.lifetime): pT_cuts}


with open('SleptonCalc{}_{}.json'.format(args.mass, args.lifetime), 'w') as fp:
  json.dump(data, fp)


print("Number of events: ", events)
print("Percent of \"seen\" events: ", 100 * seen_event_count_total / events, "%")
print("Percent of \"Lxy\" events: ", 100 * Lxy_ok_list / events, "%")
print("Percent of \"pT\" events: ", 100 * pT_ok_list / events, "%")
print(Lxy_ok_list)
print(pT_ok_list)
