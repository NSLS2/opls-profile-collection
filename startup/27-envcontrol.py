print(f'Loading {__file__}')

'''modified from SMI-SWAXS'''

from ophyd import EpicsSignal, Device, Component as Cpt

from epics import caget, caput


class output_lakeshore(Device):

    status = Cpt(EpicsSignal, "Val:Range-Sel")
    P = Cpt(EpicsSignal, "Gain:P-SP")
    I = Cpt(EpicsSignal, "Gain:I-SP")
    D = Cpt(EpicsSignal, "Gain:I-SP")
    temp_set_point = Cpt(EpicsSignal, "T-SP")

    def turn_on(self, range):
        if range in [1, 2, 3]:
            yield from bps.mv(self.status, range)
        else:
            print('The output range need be 1, 2, or 3!')

    def turn_off(self):
        yield from bps.mv(self.status, 0)

    def set_temp(self, temp):
        yield from bps.mv(self.temp_set_point, temp)

    def set_temp_celsius(self, temp):
        yield from self.set_temp(temp+273.15)


    ramp_sp = Cpt(EpicsSignal, "Val:Ramp-SP")
    ramp_status = Cpt(EpicsSignal, "Enbl:Ramp-Sel")

    def set_ramp(self, ramp):
        yield from bps.mv(self.ramp_sp, ramp)

    def ramp_on(self):
        yield from bps.mv(self.ramp_status, 1)
    def ramp_off(self):
        yield from bps.mv(self.ramp_status, 0)


class new_LakeShore(Device):
    """
    Lakeshore is the device reading the temperature from the heating stage for SAXS and GISAXS.
    This class define the PVs to read and write to control lakeshore
    :param Device: ophyd device
    """

    input_A = Cpt(EpicsSignal, "{Env:01-Chan:A}T-I")
    input_A_celsius = Cpt(EpicsSignal, "{Env:01-Chan:A}T:C-I")

    input_B = Cpt(EpicsSignal, "{Env:01-Chan:B}T-I")
    input_C = Cpt(EpicsSignal, "{Env:01-Chan:C}T-I")
    input_D = Cpt(EpicsSignal, "{Env:01-Chan:D}T-I")

    output1 = output_lakeshore("XF:12ID1-ES{Env:01-Out:1}", name="ls_outpu1")
    output2 = output_lakeshore("XF:12ID1-ES{Env:01-Out:2}", name="ls_outpu2")
    output3 = output_lakeshore("XF:12ID1-ES{Env:01-Out:3}", name="ls_outpu3")
    output4 = output_lakeshore("XF:12ID1-ES{Env:01-Out:4}", name="ls_outpu4")
    # xrange =


lakeshore = new_LakeShore("XF:12ID1-ES", name="lakeshore")
lakeshore.input_A_celsius.kind='hinted'
# lakeshore.ch1_read.kind = 'hinted'
# # lakeshore.ch1_sp.kind = 'hinted'
# lakeshore.ch2_read.kind = 'hinted'
# # lakeshore.ch2_sp.kind = 'hinted'
# lakeshore.ch3_read.kind = 'hinted'


