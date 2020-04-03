import curses
from utilities import arith

def get_width(stdscr):
    return stdscr.getmaxyx()[1]
def get_height(stdscr):
    return stdscr.getmaxyx()[0]

def title(stdscr, title):
    display_x = arith.title_start(title, get_width(stdscr))
    stdscr.attron(curses.color_pair(1))
    stdscr.attron(curses.A_BOLD)
    stdscr.addstr(0, display_x, title)
    stdscr.attroff(curses.A_BOLD)
    stdscr.attroff(curses.color_pair(1))

def status_bar(stdscr, status_msg):
    display_y = get_height(stdscr) - 1
    magic_number = (get_width(stdscr) - len(status_msg) - 1)

    stdscr.attron(curses.color_pair(3))
    stdscr.addstr(display_y, 0, status_msg)
    stdscr.addstr(display_y, len(status_msg), " " * magic_number)
    stdscr.attroff(curses.color_pair(3))


def menu_option(stdscr, string, display_y, display_x, cursor_y):
    if cursor_y == display_y:
        stdscr.attron(curses.color_pair(3))
    stdscr.addstr(display_y, display_x, string)
    if cursor_y == display_y:
        stdscr.attroff(curses.color_pair(3))
