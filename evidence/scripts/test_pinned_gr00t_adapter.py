"""Characterization test for the pinned GR00T SO100 adapter.

Loads the real eval_so100.py from GR00T_SRC. External robot/client packages are
stubbed because the test only exercises action decoding and selection; no robot
or policy server is started. This test documents current behaviour, not a fix.
"""
from __future__ import annotations

import importlib.util
import math
import os
import sys
import types
from pathlib import Path

import numpy as np
import pytest

GR00T_SHA = "d2b7e75b937e3ec9aa5dbc798f08b89692c49734"
GR00T_SRC = Path(os.environ["GR00T_SRC"]).resolve()
TARGET = GR00T_SRC / "gr00t/eval/real_robot/SO100/eval_so100.py"
assert TARGET.is_file(), f"Missing pinned GR00T source file: {TARGET}"
print(f"GR00T source: {GR00T_SRC}")
print(f"Expected GR00T revision: {GR00T_SHA}")


def _module(name: str, **attrs):
    mod = types.ModuleType(name)
    for key, value in attrs.items():
        setattr(mod, key, value)
    return mod


# Stub only imports unrelated to adapter decoding. The target source file itself
# is loaded unmodified from the checkout under test.
sys.modules["gr00t.policy.server_client"] = _module(
    "gr00t.policy.server_client", PolicyClient=type("PolicyClient", (), {})
)
draccus = _module("draccus")
draccus.wrap = lambda *args, **kwargs: (lambda fn: fn)
sys.modules["draccus"] = draccus

lerobot = _module("lerobot")
lerobot.__path__ = []
cameras = _module("lerobot.cameras")
cameras.__path__ = []
cameras_opencv = _module(
    "lerobot.cameras.opencv.configuration_opencv",
    OpenCVCameraConfig=type("OpenCVCameraConfig", (), {}),
)
cameras_opencv_pkg = _module("lerobot.cameras.opencv")
cameras_opencv_pkg.__path__ = []
robots = _module(
    "lerobot.robots",
    Robot=type("Robot", (), {}),
    RobotConfig=type("RobotConfig", (), {}),
    koch_follower=object(),
    make_robot_from_config=lambda cfg: None,
    so100_follower=object(),
    so101_follower=object(),
)
utils = _module(
    "lerobot.utils.utils",
    init_logging=lambda: None,
    log_say=lambda *args, **kwargs: None,
)
utils_pkg = _module("lerobot.utils")
utils_pkg.__path__ = []
sys.modules.update({
    "lerobot": lerobot,
    "lerobot.cameras": cameras,
    "lerobot.cameras.opencv": cameras_opencv_pkg,
    "lerobot.cameras.opencv.configuration_opencv": cameras_opencv,
    "lerobot.robots": robots,
    "lerobot.utils": utils_pkg,
    "lerobot.utils.utils": utils,
})

spec = importlib.util.spec_from_file_location("gr00t_so100_eval_under_test", TARGET)
assert spec and spec.loader
eval_so100 = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = eval_so100
spec.loader.exec_module(eval_so100)


class FakePolicy:
    def __init__(self, value: float):
        self.value = value

    def get_action(self, _model_input):
        # Two timesteps, five arm joints and one gripper value per timestep.
        arm = np.zeros((1, 2, 5), dtype=np.float64)
        gripper = np.zeros((1, 2, 1), dtype=np.float64)
        arm[0, 0, 0] = self.value
        gripper[0, 0, 0] = self.value
        return {"single_arm": arm, "gripper": gripper}, {}


def make_adapter(value: float):
    adapter = eval_so100.So100Adapter(FakePolicy(value))
    return adapter


def make_obs():
    return {
        "front": np.zeros((2, 2, 3), dtype=np.uint8),
        "wrist": np.zeros((2, 2, 3), dtype=np.uint8),
        "shoulder_pan.pos": 0.0,
        "shoulder_lift.pos": 0.0,
        "elbow_flex.pos": 0.0,
        "wrist_flex.pos": 0.0,
        "wrist_roll.pos": 0.0,
        "gripper.pos": 0.0,
        "lang": "test",
    }


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf"), 1e100, -1e100])
def test_invalid_numeric_policy_values_reach_action_dict_and_send_action(value):
    """Current-code characterization: invalid values are not rejected by GR00T."""
    adapter = make_adapter(value)
    actions = adapter.get_action(make_obs())
    selected = eval_so100._select_action_steps(actions, 1)

    assert len(selected) == 1
    action = selected[0]
    assert math.isnan(action["shoulder_pan.pos"]) if math.isnan(value) else action["shoulder_pan.pos"] == value
    assert math.isnan(action["gripper.pos"]) if math.isnan(value) else action["gripper.pos"] == value

    class RecordingRobot:
        def __init__(self):
            self.received = []

        def send_action(self, action_dict):
            self.received.append(action_dict)

    robot = RecordingRobot()
    robot.send_action(action)
    assert len(robot.received) == 1
    assert robot.received[0] is action


def test_finite_value_still_passes():
    actions = make_adapter(12.5).get_action(make_obs())
    selected = eval_so100._select_action_steps(actions, 1)
    assert selected[0]["shoulder_pan.pos"] == 12.5
    assert selected[0]["gripper.pos"] == 12.5
