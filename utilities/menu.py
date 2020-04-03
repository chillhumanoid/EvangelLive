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

def input_option(stdscr, string, display_y, display_x, cursor_y, isEmpty):
    if cursor_y == display_y:
        if isEmpty:
            stdscr.attron(curses.color_pair(2))
        else:
            stdscr.attron(curses.color_pair(1))
    stdscr.addstr(display_y, display_x, string)
    if cursor_y == display_y:
        if isEmpty:
            stdscr.attroff(curses.color_pair(2))
        else:
            stdscr.attroff(curses.color_pair(1))

def add_label(stdscr, string, display_y, display_x):
    stdscr.addstr(display_y, display_x, string)

def add_solid(stdscr, string, display_y, display_x, cursor_y):
    if display_y == cursor_y:
        stdscr.attron(curses.color_pair(3))
    stdscr.addstr(display_y, display_x, string)
    if display_y == cursor_y:
        stdscr.attroff(curses.color_pair(3))

def add_string(stdscr, string, display_y, display_x):
    stdscr.addstr(display_y, display_x, string)

def status(stdscr, isError, success, display_y, error_color, success_color):
    width = get_width(stdscr)
    if isError:
        stdscr.attron(error_color)
    else:
        stdscr.attron(success_color)
    stdscr.addstr(display_y, (width - len(success)) // 2, success)
    if isError:
        stdscr.attroff(error_color)
    else:
        stdscr.attroff(success_color)

def inputs(text, k, x_pos_max, cursor_x):
    char = str(chr(k))
    if char.isnumeric():
        if not cursor_x == x_pos_max + len(text):
            s_pos = cursor_x - x_pos_max
            temp = list(text)
            temp[s_pos] = char
            text = "".join(temp)
    return text

def time_markers(isEnabled, display_y, display_x, stdscr):
    if isEnabled:
        stdscr.attron(curses.color_pair(4))
        stdscr.addstr(display_y, display_x, "TRUE")
        stdscr.attroff(curses.color_pair(4))
    else:
        stdscr.attron(curses.color_pair(2))
        stdscr.addstr(display_y, display_x, "FALSE")
        stdscr.attroff(curses.color_pair(2))
