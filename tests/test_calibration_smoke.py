import importlib.util
from pathlib import Path
import unittest

SPEC = importlib.util.spec_from_file_location("calibration_smoke", Path(__file__).resolve().parents[1] / "scripts/calibration_smoke.py")
smoke = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(smoke)


class CalibrationSmokeTests(unittest.TestCase):
    def test_only_current_step_and_valid_channel_can_drive_gui(self):
        self.assertEqual(smoke.parse_channel("12.4 s elapsed. Step 3: Channel 2 after 12 s total.", 3), 2)
        for value in ["Step 2: Channel 2", "Step 3: Channel 9", "Step 3: ChanneI 2", "", "Channel 2"]:
            with self.assertRaises(RuntimeError): smoke.parse_channel(value, 3)
