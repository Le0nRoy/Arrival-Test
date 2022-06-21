import requests
# from helper import uniform
from random import choice
from random import uniform

REQUEST_URL_BASE = "http://localhost:8099/api"


class APIError(AssertionError):
    def get_message(self):
        return self.__str__()


def send_request(request_url: str, request_method: str = "get", data: dict = None,
                 json_data: dict = None) -> requests.Response:
    if request_method.lower() == "get":
        r = requests.get(request_url)
    elif request_method.lower() == "post":
        if type(data) is dict and json_data is None:
            r = requests.post(request_url, data=data)
        elif type(json_data) is dict and data is None:
            r = requests.post(request_url, json=json_data)
        else:
            raise ValueError(f"No data was provided for request_method `{request_method}`")
    else:
        raise ValueError(f"Unknown request_method `{request_method}` was passed to function")

    if r.status_code != 200:
        raise APIError(f"Error occurred while sending request '{request_url}'")
    return r


class Pins:
    Gear_1 = 1
    Gear_2 = 2
    AccPedal = 3
    BrakePedal = 4
    BatteryVoltage = 5

    @staticmethod
    def get_pin_voltage(pin_id: int) -> float:
        request_url = f"{REQUEST_URL_BASE}/pins/{pin_id}"
        return send_request(request_url).json()['Voltage']

    @staticmethod
    def get_all_pins_voltages() -> list:
        request_url = f"{REQUEST_URL_BASE}/pins"
        return send_request(request_url).json()

    @staticmethod
    def set_pin_voltage(pin_id: int, voltage: float):
        request_url = f"{REQUEST_URL_BASE}/pins/{pin_id}/update_pin"
        send_request(request_url, request_method="post", data={'Voltage': voltage})

    @staticmethod
    def set_multiple_pins_voltage(json_data: dict):
        request_url = f"{REQUEST_URL_BASE}/pins/update_pin"
        send_request(request_url, request_method="post", json_data=json_data)


class Signal:
    ID = None
    SIGNAL_NAME = None
    __REQUEST_URL_SIGNAL = f"{REQUEST_URL_BASE}/signals"

    @classmethod
    def get_signal_state(cls) -> str:
        if cls.ID is None or not 1 <= cls.ID <= 5:
            raise TypeError("`Signal` is abstract class and should not be used directly")
        request_url = f"{cls.__REQUEST_URL_SIGNAL}/{cls.ID}"
        return send_request(request_url).json()['Value']

    @staticmethod
    def get_all_signals_states() -> list:
        return send_request(Signal.__REQUEST_URL_SIGNAL).json()


# TODO `set_state_*` functions may be upgraded to set needed state of other signals.
#  However for now it is not needed and may make logic too complicated.
class GearPosition(Signal):
    ID = 1
    SIGNAL_NAME = "GearPosition"
    __PARK = {Pins.Gear_1: 0.67, Pins.Gear_2: 3.12}
    __NEUTRAL = {Pins.Gear_1: 1.48, Pins.Gear_2: 2.28}
    __REVERSE = {Pins.Gear_1: 2.28, Pins.Gear_2: 1.48}
    __DRIVE = {Pins.Gear_1: 3.12, Pins.Gear_2: 0.67}

    @staticmethod
    def set_state_park():
        Pins.set_pin_voltage(Pins.Gear_1, GearPosition.__PARK[Pins.Gear_1])
        Pins.set_pin_voltage(Pins.Gear_2, GearPosition.__PARK[Pins.Gear_2])

    @staticmethod
    def set_state_neutral():
        Pins.set_pin_voltage(Pins.Gear_1, GearPosition.__NEUTRAL[Pins.Gear_1])
        Pins.set_pin_voltage(Pins.Gear_2, GearPosition.__NEUTRAL[Pins.Gear_2])

    @staticmethod
    def set_state_reverse():
        Pins.set_pin_voltage(Pins.Gear_1, GearPosition.__REVERSE[Pins.Gear_1])
        Pins.set_pin_voltage(Pins.Gear_2, GearPosition.__REVERSE[Pins.Gear_2])

    @staticmethod
    def set_state_drive():
        Pins.set_pin_voltage(Pins.Gear_1, GearPosition.__DRIVE[Pins.Gear_1])
        Pins.set_pin_voltage(Pins.Gear_2, GearPosition.__DRIVE[Pins.Gear_2])


