from datetime import datetime, timezone
import unittest

from visionshield.agent import VisionShieldAgent
from visionshield.config import AgentConfig, FusionConfig
from visionshield.models import EventState, FrameObservation, ObjectDetection, ThermalObservation
from visionshield.notifier import NullNotifier, format_event_alert
from visionshield.anomaly import ThermalAnomalyDetector
from visionshield.perimeter import evaluate
from visionshield.perception import point_in_polygon
from visionshield.storage import EventStore
from visionshield.sensors import MLX90640Source


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
            FrameObservation(
                self.timestamp, rgb, 0.8, visibility, (0.5, 0.5),
                detections=(ObjectDetection("person", 0.91),),
            ),
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
        alert = format_event_alert(event)
        self.assertIn("Detected: person (91%)", alert)
        self.assertIn("Thermal sensor: ACTIVE", alert)

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

    def test_unconfigured_notifier_does_not_send(self):
        self.assertIsInstance(self.agent.notifier, NullNotifier)

    def test_thermal_anomaly_baseline(self):
        detector = ThermalAnomalyDetector.fit([[20, 20, 20], [20, 20.1, 19.9]])
        result = detector.analyze([25, 25, 25])
        self.assertTrue(result.active)
        self.assertGreater(result.score, 0)

    def test_perimeter_reports_unconfigured_state(self):
        decision = evaluate((0.5, 0.5), ())
        self.assertFalse(decision.configured)
        self.assertFalse(decision.inside)

    def test_event_store_round_trip(self):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as directory:
            store = EventStore(f"{directory}/events.jsonl", retention_seconds=300)
            rgb, thermal = self.observation()
            self.agent.process(rgb, thermal)
            event = self.agent.create_event(self.agent.process(rgb, thermal))
            store.append(event)
            self.assertEqual(store.recent()[0]["event_id"], event.event_id)

    def test_mlx_source_validates_frame_shape(self):
        source = MLX90640Source(lambda: [20.0] * 768)
        values, timestamp = source.read()
        self.assertEqual(len(values), 768)
        self.assertIsNotNone(timestamp)
        with self.assertRaises(ValueError):
            MLX90640Source(lambda: [20.0]).read()

    def test_confirmed_event_alert_is_not_repeated(self):
        first_rgb, first_thermal = self.observation()
        self.agent.process(first_rgb, first_thermal)
        second = self.agent.process(first_rgb, first_thermal)
        self.assertEqual(second.state, EventState.CONFIRMED)
        third = self.agent.process(first_rgb, first_thermal)
        self.assertEqual(third.state, EventState.CONFIRMED)


if __name__ == "__main__":
    unittest.main()
