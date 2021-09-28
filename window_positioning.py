def centered(w, h, ws, hs):
    x = int((ws / 2) - (w / 2))
    y = int((hs / 2) - (h / 2))

    return f"{w}x{h}+{x}+{y}"
