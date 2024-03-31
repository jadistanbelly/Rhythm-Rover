# Function to find total seconds of a timestamp
def totalseconds(time_str):
    components = time_str.split(':') # Split by colon
    if len(components) == 3:
        # Format: HH:MM:SS
        hours, minutes, seconds = map(int, components)
        total_seconds = hours * 3600 + minutes * 60 + seconds
    elif len(components) == 2:
        # Format: MM:SS
        minutes, seconds = map(int, components)
        total_seconds = minutes * 60 + seconds
    elif len(components) == 1:
        # Format: SS
        total_seconds = int(components[0])
    else:
        raise ValueError("Invalid timestamp format")
    return total_seconds