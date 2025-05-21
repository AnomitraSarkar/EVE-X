import curses
from curses import wrapper
import time

def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_RED)
    
    stdscr.clear()
    
    stdscr.addstr(0,0,"hello world")
    stdscr.addstr(2,0,"input stuff", curses.color_pair(1))
    
    
    stdscr.refresh()
    stdscr.getch()

wrapper(main)

