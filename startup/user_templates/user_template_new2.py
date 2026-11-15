import pprint
import time


'''
######################################################

If you need to cancel an operation hit "Ctrl + c" wait for the program to stop then type "RE.abort()"
If you need to search for a command hit "Ctrl + r" and type any part of the command



### slit_x2 setting ####
slit_x2_offset_edge = 0 # the edge position of slit_x2 (opposite of x2.position)
slit_x2_offset_gap = 10.3 # offset between the edge and the slit gap
slit_x2_offset_block = slit_x2_offset_edge + 1 # to block the beam

soller trans = 4 for regular Sollermeasurement
soller trans = -1.5 for gap for PXR

RE(bp.rel_scan([pilatus100kA],op_slitx,-4, 4, 41,per_step=shutter_flash_scan))

flow1 for XRF collimator is 2.2


Procedure:

1. Remove the sample that has been finished, put a clean trough and load a new sample (DO NOT LOAD THE NEW SAMPLE WHEN TIRED)
2. Put on the cover, check the x2 to avoid the XRF probe touching the walls on both x2 limits (51 and -79)
3. Add the new sample name to the dict and note the loading time (Note: the Front and Back are alternating)
4. Uncomment the sample name for the next run 
4. Run the measurement
5. Clean the trough

Repeat the procedure above for the next sample



'''

# set_project_name('0_alignment')
set_project_name('1_PFOS')
# currently working at /nsls2/data/smi/proposals/2026-3/pass-319804/projects/1_PFOS/

# 
atten_slit = 0 # -1.767 # -1.7843
soller_tran_soller = 4 # 5.5 # 5.5 # 4
soller_tran_gap = -1.5 # 4 # 5 # to use the center gap on the soller slits
constant_he_gid = 2.6 # 2.5 #2.6
collimator_he_rate = 2.2 
counter=0 ## the counter is used as a file discriptor
Sensor1 = 17.8
Sensor2 = 28.99
KibronP = 132.111
global File_type, Epoch_start, Simulate
# allowed File_type Senso1, Senso2, Kibron, None, time
File_type = "Sensor1"
Epoch_start = time.time()
Simulate = False
# slit_x2 to sample distance: ~87mm, HZ, 2025/06/20

#Not sure where to store the following
def changeSample():
    print('move the soller mode to change the sample')
    yield from set_mode('Soller')
    yield from mabt(0,0,0)

def slitX2_cleanup():

    '''to move the motor to initial positoins after control C
    '''
    yield from beam_off()
    yield from bps.mov(abs2,5)
    yield from slitX2_out()

#This sets up the class for each sample
# name is ascii
# other is either an x2_position, pressure or some other variable that is 
class Sample():
    def __init__(self, name, pos, counter, name_type, sh):
        self.name = name
        self.pos = pos
        self.counter = counter
        self.name_type = name_type
        self.sh = sh

x2_pos1 =-60
x2_pos2 = 10
x2_pos3 = 50

checks_init_all = {"mode":"Soller","coarse":True,"file_type": "Time","epoch_start": False}
xr_init_all ={"start": "all", "end":99,"scan_dir": "global", "auto_atten":False}

checks_init1 = {"method":"XR","det_mode":"XR","phi":False, "ih":False, "tth":False, "astth":False, "coarse":True,"file_type":"Kibron"}
checks_init2 = {"method":"XR","det_mode":"XR","coarse":True,"file_type": "Sensor1"}
checks_init3 = {"method":"XR","det_mode":"XR","coarse":True,"file_type": "Time","epoch_start": False}
checks_init4 = {"method":"checks","det_mode":"XR","coarse":True,"file_type": "none","epoch_start": False}


xr_init={"method":"XR","start": "all", "end":99,"scan_dir": "global", "auto_atten":False}
xrf_init={"method":"XRF","start": "all", "end":99,"scan_dir": "global", "auto_atten":False}
soller_init ={"method":"Soller","x2_direction":1,"block_pos": 0,"q_start":1.3,"q_end":1.8,"npts":21,"exp_time":20, "alpha_i":0.0728, "wait_time":5,"atten":-1.775}
gisaxs_init = {"method":"gisaxs","x2_direction":1,"atten": 0, "exposure_time":1, "incident_angle": 0.0728, "bs_pos": -15.82}
giwaxs_init = {"method":"giwaxs","incident_angle": 0.0728, "atten": 0, "exposure_time": 1.7, "tth": 0, "x2_direction":17 , "block_pos": 60, "use_slitx2": True, "sh_offset": -1}
giwaxs_bkg_init ={"method":"giwaxs_bkg","incident_angle": 0.0728, "atten": 0, "exposure_time": 1.7, "tth": 0, "x2_direction":17 , "block_pos": 60, "use_slitx2": True, "sh_offset": -1}
pseudo_init= {"method":"pseudo","alpha":0.0728, "num_point": 2, "exp_time": 30, "x2_per_step": 0, "atten": -1.5, "soller_tran":-1.5, "slit":'slit_x2'}