class AccPedalState(Signal):
    ID = 2
    SIGNAL_NAME = "AccPedalPos"
    __0_LOW = 1
    __0_HIGH = 2
    __30_LOW = __0_HIGH
    __30_HIGH = 2.5
    __50_LOW = __30_HIGH
    __50_HIGH = 3
    __100_LOW = __50_HIGH
    __100_HIGH = 3.5

    @staticmethod
    def set_state_0():
        Pins.set_pin_voltage(Pins.AccPedal, uniform(AccPedalState.__0_LOW, AccPedalState.__0_HIGH))

    @staticmethod
    def set_state_30():
        Pins.set_pin_voltage(Pins.AccPedal, uniform(AccPedalState.__30_LOW, AccPedalState.__30_HIGH))

    @staticmethod
    def set_state_50():
        Pins.set_pin_voltage(Pins.AccPedal, uniform(AccPedalState.__50_LOW, AccPedalState.__50_HIGH))

    @staticmethod
    def set_state_100():
        Pins.set_pin_voltage(Pins.AccPedal, uniform(AccPedalState.__100_LOW, AccPedalState.__100_HIGH))

    @staticmethod
    def set_state_error():
        random_error_value_low = uniform(0, AccPedalState.__0_LOW)
        random_error_value_high = uniform(AccPedalState.__100_HIGH, AccPedalState.__100_HIGH * 2)
        Pins.set_pin_voltage(Pins.AccPedal, choice([random_error_value_low, random_error_value_high]))


class BrakePedalState(Signal):
    ID = 3
    SIGNAL_NAME = "BrakePedalState"
    __PRESSED_LOW = 1
    __PRESSED_HIGH = 2
    __RELEASED_LOW = __PRESSED_HIGH
    __RELEASED_HIGH = 3

    @staticmethod
    def set_state_pressed():
        Pins.set_pin_voltage(Pins.BrakePedal, uniform(BrakePedalState.__PRESSED_LOW, BrakePedalState.__PRESSED_HIGH))

    @staticmethod
    def set_state_released():
        Pins.set_pin_voltage(Pins.BrakePedal, uniform(BrakePedalState.__RELEASED_LOW, BrakePedalState.__RELEASED_HIGH))

    @staticmethod
    def set_state_error():
        random_error_value_low = uniform(0, BrakePedalState.__PRESSED_LOW)
        random_error_value_high = uniform(BrakePedalState.__PRESSED_HIGH, BrakePedalState.__PRESSED_HIGH * 2)
        Pins.set_pin_voltage(Pins.BrakePedal, choice([random_error_value_low, random_error_value_high]))


class ReqTorque(Signal):
    ID = 4
    SIGNAL_NAME = "ReqTorque"


class BatteryState(Signal):
    ID = 5
    SIGNAL_NAME = "BatteryState"
    __NOT_READY_LOW = 0
    __NOT_READY_HIGH = 400
    __READY_LOW = __NOT_READY_HIGH
    __READY_HIGH = 800

    @staticmethod
    def set_state_ready():
        Pins.set_pin_voltage(Pins.BatteryVoltage, uniform(BatteryState.__READY_LOW, BatteryState.__READY_HIGH))

    @staticmethod
    def set_state_not_ready():
        Pins.set_pin_voltage(Pins.BatteryVoltage,
                             uniform(BatteryState.__NOT_READY_LOW, BatteryState.__NOT_READY_HIGH))

    @staticmethod
    def set_state_error():
        random_error_value_low = uniform(0, BatteryState.__NOT_READY_LOW)
        random_error_value_high = uniform(BatteryState.__NOT_READY_HIGH, BatteryState.__NOT_READY_HIGH * 2)
        Pins.set_pin_voltage(Pins.BatteryVoltage, choice([random_error_value_low, random_error_value_high]))
