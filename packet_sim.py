# =============================================================================
# Project: Network Packet Transmission & Integrity Simulator
# Description: Simulates data packetization, ASCII checksum generation,
#              transmission line corruption, and automated packet retransmission.
# =============================================================================

def create_packets(message, chunk_size=3):
    """
    Slices a continuous data stream into smaller packet chunks.
    Attaches a sequence ID and calculates a checksum for error detection.
    """
    packets = []
    packet_id = 1

    for i in range(0, len(message), chunk_size):
        chunk = message[i:i + chunk_size]

        # Calculate checksum: sum of ASCII values of each character
        checksum = 0
        for char in chunk:
            checksum += ord(char)

        packet = {
            "id": packet_id,
            "data": chunk,
            "checksum": checksum
        }
        packets.append(packet)
        packet_id += 1

    return packets


def display_packets(packets, title="Packet Buffer"):
    """Displays packet headers and payload contents in an aligned table."""
    print(f"\n--- {title} ---")
    print(f"{'Packet ID':<10} | {'Payload Data':<15} | {'Checksum':<10}")
    print("-" * 42)
    for p in packets:
        print(f"{p['id']:<10} | {p['data']:<15} | {p['checksum']:<10}")
    print("-" * 42)


def simulate_transmission_noise(packets):
    """
    Simulates noise on the physical transmission line by altering
    a character in the first packet without updating its checksum.
    """
    if not packets:
        return

    print("\n[Simulating Channel Noise / Line Interference]")
    target = packets[0]
    original_data = target["data"]

    # Alter the first character to simulate a bit flip
    corrupted_data = "?" + original_data[1:]
    target["data"] = corrupted_data

    print(f">> Channel Noise Injected: Packet #{target['id']} payload altered from '{original_data}' to '{corrupted_data}'.")


def receive_and_verify(packets, sender_cache):
    """
    Simulates the receiver node auditing each packet.
    Recalculates the checksum, flags corruptions, and triggers retransmission.
    """
    print("\n--- Receiver Node: Inbound Verification ---")
    reconstructed_message = ""
    retransmission_count = 0

    for p in packets:
        # Step 1: Recalculate checksum at the receiving terminal
        computed_checksum = 0
        for char in p["data"]:
            computed_checksum += ord(char)

        # Step 2: Compare recalculated sum against the header checksum
        if computed_checksum == p["checksum"]:
            print(f"[VERIFIED] Packet #{p['id']} passed data integrity check.")
            reconstructed_message += p["data"]
        else:
            print(f"[CORRUPTED] Checksum mismatch in Packet #{p['id']}!")
            print(f"   Header Checksum: {p['checksum']} | Computed: {computed_checksum}")
            print(f">> Sending Retransmission Request (NACK) for Packet #{p['id']}...")

            # Step 3: Fetch uncorrupted copy from the sender's cache
            for clean_packet in sender_cache:
                if clean_packet["id"] == p["id"]:
                    reconstructed_message += clean_packet["data"]
                    retransmission_count += 1
                    print(f">> Packet #{p['id']} retransmitted and verified successfully.")
                    break

    # Final transmission summary
    print("\n" + "=" * 48)
    print("           TRANSMISSION AUDIT REPORT")
    print("=" * 48)
    print(f"Total Packets Transmitted : {len(packets)}")
    print(f"Packets Corrupted on Wire : {retransmission_count}")
    print(f"Reconstructed Payload     : '{reconstructed_message}'")
    print("Integrity Verification    : 100% Data Restored")
    print("=" * 48)


def main():
    print("=== NETWORK PACKET TRANSMISSION & INTEGRITY SIMULATOR ===")
    user_input = input("Enter payload message to transmit: ").strip()

    if not user_input:
        user_input = "NETWORK PROTOCOL TEST"
        print(f"Defaulting payload to: '{user_input}'")

    # 1. Sender segments the payload into discrete packets
    packets = create_packets(user_input)
    display_packets(packets, "Packets Generated at Sender Node")

    # Maintain an unmodified sender cache for retransmission handling
    sender_cache = [dict(p) for p in packets]

    # 2. Transmission phase (optional noise simulation)
    choice = input("\nSimulate transmission channel noise / bit corruption? (y/n): ").strip().lower()
    if choice == "y":
        simulate_transmission_noise(packets)
        display_packets(packets, "Packets Arriving at Inbound Buffer")

    # 3. Receiver verifies integrity, detects errors, and reassembles payload
    receive_and_verify(packets, sender_cache)


if __name__ == "__main__":
    main()