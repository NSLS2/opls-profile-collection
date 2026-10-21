import pprint

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


atten_slit = 0 # -1.767 # -1.7843
soller_tran_soller = 4 # 5.5 # 5.5 # 4
soller_tran_gap = -1.5 # 4 # 5 # to use the center gap on the soller slits
constant_he_gid = 2.6 # 2.5 #2.6
collimator_he_rate = 2.2 



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

def setup():
    x2_direction = -1 # 1
    num_repeat = 10 
    gid_repeat = False
    xrf_repeat = False
    skip_gid = False

    samp_name_dict = {
        1: 'C263_A5_NH42SO4_10mM_Run2', # front, 32mL, loaded at 11am; run at 11:20am (XRF)
        2: 'C263_A4_PFOS_DoTAB_6uM_ea_Run2', # front, 32mL, loaded at 6:47pm; run at xxpm (PXR/GID/XRF/XRR)
    }

    samp_x2_pos ={
        1: [-93.4+76.2/2 ],    # front,  -55.3
        2: [-93.4+76.2/2+76.2+5],  # back # remove -5 if not doing time dependence
    }   
    return(samp_name_dict,samp_x2_pos)


def xdict():

# Need to figure out what to do with this code, will do last
    pxr_run_dict = {
        1: False,
        2: False,
        3: False
    }

# Chaning gid to soller, must change in other places
    soller_run_dict = {
        1: False,
        2: False,
        3: False,
    }

    xr_run_dict = {
        1: False,
        2: False,
        3: False, 
    }

    xrf_run_dict = {
        1: False, 
        2: False, 
        3: False,
    }

    gisaxs_run_dict = {
        1: False,
        2: False,
        3: False,
    }

    giwaxs_run_dict = {
        1: False,
        2: False,
        3: False,
    }
    return(pxr_run_dict, soller_run_dict, xr_run_dict, xrf_run_dict, gisaxs_run_dict, giwaxs_run_dict )

# slit_x2 to sample distance: ~87mm, HZ, 2025/06/20


# This is where the type of XR scans are defined.
# Below is the case where all of the scans are the same and from a scan file
# This could be generalized so that they are different by using if statements
# Could also include calling old fashion scans that were hard wired
def xr(number):
    print("Running XR scan for sample",str(number)[0], "for ", samp_name_dict[number])
#    yield from xr_scan_file(samp_name_dict[number],"xr_scan1.csv","all",99,scan_dir="global", auto_atten=False)

# This is where the type of XRF scans are defined. The same as xr() except the name
# Below is the case where all of the scans are the same and from a scan file
# This could be generalized so that they are different by using if statements
# Could also include calling old fashion scans that were hard wired
def xrf(number):
    print("Starting XRF scan for sample",str(number)[0], "for ", samp_name_dict[number])
    if xrf_short:
        print("we would need to fill in")
    else:
  #      yield from xrf_scan_file(samp_name_dict[number],"xr_scan1.csv","all",99,scan_dir="global", auto_atten=False)
        print("scan commented out")

# This is where the type of Soller scans are defined.  This does not read from a file.
# This can be generalized so that different samples used different scans
# Currently this is define in q space but the intent is to write this in anngle space
def soller(number,start=1.3,q_end=1.8,npts=21,exp_time=20):
    print("Soller scan for sample",str(number)[0], "for ", samp_name_dict[number])
    print("From q=",q_start, "to", q_end, "with", npts, "points for",exp_time, "sec")
#   yield from soller_scanq(samp_name_dict[number], block_pos = 0,q_start,q_end,npts,exp_time, x2_direction=1,alpha_i=0.0728, wait_time=5, atten=-1.775): # block edge at -31.5
    print('Starting Soller measurement')

# This is where the type of GISAXS scans are defined.  This does not read from a file.
# This can be generalized so that different samples used different scans
def gisaxs(number):
    print("Starting GISAXS scan for sample",str(number)[0], "for ", samp_name_dict[number])
    #yield from gisaxs_scan(samp_name_dict[number], x2_direction = x2_direction, atten=atten_slit)


