# Local architecture

USB microphone → mono 16kHz PCM → Vosk restricted local grammar → exact lamp command policy. PIR on BCM17 is telemetry. INA219 on I2C1 0x40 polls lamp current; invalid readings/overflow/reset/absolute current above 300mA turn BCM27 relay off and require explicit re-enable. No networking or hidden model download at runtime. Use README/SVG exact voltage/pin map.
