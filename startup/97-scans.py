import ast, os
import matplotlib.pyplot as plt 
import csv 
import os
import numpy as np
import pandas as pd
import pprint


# #  These would eventually be dfine to control the type of scan, like  RE(soller_scan_new("ben_test",q_start=1.25,q_end=1.75,npts=17))
#  #xr_scan_file(sample_name,scan_name,start,end,scan_dir="global", auto_atten=False): 
#     def xr0(): print("running xr1 with file ",sample_name_dict[0])
#     def xr1(): print("running xr1 with file ",sample_name_dict[1])
#     def xr2(): print("running xr1 with file ",sample_name_dict[2])


# If TRUE than we can pick the scan detail 
#     if ii == 0: yield from xr0()
#     if ii == 1: yield from xr1()
#     if ii == 1: yield from xr2()


# Safely converts a value into a floating-point number (float) without crashing the program if the conversion fails
def to_float_safe(val):
    try:
        return float(val)
    except ValueError:
        return val  # Keep as original string, or return None/skip
    
#This Python function extracts a row of data from a Pandas DataFrame,
#converts its values into floating-point numbers, and returns them as a standard Python list.    
def try_int_safe(val):
    val_maybe_float = to_float_safe(val)
    if(type(val_maybe_float) == type(.2)):
        return int(val_maybe_float)
    else:
        return val_maybe_float

# Extract a row from a Pandas DataFrame by its name, safely convert every value in that row into a float where possible,
# and return the result as a standard Python list. 
def trans1(name,tmp):
    return [to_float_safe(item) for item in tmp.loc[name].tolist()]

# Extracts a row from a Pandas DataFrame by its name, safely converts every value into an integer where possible,
# and returns the result as a standard Python list.
def trans2(name,tmp):
    return [try_int_safe(item) for item in tmp.loc[name].tolist()]


# Runs a reflectivity scans from a file
def xr_scan_file(sample_name,scan_name,start,end,scan_dir="global", auto_atten=False): 
    print("starting xr_scan_file,  sample name =",sample_name)

    if start == "all":
        start=0
        end=99
    if scan_dir=="global":
        print("global directory")
        directory='/home/xf12id1/.ipython/profile_collection/startup/scans/'

    else:
        print("local directory")
 #       user="ocko"
 #       user="tobias_cornell"
        directory="/home/xf12id1/.ipython/profile_collection/startup/users/"+scan_dir+"/scans/"
    print(directory)
    
    tmp=pd.read_csv(directory+scan_name,skiprows=0, sep='\s+')

    scan_p={
    "start":trans1('alpha_start',tmp)[start:end],
    "stop":trans1('alpha_stop',tmp)[start:end],
    "n":trans2('number_points',tmp)[start:end],
    "atten":trans2('auto_atten',tmp)[start:end],
    "s2vg":trans1('s2_vg',tmp)[start:end],
    "exp_time":trans1('exp_time',tmp)[start:end],
    "pre_time":trans1('precount_time',tmp)[start:end],
    "wait_time":trans1('wait_time',tmp)[start:end],
    "x2_offset_start":trans1('x2_offset_start',tmp)[start:end],
    "x2_offset_stop":trans1('x2_offset_stop',tmp)[start:end],
    "beam_block_offset":trans1('block_offset',tmp)[start:end],
    }

    if auto_atten:
        scan_p['atten'] = ['auto' for _ in range(len(scan_p['atten']))]
  
    pprint.pprint(scan_p,sort_dicts=False)
    yield from bps.mv(geo.det_mode,1)
    # yield from reflection_scan_full(scan_param=scan_p,
    #     md={'sample_name': sample_name},
    #     detector=lambda_det, 
    #     tilt_stage=False)
    return

# scan_p=xr_scan_file("test","foo4a.csv","all",3,"global")
# pprint.pprint(scan_p)

