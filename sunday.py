import curses, sys, win32com.client

def main_display(stdscr):
    cursor_y = 1
    cursor_x = 1

def start():
    scheduler = win32com.client.Dispatch('Schedule.Service')
    scheduler.Connect()
    root_folder = scheduler.GetFolder('\\')
    colTasks = objTaskFolder.GetTasks(1)

    for task in colTasks:
        print(task.Name)
    #curses.wrapper(main_display)