counter=33
sample1 =Sample("name1",17, counter, "Kibron",15)
sample2 =Sample("name2",17, counter, "Time",15)
sample3 =Sample("name2",17, counter, "none",15)

run1 = (sample1, xr_init)
run2 = (sample2, checks_init4)
run3  = (sample3, xrf_init)
runs= [run1, run2, run3]


# all this is called samples, it is really a technique run and may or may not canple the sample and sample position
# this version has two variables for the x2 position, one could be removed

# samples = []
# samples.append(Sample("sample_1", x2_pos1,[ "checks",checks_init1]))
# samples.append(Sample("sample_1", x2_pos2,[ "gisaxs",gisaxs_init]))
# samples.append(Sample("sample_1", x2_pos1,[ "checks",checks_init2]))
# samples.append(Sample("sample_1", x2_pos2,[ "gisaxs",gisaxs_init]))
# samples.append(Sample("sample_1", x2_pos1,[ "checks",checks_init3]))
# samples.append(Sample("sample_1", x2_pos2,[ "gisaxs",gisaxs_init]))



# This is the routine that checks to make sure that the same is allowed
#allowed_list=['XR','XRF','GISAXS','GIWAXS','GIWAXS_BKG','Soller','pseudo', 'checks']
allowed_list=['xr','xrf','gisaxs','giwaxs','giwaxs_bkg','soller','pseudo', 'checks']

def check_commands():
    set_allowed=1
    all_list = list(range(len(runs)))
    for ii in all_list:
        method=runs[ii][1]["method"]
        # this is to make it case insensitive, not working
        if allowed_list.count(method.lower()) == 1:
            print(method,"is an allowed method:", method)
        if allowed_list.count(method.lower()) == 0 : 
            print(method,"is NOT an allowed method:", method)
            set_allowed=0
    return(set_allowed)

Epoch_start=time.time()

#


def xr(item):
    yield from set_mode("XR")
    file_name=get_name(item)
    x2_pos=runs[item][0].pos
    extras=runs[item][1]
    print("Starting XR scan with file-", file_name, "  at x2=",x2_pos,"extras:",extras)
    yield from xr_scan_file(file_name,x2_pos, "xr_scan1.csv", **extras)

# This is where the type of XRF scans are defined. The same as xr() except the name        
# Below is the case where all of the scans are the same and from a scan file
# This could be generalized so that they are different by using if statements
# Could also include calling old fashion scans that were hard wired
def xrf(item):
    yield from set_mode("XRF")
    file_name=get_name(item)
    x2_pos=runs[item][0].pos
    extras=runs[item][1]
    print("Starting XRF scan with file-", file_name, "  at x2=",x2_pos,"extras:",extras)
    yield from xrf_scan_file(file_name,x2_pos,"xrf_scan1.csv", **extras)

# This is where the type of Soller scans are defined.  This does not read from a file.
# This can be generalized so that different samples used different scans
# Currently this is define in q space but the intent is to write this in anngle spacecall
def soller(item):
    yield from set_mode("Soller")
    file_name=get_name(item)
    x2_pos=runs[item][0].pos
    extras=runs[item][1]
    print("Starting Soller scan with file-", file_name, "  at x2=",x2_pos,"extras:",extras)
    yield from soller_scanq(file_name, **extras) # block edge at -31.5

# This is where the type of GISAXS scans are defined.  This does not read from a file.
# This can be generalized so that different samples used different scans
def gisaxs(item):
    yield from set_mode("GISAXS")
    file_name=get_name(item)
    x2_pos=runs[item][0].pos
    extras=runs[item][1]
    print("Starting GISAXS scan with file- ",file_name, "  at x2=",x2_pos,extras)
    yield from gisaxs_scan(file_name, **extras)

# This is where the type of GIWAXS scans are defined.  This does not read from a file.
# This can be generalized so that different samples used different scans
def giwaxs(item):
    yield from set_mode("GIWAXS")
    file_name=get_name(item)
    x2_pos=runs[item][0].pos
    extras=runs[item][1]
    print("Starting GIWAXS scan with file- ",file_name, "  at x2=",x2_pos)
    yield from giwaxs_scan(file_name, **extras)

