# Room Climate Hub Voice Control

Build a smart home prototype that uses relay module, current sensor, PIR sensor to accept local voice commands. Include setup instructions, a circuit diagram, tested firmware, and sample output.

## Project details

| Field | Value |
| --- | --- |
| Roadmap ID | 3 |
| Category | Smart Home |
| Platform | Raspberry Pi Zero 2 W |
| Difficulty | Intermediate |
| Estimated build time | 28 hours |
| Connectivity | Local only |
| Core components | relay module, current sensor, PIR sensor |
| Control mode | closed loop control |

## Repository layout

- `src/main.py`: runnable firmware or application
- `docs/wiring.md`: suggested low-voltage wiring plan
- `docs/architecture.md`: system data flow
- `docs/test-plan.md`: repeatable verification steps
- `sample-data/example.json`: example telemetry record
- `tools/validate.py`: dependency-free repository validation

## Quick start

1. Run `python -m src.main --iterations 10 --interval 0.5`.
2. Run `python -m unittest discover -s tests -v`.
3. Replace `simulated_values()` with a hardware adapter after bench testing.

## Expected behavior

Voice Control demonstration with repeatable test steps. The default implementation supports simulated or generic analog inputs so the control path can be exercised before hardware-specific drivers are added.

## Hardware adaptation

The included code is a safe reference implementation. Update pin assignments and sensor conversions from the exact component datasheets, then repeat the test plan before connecting actuators.

## License

MIT