#
def xrf_scan_file(sample_name,scan_name,start,end,scan_dir="global", auto_atten=False):
    print("auto atten=",auto_atten)

    if start == "all":
        start=0
        end=99
    if scan_dir=="global":
        print("global directory")
        directory='/home/xf12id1/.ipython/profile_collection/startup/scans/'

    else:
        print("local directory")
 #       user="ocko"
 #       user="tobias_cornell"
        directory="/home/xf12id1/.ipython/profile_collection/startup/users/"+scan_dir+"/scans/"
    print(directory)
    
    tmp=pd.read_csv(directory+scan_name,skiprows=0, sep='\s+')
    print("scan name")
    scan_p={
    "start":trans1('alpha_start',tmp)[start:end],
    "stop":trans1('alpha_stop',tmp)[start:end],
    "n":trans2('number_points',tmp)[start:end],
    "atten":trans2('auto_atten',tmp)[start:end],
    "s2vg":trans1('s2_vg',tmp)[start:end],
    "exp_time":trans1('exp_time',tmp)[start:end],
    "wait_time":trans1('wait_time',tmp)[start:end],
    "x2_offset_start":trans1('x2_offset_start',tmp)[start:end],
    "x2_offset_stop":trans1('x2_offset_stop',tmp)[start:end],
    }

    if auto_atten:
        scan_p['atten'] = auto_atten
    
    pprint.pprint(scan_p,sort_dicts=False)

#     yield from bps.mv(geo.det_mode,1)
    yield from bps.mv(abs3,1)
#     yield from reflection_fluorescence_scan_full(scan_param=scan_p,
#         md={'sample_name': name},
#         detector=xs, 
#         tilt_stage=False,)
#     # yield from bps.mv(abs3,0)
    return


def soller_scanq(name, block_pos = 0,q_start=1.3,q_end=1.8,npts=21,exp_time=20, x2_direction=1,alpha_i=0.0728, wait_time=5, atten=-1.775): # block edge at -31.5
    th_start= (180/np.pi)*np.asin(q_start*geo.wlength/4/np.pi)*2
    th_end  = (180/np.pi)*np.asin(q_end*geo.wlength/4/np.pi)*2
    th_start = float(f"{th_start:0.1f}")
    th_end = float(f"{th_end:0.1f}")
 #   print("th_start=",th_start,"th_end=",th_end)

    stth_start_list =    [th_start]
    stth_stop_list =     [th_end]
    number_points_list = [npts]
    exp_time_list      = [exp_time]
    x2_range_list      = [4*x2_direction]
    atten_2_list       = [atten]
    wait_time_list     = [wait_time]

    scan_dict={
        "start":stth_start_list, 
        "stop":stth_stop_list,
        "n":number_points_list,
        "exp_time":exp_time_list,
        "x2_range":x2_range_list,
        "atten_2":atten_2_list,
        "wait_time":wait_time_list,
      }
    pprint.pprint(scan_dict,sort_dicts=False)


    # yield from bps.mov(block.y,block_pos)
    # yield from bps.mv(soller.tran,-6)
    yield from bps.mv(soller.tran,5.5)
#     x2_position_original = x2.position
#     yield from bps.mov(slit_x2,slit_x2_offset_block-x2_position_original)

# #mode 5 is for GID with soller
#     yield from bps.mv(geo.det_mode,5)
#     yield from bps.mv(geo.track_mode,2)
#     # yield from bps.mv(fp_saxs.y1,50,fp_saxs.y2,35)# with extension for gisaxs flight path
#     yield from bps.mv(fp_saxs.y1,15,fp_saxs.y2,35)# for normal run without extension
#     print("calling GID_soller")
#     yield from gid_scan_soller(scan_dict,
#                                 md={'sample_name': name}, 
#                                 detector = pilatus100kA,
#                                 alphai = alpha_i,
#                                 beamstop = None,
#                                 )
    
#     yield from bps.mv(abs2,5)
#     # yield from bps.mv(geo.det_mode,1)
#     # yield from bps.mv(geo.track_mode,1)
#     # yield from bps.mov(block.y,60)
#     yield from slitX2_out()

    return


