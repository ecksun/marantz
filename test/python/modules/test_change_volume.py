from unittest import TestCase
from unittest.mock import patch, MagicMock, call

from modules.Volume import change_volume
from zone import Zones


class TestVolumeChange(TestCase):
    @patch('modules.Volume.get_status')
    @patch('modules.Volume.send_command')
    def test_positive_change(self,
                             send_command_mock: MagicMock,
                             get_status_mock: MagicMock):
        get_status_mock.return_value = {'volume': 30}
        change_volume(+2.5)

        set_call = lambda vol: call('PutMasterVolumeSet', vol)

        calls = [set_call(vol) for vol in ['31.0', '32.0', '32.5']]
        send_command_mock.assert_has_calls(calls, any_order=False)

    @patch('modules.Volume.get_status')
    @patch('modules.Volume.send_command')
    def test_negative_change(self,
                             send_command_mock: MagicMock,
                             get_status_mock: MagicMock):
        get_status_mock.return_value = {'volume': -5}
        change_volume(Zones.MainZone, -2.5)

        set_call = lambda vol: call(Zones.MainZone, 'PutMasterVolumeSet', vol)

        calls = [set_call(vol) for vol in ['-6.0', '-7.0', '-7.5']]
        send_command_mock.assert_has_calls(calls, any_order=False)
