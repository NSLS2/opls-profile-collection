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

    

def to_float_safe(val):
    try:
        return float(val)
    except ValueError:
        return val  # Keep as original string, or return None/skip
    
def try_int_safe(val):
    val_maybe_float = to_float_safe(val)
    if(type(val_maybe_float) == type(.2)):
        return int(val_maybe_float)
    else:
        return val_maybe_float
    
def trans1(name,tmp):
    return [to_float_safe(item) for item in tmp.loc[name].tolist()]
    #return tmp.loc[name].tolist()

def trans2(name,tmp):
    return [try_int_safe(item) for item in tmp.loc[name].tolist()]
    #return tmp.loc[name].tolist()

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


def soller_scan(name, block_pos = 0,q_start=1.3,q_end=1.8,npts=21,exp_time=20, x2_direction=1,alpha_i=0.0728, wait_time=5, atten=-1.775): # block edge at -31.5
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

