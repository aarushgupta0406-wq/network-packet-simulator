# Network Packet Transmission & Integrity Simulator

A Python-based simulation demonstrating data packetization, transmission over an unreliable channel, ASCII checksum verification, and automatic retransmission.

## Overview
When data moves across physical networks, continuous data streams are divided into discrete packets. This simulation models:
- **Packet Segmentation:** Slicing continuous strings into numbered chunks.
- **Data Integrity Verification:** Generating ASCII-based checksums for each packet payload using `ord()`.
- **Channel Noise Simulation:** Simulating line interference and bit corruption.
- **Retransmission Protocol:** Identifying checksum mismatches and requesting replacement packets to guarantee 100% data fidelity.

## Tech Stack
- Python 3 (Lists, Dictionaries, String Slicing)
- Standard Library only (Zero external dependencies)

## How to Run
Run the script directly in your terminal:
```bash
python packet_sim.py
