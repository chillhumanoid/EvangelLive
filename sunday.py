import curses, sys, win32com.client, os
import dateutil.parser
import datetime
from utilities import menu as m
import scheduler as sc

x_pos_cService = 0
x_pos_cServTime = 0
x_pos_hours = 0
x_pos_minutes = 0
x_pos_seconds = 0

temp_hour = 0
temp_minute = 0
temp_second = 0
temp_current = ""
temp_nine = 0
temp_eleven = 0
temp_one = 0
temp_three = 0
temp_five = 0
temp_seven = 0

def main_display(stdscr):
    cursor_y = 1
    editing = False
    k = 0

    scheduler = win32com.client.Dispatch('Schedule.Service')

    curses.curs_set(0)

    stdscr.clear()
    stdscr.refresh()

    height, width = stdscr.getmaxyx()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)

    global x_pos_cService
    global x_pos_cServTime
    global x_pos_hours
    global x_pos_minutes
    global x_pos_seconds

    title_str           = "Adjust Sunday Service"
    label_service_day   = "Current Service Day: "
    label_service_times = "Current Service Times: "
    label_length        = "Service Length: "
    label_hours         = "Hours: "
    label_minutes       = "Minutes: "
    label_seconds       = "Seconds: "
    status_msg_1        = " Press (e) to edit "
    status_msg_2        = " Press (tab) to go to next input | Press (s) to save "
    status_msg_3        = " Press (return) to Change Times | Press (tab) to go to next input | Press (s) to save "
    success             = ""
    if not temp_current == "":
        current_service = temp_current
    else:
        current_service       = get_current_service(scheduler)
    if not temp_nine == 0:
        if temp_nine == True:
            current_service_times = current_service_times +  "9am"
        if temp_eleven == True:
            if len(current_service_times) == 0:
                current_service_times = current_service_times + "11am"
            else:
                current_service_times = current_service_times + ", 11am"
        if temp_one == True:
            if len(current_service_times) == 0:
                current_service_times = current_service_times + "1pm"
            else:
                current_service_times = current_service_times + ", 1pm"
        if temp_three == True:
            if len(current_service_times) == 0:
                current_service_times = current_service_times + "3pm"
            else:
                current_service_times = current_service_times + ", 3pm"
        if temp_five == True:
            if len(current_service_times) == 0:
                current_service_times = current_service_times + "5pm"
            else:
                current_service_times = current_service_times + ", 5pm"
        if temp_six == True:
            if len(current_service_times) == 0:
                current_service_times = current_service_times + "7pm"
            else:
                current_service_times = current_service_times + ", 7pm"
    else:
        current_service_times = get_current_serv_times(scheduler)

    x_pos_cService      = len(label_service_day) + 2
    x_pos_cServTime     = len(label_service_times) + 2
    x_pos_hours         = len(label_hours) + 2
    x_pos_minutes       = len(label_minutes) + 2
    x_pos_seconds       = len(label_seconds) + 2
    if not temp_hour == 0:
        hours = temp_hour
        minutes = temp_minute
        seconds = temp_seconds
    else:
        hours, minutes, seconds = get_length_time()

    isError = False

    while(True):
        stdscr.clear()
        m.title(stdscr, title_str)
        if editing == False:
            cursor_x = 1
            curses.curs_set(0)
            m.status_bar(stdscr, status_msg_1)

            m.add_label(stdscr, label_service_day, 1, 1)
            m.add_solid(stdscr, current_service, 1, x_pos_cService, cursor_y)
            m.add_label(stdscr, label_service_times, 2, 1)
            m.add_solid(stdscr, current_service_times, 2, x_pos_cServTime, cursor_y)
            m.add_label(stdscr, label_length, 3, 1)
            m.add_label(stdscr, label_hours, 4, 1)
            m.add_solid(stdscr, hours, 4, x_pos_hours, cursor_y)
            m.add_label(stdscr, label_minutes, 5, 1)
            m.add_solid(stdscr, minutes, 5, x_pos_minutes, cursor_y)
            m.add_label(stdscr, label_seconds, 6, 1)
            m.add_solid(stdscr, seconds, 6, x_pos_seconds, cursor_y)


        else:
            if not cursor_y == 2:
                curses.curs_set(1)
            if cursor_y == 1:
                m.status_bar(stdscr, status_msg_2)
            else:
                m.status_bar(stdscr, status_msg_3)

            if isError == True:
                cursor_y = 1
                m.input_option(stdscr, label_service_day, 1, 1, cursor_y, True)
            else:
                m.input_option(stdscr, label_service_day, 1, 1, cursor_y, False)
            m.add_label(stdscr, label_service_times, 2, 1)
            m.add_label(stdscr, label_length, 3, 1)
            m.input_option(stdscr, label_hours, 4, 1, cursor_y, False)
            m.input_option(stdscr, label_minutes, 5, 1, cursor_y, False)
            m.input_option(stdscr, label_seconds, 6, 1, cursor_y, False)

            m.add_string(stdscr, current_service, 1, x_pos_cService)
            m.add_solid(stdscr, current_service_times, 2, x_pos_cServTime, cursor_y)
            m.add_string(stdscr, hours, 4, x_pos_hours)
            m.add_string(stdscr, minutes, 5, x_pos_minutes)
            m.add_string(stdscr, seconds, 6, x_pos_seconds)


            m.status(stdscr, isError, success, 4, curses.color_pair(2), curses.color_pair(4))


        stdscr.move(cursor_y, cursor_x)
        stdscr.refresh()
        k = stdscr.getch()
        if k == 27:
            sc.start()
        elif k == curses.KEY_UP:
            cursor_y -= 1
            if cursor_y == 0:
                cursor_y = 6
            elif cursor_y == 3:
                cursor_y = 2
            cursor_x = move_x(cursor_y)
        elif k == curses.KEY_DOWN:
            cursor_y += 1
            if cursor_y == 3:
                cursor_y = 4
            elif cursor_y == 7:
                cursor_y = 1
            cursor_x = move_x(cursor_y)
        elif k == ord('e') and editing == False:
            editing = True
            cursor_x = move_x(cursor_y)
        elif k == ord('s') and editing == True:
            pass
        elif k == 9 and editing == True:
            if cursor_y == 1:
                cursor_y = 2
            elif cursor_y == 2:
                cursor_y = 3
                time_spot = 1
            elif cursor_y == 3:
                if time_spot == 1:
                    time_spot = 2
                elif time_spot == 2:
                    time_spot = 3
                elif time_spot == 3:
                    time_spot = 1
                    cursor_y = 1
        elif k == 10 and editing == True and cursor_y == 2:
            global temp_hour
            global temp_minute
            global temp_second
            global temp_current
            temp_hour = hours
            temp_minute = minutes
            temp_second = seconds
            temp_current = current_service
            curses.wrapper(get_service_times)
        elif editing == True and k == curses.KEY_LEFT:
            if cursor_y == 1 and not cursor_x <= x_pos_cService:
                cursor_x -= 1
                str_pos = cursor_x - x_pos_cService
                if str_pos == 2 or str_pos == 5:
                    cursor_x -= 1
            elif cursor_y == 4 and not cursor_x <= x_pos_hours:
                cursor_x -= 1
            elif cursor_y == 5 and not cursor_x <= x_pos_minutes:
                cursor_x -= 1
            elif cursor_y == 6 and not cursor_x <= x_pos_hours:
                cursor_x -= 1
        elif editing == True and k == curses.KEY_RIGHT:
            if cursor_y == 1 and not cursor_x >= x_pos_cService +  len(current_service):
                cursor_x += 1
                str_pos = cursor_x - x_pos_cService
                if str_pos == 2 or str_pos == 5:
                    cursor_x += 1
            elif cursor_y == 4 and not cursor_x >= x_pos_hours + len(hours):
                cursor_x += 1
            elif cursor_y == 5 and not cursor_x >= x_pos_minutes + len(minutes):
                cursor_x += 1
            elif cursor_y == 6 and not cursor_x >= x_pos_seconds + len(seconds):
                cursor_x += 1
        elif editing == True:
            if cursor_y == 1:
                current_service = m.inputs(current_service, k, x_pos_cService, cursor_x)
                cursor_x += 1
                str_pos = (cursor_x - x_pos_cService)
                if str_pos == 2 or str_pos == 5:
                    cursor_x += 1
                if cursor_x == len(current_service) + x_pos_cService:
                    cursor_y = 2
                    cursor_x = move_x(cursor_y)
            elif cursor_y == 4:
                hours = m.inputs(hours, k, x_pos_hours, cursor_x)
                cursor_x += 1
                str_pos = (cursor_x - x_pos_hours)
                if str_pos == 2:
                    cursor_y = 5
                    cursor_x = move_x(cursor_y)
            elif cursor_y == 5:
                minutes = m.inputs(minutes, k, x_pos_minutes, cursor_x)
                cursor_x += 1
                str_pos = (cursor_x - x_pos_minutes)
                if str_pos == 2:
                    cursor_y = 6
                    cursor_x = move_x(cursor_y)
            elif cursor_y == 6:
                seconds = m.inputs(seconds, k, x_pos_seconds, cursor_x)
                cursor_x += 1
                str_pos = cursor_x - x_pos_seconds
                if str_pos == 2:
                    cursor_y = 1
                    cursor_x = move_x(cursor_y)

