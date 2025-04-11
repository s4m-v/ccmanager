import curses
from curses.textpad import Textbox
import commands


class CalList:

    def __init__(self, width: int, wsy: int, wsx: int, wey: int, wex: int) -> None:

        self.cal_list = commands.list()
        self.cal_list_len = len(self.cal_list)
        self.selected = 0

        self.block_size = 50
        self.blocks = (self.cal_list_len // self.block_size) + 1

        self.height = self.blocks * self.block_size
        self.width = width - 8

        self.pad = curses.newpad(self.height, self.width)

        self.wsy = wsy
        self.wsx = wsx
        self.wey = wey
        self.wex = wex
        self.ppl = 0
        self.ppu = wey - wsy

    def get_selected(self) -> str:
        return self.cal_list[self.selected]

    def move_up(self) -> None:

        if not self.selected == 0:
            self.selected -= 1

            if self.selected < self.ppl:
                self.ppl -= 1
                self.ppu -= 1

    def move_down(self) -> None:

        if not self.selected == self.cal_list_len - 1:
            self.selected += 1

            if self.selected > self.ppu:
                self.ppl += 1
                self.ppu += 1

    def draw(self) -> None:

        self.pad.erase()
    
        self.cal_list = commands.list()
        self.cal_list_len = len(self.cal_list)
    
        block_check = (self.cal_list_len // self.block_size) + 1
        if block_check > self.blocks:
            self.blocks = block_check
            self.height = self.blocks * self.block_size
            self.pad.resize(self.height, self.width)
            self.pad.erase()
    
        for i, cal in enumerate(self.cal_list):
    
            if i == self.selected:
                self.pad.addstr(i, 0, cal, curses.A_BOLD | curses.A_REVERSE )
            else:
                self.pad.addstr(i, 0, cal)

        self.pad.refresh(
                self.ppl,
                0,
                self.wsy, 
                self.wsx, 
                self.wey, 
                self.wex 
                )

class Console:

    def __init__(self, ncols: int, begin_y: int, begin_x: int) -> None:

        self.ncols = ncols
        self.begin_y = begin_y
        self.begin_x = begin_x

        self.statuswin = curses.newwin(1, ncols, begin_y, begin_x)
        self.textwin = curses.newwin(1, ncols, begin_y + 1, begin_x)
        self.textbox = Textbox(self.textwin)

    def get_input(self, prompt: str) -> str:

        self.statuswin.erase()
        self.statuswin.addstr(prompt)
        self.statuswin.noutrefresh()

        curses.curs_set(1)
        self.textwin.move(0, 0)

        self.textbox.edit()
        input = self.textbox.gather().strip(" \n")
            
        curses.curs_set(0)

        self.textwin.erase()
        self.textwin.noutrefresh()
        
        self.statuswin.erase()
        self.statuswin.refresh()

        curses.doupdate()

        return input

    def update_status(self, msg: str) -> None:

        self.statuswin.erase()
        self.statuswin.addstr(msg)
        self.statuswin.refresh()

    def add_cal(self) -> bool:

        name = self.get_input("Please input calendar name:")
        return commands.add(name)

    def remove_cal(self, name: str) -> bool:

        while True:
            confirm = self.get_input("Are you sure you want to delete: " + name + "? (y/n)")

            if confirm == "y":
                break
            elif confirm == "n":
                return False

        return commands.remove(name)

    def sync_cal(self, name: str) -> bool:
        return commands.sync(name)

    def backup_cal(self, name: str) -> bool:
        return commands.backup(name)


class App:

    def __init__(self, stdscr:curses.window) -> None:

        self.stdscr = stdscr
        curses.curs_set(0)
        self.init_colors()
        self.stdscr.clear()
        self.stdscr.refresh()


        self.height, self.width = self.stdscr.getmaxyx()
        self.create_windows()
        self.draw_all()

    def init_colors(self):
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)  # Header/Footer color
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Action/Status color


    def handle_resize(self):

        self.height, self.width = self.stdscr.getmaxyx()
        curses.resizeterm(self.height, self.width)
        self.stdscr.getkey()

        self.stdscr.clear()
        self.stdscr.refresh()
        self.create_windows()
        self.draw_all()

    def create_windows(self):

        self.header = curses.newwin(1, self.width, 0, 0)
        self.header.bkgd(' ', curses.color_pair(1))

        self.footer = curses.newwin(3, self.width, self.height-3, 0)
        self.footer.bkgd(' ', curses.color_pair(1))

        self.console = Console(self.width, self.height - 5, 0)
        self.console.statuswin.bkgd(' ', curses.color_pair(2))

        self.cal_list = CalList(self.width - 8, 2, 4, self.height - 6, self.width - 4)

    def draw_all(self) -> None:

        self.cal_list.draw()
        self.draw_footer()
        self.draw_header()
        self.console.textwin.clear()
        self.console.statuswin.clear()
        self.console.textwin.refresh()
        self.console.statuswin.refresh()

    def draw_footer(self) -> None:
    
        self.footer.clear()
    
        actions = [
                " (a)dd ",
                " (r)emove ",
                " (o)pen ",
                " (s)ync ",
                " (b)ackup ",
                " (q)uit "
                ]
    
        x_pos = self.width // 2 - (sum(len(a) + 4 for a in actions) - 4) // 2
    
        for act in actions:
    
            self.footer.addstr(1, x_pos, act, curses.A_BOLD | curses.color_pair(2))
            x_pos += len(act) + 4
    
        self.footer.refresh()
    
    def draw_header(self):

        self.header.clear()
        self.header.addstr(0, 2, " Calcurse Manager ", curses.A_BOLD | curses.color_pair(2))
        self.header.refresh()

    def run(self):

        while True:

            c = self.stdscr.getch()

            if c == curses.KEY_RESIZE:

                self.handle_resize()

                continue

            elif c == ord('q'):

                break

            elif c == ord('j'):

                self.cal_list.move_down()

            elif c == ord('k'):

                self.cal_list.move_up()

            elif c == ord('a'):

                if self.console.add_cal():
                    self.console.update_status("added calendar!")

                else:
                    self.console.update_status("failed to add calendar!")

            elif c == ord('r'):

                if self.console.remove_cal(self.cal_list.get_selected()):
                    self.console.update_status("removed calendar!")
                    self.cal_list.selected -= 1

                else:
                    self.console.update_status("failed to remove calendar!")

            elif c == ord('o'):

                curses.def_prog_mode()
                curses.endwin()

                commands.open(self.cal_list.get_selected())

                curses.reset_prog_mode()
                curses.doupdate()

            elif c == ord('s'):

                if self.console.sync_cal(self.cal_list.get_selected()):
                    self.console.update_status("synced calendar!")

                else:
                    self.console.update_status("failed to sync calendar!")

            elif c == ord('b'):

                if self.console.backup_cal(self.cal_list.get_selected()):
                    self.console.update_status("backed up calendar!")

                else:
                    self.console.update_status("failed to back up calendar!")

            self.cal_list.draw()


def main(stdscr: curses.window):

    app = App(stdscr)
    app.run()

def start_tui():
    curses.wrapper(main)
