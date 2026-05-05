print(f'Loading {__file__}')

from bluesky.callbacks.fitting import PeakStats
import bluesky.preprocessors as bpp


# NEEDS TO BE FIXED
def set_zero_alpha():
    chi_nom=geo.forward(0,0,0).chi
    yield from set_chi(chi_nom)
    phi_nom=geo.forward(0,0,0).phi  
    yield from set_phi(phi_nom)
    tth_nom=geo.forward(0,0,0).tth 
    yield from set_tth(tth_nom)
    sh_nom=geo.forward(0,0,0).sh
    yield from set_sh(sh_nom)
    yield from set_ih(0)
    yield from set_ia(0)
    yield from set_oa(0)
    yield from set_oh(0)


def direct_beam():
    yield from bps.mov(abs1,1)
    yield from bps.mov(abs2,8)
    yield from bps.mov(shutter,1)
    yield from mab(0,0)
    yield from bps.movr(sh,-0.2)
    alphai = 0.11


# def check_phi():
#     '''Align the deflector crystal phi
#     '''
#     yield from det_set_exposure([quadem], exposure_time=1.0, exposure_number = 1)
#     yield from bps.mv(geo.det_mode,1)  #move lamda detector in ?
#     yield from bps.mv(abs2,6)   #move the second absorber in 
#     yield from mabt(0,0,0)    # don't understand???, ih_tra
#     #yield from det_exposure_time_new([lambda_det], 1,1)
#     tmp1=geo.phi.position
#     yield from bps.mv(shutter,1) # open shutter
#     print('resetting phi') 
#     local_peaks = PeakStats(phi.user_readback.name, quadem.current2.mean_value.name)
#     yield from bpp.subs_wrapper(bp.rel_scan([quadem],phi,-0.015,0.015,21), local_peaks)
#     tmp = local_peaks.cen  #get the height for roi2 of quadem with a max intens
#     yield from bps.mv(phi,tmp)  #move the XtalDfl to this height
#     yield from set_phi(tmp1)  #set this height as 0
#     yield from bps.mv(shutter,0) # close shutter


# def check_ih():
#     '''Align the Align the spectrometer stage height
#     '''
#     yield from bps.mv(geo.det_mode,1)  #move lamda detector in ?
#     yield from det_set_exposure([quadem], exposure_time=0.5, exposure_number = 1)
#     yield from bps.mv(abs2,6)   #move the second absorber in 
#     yield from mabt(0,0,0)    # don't understand???, 
#     yield from bps.mv(sh,-1)  # move the Sample vertical translation to -1
#     yield from bps.mv(shutter,1) # open shutter
#     print('resetting ih')
#     #yield from bp.rel_scan([quadem],ih,-0.1,0.15,16)  #scan the quadem detector against XtalDfl-height
#     #tmp=peaks.cen['quadem_current3_mean_value']  #get the height for roi2 of quadem with a max intensity 
#     local_peaks = PeakStats(ih.user_readback.name, quadem.current3.mean_value.name)
#     # yield from bpp.subs_wrapper(bp.rel_scan([quadem],ih,0.06,-0.06,13), local_peaks)
#     yield from bpp.subs_wrapper(bp.rel_scan([quadem],ih,0.1,-0.1,21), local_peaks)
#     tmp = local_peaks.cen  #get the height for roi2 of quadem with a max intens
#     yield from bps.mv(ih,tmp)  #move the XtalDfl to this height
#     yield from set_ih(0)  #set this height as 0
#     yield from bps.mv(shutter,0) # close shutter