def get_service_times(stdscr):
    cursor_y = 1
    cursor_x = 0
    k        = 0

    nine   = False
    eleven = False
    one    = False
    three  = False
    five   = False
    seven  = False

    label_nine   = "9AM: "
    label_eleven = "11AM: "
    label_one    = "1PM: "
    label_three  = "3PM: "
    label_five   = "5PM: "
    label_seven  = "7PM: "

    item_nine    = ""
    item_eleven  = ""
    item_one     = ""
    item_three   = ""
    item_five    = ""
    item_seven   = ""

    x_pos_nine   = len(label_nine)   + 2
    x_pos_eleven = len(label_eleven) + 2
    x_pos_one    = len(label_one)    + 2
    x_pos_three  = len(label_three)  + 2
    x_pos_five   = len(label_five)   + 2
    x_pos_seven  = len(label_seven)  + 2

    curses.curs_set(0)

    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)

    title_str  = "Select Times"
    status_msg = " Press (tab) To Enable/Disable Time | Press (Enter) or (esc) to Save and Go Back "

    while (True):
        stdscr.clear()
        m.title(stdscr, title_str)
        m.status_bar(stdscr, status_msg)

        m.menu_option(stdscr, label_nine,   1, 1, cursor_y)
        m.menu_option(stdscr, label_eleven, 2, 1, cursor_y)
        m.menu_option(stdscr, label_one,    3, 1, cursor_y)
        m.menu_option(stdscr, label_three,  4, 1, cursor_y)
        m.menu_option(stdscr, label_five,   5, 1, cursor_y)
        m.menu_option(stdscr, label_seven,  6, 1, cursor_y)

        m.time_markers(nine,   1, x_pos_nine,   stdscr)
        m.time_markers(eleven, 2, x_pos_eleven, stdscr)
        m.time_markers(one,    3, x_pos_one,    stdscr)
        m.time_markers(three,  4, x_pos_three,  stdscr)
        m.time_markers(five,   5, x_pos_five,   stdscr)
        m.time_markers(seven,  7, x_pos_seven,  stdscr)

        stdscr.move(cursor_x, cursor_y)
        stdscr.refresh()
        k = stdscr.getch()

        if k == 27 or k == 10:
            stdscr.clear()
            stdscr.refresh()
            curses.wrapper(main_display)
        elif k == curses.KEY_DOWN:
            cursor_y += 1
            if cursor_y == 8:
                cursor_y = 1
        elif k == curses.KEY_UP:
            cursor_y -= 1
            if cursor_y == 0:
                cursor_y = 7
        elif k == 9:
            global temp_nine
            global temp_eleven
            global temp_one
            global temp_three
            global temp_five
            global temp_seven
            if cursor_y == 1:
                nine = not nine
            elif cursor_y == 2:
                eleven = not eleven
            elif cursor_y == 3:
                one = not one
            elif cursor_y == 4:
                three = not three
            elif cursor_y == 5:
                five = not five
            elif cursor_y == 6:
                seven = not seven
            temp_nine = nine
            temp_eleven = eleven
            temp_one = one
            temp_three = three
            temp_five = five
            tmep_seven = seven
