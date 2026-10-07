print(f'Loading {__file__}')

from bluesky.callbacks.fitting import PeakStats
import bluesky.preprocessors as bpp


slit_x2_offset_edge = 0 # 46.73 - 3.7 # 42.6131125 # updated, 09/30/25; 42.418  
slit_x2_offset_gap = 10.3 # 57.139 - 3.7 # 53.006 # updated, 09/30/25, # 52.75273301552 # 53.9723 # 53.67 # 55.62 # center of the slit
slit_x2_offset_block = slit_x2_offset_edge + 1 # 0.6  # 45.2 + 1.5 # plus 1.5 to block the beam
# atten_slit =  -1.70856490 #-1.72081 # -1.775129
# slit_x2_out = -60 # -9.5-3.7



def slitX2_out(offset=15):
    low_limit = slit_x2.limits[0]
    low_limit_offset = 1.5
    slit_x2_max = max(-1*x2.position-offset, low_limit+low_limit_offset)
    print(f'target position is {slit_x2_max}.')
    yield from bps.mov(slit_x2,slit_x2_max)
    print('slit_x2 is out.')

def slitX2_in():
    '''put the slitx2 in with the CENTER aligning with the beam'''
    x2_position_original = x2.position
    yield from bps.mov(slit_x2,slit_x2_offset_gap-x2_position_original)
    print('slit_x2 is in.')

def slitX2_in_edge():
    '''put the slitx2 in with the EDGE aligning with the beam'''
    x2_position_original = x2.position
    yield from bps.mov(slit_x2,slit_x2_offset_edge-x2_position_original)
    print('slit_x2 edge is in.')


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
    yield from dscanr(slit_x2, -0.5, 0.5, 41, 0.5)


def check_slitX2_block(block_offset=1):
    '''Align the slit x2 edge and block the beam by 1mm
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