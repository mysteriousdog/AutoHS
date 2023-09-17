import sys
sys.path.append(r"..")
from click import *



def test_rand_sleep(interval):
    print(1)
    rand_sleep(interval)
    print(2)

def test_left_click(x, y):
    left_click(x, y)

def test_right_click(x, y):
    right_click(x, y)

MAIN_MENU_XY = {
    CLICK_MAIN_START_GAME : (950, 320),
    CLICK_MAIN_START_SINGLE_GAME : (950, 570),
    CLICK_MAIN_START_OPTION : (1880, 1060),
    CLICK_MAIN_QUIT_GAME : (950, 450),
    CLICK_MAIN_START_MISSION : (500, 950),
    CLICK_MAIN_START_REWARD : (350, 350),
    CLICK_MAIN_NEXT_REWARD : (1550, 880),
    CLICK_MAIN_PREV_REWARD : (550, 880)
}

def test_main_start_game_click():
    enter_HS()
    x, y = MAIN_MENU_XY[CLICK_MAIN_START_GAME]
    left_click(x, y)

def test_main_start_single_game_click():
    enter_HS()
    x, y = MAIN_MENU_XY[CLICK_MAIN_START_SINGLE_GAME]
    left_click(x, y)

def test_main_start_option_click():
    enter_HS()
    x, y = MAIN_MENU_XY[CLICK_MAIN_START_OPTION]
    left_click(x, y)

def test_main_quit_game_click():
    test_start_option_click()
    time.sleep(1)
    x, y = MAIN_MENU_XY[CLICK_MAIN_QUIT_GAME]
    left_click(x, y)

def test_main_start_mission_click():
    enter_HS()
    x, y = MAIN_MENU_XY[CLICK_MAIN_START_MISSION]
    left_click(x, y)

def test_main_start_reward_click():
    enter_HS()
    x, y = MAIN_MENU_XY[CLICK_MAIN_START_REWARD]
    left_click(x, y)

def test_main_start_reward_click_next_reward_click():
    enter_HS()
    x, y = MAIN_MENU_XY[CLICK_MAIN_NEXT_REWARD]
    left_click(x, y)

def test_main_start_reward_click_prev_reward_click():
    enter_HS()
    x, y = MAIN_MENU_XY[CLICK_MAIN_PREV_REWARD]
    left_click(x, y)

SINGLE_MAIN_MENU_XY = {
     CLICK_ANOTHER_MODE : (1350, 470),
     CLICK_PRITICE_MODE : (1350, 150),
     CLICK_PRITICE_MODE_NEXT : (1350, 210),
     CLICK_PRITICE_MODE_NEXT_START_GAME : (1450, 900),
}

def test_single_main_start_game_click():
    enter_HS()
    x, y = SINGLE_MAIN_MENU_XY[CLICK_ANOTHER_MODE]
    left_click(x, y)
    time.sleep(1)
    x, y = SINGLE_MAIN_MENU_XY[CLICK_PRITICE_MODE]
    left_click(x, y)
    time.sleep(1)
    x, y = SINGLE_MAIN_MENU_XY[CLICK_PRITICE_MODE_NEXT]
    left_click(x, y)
    time.sleep(1)
    x, y = SINGLE_MAIN_MENU_XY[CLICK_PRITICE_MODE_NEXT_START_GAME]
    left_click(x, y)