def move_x(cursor_y):
    if cursor_y == 1:
        return x_pos_cService
    elif cursor_y == 2:
        return x_pos_cServTime
    elif cursor_y == 4:
        return x_pos_hours
    elif cursor_y == 5:
        return x_pos_minutes
    elif cursor_y == 6:
        return x_pos_seconds

def start():
    curses.wrapper(main_display)
def get_length_time():
    if not os.path.exists("current.txt"):
        return ("00", "00", "00")
    else:
        f = open("test.txt", "r")
        lines = f.readlines()
        print(len(lines))
        sys.exit()
def get_current_service(scheduler):
    scheduler.connect()
    root_folder = scheduler.GetFolder('\\')
    colTasks = root_folder.GetTasks(1)
    for task in colTasks:
        if task.Name == "sunday":
            taskDef = task.Definition
            t = taskDef.triggers
            for trigger in t:
                datestr = trigger.StartBoundary[:10]
                year, month, day = datestr.split('-')
                return "{}/{}/{}".format(month, day, year)
def get_current_serv_times(scheduler):
    scheduler.connect()
    root_folder = scheduler.GetFolder('\\')
    colTasks = root_folder.GetTasks(1)
    for task in colTasks:
        if task.Name == "sunday":
            rStr = ""
            triggers = task.Definition.triggers
            for trigger in triggers:
                datestr = trigger.StartBoundary[11:]
                hour, minutes, seconds = datestr.split(":")
                print(hour)
                if hour == "08":
                    rStr = rStr + "9am"
                elif hour == "10":
                    if len(rStr) == 0:
                        rStr = rStr + "11am"
                    else:
                        rStr = rStr + ", 11am"
                elif hour == "12":
                    if len(rStr) == 0:
                        rStr = rStr + "1pm"
                    else:
                        rStr = rStr + ", 1pm"
                elif hour == "14":
                    if len(rStr) == 0:
                        rStr = rStr + "3pm"
                    else:
                        rStr = rStr + ", 3pm"
                elif hour == "16":
                    if len(rStr) == 0:
                        rStr = rStr + "5pm"
                    else:
                        rStr = rStr + ", 5pm"
                elif hour == "18":
                    if len(rStr) == 0:
                        rStr = rStr + "7pm"
                    else:
                        rStr = rStr + ", 7pm"
    return rStr

def checkStart():
    scheduler = win32com.client.Dispatch('Schedule.Service')
    scheduler.Connect()
    root_folder = scheduler.GetFolder('\\')
    colTasks = root_folder.GetTasks(1)
    for task in colTasks:
        if task.Name == "sunday":
            taskDef = task.Definition
            t = taskDef.triggers
            for trigger in t:
                datestr = trigger.StartBoundary[:10]
                year, month, day = datestr.split("-")
                current = "{}".format(datetime.datetime.now())
                currentStr = current[:10]
                cYear, cMonth, cDay = currentStr.split("-")
                delete = False
                if cYear > year: #so if current = 2021, but alloted is 2020
                    trigger.enabled = False
                    delete = True
                elif cMonth > month:
                    trigger.enabled = False
                    delete = True
                elif cDay > day:
                    trigger.enabled = False
                    delete = True
