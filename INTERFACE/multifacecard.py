import curses
import time
import random
import psutil

# EVE-X feminine faces
eve_faces = {
    "normal": [
        "     _________________________     ",
        "    |                         |    ",
        "    |       E V E - X         |    ",
        "    |_________________________|    ",
        "    |   .-------------------. |    ",
        "    |  |  ◕         ◕       | |    ",
        "    |  |       ⏝⏝⏝         | |    ",
        "    |  |____________________| |    ",
        "    |  <I see everything...>  |    ",
        "    |_________________________|    "
    ],
    "blink": [
        "     _________________________     ",
        "    |                         |    ",
        "    |       E V E - X         |    ",
        "    |_________________________|    ",
        "    |   .-------------------. |    ",
        "    |  |  -         -       | |    ",
        "    |  |     _____         | |    ",
        "    |  |____________________| |    ",
        "    |  <Analyzing input...>  |    ",
        "    |_________________________|    "
    ],
    "angry": [
        "     _________________________     ",
        "    |                         |    ",
        "    |       E V E - X         |    ",
        "    |_________________________|    ",
        "    |   .-------------------. |    ",
        "    |  |  >         <       | |    ",
        "    |  |     /////         | |    ",
        "    |  |____________________| |    ",
        "    |  <System alert!>       |    ",
        "    |_________________________|    "
    ],
    "safe": [
        "     _________________________     ",
        "    |                         |    ",
        "    |       E V E - X         |    ",
        "    |_________________________|    ",
        "    |   .-------------------. |    ",
        "    |  |  ^         ^       | |    ",
        "    |  |     ---           | |    ",
        "    |  |____________________| |    ",
        "    |  <You're protected.>     |    ",
        "    |_________________________|    "
    ],
    "worry": [
        "     _________________________     ",
        "    |                         |    ",
        "    |       E V E - X         |    ",
        "    |_________________________|    ",
        "    |   .-------------------. |    ",
        "    |  |  o         o       | |    ",
        "    |  |     ~~~~~         | |    ",
        "    |  |____________________| |    ",
        "    |  <Are you okay...?>    |    ",
        "    |_________________________|    "
    ],
    "risk": [
        "     _________________________     ",
        "    |                         |    ",
        "    |       E V E - X         |    ",
        "    |_________________________|    ",
        "    |   .-------------------. |    ",
        "    |  |  !         !       | |    ",
        "    |  |     XXX           | |    ",
        "    |  |____________________| |    ",
        "    |  <Dangerous levels.>    |    ",
        "    |_________________________|    "
    ],
    "war": [
        "     _________________________     ",
        "    |                         |    ",
        "    |       E V E - X         |    ",
        "    |_________________________|    ",
        "    |   .-------------------. |    ",
        "    |  |  X         X       | |    ",
        "    |  |     !!!           | |    ",
        "    |  |____________________| |    ",
        "    |  <Entering combat...>  |    ",
        "    |_________________________|    "
    ],
    "sleep": [
        "     _________________________     ",
        "    |                         |    ",
        "    |       E V E - X         |    ",
        "    |_________________________|    ",
        "    |   .-------------------. |    ",
        "    |  |  -         -       | |    ",
        "    |  |     zzz           | |    ",
        "    |  |____________________| |    ",
        "    |  <...sleeping...>      |    ",
        "    |_________________________|    "
    ]
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

    while True:
        face_key_to_use = "blink" if counter % 5 == 0 else current_face_key
        face = eve_faces[face_key_to_use]
        color_pair = curses.color_pair(pair_ids[face_key_to_use])

        stdscr.clear()
        for i, line in enumerate(face):
            x = width // 2 - len(line) // 2
            y = height // 2 - len(face) // 2 + i
            stdscr.addstr(y, x, line, color_pair)

        # Get system stats
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory()
        stats_line = f"CPU: {cpu}% | MEM: {mem.percent}%"

        # Display system stats at bottom
        stdscr.addstr(height - 2, width // 2 - len(stats_line) // 2, stats_line, color_pair)

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
