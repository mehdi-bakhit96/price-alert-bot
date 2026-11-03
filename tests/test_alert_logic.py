import unittest
from src.alert_logic import ThresholdAlertManager


class TestThresholdAlertManager(unittest.TestCase):
    def test_alert_triggers_at_or_above_threshold(self):
        manager = ThresholdAlertManager(threshold=50000.0)

        # Below threshold -> no alert
        self.assertFalse(manager.process_price(49999.0))

        # Reached threshold -> trigger alert
        self.assertTrue(manager.process_price(50000.0))
        manager.mark_sent()

        # Still above threshold -> do not spam
        self.assertFalse(manager.process_price(50500.0))
        self.assertFalse(manager.process_price(52000.0))

    def test_alert_rearms_when_price_drops_and_rises_again(self):
        manager = ThresholdAlertManager(threshold=50000.0)

        # Trigger & mark sent
        self.assertTrue(manager.process_price(51000.0))
        manager.mark_sent()

        # Drops below threshold -> disarms
        self.assertFalse(manager.process_price(49000.0))

        # Rises back above -> triggers again
        self.assertTrue(manager.process_price(50001.0))


if __name__ == "__main__":
    unittest.main()