# This is where the type of GIWAXS scans are defined.  This does not read from a file.
# This can be generalized so that different samples used different scans
def giwaxs(number):
    print("Starting GIWAXS scan for sample",str(number)[0], "for ", samp_name_dict[number])
    name=samp_name_dict[number]
    #yield from giwaxs_scan(name+'_giwaxs', incident_angle=0.0728, atten=atten_slit, block_pos=60, exposure_time=30, use_slitx2=True, slit_x2_offset_block=slit_x2_offset_block_new)
    #yield from giwaxs_scan_bkg(name+'_giwaxs_bkg', incident_angle=0.0728, atten=atten_slit, block_pos=60, exposure_time=30, use_slitx2=True, sh_offset=-1, slit_x2_offset_block=slit_x2_offset_block_new)

# This is where the type of PSEUDO scans are defined.  This does not read from a file.
# This can be generalized so that different samples used different scans
# Here we would probably want to inlude other descriptors such as a list of stth values

def pxr(number):
    print("Starting Pseudo XR scan for sample",str(number)[0], "for ", samp_name_dict[number])
    #yield from gixos_multiqxy(samp_name_dict[number]+'_pxr', alpha = 0.0728, 
    #    num_point = 1, exp_time = 30, 
    #    x2_per_step = 0, atten=-1.5,
    #    slit='slit_x2')


# Pre scans
def xr_pre():
    print('XRR prescans')
    yield from slitX2_out()
    yield from set_mode('XR')
    yield from bps.mv(flow2,2.4)
    yield from bps.mv(geo.stblx2,samp_x2_start-5*x2_direction)
    yield from bps.sleep(15)
    yield from sample_height_set_fine() #scan the detector arm height from -0.2 to 0.2 with 21 points
    

def xrf_pre():
    print('XRF prescans')
    yield from bps.mv(flow1,collimator_he_rate)
    yield from bps.mv(flow2,constant_he_gid)
    yield from slitX2_out()
    yield from bps.sleep(2*60)
    yield from det_set_exposure([detector], exposure_time=1, exposure_number = 1)
    yield from bps.mv(geo.stblx2,samp_x2_start+2.5*x2_direction) # Normal run
    yield from bps.sleep(15)
    yield from sample_height_set_fine()   #scan the detector arm height from -0.2 to 0.2 with 21 points

def soller_pre():
    print('Soller prescans')
    yield from set_mode('Soller')
    yield from bps.mv(flow2,constant_he_gid)
    yield from bps.mv(geo.stblx2,samp_x2_start+5*x2_direction)   # we need to fix this
    yield from slitX2_out()
    yield from bps.sleep(15)
    # increase He flow rate a little bit
    yield from sample_height_set_fine()
    x2_original = x2.position
    slit_x2_offset_block = yield from check_slitX2_block(block_offset=1.5)

def gisaxs_pre():
    print('GISAXS prescans')
    yield from set_mode('GISAXS')
    yield from slitX2_out()
    yield from bps.mv(geo.stblx2,samp_x2_start+8.5*x2_direction)  #move the  Sample Table X2 to xpos
    yield from bps.sleep(5)
    yield from det_set_exposure([detector], exposure_time=1, exposure_number = 1)
    yield from sample_height_set_fine()   #scan the detector
    x2_nominal= geo.stblx2.position

def giwaxs_pre():
    print('GIWAXS prescans')
    yield from set_mode('Soller')
    yield from slitX2_out()
    yield from sample_height_set_fine()   #scan the detector
    yield from bps.mv(flow2,2.5)
    yield from det_set_exposure([pilatus300k], exposure_time=1, exposure_number = 1)
    slit_x2_offset_block_new = yield from check_slitX2_bloRck()
    yield from giwaxs_scan1(ii)

def pxr_pre():
    print('PSEUDO/GIXOS prescans')
    yield from set_mode('Soller')
    yield from slitX2_out()
    yield from bps.mv(flow2,constant_he_gid)
    yield from set_mode('Soller')
    yield from bps.mv(geo.stblx2,samp_x2_start+8*x2_direction)  # normal run
    yield from bps.sleep(5)
    yield from sample_height_set_fine()


