import curses
import time
import random
import psutil
from pyfiglet import Figlet

# EVE-X feminine faces
eve_faces = {
    "normal": [...],  # (same content as before)
    "blink": [...],
    "angry": [...],
    "safe": [...],
    "worry": [...],
    "risk": [...],
    "war": [...],
    "sleep": [...]
}

face_keys = ["normal", "angry", "safe", "worry", "risk", "war", "sleep"]

face_colors = {
    "normal": (curses.COLOR_BLACK, curses.COLOR_WHITE),
    "blink": (curses.COLOR_BLACK, curses.COLOR_WHITE),
    "angry": (curses.COLOR_RED, curses.COLOR_WHITE),
    "safe": (curses.COLOR_GREEN, curses.COLOR_WHITE),
    "worry": (curses.COLOR_BLUE, curses.COLOR_WHITE),
    "risk": (curses.COLOR_RED, curses.COLOR_BLACK),
    "war": (curses.COLOR_BLACK, curses.COLOR_RED),
    "sleep": (curses.COLOR_WHITE, curses.COLOR_BLACK)
}

def draw_eve_feminine(stdscr):
    curses.start_color()
    curses.curs_set(0)
    stdscr.nodelay(True)
    height, width = stdscr.getmaxyx()

    counter = 0
    current_face_key = "normal"

    # Initialize color pairs
    pair_ids = {}
    pair_counter = 1
    for name, (fg, bg) in face_colors.items():
        curses.init_pair(pair_counter, fg, bg)
        pair_ids[name] = pair_counter
        pair_counter += 1

    fig = Figlet(font='slant')
    title_lines = fig.renderText("EVE-X").split('\n')

    while True:
        face_key_to_use = "blink" if counter % 5 == 0 else current_face_key
        face = eve_faces[face_key_to_use]
        color_pair = curses.color_pair(pair_ids[face_key_to_use])

        stdscr.clear()

        # Print ASCII title
        for i, line in enumerate(title_lines):
            x = width // 2 - len(line) // 2
            stdscr.addstr(i, x, line[:width - 1], color_pair)

        # Print face
        for i, line in enumerate(face):
            x = width // 2 - len(line) // 2
            y = height // 2 - len(face) // 2 + i
            stdscr.addstr(y, x, line, color_pair)

        # Show current mode
        mode_text = f"<MODE: {face_key_to_use.upper()}>"
        stdscr.addstr(height // 2 + len(face) // 2 + 1, width // 2 - len(mode_text) // 2, mode_text, color_pair)

        # Draw CPU & MEM usage as bars
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory().percent
        cpu_bar = "█" * (int(cpu / 5)).clip(0, 20)
        mem_bar = "█" * (int(mem / 5)).clip(0, 20)
        stats_line1 = f"CPU [{cpu:3}%]: {cpu_bar:<20}"
        stats_line2 = f"MEM [{mem:3}%]: {mem_bar:<20}"
        stdscr.addstr(height - 3, width // 2 - len(stats_line1) // 2, stats_line1, color_pair)
        stdscr.addstr(height - 2, width // 2 - len(stats_line2) // 2, stats_line2, color_pair)

        stdscr.refresh()
        time.sleep(0.5)

        counter += 1
        if counter % 10 == 0:
            current_face_key = random.choice(face_keys)

        try:
            if stdscr.getch() == ord('q'):
                break
        except:
            pass

if __name__ == "__main__":
    curses.wrapper(draw_eve_feminine)