# def check_tth():
#     '''Align the spectrometer rotation angle'''
#     yield from bps.mv(geo.det_mode,1)
#     yield from bps.mv(abs2,6)
#     yield from mabt(0,0,0)
#     tmp1= geo.tth.position
#     print('resetting tth')
#     yield from bps.mv(sh,-1)
#     yield from bps.mv(shutter,1) # open shutter
#     local_peaks = PeakStats(tth.user_readback.name, quadem.current3.mean_value.name)
#     #yield from bp.rel_scan([quadem],tth,-0.1,0.1,21)
#     yield from bpp.subs_wrapper(bp.rel_scan([quadem],tth,-0.1,0.1,21), local_peaks)
#     tmp2 = local_peaks.cen  #get the height for roi2 of quadem with a max intens
#     yield from bps.mv(tth,tmp2)
#     yield from set_tth(tmp1)
#     yield from bps.mv(shutter,0) # close shutter


def check_tth_pseudo(detector=lambda_det):
    print('Align the spectrometer rotation angle')
    yield from bps.mv(geo.det_mode,1)
    yield from bps.mv(S2.hg, 2)
    yield from bps.mv(abs3,4)
    yield from bps.mv(abs2,-1.5)
    yield from mabt(0,0,0)
    print('resetting tth with the pseudo slit')
    yield from bps.mv(sh,-1)
    yield from bps.mv(shutter,1) # open shutter
    yield from dscanr(geo.tth,-0.15, 0.15, 21, 0.1)
    yield from bps.mv(S2.hg, 0.5)
    yield from dscan(S2.hc,-1,1,21,0.1)
    yield from bps.mv(abs3,0)
    yield from bps.mv(shutter,0) # close shutter



        
# def check_astth(detector=lambda_det):
#     '''Align the detector arm rotation angle'''  
#     yield from bps.mv(geo.det_mode,1)
#     yield from bps.mv(abs2,6)
#     yield from mabt(0.0,0.0,0)
#     tmp1=geo.astth.position
#     yield from bps.mvr(sh,-1)
#     print('setting astth')
#     yield from bps.mv(shutter,1) # open shutter
# #    yield from bp.rel_scan([detector],astth,-0.1,0.1,21)
#  #   tmp2=peaks.cen['%s_stats2_total'%detector.name] 
#     local_peaks = PeakStats(astth.user_readback.name, '%s_stats2_total'%detector.name)
#     yield from bpp.subs_wrapper(bp.rel_scan([detector],astth,-0.1,0.1,21), local_peaks)
#     tmp2 = local_peaks.cen  #get the height for roi2 of detector.name with max intens
#     yield from bps.mv(astth,tmp2)
#     yield from bps.mv(shutter,0) # close shutter
#     yield from set_astth(tmp1)
    





def sample_height(alpha=0.08, range=0.3, npts=31,time=1, settle_time = 2, finescan=False):
   
    yield from bps.mv(abs2,5)
    yield from mabt(alpha,alpha,0)
    yield from bps.sleep(1)
    yield from mabt(alpha,alpha,0)
    
    if liquids_mode()=='GISAXS':
        yield from bps.movr(geo.astth,0.1)
        yield from bps.mv(detsaxs.x, 0)
        yield from bps.mv(detsaxs.y, 0)
        yield from bps.mv(fp_saxs.y1,20-5,fp_saxs.y2,40-5)# with CRLS


    Msg('reset_settle_time', sh.settle_time, settle_time)

    ## use sh2 motor do the scan only if 1) doing fine scan AND 2) sh_mode is 2 or 3
    if finescan and (geo.sh_mode.get()>1):
        yield from dscanr(geo.sh2, -0.5*range,0.5*range, npts, time)
    else:
    # For the fine elevator you need to change geo.sh to geo.sh2
        yield from dscanr(geo.sh, -0.5*range,0.5*range, npts, time)


def sample_height_set_fine_o(value=3, finescan=True):
    yield from sample_height(alpha=0.06, range=0.3,npts=31,time=1,settle_time = 2, finescan=finescan)

def sample_height_set_coarse(value=0):
    yield from sample_height(alpha=0.06, range=4,npts=31,time=0.5,settle_time = 0.5, finescan=False)