def giwaxs_bkg(item):
    yield from set_mode("GIWAXS")
    file_name=get_name(item)
    x2_pos=runs[item][0][0].pos
    extras=runs[item][1]
    print("Starting GIWAXS scan with file- ",file_name, "  at x2=",x2_pos)
    yield from giwaxs_scan_bkg(file_name, **extras)

# This is where the type of PSEUDO scans are defined.  This does not read from a file.
# This can be generalized so that different samples used different scans
# Here we would probably want to inlude other descriptors such as a list of stth values

def pseudo(item):
    yield from set_mode("PSEUDO")
    file_name=get_name(item)
    x2_pos=runs[item][0].pos
    print("Starting PSEUDO scan with file- ",file_name, "  at x2=",x2_pos)
    yield from gixos_multiqxy(file_name_dict[number]+'_pxr', alpha = 0.0728, num_point = 1, exp_time = 30, x2_per_step = 0, atten=-1.5, slit='slit_x2')

def kibron(item):
    print("Simulation mode: checking accuracy of kibron variables")
    kibron.runConstantPressure(target_pressure=pressure, target_speed = 70)
    print('Compression is finishied; stop the Kibron')
    # do we add a sleep here, how much
    kibron.device.call('StepStop')
    kibron.device.call('StopMeasure')
    # do we need to add the following


def kibron_stop_measure():
    kibron.device.call("StopMeasure")

################### TO USE KIBRON ####################
# To start, run these commands in the bluesky finescanbelow
    # HOST, PORT = "10.66.91.26", 9897 ## HZ
    # sock = mtx.connect(HOST, PORT)
    # device = mtx.Trough(sock)
    # kibron = KibronTrough(device, sock)
# To stop the measurement:
    # kibron.device.call('StepStop')
    # kibron.device.call('StopMeasure')

#     # kibron_stop_measure()
# def kibron_stop_measure():
    # kibron.device.call('StepStop')
    # kibron.device.call('StopMeasure')
# To stop the remote server:
    # kibron.close()f
##################################################
#TODO remove file_type below
# THis allows you to configure a line with sample checks
def check_all(item,mode="checks",det_mode="XR",phi=True, ih=True, tth=True, astth=True,
            coarse=True, file_type="none", epoch_start=False,**kwargs):
    global Epoch_start
    if epoch_start == True:
        Epoch_start=time.time() #starts the clock for the time to be used in the file name
    #print(f"check_all({', '.join(f'{k}={v}' for k, v in kwargs.items())})")
    x2_pos=runs[item][0].pos
    yield from set_mode(det_mode)
    print("Checking the alignment at x2=",x2_pos, " using mode: ",det_mode)
    if phi    == True:
        print("running phi check")
        #  check_phi()
    if ih     == True:
        print("running ih check")
        #check_ih()
    if tth    == True:
        print("running tth check")
            #check_tth()
    if astth  == True:
        print("running astth check")
    # yield from slitX2_out() # what if we are not using x2
    # yield from bps.mv(geo.stblx2,samp_x2_start)
    if coarse == True:
        print("running coarse sample height check")
    #  check_coarse()
    return()

# Pre scans
def xr_pre(item):
    print('XRR prescans')
    samp_x2_start=samples[item].pos
    yield from set_mode('XR')
    yield from bps.mv(geo.stblx2,samp_x2_start)
    yield from bps.sleep(10)
    yield from slitX2_out()
    yield from bps.mv(flow2,2.4)
    yield from sample_height_set_fine() #scan the detector arm height from -0.2 to 0.2 with 21 points
    

def xrf_pre(item):
    print('XRF prescans')
    samp_x2_start=runs[item][0].pos
    yield from set_mode('XR')
    yield from bps.mv(geo.stblx2,samp_x2_start)
    yield from bps.sleep(10)
    yield from bps.mv(flow1,collimator_he_rate)
    yield from bps.mv(flow2,constant_he_gid)
    yield from slitX2_out()
    yield from det_set_exposure([detector], exposure_time=1, exposure_number = 1)
    yield from sample_height_set_fine()   #scan the detector arm height from -0.2 to 0.2 with 21 points