SINGLE_CHOSE_HERO_MENU_XY = {
     SINGLE_GAME_CHOSE_HERO_1 : (500, 260),
     SINGLE_GAME_CHOSE_HERO_2 : (700, 260),
     SINGLE_GAME_CHOSE_HERO_3 : (1000, 260),
     SINGLE_GAME_CHOSE_HERO_4 : (500, 500),
     SINGLE_GAME_CHOSE_HERO_5 : (700, 500),
     SINGLE_GAME_CHOSE_HERO_6 : (1000, 500),
     SINGLE_GAME_CHOSE_HERO_7 : (500, 720),
     SINGLE_GAME_CHOSE_HERO_8 : (700, 720),
     SINGLE_GAME_CHOSE_HERO_9 : (1000, 720),

     SINGLE_GAME_CHOSE_HERO_OPPO_1 : (1400, 120),
     SINGLE_GAME_CHOSE_HERO_OPPO_2 : (1400, 200),
     SINGLE_GAME_CHOSE_HERO_OPPO_3 : (1400, 260),
     SINGLE_GAME_CHOSE_HERO_OPPO_4 : (1400, 320),
     SINGLE_GAME_CHOSE_HERO_OPPO_5 : (1400, 400),
     SINGLE_GAME_CHOSE_HERO_OPPO_6 : (1400, 450),
     SINGLE_GAME_CHOSE_HERO_OPPO_7 : (1400, 520),
     SINGLE_GAME_CHOSE_HERO_OPPO_8 : (1400, 590),
     SINGLE_GAME_CHOSE_HERO_OPPO_9 : (1400, 650),
     SINGLE_GAME_CHOSE_HERO_OPPO_10 : (1400, 710),
     SINGLE_GAME_START_GAME : (1400, 850),
}

def test_single_chose_hero_oppo_x_click(index):
    enter_HS()
    key = SINGLE_GAME_CHOSE_HERO_OPPO_PRE + str(index)
    x, y = SINGLE_CHOSE_HERO_MENU_XY[key]
    left_click(x, y)

def test_single_chose_hero_x_click(index):
    enter_HS()
    key = SINGLE_GAME_CHOSE_HERO_PRE + str(index)
    x, y = SINGLE_CHOSE_HERO_MENU_XY[key]
    left_click(x, y)


def test_single_game_start_click():
    enter_HS()
    x, y = SINGLE_CHOSE_HERO_MENU_XY[SINGLE_GAME_START_GAME]
    left_click(x, y)

def test_single_game_start_choose_oppo_click():
    enter_HS()
    x, y = SINGLE_CHOSE_HERO_MENU_XY[SINGLE_GAME_START_GAME]
    left_click(x, y)


CHOSE_HERO_MENU_XY = {
    CLICK_CHOSE_HERO_OPEN_GAME : (1400, 900),
    CLICK_CHOSE_HERO_CANCEL_GAME : (1000, 900),
    CLICK_CHOSE_HERO_1_CLICK : (500, 300),
    CLICK_CHOSE_HERO_2_CLICK : (700, 300),
    CLICK_CHOSE_HERO_3_CLICK : (1000, 300),
    CLICK_CHOSE_HERO_4_CLICK : (500, 500),
    CLICK_CHOSE_HERO_5_CLICK : (700, 500),
    CLICK_CHOSE_HERO_6_CLICK : (1000, 500),
    CLICK_CHOSE_HERO_7_CLICK : (500, 750),
    CLICK_CHOSE_HERO_8_CLICK : (700, 750),
    CLICK_CHOSE_HERO_9_CLICK : (1000, 750),
}

def test_chose_hero_open_game_click():
    enter_HS()
    x, y = CHOSE_HERO_MENU_XY[CLICK_CHOSE_HERO_OPEN_GAME]
    left_click(x, y)

def test_chose_hero_open_game_click_cancel_open_click():
    enter_HS()
    x, y = CHOSE_HERO_MENU_XY[CLICK_CHOSE_HERO_CANCEL_GAME]
    left_click(x, y)

def test_chose_hero_1_click():
    enter_HS()
    x, y = CHOSE_HERO_MENU_XY[CLICK_CHOSE_HERO_1_CLICK]
    left_click(x, y)

def test_chose_hero_2_click():
    enter_HS()
    x, y = CHOSE_HERO_MENU_XY[CLICK_CHOSE_HERO_2_CLICK]
    left_click(x, y)

def test_chose_hero_3_click():
    enter_HS()
    x, y = CHOSE_HERO_MENU_XY[CLICK_CHOSE_HERO_3_CLICK]
    left_click(x, y)

def test_chose_hero_4_click():
    enter_HS()
    x, y = CHOSE_HERO_MENU_XY[CLICK_CHOSE_HERO_4_CLICK]
    left_click(x, y)

def test_chose_hero_5_click():
    enter_HS()
    x, y = CHOSE_HERO_MENU_XY[CLICK_CHOSE_HERO_5_CLICK]
    left_click(x, y)

