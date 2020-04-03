from math import ceil

def title_start(title, width):
    return int((width // 2) - (len(title) // 2) - len(title) % 2)
