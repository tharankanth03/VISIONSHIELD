from datetime import datetime, timezone
import unittest

from visionshield.agent import VisionShieldAgent
from visionshield.config import AgentConfig, FusionConfig
from visionshield.models import EventState, FrameObservation, ThermalObservation
from visionshield.perception import point_in_polygon


class AgentTests(unittest.TestCase):
    def setUp(self):
        fusion = FusionConfig(
            rgb_weight=0.4,
            thermal_weight=0.4,
            change_weight=0.05,
            perimeter_weight=0.05,
            persistence_weight=0.1,
            required_confirmations=2,
        )
        self.agent = VisionShieldAgent(
            AgentConfig(fusion=fusion, perimeter=((0, 0), (1, 0), (1, 1), (0, 1)))
        )
        self.timestamp = datetime.now(timezone.utc)

    def observation(self, rgb=0.9, thermal=0.9, visibility=1.0):
        return (
            FrameObservation(self.timestamp, rgb, 0.8, visibility, (0.5, 0.5)),
            ThermalObservation(self.timestamp, thermal),
        )

    def test_confirmation_requires_persistence(self):
        rgb, thermal = self.observation()
        first = self.agent.process(rgb, thermal)
        second = self.agent.process(rgb, thermal)
        self.assertEqual(first.state, EventState.CANDIDATE)
        self.assertEqual(second.state, EventState.CONFIRMED)
        event = self.agent.create_event(second, {"source": "test"})
        self.assertEqual(len(event.event_id), 16)

    def test_low_visibility_reduces_rgb_contribution(self):
        rgb, thermal = self.observation(rgb=1.0, thermal=0.0, visibility=0.2)
        clear = self.agent.process(rgb, thermal)
        self.assertLess(clear.score, 0.5)
        self.assertTrue(any("visibility" in item for item in clear.explanations))

    def test_polygon_boundary_and_outside(self):
        self.assertTrue(point_in_polygon((0.5, 0.5), ((0, 0), (1, 0), (1, 1), (0, 1))))
        self.assertFalse(point_in_polygon((1.5, 0.5), ((0, 0), (1, 0), (1, 1), (0, 1))))

    def test_mismatched_timestamps_are_rejected(self):
        rgb, _ = self.observation()
        thermal = ThermalObservation(datetime.now(timezone.utc), 0.8)
        with self.assertRaises(ValueError):
            self.agent.process(rgb, thermal)


if __name__ == "__main__":
    unittest.main()