def test_chose_hero_6_click():
    enter_HS()
    x, y = CHOSE_HERO_MENU_XY[CLICK_CHOSE_HERO_6_CLICK]
    left_click(x, y)

def test_chose_hero_7_click():
    enter_HS()
    x, y = CHOSE_HERO_MENU_XY[CLICK_CHOSE_HERO_7_CLICK]
    left_click(x, y)

def test_chose_hero_8_click():
    enter_HS()
    x, y = CHOSE_HERO_MENU_XY[CLICK_CHOSE_HERO_8_CLICK]
    left_click(x, y)

def test_chose_hero_9_click():
    enter_HS()
    x, y = CHOSE_HERO_MENU_XY[CLICK_CHOSE_HERO_9_CLICK]
    left_click(x, y)


BATTLE_MENU_XY = {
    CLICK_CHOSE_CARD_LATER_1 : (600, 500),
    CLICK_CHOSE_CARD_LATER_2 : (850, 500),
    CLICK_CHOSE_CARD_LATER_3 : (1100, 500),
    CLICK_CHOSE_CARD_LATER_4 : (1350, 500),
    CLICK_CHOSE_CARD_LATER_CONFIRM : (950, 850),
    CLICK_BATTLE_HERO_POWER_CLICK : (1150, 820),
    CLICK_BATTLE_END_TURN_CLICK : (1550, 500),
    CLICK_BATTLE_OPTION_CLICK : (1890, 1060),
    CLICK_BATTLE_SURRENDER_CLICK : (950, 380),
    CLICK_BATTLE_QUITGAME_CLICK : (950, 650),
}

def test_battle_chose_card_1_click():
    enter_HS()
    x, y = BATTLE_MENU_XY[CLICK_CHOSE_CARD_LATER_1]
    left_click(x, y)

def test_battle_chose_card_2_click():
    enter_HS()
    x, y = BATTLE_MENU_XY[CLICK_CHOSE_CARD_LATER_2]
    left_click(x, y)

def test_battle_chose_card_3_click():
    enter_HS()
    x, y = BATTLE_MENU_XY[CLICK_CHOSE_CARD_LATER_3]
    left_click(x, y)

def test_battle_chose_card_4_click():
    enter_HS()
    x, y = BATTLE_MENU_XY[CLICK_CHOSE_CARD_LATER_4]
    left_click(x, y)

def test_battle_chose_card_confirm_click():
    enter_HS()
    x, y = BATTLE_MENU_XY[CLICK_CHOSE_CARD_LATER_CONFIRM]
    left_click(x, y)

def test_battle_hero_power_click():
    enter_HS()
    x, y = BATTLE_MENU_XY[CLICK_BATTLE_HERO_POWER_CLICK]
    left_click(x, y)

def test_battle_end_turn_click():
    enter_HS()
    x, y = BATTLE_MENU_XY[CLICK_BATTLE_END_TURN_CLICK]
    left_click(x, y)

def test_battle_option_click():
    enter_HS()
    x, y = BATTLE_MENU_XY[CLICK_BATTLE_OPTION_CLICK]
    left_click(x, y)

def test_battle_surrender_click():
    enter_HS()
    x, y = BATTLE_MENU_XY[CLICK_BATTLE_SURRENDER_CLICK]
    left_click(x, y)

def test_battle_quit_game_click():
    enter_HS()
    x, y = BATTLE_MENU_XY[CLICK_BATTLE_QUITGAME_CLICK]
    left_click(x, y)