def gisaxs_scan(name, incident_angle = 0.0728, x2_direction=1, bs_pos = -15.82, atten = 0, exposure_time=1):

    '''For Pilatus1m
    SAXSY1: 15
    SAXSY2: 25
    det2_off(SAXS): -10.8
    det x = -0.7
    det y = 0
    bs_x: -15.82
    bs_y: 25

    
    '''
    det_saxs_x = -0.7
    det_saxs_y_list         = [0, 0]
    det_saxs_y_offset_list  = [0, 1]
    stth_list               = [0, 0]
    exp_time_list           = [exposure_time, exposure_time] 
    x2_offset_list          = [0*x2_direction, 0*x2_direction]
    atten_2_list            = [atten for _ in range(len(det_saxs_y_list))]
    wait_time_list          = [10, 10]
    beam_stop_x             = [bs_pos for _ in range(len(det_saxs_y_list))]
    beam_stop_y             = [25, 25] # low the bs to have low qxy signal

    scan_dict={"det_saxs_y":det_saxs_y_list,
        "det_saxs_y_offset":det_saxs_y_offset_list,
        "stth":stth_list,
        "exp_time":exp_time_list,
        "x2_offset":x2_offset_list,
        "atten_2":atten_2_list,
        "wait_time":wait_time_list,
        "beam_stop_x":beam_stop_x,
        "beam_stop_y":beam_stop_y,}

    # block_yo = block.y.position #
    # yield from bps.mov(block.y,60)

    yield from bps.mv(geo.det_mode,2)
    yield from bps.mv(detsaxs.x, det_saxs_x)
    # yield from beta_gid(2.3,0)
    # yield from bps.mv(abs2,0)
   # yield from bps.mv(fp_saxs.y1,20,fp_saxs.y2,40)# with vertical mirrors
    yield from bps.mv(fp_saxs.y1,20-5,fp_saxs.y2,40-5)# with CRLS
    print("calling GID_stitch")
    yield from gid_scan_stitch(scan_dict,
                                md={'sample_name': name}, 
                                detector = pilatus1m,
                                alphai = incident_angle)

    yield from bps.mv(abs2,5)
    # block_yo = block.y.position
    # yield from bps.mov(block.y,block_yo)

atten_slit =0
def giwaxs_scan(name, incident_angle = 0.0728, x2_direction=1, block_pos = 60, atten = atten_slit, 
                 exposure_time=1, tth=0, use_slitx2 = True, slit_x2_offset_block=43.955):


    '''For Pilatus300k for GIWAXS

    '''
    det_saxs_y_list         = [0]
    det_saxs_y_offset_list  = [0]
    stth_list               = [tth]
    exp_time_list           = [exposure_time] 
    x2_offset_list          = [0*x2_direction]
    atten_2_list            = [atten for _ in range(len(det_saxs_y_list))]
    wait_time_list          = [5]
    beam_stop_x             = [bstop.x.position for _ in range(len(det_saxs_y_list))]
    beam_stop_y             = [bstop.y.position for _ in range(len(det_saxs_y_list))] 

    scan_dict={"det_saxs_y":det_saxs_y_list,
        "det_saxs_y_offset":det_saxs_y_offset_list,
        "stth":stth_list,
        "exp_time":exp_time_list,
        "x2_offset":x2_offset_list,
        "atten_2":atten_2_list,
        "wait_time":wait_time_list,
        "beam_stop_x":beam_stop_x,
        "beam_stop_y":beam_stop_y,}

    # block_yo = block.y.position #
    yield from bps.mov(block.y,block_pos)
    if use_slitx2:
            x2_position_original = x2.position
            yield from bps.mov(slit_x2,slit_x2_offset_block-x2_position_original)


    yield from bps.mv(geo.det_mode,3)
    # yield from bps.mv(fp_saxs.y1,15,fp_saxs.y2,40)# with CRLS
    # yield from bps.mv(fp_saxs.y1,50,fp_saxs.y2,35)# use the gid setting
    yield from bps.mv(fp_saxs.y1,15,fp_saxs.y2,35)# for normal run without extension
    print("calling GID_stitch")
    yield from gid_scan_stitch(scan_dict,
                                md={'sample_name': name}, 
                                detector = pilatus300k,
                                alphai = incident_angle)

    yield from bps.mv(abs2,5)
    yield from bps.mov(block.y,60)
    if use_slitx2:
        # yield from bps.mov(slit_x2,-9.5)
        yield from slitX2_out()




