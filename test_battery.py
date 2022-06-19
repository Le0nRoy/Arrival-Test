import pytest
from api import Pins
from api import Signals
from helper import get_random_float


@pytest.fixture()
def setup():
    payload = {"Pins": [
        {"PinID": Pins.BatteryVoltage, "Voltage": get_random_float(0, 399)},
        {"PinID": Pins.BrakePedal, "Voltage": get_random_float(1, 2)},
        {"PinID": Pins.AccPedal, "Voltage": get_random_float(1, 2)},
        {"PinID": Pins.Gear_2, "Voltage": 2.28},
        {"PinID": Pins.Gear_1, "Voltage": 1.48},
    ]}
    Pins.set_multiple_pins_voltage(json_data=payload)


def test_state_ready():
    pass