def soller_pre(item):
    print('Soller prescans')
    samp_x2_start=samples[item][0].pos
    yield from set_mode('Soller')
    yield from bps.mv(geo.stblx2,samp_x2_start)
    yield from bps.sleep(10)
    yield from bps.mv(flow2,constant_he_gid)
   # yield from bps.mv(geo.stblx2,samp_x2_start+5*x2_direction)   # we need to fix this
    yield from slitX2_out()
    # increase He flow rate a little bit
    slit_x2_offset_block = yield from check_slitX2_block(block_offset=1.5)
    yield from det_set_exposure([detector], exposure_time=1, exposure_number = 1)
    yield from sample_height_set_fine()   #scan the detector arm height from -0.2 to 0.2 with 21 points

def gisaxs_pre(item):
    samp_x2_start=runs[item][0].pos

    def saxs_on():

        # '''For Pilatus1m
        # SAXSY1: 15
        # SAXSY2: 25
        # det2_off(SAXS): -10.8
        # det x = -0.7
        # det y = 0
        # bs_x: -15.82
        # bs_y: 25

        det_saxs_x = -0.7
        det_saxs_y = 0
        fp_saxs_y1 = 15
        fp_saxs_y2 = 35
        yield from bps.mv(fp_saxs.y1,fp_saxs_y1,fp_saxs.y2,fp_saxs_y2)
        yield from bps.mv(detsaxs.x, det_saxs_x)
        yield from bps.mv(detsaxs.y, det_saxs_y)

    yield from saxs_on()

    print('GISAXS prescans')
    yield from set_mode('GISAXS')
    yield from bps.mv(geo.stblx2,samp_x2_start)
    yield from slitX2_out()
    yield from det_set_exposure([detector], exposure_time=1, exposure_number = 1)
    yield from sample_height_set_fine()   


def giwaxs_pre(item):
    print('GIWAXS prescans')
    samp_x2_start=runs[item][0].pos
    yield from set_mode('GIWAXS')
    yield from bps.mv(geo.stblx2,samp_x2_start)  #move the  Sample Table X2 to xpos
    yield from bps.sleep(10)
    yield from slitX2_out()
    yield from bps.mv(flow2,2.5)
    slit_x2_offset_block_new = yield from check_slitX2_bloRck()
    yield from det_set_exposure([pilatus300k], exposure_time=1, exposure_number = 1)
    yield from sample_height_set_fine()   #scan the detector

def pseudo_pre(item):
    print('PSEUDO/GIXOS prescans')
    samp_x2_start=runs[item][0].pos
    yield from set_mode('Soller')
    yield from bps.mv(geo.stblx2,samp_x2_start)  #move the  Sample Table X2 to xpos
    yield from bps.sleep(10)
    yield from sample_height_set_fine()   #scan the detector

def gisaxs_post(item):
    yield from det_set_exposure([detector,quadem], exposure_time=1, exposure_number = 1)
    print('GISAXS is done')


# Post scansure_time=1, exposure_number = 1)
    n_pseudo = n_xr =n_xrf = n_soller = n_gisaxs = n_giwaxs=0

def xrf_post(item):
    yield from det_set_exposure([lambda_det,quadem], exposure_time=1, exposure_number = 1)
    yield from bps.mv(flow2,2.1)
    yield from bps.mv(flow1,0)
    yield from set_mode('XR')
    print('XRF is done')

def soller_post(item):
    yield from det_set_exposure([lambda_det,quadem], exposure_time=1, exposure_number = 1)
    yield from bps.mv(flow2,2.1) ## change He rate back
    print('Soller is done')

def xr_post(item):
    yield from det_set_exposure([detector,quadem], exposure_time=1, exposure_number = 1)
    print('XR  is done')

def xrf_post(item):
    yield from det_set_exposure([lambda_det,quadem], exposure_time=1, exposure_number = 1)
    yield from bps.mv(flow2,2.1)
    yield from bps.mv(flow1,0)
    print('XRF  is done')

def gisaxs_post(item):
    yield from det_set_exposure([detector,quadem], exposure_time=1, exposure_number = 1)
    print('GISAXS is done')

def giwaxs_post(item):

    yield from det_set_exposure([pilatus300k,quadem], exposure_time=1, exposure_number = 1)
    yield from bps.mv(flow2,2.1)
    yield from slitX2_out()
    print('GIWAXS is done')

def pseudo_post(item):
    yield from det_set_exposure([lambda_det,quadem], exposure_time=1, exposure_number = 1)
    yield from bps.mv(flow2,2.1)
    yield from slitX2_out()
    print('Pseudo/GIOXS is done')  


