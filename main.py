import requests

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


class Signals:
    GearPosition = 1
    AccPedalPos = 2
    BrakePedalState = 3
    ReqTorque = 4
    BatteryState = 5

    @staticmethod
    def get_signal_state(signal_id: int) -> str:
        request_url = f"{REQUEST_URL_BASE}/signals/{signal_id}"
        return send_request(request_url).json()['Value']

    @staticmethod
    def get_all_signals_states() -> dict:
        request_url = f"{REQUEST_URL_BASE}/signals"
        return send_request(request_url).json()


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
    def get_all_pins_voltages() -> dict:
        request_url = f"{REQUEST_URL_BASE}/pins"
        return send_request(request_url).json()

    @staticmethod
    def set_pin_voltage(pin_id: int, voltage: float):
        request_url = f"{REQUEST_URL_BASE}/pins/{pin_id}/update_pin"
        send_request(request_url, data={'Voltage': voltage})

    @staticmethod
    def set_multiple_pins_voltage(json_data: dict):
        request_url = f"{REQUEST_URL_BASE}/pins/update_pin"
        send_request(request_url, json_data=json_data)
