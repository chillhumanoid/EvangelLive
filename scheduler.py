import curses, time, sys
from utilities import menu as m
def start(stdscr):
    cursor_x = 1
    cursor_y = 1
    k = 0

    curses.curs_set(0)

    stdscr.clear()
    stdscr.refresh()

    height, width = stdscr.getmaxyx()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)

    title_str = "Evangel Live Scheduler"
    status_msg = " Made by Jonathan Thorne | For Help Contact jonathan@evangelchurch.com "
    option_1 = "1. Sunday Morning"
    option_2 = "2. Wednesday Night"
    option_3 = "3. Exit"

    while(True):
        stdscr.clear()

        m.title(stdscr, title_str)
        m.status_bar(stdscr, status_msg)

        m.menu_option(stdscr, option_1, 1, 1, cursor_y)
        m.menu_option(stdscr, option_2, 2, 1, cursor_y)
        m.menu_option(stdscr, option_3, 3, 1, cursor_y)

        stdscr.move(cursor_y, cursor_x)
        stdscr.refresh()
        k = stdscr.getch()
        if k == 27 or k == ord('q'):
            sys.exit()
        elif k == curses.KEY_UP:
            cursor_y -= 1
            if cursor_y == 0:
                cursor_y = 3
        elif k == curses.KEY_DOWN:
            cursor_y += 1
            if cursor_y == 4:
                cursor_y = 1
        elif k == ord('1') or (k == 10 and cursor_y == 1):
            print("SUNDAY MORNING")
            time.sleep(1)
        elif k == ord('2') or (k == 10 and cursor_y == 2):
            print("WEDNESDAY NIGHT")
            time.sleep(1)
        elif k == ord('3') or (k == 10 and cursor_y == 3):
            sys.exit()




curses.wrapper(start)