CHOSE_HAND_MENU_XY = {

    CLICK_CHOSE_HAND_1_1 : (950, 1000),

    CLICK_CHOSE_HAND_1_2 : (910, 1000),
    CLICK_CHOSE_HAND_2_2 : (1050, 1000),

    CLICK_CHOSE_HAND_1_3 : (800, 1000),
    CLICK_CHOSE_HAND_2_3 : (910, 1000),
    CLICK_CHOSE_HAND_3_3 : (1050, 1000),

    CLICK_CHOSE_HAND_1_4 : (700, 1000),
    CLICK_CHOSE_HAND_2_4 : (850, 1000),
    CLICK_CHOSE_HAND_3_4 : (1000, 1000),
    CLICK_CHOSE_HAND_4_4 : (1120, 1000),

    CLICK_CHOSE_HAND_1_5 : (700, 1000),
    CLICK_CHOSE_HAND_2_5 : (800, 1000),
    CLICK_CHOSE_HAND_3_5 : (900, 1000),
    CLICK_CHOSE_HAND_4_5 : (1000, 1000),
    CLICK_CHOSE_HAND_5_5 : (1150, 1000),

    CLICK_CHOSE_HAND_1_6 : (680, 1000),
    CLICK_CHOSE_HAND_2_6 : (780, 1000),
    CLICK_CHOSE_HAND_3_6 : (850, 1000),
    CLICK_CHOSE_HAND_4_6 : (950, 1000),
    CLICK_CHOSE_HAND_5_6 : (1050, 1000),
    CLICK_CHOSE_HAND_6_6 : (1100, 1000),

    CLICK_CHOSE_HAND_1_7 : (650, 1000),
    CLICK_CHOSE_HAND_2_7 : (750, 1000),
    CLICK_CHOSE_HAND_3_7 : (810, 1000),
    CLICK_CHOSE_HAND_4_7 : (900, 1000),
    CLICK_CHOSE_HAND_5_7 : (980, 1000),
    CLICK_CHOSE_HAND_6_7 : (1060, 1000),
    CLICK_CHOSE_HAND_7_7 : (1150, 1000),

    CLICK_CHOSE_HAND_1_8 : (650, 1020),
    CLICK_CHOSE_HAND_2_8 : (720, 1000),
    CLICK_CHOSE_HAND_3_8 : (800, 1000),
    CLICK_CHOSE_HAND_4_8 : (860, 1000),
    CLICK_CHOSE_HAND_5_8 : (930, 1000),
    CLICK_CHOSE_HAND_6_8 : (1000, 1000),
    CLICK_CHOSE_HAND_7_8 : (1080, 1000),
    CLICK_CHOSE_HAND_8_8 : (1150, 1000),

    CLICK_CHOSE_HAND_1_9 : (630, 1050),
    CLICK_CHOSE_HAND_2_9 : (710, 1000),
    CLICK_CHOSE_HAND_3_9 : (780, 1050),
    CLICK_CHOSE_HAND_4_9 : (820, 1000),
    CLICK_CHOSE_HAND_5_9 : (900, 1000),
    CLICK_CHOSE_HAND_6_9 : (950, 1000),
    CLICK_CHOSE_HAND_7_9 : (1010, 1000),
    CLICK_CHOSE_HAND_8_9 : (1080, 1000),
    CLICK_CHOSE_HAND_9_9 : (1150, 1010),

    CLICK_CHOSE_HAND_1_10 : (630, 1050),
    CLICK_CHOSE_HAND_2_10 : (700, 1000),
    CLICK_CHOSE_HAND_3_10 : (750, 1050),
    CLICK_CHOSE_HAND_4_10 : (800, 1000),
    CLICK_CHOSE_HAND_5_10 : (860, 1000),
    CLICK_CHOSE_HAND_6_10 : (910, 1000),
    CLICK_CHOSE_HAND_7_10 : (960, 1000),
    CLICK_CHOSE_HAND_8_10 : (1020, 1000),
    CLICK_CHOSE_HAND_9_10 : (1050, 1000),
    CLICK_CHOSE_HAND_10_10 : (1150, 1050),
}

def test_CHOSE_HAND_x_x_click(index, size):
    enter_HS()
    key = CLICK_CHOSE_HAND_x_PRE + str(index) + CLICK_CHOSE_HAND_x_MID + str(size)
    x, y = CHOSE_HAND_MENU_XY[key]
    left_click(x, y)


