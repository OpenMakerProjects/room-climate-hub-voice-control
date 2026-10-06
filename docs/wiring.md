# Wiring

The exact pin table is in README and editable circuit-diagram.svg. Pi pin1 3V3 → INA VCC; pin6 GND → all grounds/external negative; pin3 BCM2 SDA and pin5 BCM3 SCL → INA. Pin11 BCM17 ← 3.3V-safe PIR OUT. Pin13 BCM27 → active-high 3.3V-compatible relay IN. Fused external5V → relay COM; NO → INA VIN+; VIN− → 5V-rated LED lamp+; lamp− → externalnegative. External5V powers relay/PIR but never Pi GPIO or INA logic. USB microphone via OTG hub; Pi power separate USB.