# #file naming, could be extended to add pressure or run number
# def get_name(name,index,type):
#     return(name+'_'+index+'_'+str(type))

# File_types
# None, Sensor1, Sensor2, Kibron, Time

def get_name(index):
    name=runs[index][0].name
    method=runs[index][1]["method"]
    pos=runs[index][0].pos
    name_type=runs[index][0].name_type
    print("name type=",name_type)

    val=5
    other=""
    if name_type == "Kibron":
        other =f"p{val:.0f}_"
    if name_type == "Sensor1_":
        other =f"p{val:.0f}_"
    if name_type == "Sensor2":
        other =f"p{val:.0f}_"
    if name_type == "Time":
        other = f"t{str(int((time.time()-start_time)/60))}_"
    naming = f'{name}_{method}_x{pos:.0f}_{other}{index}'
    return naming

    ## using f-string
    # if File_type == "Kibron": 
    #     naming = f'{name}_P{Kibron:.0f}_{xr_method}_{index}'
    #     return naming
    
    # if File_type == "Sensor1": 
    #     return(name+"_P"+str(int(Sensor1))+"_"+xr_method+"_"+str(index))
    # if File_type == "Sensor2":
    #     return(name+"_P"+str(int(Sensor2))+"_"+xr_method+"_"+str(index))
    # if File_type == "Kibron":
    #     return(name+"_P"+str(int(KibronP))+"_"+xr_method+"_"+str(index))
    # if File_type == "Time":
    #     minutes = str(int((time.time()-start_time)/60))
    #     return(name+"_T"+str(int(minutes))+"_"+xr_method+"_"+str(index))
    # else:
    #     return(name+"_"+str(xr_method)+"_"+str(index))


# we probably need a kibron mode where we add the pressure to the name This was sometimes used in the old code
#samp_name_new = samp_name+f'_P{one_pressure}'samples[item].name

def run():
    if check_commands() ==0:
        print("\a\a\a")
        print("\033[91mERROR: WILL NOT TAKE DATA\033[0m")
        print("\a\a\a")
        return
    all_list = list(range(len(runs)))
    counter=0 
    n_pseudo = n_xr =n_xrf = n_soller = n_gisaxs = n_giwaxs=0

    # sample_n is the sample number
    for item in all_list:
        counter  +=1
        sample_name=runs[item][0].name
        pos=runs[item][0].pos
        method=runs[item][1]["method"].lower()
        print(f'\n\nCurrrently measuring {sample_name} with {method}')

    # method is the method number for each sample

        if method =="checks":
            counter  -=1 # we do not want to increment the count if it is running check_all
            yield from check_all(item)

        if method == "pseudo":
             n_psuedo =counter
             yield from pseudo_pre(item)
             yield from pseudo(item)
             yield from pseudo_post(item)

        if method == "soller":
            n_soller = counter
            #yield from soller_pre(item)
            yield from soller(item)
            #yield from soller_post(item)

        if method == "xrf":
            n_xrf = counter
          #  yield from xrfpre(item)
            yield from xrf(item)
           # yield from xrf_post(item)

        if  method == "xr":
            n_xr = counter
            #yield from xr_pre(item)
            yield from xr(item)
            #yield from xr_post(item)

        if method == "gisaxs":
            n_gisaxs = counter
           # yield from gisaxs_pre(item)
            yield from gisaxs(item)
           # yield from gisaxs_post(item)

        if method == "giwaxs":
            n_giwaxs = counter
          #  yield from giwaxs_pre(other,item)
            yield from giwaxs(item)
           # yield from giwaxs_post(item)

        if method == "giwaxs_bkg":
            n_giwaxs = counter
         #   yield from giwaxs_pre(item)
            yield from giwaxs_bkg(item)
         #   yield from giwaxs_post(item)

        if method == "kibron":
            val=3
            print("running pressure with ",val) # In this case other is the pressure and not the x2 position

        if method == "wait":
            val=3
            print("running wait with ", val)
            yield from bps.sleep(0)

    # yield from det_set_exposure([quadem, lambda_det, pilatus100kA ], exposure_time=1, exposure_number = 1)
    # yield from bps.mv(geo.stblx2,-55)  #move the  Sample Table X2 to the center
    # yield from slitX2_out()
    # yield from set_mode('Soller')
    # # yield from set_mode('XR')
    # yield from mabt(0,0,0)



