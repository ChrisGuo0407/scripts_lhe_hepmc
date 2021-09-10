#!/usr/bin/env python
#Imported Libraries to use for the script
import json
import pyhepmc_ng as hep
import matplotlib.pyplot as plt
import numpy
import argparse
import math
from func.get_iso import *  #grabs functions from get_iso.py

#These are arguments when calling the script. Do --mass # --lifetime 1ns doTest=True to run the code
parser = argparse.ArgumentParser(description='Runs configuration for Slepton files')
parser.add_argument('--mass', type=str, default = '400', help = 'Default mass for Slepton ')
parser.add_argument('--lifetime', type=str, default = '1ns', help = 'Default lifetime for Slepton')
#parser.add_argument('--events', type=str, default = '100', help = 'Number of events to run through')
parser.add_argument('dotest', type=bool, default = False, help = 'Set to false so no test is run, change to True to run test')

args = parser.parse_args()

#Reads the file given arguments from this user folder.
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
zarray = []
Staus = [2000015, 1000015]
acceptstau = []
Lxy_stau_ok = [0,0,0,0]

    #Lxy arrays for specific acceptance cuts
Lxy600 = []
Lxy800 = []
Lxy1000 = []
Lxy1200 = []

    #pT arrays for specific acceptance cuts, can change
pT10 = []
pT25 = []
pT35 = []
pT50 = []

seen_event_count_total = 0
events = 0
n = 0

#Initializes arrays for TrackTriggerAcceptance Function
Lxy_pass_check = [600, 800, 1000, 1200]
pT_pass_check = [20,50,100,125]
eta_pass_check = [1.0, 2.5]
z_cut = [2600]
eta_cut = [2.5]
track_low_cut = 1
pT_stau_ok = [0, 0, 0, 0]


event_counts = 0 
Stau_counts = 0
event_pass_lxy_cuts = []
cutflow_list = []
Lxy_cuts = []
pT_cuts = []

stau_passes = []

#Array for adding up every Stau that passes through each cut of the given value.
nEventStauOkListLxy = [0, 0, 0, 0]
nEventStauOkListpT = [0,0,0,0]
#-------------------------------------------------------------------------------------------------------------------------

#This Function will count how many Staus pass through the given cuts of each value. If it goes through Lxy, z, and eta cuts, then the first value in the array becomes True
#if the stau passes through the pT cut, the 2nd value in the array will become true, and if both 1&2 become true then the 3rd value in the array becomes true.
def passTrackTrigger(Lxy, Lxy_cuts, pT, pT_cuts, z, z_cuts, eta, eta_cuts):
    passCounts = [0, 0, 0]
    if (Lxy > Lxy_cuts or abs(z) > z_cuts) and abs(eta) < eta_cuts:
        passCounts [0] = 1
    if pT > pT_cuts:
        passCounts[1] = 1
    if (Lxy > Lxy_cuts and pT > pT_cuts):
        passCounts[2] = 1
    return passCounts

#These 3 Acceptance functions check if the values of Lxy, z, pT, and eta pass through the given cut conditions. The values given are checked and if they pass through certain cuts 
#in the array, it will show up as a 1, if it does not, then there will be a 0. For example, if in LxyAcceptance, the Lxy is 1100, but the cuts are [600, 800, 1000, 1200]
#then when you run the function, it will give an array that shows [1, 1, 1, 0], meaning that the Lxy passed every cut but the last one.
def LxyAcceptance(Lxy, Lxy_pass_check, z, z_cuts):
    pass_Lxys_zs = []
    for z_cut in z_cuts:
        pass_Lxys = []
        for Lxy_cut in Lxy_pass_check:
            pass_Lxy = Lxy > Lxy_cut or abs(z) > z_cut
            pass_Lxys.append(pass_Lxy)
        pass_Lxys_zs.append(pass_Lxys)

    #print (pass_Lxys_zs)

    return pass_Lxys_zs

def pTAcceptance(pT, pT_pass_check):
    pass_pTs = []
    for pT_cut in pT_pass_check:
        pass_pT = pT > pT_cut
        pass_pTs.append(pass_pT)

    #print (pass_pT)

    return pass_pTs
    
