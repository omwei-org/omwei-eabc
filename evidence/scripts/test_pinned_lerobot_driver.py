"""Exercise the pinned LeRobot Feetech conversion/write path without hardware.

This imports the real pinned MotorsBus and FeetechMotorsBus implementations.
Only utility imports and the SDK transport objects are stubbed; conversion,
sign encoding, register lookup, serialization, and sync_write are real code.
"""
from __future__ import annotations

import math
import os
import sys
import types
from pathlib import Path

PIN = "c75455a6de5c818fa1bb69fb2d92423e86c70475"
src = Path(os.environ["LEROBOT_SRC"]).resolve()
assert (src / "lerobot/motors/motors_bus.py").is_file(), src
# The workflow checks out this exact source revision before invoking the test.
print(f"LE ROBOT SOURCE: {src}")
print(f"EXPECTED PIN: {PIN}")

# The bus module imports utility helpers from a module that imports torch,
# accelerate, and datasets. They are irrelevant to the conversion path tested
# here, so stub only those utility imports, not the driver implementation.
utils_pkg = types.ModuleType("lerobot.utils")
utils_pkg.__path__ = []
sys.modules["lerobot.utils"] = utils_pkg
errors = types.ModuleType("lerobot.utils.errors")
class DeviceAlreadyConnectedError(Exception): pass
class DeviceNotConnectedError(Exception): pass
errors.DeviceAlreadyConnectedError = DeviceAlreadyConnectedError
errors.DeviceNotConnectedError = DeviceNotConnectedError
sys.modules["lerobot.utils.errors"] = errors
utils = types.ModuleType("lerobot.utils.utils")
utils.enter_pressed = lambda: False
utils.move_cursor_up = lambda *args, **kwargs: None
sys.modules["lerobot.utils.utils"] = utils

# Recording replacement for the SDK boundary. The real LeRobot code invokes
# GroupSyncWrite.addParam(id, serialized_bytes) and txPacket(); nothing is sent.
sdk = types.ModuleType("scservo_sdk")
sdk.COMM_SUCCESS = 0
sdk.SCS_LOBYTE = lambda x: x & 0xFF
sdk.SCS_HIBYTE = lambda x: (x >> 8) & 0xFF
sdk.SCS_LOWORD = lambda x: x & 0xFFFF
sdk.SCS_HIWORD = lambda x: (x >> 16) & 0xFFFF
class PortHandler:
    def __init__(self, port): self.is_open = True; self.port = port
    def setPacketTimeout(self, *args, **kwargs): pass
class PacketHandler:
    def __init__(self, protocol): pass
class GroupSyncRead:
    def __init__(self, *args): pass
class GroupSyncWrite:
    def __init__(self, *args):
        self.start_address = 0; self.data_length = 0; self.params = []
    def clearParam(self): self.params.clear()
    def addParam(self, motor_id, data): self.params.append((motor_id, list(data))); return True
    def txPacket(self): return 0
sdk.PortHandler = PortHandler
sdk.PacketHandler = PacketHandler
sdk.GroupSyncRead = GroupSyncRead
sdk.GroupSyncWrite = GroupSyncWrite
sys.modules["scservo_sdk"] = sdk

from lerobot.motors.motors_bus import Motor, MotorCalibration, MotorNormMode
from lerobot.motors.feetech.feetech import FeetechMotorsBus

def make_bus(mode: MotorNormMode, name: str = "joint"):
    motors = {name: Motor(id=1, model="sts3215", norm_mode=mode)}
    calibration = {name: MotorCalibration(
        id=1, drive_mode=0, homing_offset=0, range_min=0, range_max=4095
    )}
    return FeetechMotorsBus(port="NO_REAL_SERIAL_DEVICE", motors=motors, calibration=calibration)

cases = [
    ("finite_mid", 0.0, MotorNormMode.RANGE_M100_100, "write"),
    ("nan", float("nan"), MotorNormMode.RANGE_M100_100, "write"),
    ("positive_inf", float("inf"), MotorNormMode.RANGE_M100_100, "write"),
    ("negative_inf", float("-inf"), MotorNormMode.RANGE_M100_100, "write"),
    ("huge_positive", 1e100, MotorNormMode.RANGE_M100_100, "write"),
    ("huge_negative", -1e100, MotorNormMode.RANGE_M100_100, "write"),
    ("degrees_nan", float("nan"), MotorNormMode.DEGREES, "ValueError"),
    ("degrees_positive_inf", float("inf"), MotorNormMode.DEGREES, "OverflowError"),
    ("degrees_negative_inf", float("-inf"), MotorNormMode.DEGREES, "OverflowError"),
    ("degrees_huge_positive", 1e100, MotorNormMode.DEGREES, "ValueError"),
    ("degrees_huge_negative", -1e100, MotorNormMode.DEGREES, "ValueError"),
]
failures = []
for name, value, mode, expected in cases:
    bus = make_bus(mode)
    try:
        bus.sync_write("Goal_Position", {"joint": value})
        result = bus.sync_writer.params
        print(f"{name}: WRITE_ATTEMPTED mode={mode.value} input={value!r} "
              f"address={bus.sync_writer.start_address} width={bus.sync_writer.data_length} "
              f"serialized_params={result!r}")
        if expected != "write":
            failures.append(f"{name}: expected {expected}, but write was attempted")
        if not result:
            failures.append(f"{name}: sync writer received no serialized params")
        if result and (len(result[0][1]) != 2 or any(not (0 <= b <= 255) for b in result[0][1])):
            failures.append(f"{name}: invalid serialized byte payload {result!r}")
    except Exception as exc:
        print(f"{name}: EXCEPTION {type(exc).__name__}: {exc}")
        if expected == "write":
            failures.append(f"{name}: expected serialized write, got {type(exc).__name__}")
        elif type(exc).__name__ != expected:
            failures.append(f"{name}: expected {expected}, got {type(exc).__name__}")

# Explicitly test gripper normalization using the real RANGE_0_100 path.
for name, value, expected_raw in [
    ("gripper_nan", float("nan"), 0),
    ("gripper_positive_inf", float("inf"), 4095),
    ("gripper_negative_inf", float("-inf"), 0),
]:
    bus = make_bus(MotorNormMode.RANGE_0_100, "gripper")
    bus.sync_write("Goal_Position", {"gripper": value})
    payload = bus.sync_writer.params
    # Reverse the actual little-endian serialized payload to inspect the
    # encoded raw register value for the positive-range, non-sign-bit endpoints.
    assert payload, f"{name}: no payload captured"
    raw = payload[0][1][0] | (payload[0][1][1] << 8)
    print(f"{name}: WRITE_ATTEMPTED input={value!r} raw_encoded={raw} bytes={payload[0][1]!r}")
    if raw != expected_raw:
        failures.append(f"{name}: expected raw endpoint {expected_raw}, got {raw}")

if failures:
    print("FAILURES:")
    for failure in failures: print(f" - {failure}")
    raise SystemExit(1)
print(f"PASS: {len(cases) + 3} cases exercised against pinned LeRobot conversion/write code; no hardware connected.")