start_time = time.time()
def run_uccs_twotroughs_timeSeries(clock_to_measure = [7.5,10.5], start_time=start_time):
    ''' 
    run xrr measurements with different incubation time
    Note: need to define an incubation starting point (start_time = time.time())
    clock_to_measure: a list of total waiting time (in hours with respect to start_time) to start each measurement
    '''
    # yield from bps.mv(lambda_det.oper_mode,1)
    # yield from bps.mv(lambda_det.low_thr,6.5)

    detector=lambda_detsoller1

    samp_name_dict = {

        1: 'DMPG+250EGCG+Abeta_1_9',  # front
        2: 'memb+16ugmL_MUC1pTF+Gal3_2_9',  # back
    }

    sam_x2_pos ={
        # center is about -9 by scan a screw in the center # trough size 76
        #    1: [-63],   # front,  flat area [-65, -35] + 8
        #    2: [ 30],   # back,   flat area [ 35 ,  4] - 8

        #    1: [-47],   # front,  flat area [-57, -33] + 8 # for water
        #    2: [ 29],   # back,   flat area [ 42 , 15] - 8 

           1: [-61+7.5],   # front,  flat area [-61, -30] + 8 # for 22mN/m
           2: [ 40-15],   # back,   flat area [ 40 , 12] - 8 
    }

    x2_offset = 7.5 # change sample position for each measurement

    xr_run_dict = {
        1: True,
        2: True,
    }

    gid_run_dict = {
        1: True,
        2: True,
    }

    gisaxs_run_dict = {
        1: True,
        2: True,
    }

    
    for kk,clock in enumerate(clock_to_measure):
        print(f'Start incubation: Wait for {clock: .1f}h of incubation in total.')
        current_time = time.time()
        sleep_time = start_time + clock*60*60 - current_time
        if sleep_time > 1: 
            print(f'Incubate for {sleep_time/60: .1f}min in this round')
            yield from bps.sleep(sleep_time)
        else:
            print(f'No additional incubation time is needed in this round')
            clock = np.round((current_time - start_time)/3600, 1)
            print(f'Currnet clcok is {clock}h.')


            if key == 1: # front one
                x2_direction = 1
            elif key == 2: # back one
                x2_direction = -1

            for ii,samp_x2 in enumerate(samp_x2_list):
                samp_name_new = samp_name+f'_{clock}h'
                print(f'Currrently measuring {samp_name_new}')
                runNum = ii+1
                samp_x2_start = samp_x2+kk*x2_offset*x2_direction
                yield from bps.mv(S2.hg, 0.5)
                yield from bps.mv(S2.vg, 0.05)
                yield from bps.mv(geo.stblx2,samp_x2_start)  #move the  Sample Table X2 to xpos

                yield from check_phi() #resets phi, the crystal deflector at mab(0,0,0)
                yield from check_ih()
                yield from check_astth()
                yield from sample_height_set_coarse()   #scan the detector
                yield from sample_height_set_fine()   #scan the detector 

                if xr_run:
                    print('Starting XRR measurement')
                    yield from set_mode('XR')
                    yield from bps.mv(S2.hg, 0.5)
                    yield from bps.mv(S2.vg, 0.05)
                    yield from bps.mv(geo.stblx2,samp_x2_start)  #move the  Sample Table X2 to xpos
                    yield from bps.sleep(5)
                    yield from det_set_exposure([detector,quadem], exposure_time=1, exposure_number=1)
                    yield from sample_height_set_fine() 
                    yield from one_xrr_new(samp_name_new, x2_direction = x2_direction)
                    yield from det_set_exposure([detector,quadem], exposure_time=1, exposure_number=1)
                    print('XRR is done')

                if gisaxs_run:
                    print('Starting GISAXS measurement')
                    yield from set_mode('GISAXS')
                    yield from bps.mv(S2.hg, 0.3)
                    yield from bps.mv(S2.vg, 0.04) # added the vertical gap for gisaxs
                    yield from bps.mv(geo.stblx2,samp_x2_start+6*x2_direction)  #move the  Sample Table X2 to xpos
                    yield from bps.sleep(5)
                    yield from det_set_exposure([detector,quadem], exposure_time=1, exposure_number = 1)
                    yield from sample_height_set_fine() 
                    yield from gisaxs_scan1(samp_name_new, x2_direction = x2_direction, exposure_time=1)
                    yield from det_set_exposure([detector,quadem], exposure_time=1, exposure_number = 1)
                    yield from bps.mv(S2.hg, 0.5)
                    yield from bps.mv(S2.vg, 0.05)
                    print('GISAXS is done')

                if gid_run:
                    print('Starting GID measurement')
                    yield from set_mode('Soller')
                    yield from bps.mv(S2.hg, 1)
                    yield from bps.mv(S2.vg, 0.1)
                    yield from bps.mv(geo.stblx2,samp_x2_start+6*x2_direction)  #move the  Sample Table X2 to xpos
                    yield from bps.sleep(5)
                    yield from det_set_exposure([detector,quadem], exposure_time=1, exposure_number = 1)
                    yield from sample_height_set_fine() 
                    yield from bps.mv(flow2,2.5)
                    yield from gid_soller1(samp_name_new, x2_direction = x2_direction)
                    yield from det_set_exposure([detector,quadem], exposure_time=1, exposure_number = 1)
                    yield from bps.mv(flow2,2.1)
                    yield from bps.mv(S2.hg, 0.5)
                    print('GID is done')


    yield from det_set_exposure([detector,quadem], exposure_time=1, exposure_number = 1)
    yield from set_mode('XR')
    yield from mabt(0,0,0)