CHOSE_OPPO_MENU_XY = {
    CLICK_CHOSE_OPPO_BATLE_0_0 : (950, 200),

    CLICK_CHOSE_OPPO_BATLE_1_1 : (950, 350),

    CLICK_CHOSE_OPPO_BATLE_1_2 : (900, 400),
    CLICK_CHOSE_OPPO_BATLE_2_2 : (1040, 400),

    CLICK_CHOSE_OPPO_BATLE_1_3 : (800, 400),
    CLICK_CHOSE_OPPO_BATLE_2_3 : (950, 400),
    CLICK_CHOSE_OPPO_BATLE_3_3 : (1100, 400),

    CLICK_CHOSE_OPPO_BATLE_1_4 : (750, 400),
    CLICK_CHOSE_OPPO_BATLE_2_4 : (900, 400),
    CLICK_CHOSE_OPPO_BATLE_3_4 : (1050, 400),
    CLICK_CHOSE_OPPO_BATLE_4_4 : (1150, 400),

    CLICK_CHOSE_OPPO_BATLE_1_5 : (700, 400),
    CLICK_CHOSE_OPPO_BATLE_2_5 : (800, 400),
    CLICK_CHOSE_OPPO_BATLE_3_5 : (950, 400),
    CLICK_CHOSE_OPPO_BATLE_4_5 : (1100, 400),
    CLICK_CHOSE_OPPO_BATLE_5_5 : (1250, 400),

    CLICK_CHOSE_OPPO_BATLE_1_6 : (600, 400),
    CLICK_CHOSE_OPPO_BATLE_2_6 : (750, 400),
    CLICK_CHOSE_OPPO_BATLE_3_6 : (900, 400),
    CLICK_CHOSE_OPPO_BATLE_4_6 : (1050, 400),
    CLICK_CHOSE_OPPO_BATLE_5_6 : (1150, 400),
    CLICK_CHOSE_OPPO_BATLE_6_6 : (1300, 400),

    CLICK_CHOSE_OPPO_BATLE_1_7 : (550, 400),
    CLICK_CHOSE_OPPO_BATLE_2_7 : (700, 400),
    CLICK_CHOSE_OPPO_BATLE_3_7 : (800, 400),
    CLICK_CHOSE_OPPO_BATLE_4_7 : (950, 400),
    CLICK_CHOSE_OPPO_BATLE_5_7 : (1100, 400),
    CLICK_CHOSE_OPPO_BATLE_6_7 : (1250, 400),
    CLICK_CHOSE_OPPO_BATLE_7_7 : (1400, 400),
}

def test_CHOSE_OPPO_x_x_click(index, size):
    enter_HS()
    key = CLICK_CHOSE_OPPO_x_PRE + str(index) + CLICK_CHOSE_OPPO_x_MID + str(size)
    x, y = CHOSE_OPPO_MENU_XY[key]
    left_click(x, y)


CHOSE_OWN_MENU_XY = {
    CLICK_CHOSE_OWN_BATLE_0_0 : (950, 800),
    
    CLICK_CHOSE_OWN_BATLE_1_1 : (950, 600),

    CLICK_CHOSE_OWN_BATLE_1_2 : (900, 600),
    CLICK_CHOSE_OWN_BATLE_2_2 : (1050, 600),

    CLICK_CHOSE_OWN_BATLE_1_3 : (800, 600),
    CLICK_CHOSE_OWN_BATLE_2_3 : (950, 600),
    CLICK_CHOSE_OWN_BATLE_3_3 : (1100, 600),

    CLICK_CHOSE_OWN_BATLE_1_4 : (750, 600),
    CLICK_CHOSE_OWN_BATLE_2_4 : (900, 600),
    CLICK_CHOSE_OWN_BATLE_3_4 : (1050, 600),
    CLICK_CHOSE_OWN_BATLE_4_4 : (1150, 600),

    CLICK_CHOSE_OWN_BATLE_1_5 : (700, 600),
    CLICK_CHOSE_OWN_BATLE_2_5 : (800, 600),
    CLICK_CHOSE_OWN_BATLE_3_5 : (950, 600),
    CLICK_CHOSE_OWN_BATLE_4_5 : (1100, 600),
    CLICK_CHOSE_OWN_BATLE_5_5 : (1250, 600),

    CLICK_CHOSE_OWN_BATLE_1_6 : (600, 600),
    CLICK_CHOSE_OWN_BATLE_2_6 : (750, 600),
    CLICK_CHOSE_OWN_BATLE_3_6 : (900, 600),
    CLICK_CHOSE_OWN_BATLE_4_6 : (1050, 600),
    CLICK_CHOSE_OWN_BATLE_5_6 : (1150, 600),
    CLICK_CHOSE_OWN_BATLE_6_6 : (1300, 600),

    CLICK_CHOSE_OWN_BATLE_1_7 : (550, 600),
    CLICK_CHOSE_OWN_BATLE_2_7 : (700, 600),
    CLICK_CHOSE_OWN_BATLE_3_7 : (800, 600),
    CLICK_CHOSE_OWN_BATLE_4_7 : (950, 600),
    CLICK_CHOSE_OWN_BATLE_5_7 : (1100, 600),
    CLICK_CHOSE_OWN_BATLE_6_7 : (1250, 600),
    CLICK_CHOSE_OWN_BATLE_7_7 : (1400, 600),
}