def giwaxs_scan_bkg(name, incident_angle = 0.0728, x2_direction=1, block_pos = 60, atten = atten_slit, exposure_time=1, tth=0, use_slitx2 = True, slit_x2_offset_block=43.955, sh_offset = -1):


    '''For Pilatus300k for GIWAXS, lower the sh by -1 to get a chamber background

    '''
    det_saxs_y_list         = [0]
    det_saxs_y_offset_list  = [0]
    stth_list               = [tth]
    exp_time_list           = [exposure_time] 
    x2_offset_list          = [0*x2_direction]
    atten_2_list            = [atten for _ in range(len(det_saxs_y_list))]
    wait_time_list          = [5]
    beam_stop_x             = [bstop.x.position for _ in range(len(det_saxs_y_list))]
    beam_stop_y             = [bstop.y.position for _ in range(len(det_saxs_y_list))] 

    scan_dict={"det_saxs_y":det_saxs_y_list,
        "det_saxs_y_offset":det_saxs_y_offset_list,
        "stth":stth_list,
        "exp_time":exp_time_list,
        "x2_offset":x2_offset_list,
        "atten_2":atten_2_list,
        "wait_time":wait_time_list,
        "beam_stop_x":beam_stop_x,
        "beam_stop_y":beam_stop_y,}

    # block_yo = block.y.position #
    yield from bps.mov(block.y,block_pos)
    if use_slitx2:
            x2_position_original = x2.position
            yield from bps.mov(slit_x2,slit_x2_offset_block-x2_position_original)


    yield from bps.mv(geo.det_mode,3)
    # yield from bps.mv(fp_saxs.y1,15,fp_saxs.y2,40)# with CRLS
    # yield from bps.mv(fp_saxs.y1,50,fp_saxs.y2,35)# use the gid setting
    yield from bps.mv(fp_saxs.y1,15,fp_saxs.y2,35)# for normal run without SAXS flight path extension
    print("calling GID_stitch")
    yield from gid_scan_stitch(scan_dict,
                                md={'sample_name': name}, 
                                detector = pilatus300k,
                                alphai = incident_angle,
                                sh_offset = sh_offset)

    yield from bps.mv(abs2,5)
    yield from bps.mov(block.y,60)
    if use_slitx2:
        # yield from bps.mov(slit_x2,-9.5)
        yield from slitX2_out()



    
def gixos_transverse_sth(name, bkg_name, qxy_list = [0.04], alpha = 0.0728, atten = -1.775, 
                         sh_offset_pos = 0, x2_per_step =0, exp_time = 30, 
                         num_point =1, soller_tran = -1,
                         final_sthreturn=True, final_blockreturn=True):
    '''
    alpha_c = 0.085 at E = 14.4keV,
    85% alpha_c = 0.085*0.85
    uses transverse sth
    '''
    for qxy_pos in qxy_list[:-1]:
        print('inside for loop')
        print('gixos qxy: %.3f /A' % qxy_pos)
        yield from gixos_sth(name, qxy=qxy_pos, atten = atten, alpha = alpha, sh_offset = sh_offset_pos, 
                             exp_time = exp_time, num_point = num_point, soller_tran = soller_tran,
                             sthreturn = False, blockreturn = False)
        print('gixos bkg qxy: %.3f /A' % qxy_pos)
        yield from gixos_sth(bkg_name, qxy=qxy_pos, atten = atten, alpha = alpha, sh_offset = sh_offset_pos-1, 
                             exp_time = exp_time, num_point = num_point, soller_tran = soller_tran,
                             sthreturn = False, blockreturn = False)
        if x2_per_step != 0:
            yield from bps.mvr(x2, x2_per_step)
    
    print('Outside for loop')
    print('gixos qxy: %.3f /A' % qxy_list[-1])
    yield from gixos_sth(name, qxy=qxy_list[-1], atten = atten, alpha = alpha, sh_offset = sh_offset_pos, 
                         exp_time = exp_time, num_point = num_point, soller_tran = soller_tran,
                         sthreturn = False, blockreturn = False)
    print('gixos bkg qxy: %.3f /A' % qxy_list[-1])
    yield from gixos_sth(bkg_name, qxy=qxy_list[-1], atten = atten, alpha = alpha, sh_offset = sh_offset_pos-1, 
                         exp_time = exp_time, num_point = num_point, soller_tran = soller_tran,
                         sthreturn = final_sthreturn, blockreturn = final_blockreturn)
 
    if x2_per_step != 0:
        yield from bps.mvr(x2, x2_per_step)


def gixos_transverse_nochamber(name, qxy_list = [0.04], alpha = 0.0728, atten = -1.775, sh_offset_pos = 0, 
                               x2_per_step =0, exp_time = 30):
    '''
    alpha_c = 0.085 at E = 14.4keV,
    85% alpha_c = 0.085*0.85
    '''
    for qxy_pos in qxy_list:
        yield from gixos(name, qxy=qxy_pos, atten = atten, alpha = alpha, sh_offset = sh_offset_pos, exp_time = exp_time)
        # yield from gixos(bkg_name, qxy=qxy_pos, atten = atten, alpha = alpha, sh_offset = sh_offset_pos-1, exp_time = exp_time)
        if x2_per_step != 0:
            yield from bps.mvr(x2, x2_per_step)

