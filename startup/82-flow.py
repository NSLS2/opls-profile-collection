print(f'Loading {__file__}')
flow1 = EpicsSignal("XF:12ID1-ECAT:EL4104-00-AO1", name="he_flow1")
flow2 = EpicsSignal("XF:12ID1-ECAT:EL4104-00-AO2", name="he_flow2")
flow3 = EpicsSignal("XF:12ID1-ECAT:EL4104-00-AO3", name="he_flow3")
#he_pid = EpicsSignal("XF:12ID1-ES{He-Flow}PID1.FBON", name = "feed back on/off")
#oxygen_percent = EpicsSignal("XF:12ID1:O2", name = "oxygen_percent")
o2_per = EpicsSignal("XF:12ID1:O2", name = "o2_per")
he_pid = EpicsSignal("XF:12ID1-ES{He-Flow}PID1.FBON", name = "he_pid")
# he_pid_setpoint = EpicsSignal("XF:12ID1-ES{He-Flow}PID1.VAL", name = "he_pid_setpoint")

chiller = EpicsSignal("XF:12ID1-ES{Chiller}T-SP", name="chiller")



def he_on(constant_rate = 2.6):
    yield from mov(he_pid,1)
    yield from mov(flow3,5)
    yield from mov(flow2,constant_rate)

def he_off():
    yield from mov(he_pid,0)
    yield from mov(flow3,0)
    yield from mov(flow2,0)

#sets the dry helium valve opening (5 is the max)
def dry_he_on(value):
    yield from mov(flow2,value)

def dry_he_off(value):
    yield from mov(flow2,0.0)



flow_dry = flow2
flow_wet = flow3


def he_wet_on():
    yield from bps.mv(flow_wet,3)

def he_wet_off():
    yield from bps.mv(flow_wet,0)

def he_dry_on():
    yield from bps.mv(flow_dry,3)

def he_dry_off():
    yield from bps.mv(flow_dry,0)

def _he_on():
    yield from he_dry_on()
    yield from he_wet_on()

def _he_off():
    yield from he_dry_off()
    yield from he_wet_off()

def gas_valve_on(): 
    yield from _he_on()

def gas_valve_off():
    yield from _he_off()








    




def record (time,number):
    for i in range(number):
        record_file = open('/home/xf12id1/.ipython/profile_collection/startup/record','a')
        e = str(datetime.datetime.now())
        yield from bps.sleep(time)
        record_file.write(e[0:19])
        record_file.write(" {:6.3f} {:6.3f} \n".format(o2_per.get(),flow3.get()))
        print(e,o2_per.get(),flow3.get())
        record_file.close()


### A1 for dry, A2 for wet
### OP mode: 0: OPEN, 1: Close, 2: SetPoint

# MFC.setDeviceRange(device='A1', val=200)
# MFC.setScaleFactor(device='A1', val=1.45) # for Helium?
# MFC.setFlow(device='A1', rate=100)
# MFC.setMode(device='A1', mode=2) # setpoint mode
# MFC.flow(device='A1')


# MFC.setDeviceRange(device='A2', val=200)
# MFC.setScaleFactor(device='A2', val=1.45) # for Helium?
# MFC.setFlow(device='A2', rate=100)
# MFC.setMode(device='A2', mode=2)
# MFC.flow(device='A2')


def MFC_set_dryflow(flow=0):
    '''set MFC dry flow'''
    MFC.setFlow(device='A1', rate=flow)


def MFC_set_wetflow(flow=0):
    '''set MFC dry flow'''
    MFC.setFlow(device='A2', rate=flow)


def MFC_dryflow_on():
    '''turn on MFCs'''
    MFC.setMode(device='A1', mode=2)

def MFC_wetflow_on():
    '''turn on MFCs'''
    MFC.setMode(device='A2', mode=2)


def MFC_dryflow_off():
    '''turn off MFCs'''
    MFC.setMode(device='A1', mode=1)

def MFC_wetflow_off():
    '''turn off MFCs'''
    MFC.setMode(device='A2', mode=1)


def MFC_flow_on():
    '''turn on MFCs'''
    MFC.setMode(device='A1', mode=2)
    MFC.setMode(device='A2', mode=2)

def MFC_flow_off():
    '''turn off MFCs'''
    MFC.setMode(device='A1', mode=1)
    MFC.setMode(device='A5', mode=1)



def dryflow_fullrate():
    '''turn on MFCs'''
    RE(he_dry_on())
    MFC.setMode(device='A1', mode=0)


