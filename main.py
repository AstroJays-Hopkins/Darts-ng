## LAST UPDATE 03/30/2019 AT 12:45 PM ##
## THIS IS UNFINISHED CODE PLS HELP ##
## TODO LIST: ##
# - function to read PTs -- ET TO FINISH
# - function to read load cells -- GPS TO FINISH
# - function to get vent state / actuate vent solenoid - RYAN
# - function to get disconnect state / actuate disconnect solenoid - RYAN
# - function to get ball valve state - COURTNEY
# - function to detect if ignition command has been sent and if ball valve is open - COURTNEY

from datetime import datetime
from csv import writer
import time
import load_cell as lc
import RocketThermocouple as tc
import PressureTransducer as pt #change this
import QuickDisconnect as qd
try:
    import RPi.GPIO as GPIO  # RPi.GPIO documentation: https://sourceforge.net/p/raspberry-gpio-python/wiki/
except:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")
    
### LIST OF UNDEFINED VARIABLES, CONSTANTS --- UPDATE as NEEDED ###
# LC_SEL_TUPLES, EMERG_MBVALVE_SHUTOFF_PIN, VENT_VALVE_SHUTOFF_PIN, PT_CHANNELS, TC_CS_PINS

CRIT_T = 309.5
CRIT_P = 7240

Is_Critical = False

### VARIABLES TO STORE SENSOR OBJECTS ###
data = []
BALLVALVE = False # false for closed true for open

# Where load cell objects are stored
# To access the last reading of an individual load cell i,
# use LOAD_CELLS[i].last_reading
LOAD_CELLS = []

# initialize TC objects and data
TCs = []   ## ?

# initialize PT objects and data
PTs = []  ## ?

def init():
    # Initialize load cell serial and GPIO, then instantiate load cell objects
    lc.begin()
    i = 0
    for select_tuple in LC_SEL_TUPLES:  ## soo... LC_SEL_TUPLES is supposed to come from that external configuration file, but I don't know how to do that yet...
        LOAD_CELLS[i] = lc.Load_Cell(select_tuple)
        i++

    # Initialize thermocouples
    i = 0
    for cs_pin in TC_CS_PINS:
        TCs[i] = tc.Thermocouple(cs_pin)
        i++

    # Initialize PTs
    i = 0
    for pt_chan in PT_CHANNELS:
        PTs[i] = pt.PressureTransducer(pt_chan)
        i++

    # Configure GPIO pin for telling the ignition computer to close the motorized ball valve in an emergency:
    GPIO.setup(EMERG_MBVALVE_SHUTOFF_PIN, GPIO.OUT)
    GPIO.output(EMERG_MBVALVE_SHUTOFF_PIN, False)


### FUNCTIONS TO ITERATE THROUGH ALL SENSORS ###
def collectData():
    data.append(tc.readThermocouples(TCs))
    // change the critical checks to being a 2 state system so it doesnt # continuiously call emergency shutdown
    i = 0
    for thermocouple in TCs:
        if (thermocouple.last_reading > CRIT_T and Is_Critical == 0)
            emergency_shutdown()
            Is_Critical = 1
            print('EMERGENCY SHUTDOWN: Critical Temperature detected')
        i++
            
    data.append(pt.readPressureTransducers(PTs))
    i = 0
    for pt in PTs:
        if (pt.last_reading > CRIT_P and Is_Critical == 0)
            emergency_shutdown()
            Is_Critical = 1
            print('EMERGENCY SHUTDOWN: Critical Pressure detected')
        i++
        
    data.append(read_load_cells(LOAD_CELLS)) # change this 
    
    data.append(getVentState()) #write these functions
      
    data.append(getDisconnectState()) # write these functions 
    
    data.append(getBallValveState()) # write these 
            
### OTHER FUNCTIONS ###

# Tell ignition computer to close motorized ball valve.
# Doesn't actually close the valve (that's the igcomp's job) --- hence the name
def emergency_shutdown():
    GPIO.output(EMERG_MBVALVE_SHUTOFF_PIN, True)
    BALLVALVE = False
    Vent()
    
def Vent():
	GPIO.output(VENT_VALVE_SHUTOFF_PIN, True)
	VENTVALVE = False   
## FIXME MAYBE?  Should we have a function to order the igcomp to open the ball valve?

## TODO##
def getVentState():
    return vent.get_state()
    
    #kjafsdf
def getDisconnectState():
    return qd.get_state()
    
    #kjadsflk  
def getBallValveState():
    
    #klajdf
    
def Vent():
	GPIO.output(VENT_VALVE_SHUTOFF_PIN, True)
	VENTVALVE = False
    
### DATA LOGGING AND TRANSMISSION ###

#Writes data
def writedata(args):
    packet = []
    packet.append(datetime.now())
    for i in range(0,len(args)):
        packet.append(args[i])
    data_writer.writerow(packet)

## There used to be an ' import csv ' statement here and ' writer(log) ' was ' csv.writer(log) '
with open('DATA1.csv','a',newline='') as log:
    data_writer = writer(log)

    #Header row so you know what you're looking at (change as necessary)
    data_writer.writerow(['Timestamp','TC1','TC2','TC3','TC4','TC5','TC6','PT1','PT1','PT3','PT4','LC1','LC2','VentValve','FuelValve','BallValve'])

    while True:
        #collect all data here and assign to variables
        #slam all that shite into the writedata function (or append to a list each time a sensor is read)
        writedata(data)
        time.sleep(0.01)
        data = []
