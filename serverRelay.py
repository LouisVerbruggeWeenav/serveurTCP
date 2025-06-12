def extract_io_element(io_data, target_io_id):
    """
    Cherche l'élément IO avec l'ID donné (ex: 500) et retourne sa valeur brute.
    """
    index = 0
    while index < len(io_data):
        io_id = io_data[index]
        io_length = io_data[index + 1]
        io_value = io_data[index + 2:index + 2 + io_length]

        if io_id == target_io_id:
            return io_value

        index += 2 + io_length
    return None

def decode_avl_data(data):
    codec_id = data[4]
    record_count = data[5]
    print(f"📦 Codec ID: {codec_id}, Records: {record_count}")

    timestamp = struct.unpack(">Q", data[6:14])[0]
    dt = datetime.utcfromtimestamp(timestamp / 1000.0)
    print(f"🕓 Timestamp: {dt}")

    # IOs: on saute jusqu'au champ IO
    io_base = 6 + 8 + 1 + 15
    total_io = data[io_base]
    one_byte_count = data[io_base + 1]
    two_byte_count = data[io_base + 2]
    four_byte_count = data[io_base + 3]
    eight_byte_count = data[io_base + 4]

    io_start = io_base + 5
    io_data = data[io_start:]

    print(f"🔍 Total IOs: {total_io} (1B:{one_byte_count}, 2B:{two_byte_count}, 4B:{four_byte_count}, 8B:{eight_byte_count})")

    # Exemple: IO ID 500, supposé être un 8-byte CAN frame
    target_io_id = 500
    can_data = extract_io_element(io_data, target_io_id)

    if can_data:
        print(f"🟦 CAN ID 0x1806E5F4 (IO ID 500) → {can_data.hex().upper()}")
    else:
        print(f"❌ IO ID {target_io_id} non trouvé.")

    return dt
