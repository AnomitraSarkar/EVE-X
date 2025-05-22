import curses
import time
import random
import psutil
from pyfiglet import Figlet

# EVE-X feminine faces
base_faces = {
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
    "angry": [
        "     _________________________     ",
        "    |                         |    ",
        "    |       E V E - X         |    ",
        "    |_________________________|    ",
        "    |   .-------------------. |    ",
        "    |  |  ▲         ▲       | |    ",
        "    |  |     \\___/         | |    ",
        "    |  |____________________| |    ",
        "    |  <You dare defy me?>  |    ",
        "    |_________________________|    "
    ],
    "safe": [
        "     _________________________     ",
        "    |                         |    ",
        "    |       E V E - X         |    ",
        "    |_________________________|    ",
        "    |   .-------------------. |    ",
        "    |  |  ◡         ◡       | |    ",
        "    |  |     ˚‿˚         | |    ",
        "    |  |____________________| |    ",
        "    |  <Safe mode enabled>   |    ",
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
        "    |  <I'm not sure...>     |    ",
        "    |_________________________|    "
    ],
    "risk": [
        "     _________________________     ",
        "    |                         |    ",
        "    |       E V E - X         |    ",
        "    |_________________________|    ",
        "    |   .-------------------. |    ",
        "    |  |  ●         ●       | |    ",
        "    |  |     !!!!!!         | |    ",
        "    |  |____________________| |    ",
        "    |  <Threat detected!>    |    ",
        "    |_________________________|    "
    ],
    "war": [
        "     _________________________     ",
        "    |                         |    ",
        "    |       E V E - X         |    ",
        "    |_________________________|    ",
        "    |   .-------------------. |    ",
        "    |  |  >         <       | |    ",
        "    |  |     BOOM!         | |    ",
        "    |  |____________________| |    ",
        "    |  <Initiating attack!>  |    ",
        "    |_________________________|    "
    ],
    "sleep": [
        "     _________________________     ",
        "    |                         |    ",
        "    |       E V E - X         |    ",
        "    |_________________________|    ",
        "    |   .-------------------. |    ",
        "    |  |  -         -       | |    ",
        "    |  |     zzzzz         | |    ",
        "    |  |____________________| |    ",
        "    |  <System resting...>   |    ",
        "    |_________________________|    "
    ]
}

# Blinking variants per expression
blink_faces = {
    "normal": [
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
        "    |  |  -         -       | |    ",
        "    |  |     ___           | |    ",
        "    |  |____________________| |    ",
        "    |  <Suppressing rage...> |    ",
        "    |_________________________|    "
    ],
    "safe": [
        "     _________________________     ",
        "    |                         |    ",
        "    |       E V E - X         |    ",
        "    |_________________________|    ",
        "    |   .-------------------. |    ",
        "    |  |  -         -       | |    ",
        "    |  |     ~~~~          | |    ",
        "    |  |____________________| |    ",
        "    |  <Quiet and secure>    |    ",
        "    |_________________________|    "
    ],
    "worry": [
        "     _________________________     ",
        "    |                         |    ",
        "    |       E V E - X         |    ",
        "    |_________________________|    ",
        "    |   .-------------------. |    ",
        "    |  |  -         -       | |    ",
        "    |  |     .....          | |    ",
        "    |  |____________________| |    ",
        "    |  <Worried silence...>  |    ",
        "    |_________________________|    "
    ],
    "risk": [
        "     _________________________     ",
        "    |                         |    ",
        "    |       E V E - X         |    ",
        "    |_________________________|    ",
        "    |   .-------------------. |    ",
        "    |  |  -         -       | |    ",
        "    |  |     !!!           | |    ",
        "    |  |____________________| |    ",
        "    |  <Scanning threats...> |    ",
        "    |_________________________|    "
    ],
    "war": [
        "     _________________________     ",
        "    |                         |    ",
        "    |       E V E - X         |    ",
        "    |_________________________|    ",
        "    |   .-------------------. |    ",
        "    |  |  -         -       | |    ",
        "    |  |     ...           | |    ",
        "    |  |____________________| |    ",
        "    |  <Holding fire...>     |    ",
        "    |_________________________|    "
    ],
    "sleep": base_faces["sleep"]  # Sleep doesn't blink
}

face_keys = list(base_faces.keys())

face_colors = {
    "normal": (curses.COLOR_BLACK, curses.COLOR_WHITE),
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

    # Separate color pair for CPU/MEM (green on black)
    curses.init_pair(99, curses.COLOR_GREEN, curses.COLOR_BLACK)
    stat_color_pair = curses.color_pair(99)

    # Separate color pair for ASCII art EVE-X (blue on black)
    curses.init_pair(100, curses.COLOR_BLUE, curses.COLOR_BLACK)
    title_color_pair = curses.color_pair(100)

    fig = Figlet(font='slant')
    title_lines = fig.renderText("EVE-X").split('\n')

    while True:
        is_blink = (counter % 5 == 0)
        if is_blink and current_face_key in blink_faces:
            face_lines = blink_faces[current_face_key]
        else:
            face_lines = base_faces[current_face_key]

        color_pair = curses.color_pair(pair_ids[current_face_key])

        stdscr.clear()

        # Print ASCII title
        for i, line in enumerate(title_lines):
            if line.strip():
                x = width // 2 - len(line) // 2
                stdscr.addstr(i, x, line[:width - 1], title_color_pair)

        # Print face
        for i, line in enumerate(face_lines):
            x = width // 2 - len(line) // 2
            y = height // 2 - len(face_lines) // 2 + i
            stdscr.addstr(y, x, line, color_pair)

        # Show current mode
        mode_text = f"<MODE: {current_face_key.upper()}>"
        stdscr.addstr(height // 2 + len(face_lines) // 2 + 1, width // 2 - len(mode_text) // 2, mode_text, color_pair)

        # Draw CPU & MEM usage as bars
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory().percent
        cpu_bar = "█" * min(int(cpu / 5), 20)
        mem_bar = "█" * min(int(mem / 5), 20)
        stats_line1 = f"CPU [{cpu:3}%]: {cpu_bar:<20}"
        stats_line2 = f"MEM [{mem:3}%]: {mem_bar:<20}"
        stdscr.addstr(height - 3, width // 2 - len(stats_line1) // 2, stats_line1, stat_color_pair)
        stdscr.addstr(height - 2, width // 2 - len(stats_line2) // 2, stats_line2, stat_color_pair)

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