class MassFlowControl(Device):
    def __init__(self):
        self.setDevice()
        # self.FlowRate_Sts = 'XF:12ID1-ES{FC:1}F-I'
        # self.FlowRate_SP = 'XF:12ID1-ES{FC:1}F:SP-SP'
        # self.Mode_Sts = 'XF:12ID1-ES{FC:1}Mode:Opr-Sts'
        # self.Mode_SP = 'XF:12ID1-ES{FC:1}Mode:Opr-Sel'
        # self.ScaleFactor_SP = 'XF:12ID1-ES{FC:1}Val:ScaleFactor-SP'
        # self.ScaleFactor_Sts = 'XF:12ID1-ES{FC:1}Val:ScaleFactor-RB'
        # self.NominalRange_SP = 'XF:12ID1-ES{FC:1}F:FullRng-SP'
        # self.NominalRange_Sts = 'XF:12ID1-ES{FC:1}F:FullRng-RB'

    def setDevice(self, device="A1"):
        if device == "A1":
            device_no = 1
        elif device == "A2":
            device_no = 2
        elif device == "B1":
            device_no = 3
        elif device == "B2":
            device_no = 4
        else:
            print("The device is NOT valid.")
            device_no = 1
        print("Select Device {} in port {}".format(device_no, device))
        self.device = device

        self.FlowRate_Sts = "XF:12ID1-ES{{FC:{}}}F-I".format(device_no)
        self.FlowRate_SP = "XF:12ID1-ES{{FC:{}}}F:SP-SP".format(device_no)
        self.Mode_Sts = "XF:12ID1-ES{{FC:{}}}Mode:Opr-Sts".format(device_no)
        self.Mode_SP = "XF:12ID1-ES{{FC:{}}}Mode:Opr-Sel".format(device_no)
        self.ScaleFactor_SP = "XF:12ID1-ES{{FC:{}}}Val:ScaleFactor-SP".format(device_no)
        self.ScaleFactor_Sts = "XF:12ID1-ES{{FC:{}}}Val:ScaleFactor-RB".format(device_no)
        self.NominalRange_SP = "XF:12ID1-ES{{FC:{}}}F:FullRng-SP".format(device_no)
        self.NominalRange_Sts = "XF:12ID1-ES{{FC:{}}}F:FullRng-RB".format(device_no)

        self._FlowRate_Sts = Cpt(EpicsSignal, "{{FC:{}}}F-I".format(device_no))
        self._FlowRate_SP = Cpt(EpicsSignal, "{{FC:{}}}F:SP-SP".format(device_no))
        self._Mode_Sts = Cpt(EpicsSignal, "{{FC:{}}}Mode:Opr-Sts".format(device_no))
        self._Mode_SP = Cpt(EpicsSignal, "{{FC:{}}}Mode:Opr-Sel".format(device_no))
        self._ScaleFactor_SP = Cpt(EpicsSignal, "{{FC:{}}}Val:ScaleFactor-SP".format(device_no))
        self._ScaleFactor_Sts = Cpt(EpicsSignal, "{{FC:{}}}Val:ScaleFactor-RB".format(device_no))
        self._NominalRange_SP = Cpt(EpicsSignal, "{{FC:{}}}F:FullRng-SP".format(device_no))
        self._NominalRange_Sts = Cpt(EpicsSignal, "{{FC:{}}}F:FullRng-RB".format(device_no))


        # self.FlowRate_Sts = 'XF:12ID1-ES{{FC:{}}}F-I'.format(device_no)

        return device_no

    def setFlow(self, rate, device=None, tolerence=1, verbosity=3):
        # set the setpoint of flow
        if device == None:
            device = self.device

        self.setDevice(device=device)

        if rate < self.deviceRange(verbosity=0) * 0.02:
            print("The rate is too low. (<2pct of the range)")
            return

        caput(self.FlowRate_SP, rate)
        if verbosity >= 3:
            print("The flow rate has been set to {}".format(rate))
            print("The current flow rate is {}".format(caget(self.FlowRate_Sts)))
        return caget(self.FlowRate_Sts)

    def flow(self, device=None, verbosity=3):
        if device == None:
            device = self.device

        self.setDevice(device=device)
        if verbosity >= 3:
            print("The current flow rate is {}".format(caget(self.FlowRate_Sts)))
        return caget(self.FlowRate_Sts)

    def setMode(self, mode, device=None, verbosity=3):
        # mode can be 0: OPEN, 1: Close, 2: SetPoint
        if device == None:
            device = self.device

        self.setDevice(device=device)

        if mode not in range(0, 3):
            return print("The input has to be 0: OPEN, 1: Close, 2: SetPoint")
        else:
            caput(self.Mode_SP, mode)
            while self.mode(device=device) != mode:
                time.sleep(0.2)
                caput(self.Mode_SP, mode)
            if verbosity >= 3:
                self.mode(device=device)
            return caget(self.Mode_Sts)

    def mode(self, device=None, verbosity=3):
        # OP mode: 0: OPEN, 1: Close, 2: SetPoint
        if device == None:
            device = self.device

        self.setDevice(device=device)
        if verbosity >= 3:
            self.readMode(device=device)
        return caget(self.Mode_Sts)

    def readMode(self, device=None, verbosity=3):
        # OP mode: 0: OPEN, 1: Close, 2: SetPoint
        if device == None:
            device = self.device
        self.setDevice(device=device)
        if caget(self.Mode_Sts) == 0:
            return print("The current mode is {}".format("ON"))
        if caget(self.Mode_Sts) == 1:
            return print("The current mode is {}".format("OFF"))
        if caget(self.Mode_Sts) == 2:
            return print("The current mode is {}".format("SETPOINT"))

    def scaleFactor(self, device=None, verbosity=3):
        # The scale factor depends on the gas.
        # N2 and air are default as 1. Helium is 0.18.
        # More details are listed in the manual.
        if device == None:
            device = self.device

        self.setDevice(device=device)
        if verbosity >= 3:
            print("The scale factor is {}".format(caget(self.ScaleFactor_Sts)))
        return caget(self.ScaleFactor_Sts)

    def setScaleFactor(self, val, device=None, verbosity=3):
        # Three modes: 0: OPEN, 1: Close, 2: SetPoint
        if device == None:
            device = self.device

        self.setDevice(device=device)

        caput(self.ScaleFactor_SP, val)
        while abs(self.scaleFactor() - val) > 0.02:
            time.sleep(1)
            caput(self.ScaleFactor_SP, val)
        if verbosity >= 3:
            self.scaleFactor()
        return caget(self.ScaleFactor_Sts)

    def deviceRange(self, device=None, verbosity=3):
        # Set the device by seting the Nominal Range.
        # Model 201: 20SCCM.
        if device == None:
            device = self.device

        self.setDevice(device=device)
        if verbosity >= 3:
            print("The range of this MFC device is up to {} SCCM.".format(caget(self.NominalRange_Sts)))
        return caget(self.NominalRange_Sts)

    def setDeviceRange(self, val, device=None, verbosity=3):
        # Set the device by seting the Nominal Range.
        # Model 201: 20SCCM.
        if device == None:
            device = self.device

        self.setDevice(device=device)

        caput(self.NominalRange_SP, val)
        while abs(self.deviceRange() - val) > 1:
            time.sleep(1)
            caput(self.NominalRange_SP, val)
        if verbosity >= 3:
            self.deviceRange()
        return caget(self.NominalRange_Sts)



MFC = MassFlowControl()  


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