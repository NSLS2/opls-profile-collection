import asyncio

from nslsii.ophyd_async.devices import QuadEM, QuadEMGeometry
from ophyd import Component as Cpt
from ophyd import Device
from ophyd.signal import EpicsSignal


quadem = QuadEM("XF:12ID1-BI{EM:1}EM1:", name="quadem")
quadem.configure_readables(
    (quadem.current[2].mean_value, quadem.current[3].mean_value),
    hinted_signals=(quadem.current[2].mean_value, quadem.current[3].mean_value),
)


async def _configure_quadem():
    await quadem.connect()
    await asyncio.gather(
        quadem.driver.integration_time.set(0.0004),
        quadem.driver.values_per_read.set(500),
        quadem.driver.geometry.set(QuadEMGeometry.DIAMOND),
    )


asyncio.run(_configure_quadem())


def quadem_clear():
    for index in (1, 2, 3):
        yield from bps.trigger(quadem.driver.compute_current_offsets[index])


#This is for the siddons box for the DBPM

class XBPM4(Device):
    """
    XBPM are diamond windows that generate current when the beam come through. It is used to know the position
    of the beam at the bpm postion as well as the amount of incoming photons. 3 bpms are available at SMI: bpm1
    is position upstream, bpm2 after the focusing mirrons and bpm3 downstream
    :param Device: ophyd device
    """
    ch1 = Cpt(EpicsSignal, 'Current1:MeanValue_RBV')
    ch2 = Cpt(EpicsSignal, 'Current2:MeanValue_RBV')
    ch3 = Cpt(EpicsSignal, 'Current3:MeanValue_RBV')
    ch4 = Cpt(EpicsSignal, 'Current4:MeanValue_RBV')
    sumX = Cpt(EpicsSignal, 'SumX:MeanValue_RBV')
    sumY = Cpt(EpicsSignal, 'SumY:MeanValue_RBV')
    posX = Cpt(EpicsSignal, 'PosX:MeanValue_RBV')
    posY = Cpt(EpicsSignal, 'PosY:MeanValue_RBV')


#ben commented this out on 9/20/21 due to errors
bpm = XBPM4("XF:12ID1-BI{EM:2}", name="bpm")


bpm.ch1.kind = 'hinted'
bpm.ch2.kind = 'hinted'
bpm.ch3.kind = 'hinted'
bpm.ch4.kind = 'hinted'

bpm.sumX.kind = 'hinted'
bpm.sumY.kind = 'hinted'
bpm.posX.kind = 'normal'
bpm.posY.kind = 'normal'

