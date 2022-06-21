from api import Pins, Signal, BatteryState, BrakePedalState, AccPedalState, GearPosition


class TestStatePositions:
    @staticmethod
    def setup_method():
        BatteryState.set_state_ready()
        BrakePedalState.set_state_pressed()
        AccPedalState.set_state_0()
        Pins.set_pin_voltage(Pins.Gear_1, 0)
        Pins.set_pin_voltage(Pins.Gear_2, 0)

    @staticmethod
    def test_state_park():
        pre_test_states = Signal.get_all_signals_states()
        GearPosition.set_state_park()
        states = Signal.get_all_signals_states()
        for item in states:
            if item['Name'] == GearPosition.SIGNAL_NAME:
                assert item['Value'] == "Park"
            else:
                assert pre_test_states.count(item) == 1

    @staticmethod
    def test_state_neutral():
        pre_test_states = Signal.get_all_signals_states()
        GearPosition.set_state_neutral()
        states = Signal.get_all_signals_states()
        for item in states:
            if item['Name'] == GearPosition.SIGNAL_NAME:
                assert item['Value'] == "Neutral"
            else:
                assert pre_test_states.count(item) == 1

    @staticmethod
    def test_state_drive():
        pre_test_states = Signal.get_all_signals_states()
        GearPosition.set_state_drive()
        states = Signal.get_all_signals_states()
        for item in states:
            if item['Name'] == GearPosition.SIGNAL_NAME:
                assert item['Value'] == "Drive"
            else:
                assert pre_test_states.count(item) == 1

    @staticmethod
    def test_state_reverse():
        pre_test_states = Signal.get_all_signals_states()
        GearPosition.set_state_reverse()
        states = Signal.get_all_signals_states()
        for item in states:
            if item['Name'] == GearPosition.SIGNAL_NAME:
                assert item['Value'] == "Reverse"
            else:
                assert pre_test_states.count(item) == 1
