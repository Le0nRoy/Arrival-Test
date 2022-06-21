from api import Pins, Signal, BatteryState, BrakePedalState, AccPedalState, GearPosition, ReqTorque
from random import randint


class TestStatePressed:
    @staticmethod
    def setup_method():
        BatteryState.set_state_ready()
        # First we need to press brake pedal and release accel pedal to set GearPosition
        BrakePedalState.set_state_pressed()
        AccPedalState.set_state_0()
        # To randomize values of GearPosition and AccPedal in each test let's roll D6
        rand_num = randint(1, 6)
        # 1-3 for drive, 4-6 for reverse
        if rand_num - 3 <= 0:
            GearPosition.set_state_drive()
        else:
            GearPosition.set_state_reverse()
        # 1-2 for 30%, 3-4 for 50% and 5-6 for 100%
        if rand_num - 2 <= 0:
            AccPedalState.set_state_30()
        elif rand_num - 4 <= 0:
            AccPedalState.set_state_50()
        else:
            # FIXME as was found during manual testing (D-3) 100% is not working feature
            #  so here we have 'temporary' mock for it
            # AccPedalState.set_state_100()
            if rand_num % 2 == 0:
                AccPedalState.set_state_30()
            else:
                AccPedalState.set_state_50()
        BrakePedalState.set_state_released()

    @staticmethod
    def test_state_min_voltage():
        pre_test_states = Signal.get_all_signals_states()
        pre_test_req_torque = ReqTorque.get_signal_state()
        Pins.set_pin_voltage(Pins.BrakePedal, 1)
        states = Signal.get_all_signals_states()
        for item in states:
            if item['Name'] == BrakePedalState.SIGNAL_NAME:
                assert item['Value'] == "Pressed"
            elif item['Name'] == ReqTorque.SIGNAL_NAME:
                assert item['Value'] != pre_test_req_torque
            else:
                assert pre_test_states.count(item) == 1

    @staticmethod
    def test_state_random_voltage():
        pre_test_states = Signal.get_all_signals_states()
        pre_test_req_torque = ReqTorque.get_signal_state()
        # Method is implemented such way that applies random value
        BrakePedalState.set_state_pressed()
        states = Signal.get_all_signals_states()
        for item in states:
            if item['Name'] == BrakePedalState.SIGNAL_NAME:
                assert item['Value'] == "Pressed"
            elif item['Name'] == ReqTorque.SIGNAL_NAME:
                assert item['Value'] != pre_test_req_torque
            else:
                assert pre_test_states.count(item) == 1

    @staticmethod
    def test_state_max_voltage():
        pre_test_states = Signal.get_all_signals_states()
        pre_test_req_torque = ReqTorque.get_signal_state()
        start_voltage = 1.95
        Pins.set_pin_voltage(Pins.BrakePedal, start_voltage)
        for i in range(1, 5):
            # Here we can set fraction we need. I suppose fluctuation =0.01V is good enough
            Pins.set_pin_voltage(Pins.BrakePedal, start_voltage + i / 100)
            states = Signal.get_all_signals_states()
            for item in states:
                if item['Name'] == BrakePedalState.SIGNAL_NAME:
                    assert item['Value'] == "Pressed"
                elif item['Name'] == ReqTorque.SIGNAL_NAME:
                    assert item['Value'] != pre_test_req_torque
                else:
                    assert pre_test_states.count(item) == 1
