from api import Pins, Signal, BatteryState, BrakePedalState, AccPedalState, GearPosition


class TestStateReady:
    @staticmethod
    def setup_method():
        BrakePedalState.set_state_pressed()
        AccPedalState.set_state_0()
        GearPosition.set_state_neutral()
        BatteryState.set_state_not_ready()

    @staticmethod
    def test_state_max_voltage():
        pre_test_states = Signal.get_all_signals_states()
        Pins.set_pin_voltage(Pins.BatteryVoltage, 800)
        states = Signal.get_all_signals_states()
        for item in states:
            if item['Name'] == BatteryState.SIGNAL_NAME:
                assert item['Value'] == "Ready"
            else:
                assert pre_test_states.count(item) == 1

    @staticmethod
    def test_state_random_voltage():
        pre_test_states = Signal.get_all_signals_states()
        # Method is implemented such way that applies random value
        BatteryState.set_state_ready()
        states = Signal.get_all_signals_states()
        for item in states:
            if item['Name'] == BatteryState.SIGNAL_NAME:
                assert item['Value'] == "Ready"
            else:
                assert pre_test_states.count(item) == 1

    @staticmethod
    def test_state_min_voltage():
        pre_test_states = Signal.get_all_signals_states()
        start_voltage = 400.5
        Pins.set_pin_voltage(Pins.BatteryVoltage, start_voltage)
        for i in range(1, 5):
            # Here we can set fraction we need. I suppose fluctuation =0.1V is good enough for High voltage battery
            Pins.set_pin_voltage(Pins.BatteryVoltage, start_voltage - i / 10)
            states = Signal.get_all_signals_states()
            for item in states:
                if item['Name'] == BatteryState.SIGNAL_NAME:
                    assert item['Value'] == "Ready"
                else:
                    assert pre_test_states.count(item) == 1
