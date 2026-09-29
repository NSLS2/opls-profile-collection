import asyncio
import os

os.environ.pop("PYEPICS_LIBCA", None)

import ophyd
import bluesky.plans as bp
from bluesky import RunEngine
from nslsii.ophyd_async.devices import QuadEM, QuadEMGeometry
from ophyd_async.core import callback_on_mock_put, set_mock_value


def test_quadem_count_preserves_monitor_data_contract():
    quadem = QuadEM("TEST:QEM:", name="quadem")
    monitor_2 = quadem.current[2].mean_value
    monitor_3 = quadem.current[3].mean_value
    quadem.configure_readables(
        (monitor_2, monitor_3), hinted_signals=(monitor_2, monitor_3)
    )
    monitor_2.set_name("monitor_2")
    monitor_3.set_name("monitor_3")

    async def configure():
        await quadem.connect(mock=True)
        assert monitor_2.source.removeprefix("mock+") == "ca://TEST:QEM:Current2:MeanValue_RBV"
        assert monitor_3.source.removeprefix("mock+") == "ca://TEST:QEM:Current3:MeanValue_RBV"
        await asyncio.gather(
            quadem.driver.integration_time.set(0.0004),
            quadem.driver.values_per_read.set(500),
            quadem.driver.geometry.set(QuadEMGeometry.DIAMOND),
        )
        assert await quadem.driver.integration_time.get_value() == 0.0004
        assert await quadem.driver.values_per_read.get_value() == 500
        assert await quadem.driver.geometry.get_value() is QuadEMGeometry.DIAMOND

    asyncio.run(configure())
    set_mock_value(monitor_2, 2.0)
    set_mock_value(monitor_3, 3.0)

    def finish_acquisition(value):
        if value:
            asyncio.get_running_loop().call_soon(
                set_mock_value, quadem.driver.acquire, False
            )

    documents = []
    run_engine = RunEngine({})
    run_engine.subscribe(lambda name, document: documents.append((name, document)))
    with callback_on_mock_put(quadem.driver.acquire, finish_acquisition):
        run_engine(bp.count([quadem]))

    event = next(document for name, document in documents if name == "event")
    assert event["data"] == {"monitor_2": 2.0, "monitor_3": 3.0}
    assert quadem.hints["fields"] == ["monitor_2", "monitor_3"]