def sample_height_set_coarse1(value=0):
    yield from sample_height(alpha=0.06, range=5,npts=41,time=0.5,settle_time = 0.5, finescan=False)

def sample_height_set_coarse2(value=0):
    yield from sample_height(alpha=0.06, range=1.5,npts=31,time=0.5,settle_time = 0.5, finescan=False)


slit_x2_offset_edge = 0 # 46.73 - 3.7 # 42.6131125 # updated, 09/30/25; 42.418  
slit_x2_offset_gap = 10.3 # 57.139 - 3.7 # 53.006 # updated, 09/30/25, # 52.75273301552 # 53.9723 # 53.67 # 55.62 # center of the slit
slit_x2_offset_block = slit_x2_offset_edge + 1 # 0.6  # 45.2 + 1.5 # plus 1.5 to block the beam
# atten_slit =  -1.70856490 #-1.72081 # -1.775129
# slit_x2_out = -60 # -9.5-3.7


def check_slitX2():
    '''Align the slit x2
    '''
    # do we keep old mode and reset
    x2_position_original = x2.position
    # print('move slit x2 in pre-determined position')
    yield from bps.mov(slit_x2,slit_x2_offset_gap-x2_position_original)
    yield from bps.mv(abs2,5)   #move the second absorber in 
    yield from mabt(0,0,0) 
    yield from bps.mv(asth.rot,15.147)   #move the second absorber in 
    yield from bps.mv(sh, -1)
    yield from dscanr(slit_x2, -1, 1, 41, 0.5)


def check_block_slit():
    '''Align the slit on the block (smaract)
    '''
    # do we keep old mode and reset
    # print('move slit x2 in pre-determined position')
    yield from bps.mov(block.y,0)
    yield from bps.mv(abs2,5)   #move the second absorber in 
    yield from mabt(0,0,0) 
    yield from bps.mv(asth.rot,15.147)   #move the second absorber in 
    yield from bps.mv(sh, -1)
    yield from dscanr(block.y, -1, 1, 41, 0.5)



def check_slitX2_block(block_offset=1):
    '''Align the slit x2 edge and block the beam by 0.5mm
    '''
    mode='Soller'
    det=pilatus100kA
    slit_offset = block_offset
    x2_position_original = x2.position
    # print('move slit x2 in pre-determined position')
    yield from bps.mov(slit_x2,slit_x2_offset_edge-x2_position_original)
    yield from set_mode(mode)
    yield from mabt(0,0,0)
    yield from bps.mov(sh, -1)
    yield from bps.mv(abs2,5) 
    yield from bp.rel_scan([det],slit_x2,-1,1,21,per_step=shutter_flash_scan)
    peak_cen = ps_new(det='p100kA', suffix='_2', der=True, plot=False)
    yield from bps.mov(slit_x2, peak_cen+slit_offset)

    slit_x2_offset_block_new = x2.position + slit_x2.position
    print(f'The new slit_x2_offset_block: {slit_x2_offset_block_new}')
    return slit_x2_offset_block_new


def slitX2_out(offset=15):
    slit_x2_max = max(-1*x2.position-offset, -58)
    yield from bps.mov(slit_x2,slit_x2_max)
    print('slit_x2 is out.')


def blocker_out(offset=30):
    yield from bps.mov(block.y, offset)
    print('sample blocker is out.')


def slitX2_in():
    x2_position_original = x2.position
    yield from bps.mov(slit_x2,slit_x2_offset_gap-x2_position_original)
    print('slit_x2 is in.')


def check_ih():
    '''Align the spectrometer ih stage
    '''
    # do we keep old mode and reset
    old_track_mode = geo.track_mode.get()
    try:
        yield from bps.mv(geo.track_mode,0)
        yield from bps.mv(abs2,6)   #move the second absorber in 
        yield from mabt(0,0,0)  
        print('resetting ih')
        yield from dscanr(geo.ih, -0.15, 0.15, 21, 0.5)
    finally: 
        yield from bps.mv(geo.track_mode,old_track_mode)

