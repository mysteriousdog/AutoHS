from FSM_action import system_exit, AutoHS_automata
import keyboard
from log_state import check_name
from print_info import print_info_init
from FSM_action import init
from FSM_action import enter_battle_from_login
from FSM_action import read_passwd_file
from click import enter_HS_step_2
if __name__ == "__main__":
    # check_name()
    print_info_init()
    # init()
    read_passwd_file(r'value.txt')
    keyboard.add_hotkey("ctrl+q", system_exit)
    enter_battle_from_login()
    enter_HS_step_2()
    AutoHS_automata()