def run_kibron():

    detector=lambda_det

    samp_name = 'PFTeDA_pH12'  # 100uL spread at 4:55am, started compression at 5:05am
    pressure_list   = [    15,    30,    40 ]
    gid_run_list    = [  True,  True,  True ]
    xr_run_list     = [ False,  True, False ]
    gisaxs_run_list = [ False, False, False ]

    GID_highQ = False

    x2_initial = -70

    gisaxs_step = 0
    gid_step = 6.5
    xr_step = 8+3.5
    x2_direction = 1

    atten_slit = -1.873

    samp_x2_interval= np.array(gisaxs_run_list)*gisaxs_step + np.array(gid_run_list)*gid_step + np.array(xr_run_list)*xr_step
    samp_x2_list    = [x2_initial + x2_direction*np.round(np.sum(samp_x2_interval[:step]),1) for step in range(len(pressure_list))]
    print(f'target_pressure = {pressure_list}')
    print(f'x2_position = {samp_x2_list}')

    slit_hg_gisaxs = [0.3]
    for ii,(one_pressure, samp_x2, gisaxs_run, gid_run, xr_run) in enumerate(zip(pressure_list,samp_x2_list, gisaxs_run_list, gid_run_list, xr_run_list)):
        runNum = ii+1
        yield from bps.mv(S2.hg, 0.5)
        yield from bps.mv(geo.stblx2,samp_x2)  #move the  Sample Table X2 to xpos

        kibron.runConstantPressure(target_pressure=one_pressure, target_speed = 10)
        print('Sleep to wait for target pressure')
        if runNum > 0:
            yield from bps.sleep(3*60)

            # yield from check_phi() #resets phi, the crystal deflector at mab(0,0,0)
            yield from check_ih()
        yield from check_astth()
            

        if gisaxs_run:
            print('Starting GISAXS measurement')
            yield from set_mode('GISAXS')
            for kk,slit_hg in enumerate(slit_hg_gisaxs):
                print('Slit horizontal gap is set to %.2f'%slit_hg)
                yield from bps.mv(S2.hg, slit_hg)
                yield from bps.mv(S2.vg, 0.08) # added the vertical gap for gisaxs
                yield from det_set_exposure([detector], exposure_time=1, exposure_number = 1)
                yield from sample_height_set_fine()   #scan the detector arm height from -0.2 to 0.2 with 21 points
                # yield from sample_height_set_fine_pilatus(detector=pilatus300k)   #scan the detector
                yield from gisaxs_scan1(samp_name+f'_P{one_pressure}', x2_direction = x2_direction)
                yield from det_set_exposure([detector,quadem], exposure_time=1, exposure_number = 1)
                # yield from bps.mv(S2.hg, 0.3)

        
        if gid_run:

            print('Starting GID measurement')
            yield from set_mode('Soller')
            yield from bps.mv(S2.hg, 0.5)
            yield from bps.mv(S2.vg, 0.08) 
            # yield from bps.mv(fp_saxs.y1,50,fp_saxs.y2,35)# with extension for gisaxs flight path
            yield from bps.mv(fp_saxs.y1,15,fp_saxs.y2,35)# for normal run without SAXS flight path extension
            yield from bps.mv(geo.stblx2,samp_x2+0*x2_direction)  #move the  Sample Table X2 to xpos
            yield from bps.sleep(5)
            ## increase He flow rate a little bit
            # yield from he_on(constant_rate=2.5)
            yield from bps.mv(flow2,2.5)
            yield from sample_height_set_fine()
            x2_original = x2.position
            samp_name_new = samp_name+f'_P{one_pressure}_lowQ'
            
            # ##### for binary
            # yield from gid_soller2(samp_name_new, x2_direction = x2_direction, atten=atten_slit, wait_time=0.5, expo_time=10)

            #### for single component
            yield from gid_soller2_short(samp_name_new, x2_direction = x2_direction, atten=atten_slit, wait_time=0.5, expo_time=10)

            ## change He rate back
            # yield from he_on(constant_rate=2.1)
            yield from bps.mv(flow2,2.1)
            yield from det_set_exposure([detector,quadem], exposure_time=1, exposure_number = 1)
            yield from bps.mv(S2.hg, 0.5)
            yield from bps.mv(S2.vg, 0.08)
            print('GID is done')



            ##### For high q measurements
            if GID_highQ:
                print('Starting GID measurement: high Q')
                yield from set_mode('Soller')
                yield from bps.mv(S2.hg, 0.5)
                yield from bps.mv(S2.vg, 0.08) 
                # yield from bps.mv(fp_saxs.y1,50,fp_saxs.y2,35)# with extension for gisaxs flight path
                yield from bps.mv(fp_saxs.y1,15,fp_saxs.y2,35)# for normal run without SAXS flight path extension
                yield from bps.mv(geo.stblx2,samp_x2+3.5*x2_direction)  #move the  Sample Table X2 to xpos
                yield from bps.sleep(5)
                ## increase He flow rate a little bit
                # yield from he_on(constant_rate=2.5)
                yield from bps.mv(flow2,2.5)
                yield from sample_height_set_fine()
                x2_original = x2.position
                samp_name_new = samp_name+f'_P{one_pressure}_highQ'
                yield from gid_soller3(samp_name_new, x2_direction = x2_direction, atten=atten_slit, wait_time=0.5, expo_time=15)
                ## change He rate back
                # yield from he_on(constant_rate=2.1)
                yield from bps.mv(flow2,2.1)
                yield from det_set_exposure([detector,quadem], exposure_time=1, exposure_number = 1)
                yield from bps.mv(S2.hg, 0.5)
                yield from bps.mv(S2.vg, 0.08)
                print('GID is done')



        if xr_run:
            print('Starting XRR measurement')
            yield from set_mode('XR')
            yield from bps.mv(S2.hg, 0.5)
            yield from bps.mv(S2.vg, 0.08)
            # yield from bps.mv(fp_saxs.y1,50,fp_saxs.y2,35)# with extension for gisaxs flight path
            yield from bps.mv(fp_saxs.y1,15,fp_saxs.y2,35)# for normal run without SAXS flight path extension
            yield from bps.mv(geo.stblx2,samp_x2+7*x2_direction)  #move the  Sample Table X2 to xpos

            yield from check_astth() # check astth

            yield from bps.sleep(5)
            yield from sample_height_set_fine() #scan the detector arm height from -0.2 to 0.2 with 21 points
            samp_name_new = samp_name+f'_P{one_pressure}'
            yield from one_xrr_new(samp_name_new, x2_direction = x2_direction)
            yield from det_set_exposure([detector,quadem], exposure_time=1, exposure_number = 1)
            print('XRR is done')



        # print("Starting incubation for 1 hour...")  
        # yield from bps.sleep(1*60*60)

        yield from det_set_exposure([detector,quadem], exposure_time=1, exposure_number = 1)
        # yield from bps.mv(geo.det_mode,1)
        # yield from mabt(0,0,0)


    kibron.runConstantPressure(target_pressure=1, target_speed = 70)
    print('Compression is finishied; stop the Kibron')
    kibron.device.call('StepStop')
    kibron.device.call('StopMeasure')



def kibron_stop_measure():
    kibron.device.call("StopMeasure")


################### TO USE KIBRON ####################
# To start, run these commands in the bluesky finescanbelow
    # HOST, PORT = "10.66.91.26", 9897 ## HZ
    # sock = mtx.connect(HOST, PORT)
    # device = mtx.Trough(sock)
    # kibron = KibronTrough(device, sock)
# To stop the measurement:
    # kibron.device.call('StepStop')
    # kibron.device.call('StopMeasure')

#     # kibron_stop_measure()
# def kibron_stop_measure():
    # kibron.device.call('StepStop')
    # kibron.device.call('StopMeasure')
# To stop the remote server:
    # kibron.close()
######################################################
# this should eventually go into 90-setup.py
# this version of dscanr will allways user per_setp=flash
