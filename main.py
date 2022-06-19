import requests

request_url_base = "http://localhost:8099/api"


class Signals:
    GearPosition = 1
    AccPedalPos = 2
    BrakePedalState = 3
    ReqTorque = 4
    BatteryState = 5


class Pins:
    Gear_1 = 1
    Gear_2 = 2
    AccPedal = 3
    BrakePedal = 4
    BatteryVoltage = 5


def get_signal_state(signal) -> str:
    request_url = f"{request_url_base}/signals/{signal}"
    return requests.get(request_url).json()['Value']


def get_all_signals_states() -> dict:
    request_url = f"{request_url_base}/signals"
    return requests.get(request_url).json()


def get_pin_voltage(pin) -> float:
    request_url = f"{request_url_base}/pins/{pin}"
    return requests.get(request_url).json()['Voltage']


def get_all_pins_voltages() -> dict:
    request_url = f"{request_url_base}/pins"
    return requests.get(request_url).json()