# Post scans
def xr_post():
    yield from det_set_exposure([detector,quadem], exposure_time=1, exposure_number = 1)
    print('XR Soller is done')

def xrf_post():
    yield from bps.mv(flow2,2.1)
    yield from bps.mv(flow1,0)
    yield from set_mode('XR')
    print('XRF Soller is done')

def soller_post():
    yield from bps.mv(flow2,2.1) ## change He rate back
    yield from det_set_exposure([pilatus100kA,quadem], exposure_time=1, exposure_number = 1)
    print('Soller is done')

def gisaxs_post():
    yield from det_set_exposure([detector,quadem], exposure_time=1, exposure_number = 1)
    print('GISAXS is done')

def giwaxs_post():
    yield from giwaxs_scan1_bkg(ii)
    yield from det_set_exposure([pilatus300k,quadem], exposure_time=1, exposure_number = 1)
    yield from bps.mv(flow2,2.1)
    yield from slitX2_out()
    print('GIWAXS is done')

def pxr_post():
    yield from det_set_exposure([lambda_det,quadem], exposure_time=1, exposure_number = 1)
    yield from bps.mv(flow2,2.1)
    yield from slitX2_out()
    print('Pseudo/GIOXS is done')


# we probably need a kibron mode where we add the pressure to the name This was sometimes used in the old code
#samp_name_new = samp_name+f'_P{one_pressure}'
     
def run_threetroughs():
    ''' 
    run three Teflon troughs
    '''
    detector=lambda_det
    samp_name_dict,sam_x2_pos=setup()
    pxr_run_dict, soller_run_dict, xr_run_dict, xrf_run_dict, gisaxs_run_dict, giwaxs_run_dict = xdict()
  #  printSampleInfo(samp_name_dict,sam_x2_pos,xr_run_dict,xrf_run_dict,soller_run_dict,gisaxs_run_dict,pxr_run_dict)

    print('Starting running...')
    x2_offset = 0 # change sample position for each measurement
    for key in samp_name_dict:
        samp_name = samp_name_dict[key]
        samp_x2_list = sam_x2_pos[key]
        gisaxs_run = gisaxs_run_dict[key]
        soller_run = soller_run_dict[key]
        xr_run = xr_run_dict[key]
        xrf_run = xrf_run_dict[key]
        pxr_run = pxr_run_dict[key]
        giwaxs_run = giwaxs_run_dict[key]

        x2_direction = -1 # 1

        # yield from slitX2_out()
        yield from set_S2Size([0.25,0.08])
        for ii,samp_x2 in enumerate(samp_x2_list):
            samp_name_new = samp_name
            print(f'Currrently measuring {samp_name_new}')
            runNum = ii+1
            samp_x2_start = samp_x2+x2_offset*x2_direction

            # yield from bps.mv(geo.stblx2,samp_x2_start)  #move the  Sample Table X2 to xpos
            # yield from slitX2_out()
            # yield from bps.mv(flow2,constant_he_gid)
            # yield from bps.mv(flow1,collimator_he_rate)
            # yield from check_phi() #resets phi, the crystal deflector at mab(0,0,0)
            # yield from check_ih()
            # yield from check_astth()
            # yield from sample_height_set_coarse()   
            # yield from sample_height_set_fine(finescan=False)   

            if pxr_run:
                pxr_pre()
                pxr(ii)
                pxr_post()

            if soller_run:
                soller_pre()
                soller(ii)
                soller_post()

            if xrf_run:
                xrf_pre()
                xrf(ii)
                xrf_post()

            if xr_run:
                xr_pre()
                xr(ii)
                xr_post()

            if gisaxs_run:
                gisaxs_pre()
                gisaxs(ii)
                gisaxs_post()

            if giwaxs_run:
                giwaxs_pre()
                giwaxs(ii)
                giwaxs_post()

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