def test_CHOSE_OWN_x_x_click(index, size):
    enter_HS()
    key = CLICK_CHOSE_OWN_x_PRE + str(index) + CLICK_CHOSE_OWN_x_MID + str(size)
    x, y = CHOSE_OWN_MENU_XY[key]
    left_click(x, y)


def goto_cradstore_from_single():
    enter_HS()
    left_click(700, 980)

def goto_add_new_card():
    enter_HS()
    left_click(1500, 350)

def confirm_add_new_card():
    enter_HS()
    left_click(850, 620)

def confirm_complete_new_card():
    enter_HS()
    left_click(1600, 1000)

def left_confirm_complete_new_card():
    enter_HS()
    left_click(1600, 1000)

def add_new_hunter_cards_from_single(): # 从冒险模式战斗结束到进入牌库进行卡组创建，创建完成后推出到main
    goto_cradstore_from_single()
    time.sleep(1)
    import pyperclip
    string_to_copy = "AAECAR8AD6qfBOOfBOWfBJagBJqgBKGgBKSgBLugBLi0BInUBKDUBKTUBKnUBNCeBtOeBgAA"
    pyperclip.copy(string_to_copy)
    import click
    click.test_click()
    click.test_click()
    click.test_click()
    click.test_click()
    click.test_click()
    click.test_click()
    goto_add_new_card()
    confirm_add_new_card()
    time.sleep(10)
    confirm_complete_new_card()
    time.sleep(1)
    left_confirm_complete_new_card()
    time.sleep(1)
    test_single_chose_hero_x_click(1)
    time.sleep(1)
    left_confirm_complete_new_card()
    time.sleep(1)
    left_confirm_complete_new_card()


def goto_fight_single_hunter_from_main(): # 从main到进入冒险模式战斗
    time.sleep(1)
    test_main_start_single_game_click()
    time.sleep(1)
    test_single_main_start_game_click()
    time.sleep(1)
    test_single_game_start_click()
    time.sleep(1)
    test_single_chose_hero_oppo_x_click(3)
    time.sleep(1)
    test_single_game_start_click()
    from FSM_action import system_exit, AutoHS_automata
    import keyboard
    from log_state import check_name
    from print_info import print_info_init
    from FSM_action import init

    check_name()
    print_info_init()
    init()
    keyboard.add_hotkey("ctrl+q", system_exit)
    AutoHS_automata(1)

def click_zuixindongtaicancel():
    enter_HS()
    left_click(1420, 210)

def click_hs_from_battle():
    enter_HS()
    left_click(260, 200)
    time.sleep(1)
    left_click(960, 200)

def hs_left_new_commer_to_mian():
    # time.slppe(10)
    enter_HS()
    # left_click(1000, 500)
    # time.slppe(10)
    # left_click(1850, 50)
    # time.sleep(1)
    # left_click(850, 620)
    # time.sleep(10)
    left_click(1000, 50)
    left_click(1000, 50)
    left_click(1000, 50)


