def get_start_of_packet_marker(data_stream: str, packet_length: int) -> int | None:
    for i in range(len(data_stream) - packet_length):
        block = data_stream[i : i + packet_length]
        if len(set(block)) == packet_length:
            return i + packet_length


filepath = "./input"

with open(filepath, "r") as file:
    data_stream = file.read()


result = get_start_of_packet_marker(data_stream, 4)
print(f"Puzzle 1: {result}")

result = get_start_of_packet_marker(data_stream, 14)
print(f"Puzzle 2: {result}")