def etaAcceptance(eta, eta_pass_check):
    pass_eta = [abs(eta) < cut for cut in eta_pass_check]
    #print (pass_eta)

    return pass_eta

#Test difference acceptances for different scenarios and calls the LxyAcceptance and etaAcceptance functions from above. In this case, the function makes sure that the Stau's values
#pass through the given cuts and will return the arrays, telling you which cuts they have passed.
#There is a running example below, that has been commented out to try and see how TrackTriggerAcceptance works. The values have been manually inputed in.
def TrackTriggerAcceptance(Lxy, eta, z):
    Lxy_pass_check = [600, 800, 1000, 1200]
    eta_pass_check = [2.5]
    z_cuts = [2600]
    pass_eta = []

    pass_Lxy_z_arrays = LxyAcceptance(Lxy, Lxy_pass_check, z, z_cuts)
    pass_eta_array = etaAcceptance(eta, eta_pass_check)
    pass_all_array = []
    for pass_eta in pass_eta_array:
        # looping over eta cuts
        pass_all_z = []
        for pass_Lxy_z_array in pass_Lxy_z_arrays:
            # looping over z cuts
            pass_all_Lxy = []
            for pass_Lxy in pass_Lxy_z_array:
                # looping over Lxy cuts
                pass_all = pass_Lxy and pass_eta
                pass_all_Lxy.append(pass_all)
            #print("Lxy ",pass_all_Lxy)
            pass_all_z.append(pass_all_Lxy)
        pass_all_array.append(pass_all_z)
   # print("Z cuts ",pass_all_z)
    #print("Pass Everything ", pass_all_array)
    return pass_all_array    




#LxyAcceptance(1000,[600, 800, 1000, 1200], 2400, [1500, 2000, 2700, 2900])
#pTAcceptance(5, [10, 20, 30, 50])
#etaAcceptance(2.4, [1.0, 2.5])
#TrackTriggerAcceptance(1000, .7, 2000)


#LxyAcceptance(1000,[600, 800, 1000, 1200], 2400, [1500, 2000, 2700, 2900])
#pTAcceptance(5, [10, 20, 30, 50])
#etaAcceptance(2.4, [1.0, 2.5])
#TrackTriggerAcceptance(1000, .7, 2000)
#Test = TrackTriggerAcceptance(1000, .7, 2000)
#print("Test Check ",Test[0][0][3])

#This function will take the EventList and the seen_event_count and calculate the errors to be used for the errorbars when we plot the values.
def EfficiencyErrorbar (EventList, seen_event_count):
    efficiencies = []
    errors = []
    for i in range(len(EventList)):
        efficiencies.append((EventList[i] / seen_event_count))
        errors.append((math.sqrt((EventList[i] / seen_event_count) * (1 - (EventList[i] / seen_event_count)) / seen_event_count)))
        #print(EventList[i], seen_event_count, EventList[i]/seen_event_count)

    return efficiencies, errors
    



#-------------------------------------------------------------------------------------------------------------------------
#read file start
#for m in range(len(read_infile)):
  #infile = read_infile[m]
  #n += 1
seen_event_count = 0
event_count = 0
  #dotest = False

#Initializes the array to 0 for the ok lists, the values will be appended to the array if they pass through certain checks.
Lxy_ok_list = [0 for cut in Lxy_pass_check]
pT_ok_list = [0 for cut in pT_pass_check]

#Initializes the array to 0 for the length of both the pass_checks
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
    #Will only run up to that many events before stopping the code completely. Can change the value to a smaller one so you can run the code faster.
    if doTest and evt.event_number > 2000:
      break
     

    tracks = 0


    #Same as the other ok_lists, initializes the arrays to 0 based on the length of the pass_check.
    event_Lxy_ok_list = numpy.zeros(len(Lxy_pass_check))
    event_pT_ok_list = numpy.zeros(len(pT_pass_check))
    event_num_good_tracks = numpy.zeros([len(Lxy_pass_check), len(pT_pass_check)])
    track_ids = []
    for i in range(len(Lxy_pass_check)):
        track_ids.append([])
        for j in range(len(pT_pass_check)):
            track_ids[i].append([])
    event_count += 1

    #Number of events that pass through each Lxy cut
    nEventStau600 = 0
    nEventStau800 = 0
    nEventStau1000 = 0
    nEventStau1200 = 0
    
    #Number of events that pass through each pT cut
    nEventStau10 = 0
    nEventStau25 = 0
    nEventStau35 = 0
    nEventStau50 = 0

 