def gixos_multiqxy(name, alpha = 0.0728, num_point = 1, exp_time = 30, x2_per_step = 0, 
                   atten = -1.5, soller_tran=-1.5, slit='slit_x2'):
    '''
    slit: select the slits to be used in the PXR, HZ 2026-03-13
    1) 'slit_x2': using the slit_x2 insde the chamber
    2) 'slit_blocker': using the block.y outside the chamber
    3) 'both': using both slits
    
    '''
    ener = energy.energy.position # in eV 
    wavelength = 12400 / ener 
  #  qxy_list = [0.04, 0.05, 0.06, 0.08, 0.1, 0.15, 0.20, 0.25]
    # qxy_list = [0.03, 0.04, 0.05, 0.06, 0.08, 0.1, 0.15, 0.20, 0.25]
    #qxy_list = [0.04, 0.06, 0.1, 0.15, 0.3184, 0.4, 0.5]
    qxy_list = [0.04, 0.06, 0.08, 0.1, 0.15, 0.20]
    

    #tth_bulk = np.linspace(2.5, 7, 19)
    #qxy_list = [0.04, 0.05, 0.06, 0.1, 0.20]
    #tth_bulk = np.linspace(2.5, 6.5, 9)
    tth_bulk = np.array([2.5])
    qxy_list_bulk = 4*np.pi*np.sin(np.deg2rad(tth_bulk/2))/wavelength
    # # start moving blocks
    yield from set_mode('Soller')
    yield from mabt(0,0,0)
    # yield from bps.mv(block.y, 0)
    if slit == 'slit_x2':
        try:
            yield from blocker_out()
        except:
            print('Sample_BS (block.y) might not be connected!')
        yield from check_slitX2()
    elif slit == 'slit_blocker':
        yield from slitX2_out()
        yield from check_block_slit()
    elif slit == 'both':
        try:
            yield from blocker_out()
        except:
            print('Sample_BS (block.y) might not be connected!')
        yield from check_slitX2()
        yield from check_block_slit()
    else:
        print(f'[{slit}] is not allowed for PXR!')
        return

    # gixos
    yield from gixos_transverse_sth(name,f'{name}_bkg',qxy_list=qxy_list, alpha=alpha, atten = atten, x2_per_step = x2_per_step, 
                                    num_point = num_point, exp_time= exp_time, soller_tran=soller_tran,
                                    final_sthreturn=True, final_blockreturn=False)
    # # gixos large tth for bulk
    yield from gixos_transverse_sth(name,f'{name}_bkg',qxy_list=qxy_list_bulk, alpha=alpha, atten = atten, x2_per_step = x2_per_step, 
                                    num_point = num_point, exp_time= exp_time, soller_tran=soller_tran,
                                    final_sthreturn=True, final_blockreturn=False)

    yield from slitX2_out()
    if slit == 'slit_blocker' or slit == 'both':
        yield from blocker_out()
    yield from bps.mov(abs2,5)



def printSampleInfo(samp_name_dict,sam_x2_pos,xr_run_dict,xrf_run_dict,gid_run_dict,gisaxs_run_dict,pxr_run_dict):

    '''print the sample info from the parameter dict'''

    print('\n')
    # print('---------------------------------------------------------------------------')
    print('=============================================================================')
    print('Here running samples:')
    # print(f"{'Seq' : <5}|{'X2' : ^5}|{'Measurements': ^20}|{'Sample' : >20}")
    for key in samp_name_dict:
        measure_type = []
        if xr_run_dict[key]: 
            measure_type.append('XRR')
        if xrf_run_dict[key]: 
            measure_type.append('XRF')
        if gid_run_dict[key]: 
            measure_type.append('GID')
        if gisaxs_run_dict[key]: 
            measure_type.append('GISAXS')
        if gisaxs_run_dict[key]: 
            measure_type.append('GISAXS')
        if pxr_run_dict[key]: 
            measure_type.append('PXR')
    #     # print(f'{key : <5}|{sam_x2_pos[key]: ^5}|{measure_type: ^10}|{samp_name_dict[key]: >20}')
        print(f'No. {key}: {samp_name_dict[key]}, x2 = {sam_x2_pos[key]}, {measure_type}')
    print('=============================================================================')
    # print('---------------------------------------------------------------------------')
    print('\n')

