from api import Pins, Signal, BatteryState, BrakePedalState, AccPedalState, GearPosition, ReqTorque
from random import randint


class TestState100percent:
    @staticmethod
    def setup_method():
        BatteryState.set_state_ready()
        BrakePedalState.set_state_pressed()
        AccPedalState.set_state_0()
        if randint(1, 2) % 2 == 0:
            GearPosition.set_state_drive()
        else:
            GearPosition.set_state_reverse()
        BrakePedalState.set_state_released()
        # FIXME Ideally we need 0V on that pin for accurate test.
        #  However due to D-3 issue we can't set 0V here and have "Drive" or "Reverse" GearPos,
        #  so for now we leave just 0%
        # Pins.set_pin_voltage(Pins.AccPedal, 0)

    class Test100percent:
        @staticmethod
        def test_state_ready_min_voltage():
            pre_test_states = Signal.get_all_signals_states()
            Pins.set_pin_voltage(Pins.AccPedal, 3)
            states = Signal.get_all_signals_states()
            for item in states:
                if item['Name'] == AccPedalState.SIGNAL_NAME:
                    assert item['Value'] == "100%"
                elif item['Name'] == ReqTorque.SIGNAL_NAME:
                    assert item['Value'] == "10000"
                else:
                    assert pre_test_states.count(item) == 1

        @staticmethod
        def test_state_ready_random_voltage():
            pre_test_states = Signal.get_all_signals_states()
            # Method is implemented such way that applies random value
            AccPedalState.set_state_100()
            states = Signal.get_all_signals_states()
            for item in states:
                if item['Name'] == AccPedalState.SIGNAL_NAME:
                    assert item['Value'] == "100%"
                elif item['Name'] == ReqTorque.SIGNAL_NAME:
                    assert item['Value'] == "10000"
                else:
                    assert pre_test_states.count(item) == 1

        @staticmethod
        def test_state_ready_max_voltage():
            pre_test_states = Signal.get_all_signals_states()
            start_voltage = 3.45
            Pins.set_pin_voltage(Pins.AccPedal, 3)
            for i in range(1, 5):
                # Here we can set fraction we need. I suppose fluctuation =0.01V is good enough
                Pins.set_pin_voltage(Pins.AccPedal, start_voltage + i / 100)
                states = Signal.get_all_signals_states()
                for item in states:
                    if item['Name'] == AccPedalState.SIGNAL_NAME:
                        assert item['Value'] == "100%"
                    elif item['Name'] == ReqTorque.SIGNAL_NAME:
                        assert item['Value'] == "10000"
                    else:
                        assert pre_test_states.count(item) == 1