def chose_clear_reput_mail_line(mail):
    # (left, top, right, bottom) = enter_BATTLE()
    # print(left, top, right, bottom)
    left_click(1050, 550)
    time.sleep(0.5)
    from pynput.keyboard import Controller, Key
    keyboard = Controller()
    time.sleep(0.5)
    i = 0
    while (i < 30):
        i += 1
        keyboard.press(Key.backspace)
        time.sleep(0.1)
        keyboard.release(Key.backspace)
    time.sleep(1)
    for wd in mail:
        keyboard.press(wd)
        time.sleep(0.1)
        keyboard.release(wd)
    
    left_click(1050, 480)
    left_click(1050, 480)
    left_click(1050, 480)
    right_click(1050, 480)
    right_click(1050, 480)
    time.sleep(1)
    left_click(1050, 600)
    left_click(1050, 600)
    left_click(1050, 600)
    left_click(1050, 600)
    # keyboard.press('a')
    # pyautogui.keyDown('a')
    # pyautogui.keyUp('alt')
    # pyautogui.keyDown('delete')
    # time.sleep(3)  # 可选，等待一段时间
    # pyautogui.keyUp('delete')

def chose_clear_reput_pwd_line(pwd):
    # (left, top, right, bottom) = enter_BATTLE()
    left_click(1050, 600)
    from pynput.keyboard import Controller, Key
    keyboard = Controller()
    time.sleep(0.5)
    i = 0
    while (i < 30):
        i += 1
        keyboard.press(Key.backspace)
        time.sleep(0.1)
        keyboard.release(Key.backspace)
    time.sleep(1)
    for wd in pwd:
        keyboard.press(wd)
        time.sleep(0.1)
        keyboard.release(wd)
    
    keyboard.press(Key.enter)

def log_in(mail, passwod):
    chose_clear_reput_mail_line(mail)
    time.sleep(2)
    chose_clear_reput_pwd_line(passwod)
    time.sleep(10)

def clear_first_log_info_game():
    (left, top, right, bottom) = enter_BATTLE()
    left_click(left + 1140, top + 380)
    time.sleep(1)
    left_click(left + 1140, top + 80)
    time.sleep(1)

def enter_game():
    (left, top, right, bottom) = enter_BATTLE()
    # click_zuixindongtaicancel()
    left_click(left + 120, top + 100)
    time.sleep(1)
    enter_HS()

def delete_directory_contents(directory):
    for root, dirs, files in os.walk(directory, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            os.rmdir(dir_path)

# def do_single_add_newcard_back_main_tofight():
#     goto_fight_single_hunter_from_main()
#     time.sleep(2)
def delete_smaller_subdirectories(directory_path):
    # 获取子目录列表
    subdirectories = os.listdir(directory_path)

    # 将路径转换为绝对路径
    directory_path = os.path.abspath(directory_path)

    # 按字符顺序对子目录进行排序
    subdirectories.sort()

    # 删除小的子目录（包括子目录中的所有文件）
    for subdirectory in subdirectories[:-1]:
        subdirectory_path = os.path.join(directory_path, subdirectory)
        if os.path.isdir(subdirectory_path):
            delete_directory_contents(subdirectory_path)
            os.rmdir(subdirectory_path)

    # 返回最大子目录的绝对路径
    return os.path.join(directory_path, subdirectories[-1])


if __name__ == "__main__":
    
    # enter_game()
    # clear_first_log_info_enter_game()
    goto_fight_single_hunter_from_main()
    # print(delete_smaller_subdirectories(r"C:\Program Files (x86)\Apps\Hearthstone\Logs"))
    # test_single_chose_hero_x_click(9)
    # test_CHOSE_OPPO_x_x_click(5, 5)
    # time.sleep(1)
    # test_CHOSE_OWN_x_x_click(7, 7)
    # test_CHOSE_HAND_x_x_click(1, 1)
    # test_battle_hero_power_click()
    # test_battle_chose_card_confirm_click()
    # test_battle_chose_card_4_click()
    # test_battle_chose_card_3_click()
    # test_battle_chose_card_2_click()
    # test_battle_chose_card_1_click()
    # test_chose_hero_9_click()
    # test_chose_hero_3_click()
    # test_chose_hero_2_click()
    # test_chose_hero_1_click()
    # test_chose_hero_open_game_click()
    # test_chose_hero_open_game_click_cancel_open_click()
    # test_rand_sleep(1)
    # test_left_click(100, 100)
    # test_right_click(100, 100)
    # test_start_option_click()
    # test_quit_game_click()
    # test_start_mission_click()
    # test_start_reward_click()
    # test_start_reward_click_next_reward_click()
    # test_start_reward_click_prev_reward_click()