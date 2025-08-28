def prompt(msg):
    return input(msg).strip()

def safe_int(val):
    try:
        return int(val)
    except Exception:
        return None

def nl():
    print()