#----------------------------------------------------------------------------------------------------------------------
    # Get particles with evt.particles
    # Get vertices with evt.vertices
    # Various classes link the two together

    for particle in evt.particles :
    # This is what's in the "particle" class: http://hepmc.web.cern.ch/hepmc/classHepMC3_1_1GenParticle.html
      #if(abs(particle.pid)>=10000) : print(particle.id," ",particle.pid)
      #Checks the run file to see if the particle has the same pid given in Staus(Near the very top of the script), along with the same particle status. If it does, it will 
        #get the values for this stau and also add +1 to the tracks array.
      if (abs(particle.pid) in Staus and particle.status==62) :
        tracks +=1
        #print("This is a Slepton particle")
        #print(particle.status)
       

        # Get the particle four vector so gets the momentum and converts it to pT, phi, and eta.
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
          #Calculates the Lxy and z given the vertex properties
          Lxy = (fourvec.x**2+fourvec.y**2)**0.5
          z = fourvec.z
          
            #Checks the values in the passTrackTrigger function and if the values pass the given tracker conditions, it will append +1 each time to the event_ok_lists
          for i in range(len(Lxy_pass_check)):
            for j in range(len(pT_pass_check)):
                tracker = passTrackTrigger(Lxy, Lxy_pass_check[i], thispT, pT_pass_check[j], z, z_cut[0], thiseta, eta_cut[0])
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
          zarray.append(z)
          #stau_isolation.append()

#Checks to see if Lxy passes through eta and z
          acceptstau = TrackTriggerAcceptance(Lxy, thiseta, z)
          if acceptstau[0][0][0] == True:
            Lxy600.append(Lxy)
            Lxy_stau_ok[0] += 1
            nEventStau600 += 1
          if acceptstau[0][0][1] == True:
            Lxy800.append(Lxy)
            Lxy_stau_ok[1] += 1
            nEventStau800 += 1
          if acceptstau[0][0][2] == True:
            Lxy_stau_ok[2] +=1
            Lxy1000.append(Lxy)
            nEventStau1000 += 1
          if acceptstau[0][0][3] == True:
            Lxy_stau_ok[3] +=1
            Lxy1200.append(Lxy)
            nEventStau1200 += 1
         
#Checks to see if pT values pass through each cut
          pass_pTs = pTAcceptance (thispT, pT_pass_check)
          if pass_pTs[0] == True:
            pT_stau_ok[0] +=1
            nEventStau10 += 1
            pT10.append(thispT)
          if pass_pTs[1] == True:
            pT_stau_ok[1] +=1
            nEventStau25 += 1
            pT25.append(thispT)
          if pass_pTs[2] == True:
            pT_stau_ok[2] +=1
            nEventStau35 += 1
            pT35.append(thispT)
          if pass_pTs[3] == True:
            pT_stau_ok[3] +=1
            nEventStau50 += 1
            pT50.append(thispT)

            



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

#If the event passes through each specific cut, adds +1 to the array
    if nEventStau600 > 0:
        nEventStauOkListLxy[0] +=1
    if nEventStau800 > 0:
        nEventStauOkListLxy[1] +=1
    if nEventStau1000 > 0:
        nEventStauOkListLxy[2] +=1
    if nEventStau1200 > 0:
        nEventStauOkListLxy[3] +=1

#Adds +1 to the array if it passes through said pT cut
    if nEventStau10 > 0:
        nEventStauOkListpT[0] +=1
    if nEventStau25 > 0:
        nEventStauOkListpT[1] +=1
    if nEventStau35 > 0:
        nEventStauOkListpT[2] +=1
    if nEventStau50 > 0:
        nEventStauOkListpT[3] +=1

#Adds each event_count given along with each seen_event_count.
events += event_count    
seen_event_count_total += seen_event_count
#print("seen event count, ", seen_event_count)

#Places the errorbar efficiency values to Lxy and pT separately.
LxyEfficiencies, LxyErrors = EfficiencyErrorbar(nEventStauOkListLxy,seen_event_count)
pTEfficiencies, pTErrors = EfficiencyErrorbar(nEventStauOkListpT, seen_event_count)


