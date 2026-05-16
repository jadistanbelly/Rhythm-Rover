def totalseconds(time_str):
    """Convert SS, MM:SS, or HH:MM:SS timestamps into total seconds."""
    if not isinstance(time_str, str):
        raise ValueError("Timestamp must be a string")

    components = time_str.strip().split(":")
    if not components or len(components) > 3:
        raise ValueError("Invalid timestamp format")

    if any(not component.isdecimal() for component in components):
        raise ValueError("Invalid timestamp format")

    values = [int(component) for component in components]
    if len(values) >= 2 and values[-1] >= 60:
        raise ValueError("Seconds must be between 0 and 59")
    if len(values) == 3 and values[-2] >= 60:
        raise ValueError("Minutes must be between 0 and 59")

    if len(values) == 3:
        hours, minutes, seconds = values
        return hours * 3600 + minutes * 60 + seconds
    if len(values) == 2:
        minutes, seconds = values
        return minutes * 60 + seconds
    return values[0]
