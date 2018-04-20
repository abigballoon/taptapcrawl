def safe_int(num, instead=0):
    try:
        return int(num)
    except ValueError:
        return instead