#Should convert numpy types to json files
class NumpyEncoder(json.JSONEncoder):
#Special json encoder for numpy types
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


#Calculates the efficiencies of Lxy and pT by taking the number of Staus that passed through each ok_list and dividing it by the number of events that happened.
LxyEff = [x/float(events) *100 for x in Lxy_ok_list]
pTEff = [x/float(events) *100 for x in pT_ok_list]
print("eff ", LxyEff, "pTEff ", pTEff)

#Converts the arrays into json types to be placed into json files later on.
Lxy_cuts = json.dumps(LxyEff, cls=NumpyEncoder)
pT_cuts = json.dumps(pTEff, cls=NumpyEncoder)
print(Lxy_cuts)
print(pT_cuts)

#This is a dictionary that places all the potential data that we need into it. They are formatted so that when they are saved, it will have the mass and lifetime
#that you specified. For example, if you ran --mass 300 --lifetime 10ns, then for Lxy, it would be "Lxy300_10ns".
data = {"Lxy{}_{}".format(args.mass, args.lifetime): Lxyarray,
 "pT{}_{}".format(args.mass, args.lifetime): pTarray,
 "phi{}_{}".format(args.mass, args.lifetime): phiarray,
 "eta{}_{}".format(args.mass, args.lifetime): etaarray,
 "cf_list{}_{}".format(args.mass, args.lifetime): cutflow_list,
 "LxyEff{}_{}".format(args.mass, args.lifetime): LxyEff,
 "pTEff{}_{}".format(args.mass, args.lifetime): pTEff,
 "LxyCuts{}_{}".format(args.mass, args.lifetime): Lxy_pass_check,
 "pTCuts{}_{}".format(args.mass, args.lifetime): pT_pass_check,
 "LxySOL{}_{}".format(args.mass, args.lifetime): Lxy_stau_ok,
 "Lxy600{}_{}".format(args.mass, args.lifetime): Lxy600,
 "Lxy800{}_{}".format(args.mass, args.lifetime): Lxy800,
 "Lxy1000{}_{}".format(args.mass, args.lifetime): Lxy1000,
 "Lxy1200{}_{}".format(args.mass, args.lifetime): Lxy1200,
 "nEventLxySOL{}_{}".format(args.mass, args.lifetime): nEventStauOkListLxy,
 "pTSOL{}_{}".format(args.mass, args.lifetime): pT_stau_ok,
 "pT10{}_{}".format(args.mass, args.lifetime): pT10,
 "pT25{}_{}".format(args.mass, args.lifetime): pT25,
 "pT35{}_{}".format(args.mass, args.lifetime): pT35,
 "pT50{}_{}".format(args.mass, args.lifetime): pT50,
 "nEventpTSOL{}_{}".format(args.mass, args.lifetime): nEventStauOkListpT,
 "pTErrors{}_{}".format(args.mass, args.lifetime): pTErrors,
 "LxyErrors{}_{}".format(args.mass, args.lifetime): LxyErrors,
 "pTEfficiencies{}_{}".format(args.mass, args.lifetime): pTEfficiencies,
"LxyEfficiencies{}_{}".format(args.mass, args.lifetime): LxyEfficiencies
 }

#Creates a new json file with the same arguments from above and dumps the data dictionary into the file and saves it for later use.
with open('SleptonCalc{}_{}.json'.format(args.mass, args.lifetime), 'w') as fp:
  json.dump(data, fp)


#print("Number of events: ", events)
#print("Percent of \"seen\" events: ", 100 * seen_event_count_total / events, "%")
#print("Lxy ok list  ", Lxy_ok_list)
#print("Percent of \"pT\" events: ", pTEff, "%")
#print("600", Lxy600)
#print("800", Lxy800)
#print("1000", Lxy1000)
#print("1200", Lxy1200)
#print("Stau Ok List ", Lxy_stau_ok)
#print("# of events that pass through", nEventStauOkListLxy)
#print("pT Cut Check ", pT_stau_ok)
#print ("# of events that pass through pT ", nEventStauOkListpT)
#print(LxyErrors, LxyEfficiencies)