def check_phi():
    '''Align the spectrometer phi stage
    '''
    # do we keep old mode and reset
    old_track_mode = geo.track_mode.get()
    try:
        yield from bps.mv(geo.track_mode,0)
        yield from bps.mv(abs2,6)   #move the second absorber in 
        yield from mabt(0,0,0)  
        print('resetting phi')
        yield from dscanr(geo.phi, -0.015, 0.015, 21, 0.5)
    finally:
        yield from bps.mv(geo.track_mode,old_track_mode)

def check_astth():
    '''Align the detector arm rotation angle'''  
    yield from set_mode('XR')
    yield from bps.mv(abs2,5)
    yield from mabt(0,0,0)
    yield from bps.mvr(sh,-2)
    print('resetting astth')
    yield from dscanr(astth, 0.06, -0.06, 25, 0.5)
    yield from bps.mvr(sh,2)


def check_tth():
    '''Align the tth'''  
    # do we keep old mode and reset
    old_track_mode = geo.track_mode.get()
    try:
        yield from set_mode('Alignment')
        yield from bps.mv(abs2,6)  
        yield from mabt(0,0,0)  
        yield from bps.mvr(sh,-1)
        print('resetting tth')
        yield from dscanr(tth, 0.12, -0.12, 31, 0.5)
    finally:
        yield from bps.mvr(sh,1)
        yield from bps.mv(geo.track_mode,old_track_mode)    


def check_linear_time():
    # eta
    global dif    
    dif  = np.zeros((4, 7))
    t=[0.1,0.2,0.5,1,2,5,10]
    for i,j in enumerate(t):
       # yield from bps.mv(i, i)
        exp_t=j
        yield from bps.mov(
            lambda_det.cam.acquire_time, exp_t,
            lambda_det.cam.acquire_period, exp_t+0.2,
            lambda_det.cam.num_images, int(exp_t/exp_t))

        yield from bp.count([quadem,lambda_det]) 
        dif[0, i]=exp_t
        dif[1, i] = quadem.current3.mean_value.get()
        dif[2, i] = lambda_det.stats3.total.get()
        dif[3, i] = dif[2,i]/dif[0,i]  
    print(dif)

def mplot1():
    plt.figure()
    plt.plot(dif[0, :], dif[3, :])
    plt.xscale("log")
    plt.xlabel('exposure time [s]')
    plt.ylabel('pilatus100k intensity/exposure time [counts/s]')
    plt.show()
    return

def check_linear_slits():
    # eta
    global dif    
    dif  = np.zeros((4, 18))
    slit_width=[-0.01,0.00,0.01,0.02,0.03,0.03,0.04,0.04,0.05,0.05,0.06,0.06,0.07,0.07,0.08,0.08,0.09,0.09]
    for i,j in enumerate(slit_width):
        yield from bps.mov(S2.vg,j)
        yield from bp.count([quadem,lambda_det]) 
        dif[0, i]=j
        dif[1, i] = quadem.current3.mean_value.get()
        dif[2, i] = lambda_det.stats2.total.get()
        dif[3, i] = dif[2,i]/dif[1,i]  
    print(dif)


def mplot2():
    plt.figure()
    plt.plot(dif[0, :], dif[3, :]/max(dif[3, :]),color='r',label="detector/monitor")
    plt.plot(dif[0, :], dif[2, :]/max(dif[2, :]),'g',label="detector")
    plt.plot(dif[0, :], dif[1, :]/max(dif[1, :]),'b',label="monitor")
    plt.xlabel('s2.vg')
    plt.ylabel('counts/monitor')
    plt.legend()
    plt.show()
    return
def set_tth(new_value):
    yield Msg('reset_user_position', geo.tth, new_value)
    save_offsets()
     