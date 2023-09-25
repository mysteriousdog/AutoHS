# 3707 
import random
import sys
import time
import zlh
import keyboard

import click
import get_screen
from strategy import StrategyState
from log_state import *
import threading
import strategy
# import predict_model
FSM_state = ""
time_begin = 0.0
game_count = 0
win_count = 0
quitting_flag = False
log_state = LogState()
log_iter = log_iter_func(HEARTHSTONE_POWER_LOG_PATH)
choose_hero_count = 0
data_x = []
data_y = []
g_is_single = 0
passwd_list = []
passwd_index = 0
my_user = ''
my_passwd = ''
save_path = ''

def dump_data_x(data_x):
    with open('data_x.txt', 'w') as file:
        for item in data_x:
            file.write(json.dumps(item) + '\n')

def dump_data_y(data_y):
    with open('data_y.txt', 'w') as file:
        for item in data_y:
            file.write(json.dumps(item) + '\n')

def read_data_x():
    with open('data_x.txt', 'r') as file:
        for line in file:
            item = json.loads(line)
            data_x.append(item)
    return data_x


def read_data_y():
    with open('data_y.txt', 'r') as file:
        for line in file:
            item = json.loads(line)
            data_y.append(item)
    return data_y

# 用于接收输入的线程函数
def input_thread_func():
    keyboard.add_hotkey("ctrl+q", system_exit)
    while True:
        # 获取用户输入
        strategy.user_input = input("请输入数字: ")
        print("user_input is :", strategy.user_input)


import os

def delete_directory_contents(directory):
    for root, dirs, files in os.walk(directory, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            os.rmdir(dir_path)

def get_first_subdirectory(path):
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            return os.path.abspath(item_path)


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


def read_passwd_file(file_path):
    global passwd_list, passwd_index
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
           temp = line.split()
           passwd_list.append(temp)
    print(passwd_list)
    passwd_index = 0

def define_my_name():
    global MY_NAME, passwd_index, passwd_list, my_user, my_passwd
    MY_NAME= passwd_list[passwd_index][2]
    my_user = passwd_list[passwd_index][0]
    my_passwd = passwd_list[passwd_index][1]
    print("MY_NAME is : ", MY_NAME)
    print("MY_USER is : ", my_user)
    print("MY_PASSWD is : ", my_passwd)
    passwd_index += 1

def enter_battle_from_login():
    global MY_NAME, passwd_index, passwd_list, my_user, my_passwd
    define_my_name()
    from zlh.zlh_click import log_in
    log_in(my_user, my_passwd)


def init():
    global log_state, log_iter, choose_hero_count, save_path

    # 有时候炉石退出时python握着Power.log的读锁, 因而炉石无法
    # 删除Power.log. 而当炉石重启时, 炉石会从头开始写Power.log,
    # 但此时python会读入完整的Power.log, 并在原来的末尾等待新的写入. 那
    # 样的话python就一直读不到新的log. 状态机进而卡死在匹配状态(不
    # 知道对战已经开始)
    # 这里是试图在每次初始化文件句柄的时候删除已有的炉石日志. 如果要清空的
    # 日志是关于当前打开的炉石的, 那么炉石会持有此文件的写锁, 使脚本无法
    # 清空日志. 这使得脚本不会清空有意义的日志
    # read_passwd_file(r'value.txt')
    # print(HEARTHSTONE_POWER_LOG_PATH)
    log_path = delete_smaller_subdirectories(r"C:\Program Files (x86)\Apps\Hearthstone\Logs")
    log_path += r"\Power.log"
    # print(log_path)
    # log_path = "Power.log"
    if os.path.exists(log_path):
        try:
            file_handle = open(log_path, "w")
            file_handle.seek(0)
            file_handle.truncate()
            info_print("Success to truncate Power.log")
        except OSError:
            warn_print("Fail to truncate Power.log, maybe someone is using it")
    else:
        info_print("Power.log does not exist")
    save_path = log_path
    log_state = LogState()
    log_iter = log_iter_func(log_path)
    choose_hero_count = 0
    # input_thread = threading.Thread(target=input_thread_func)
    # input_thread.start()

def update_log_state():
    log_container = next(log_iter)
    if log_container.log_type == LOG_CONTAINER_ERROR:
        print("err in log_container.log_type")
        return False

    for log_line_container in log_container.message_list:
        ok = update_state(log_state, log_line_container)
        # if not ok:
        #     return False

    if DEBUG_FILE_WRITE:
        with open("./log/game_state_snapshot.txt", "w", encoding="utf8") as f:
            f.write(str(log_state))

    # 注意如果Power.log没有更新, 这个函数依然会返回. 应该考虑到game_state只是被初始化
    # 过而没有进一步更新的可能
    if log_state.game_entity_id == 0:
        print("err in log_state.game_entity_id")
        # return False

    return True


def system_exit():
    global quitting_flag

    sys_print(f"一共完成了{game_count}场对战, 赢了{win_count}场")
    print_info_close()

    quitting_flag = True

    sys.exit(0)


def print_out():
    global FSM_state
    global time_begin
    global game_count

    sys_print("Enter State " + str(FSM_state))

    if FSM_state == FSM_LEAVE_HS:
        warn_print("HearthStone not found! Try to go back to HS")

    if FSM_state == FSM_CHOOSING_CARD:
        game_count += 1
        sys_print("The " + str(game_count) + " game begins")
        time_begin = time.time()

    if FSM_state == FSM_QUITTING_BATTLE:
        sys_print("The " + str(game_count) + " game ends")
        time_now = time.time()
        if time_begin > 0:
            info_print("The last game last for : {} mins {} secs"
                       .format(int((time_now - time_begin) // 60),
                               int(time_now - time_begin) % 60))

    return


def ChoosingHeroAction():
    global choose_hero_count
    print("==========================in ChoosingHeroAction==========================")
    print_out()

    # 有时脚本会卡在某个地方, 从而在FSM_Matching
    # 和FSM_CHOOSING_HERO之间反复横跳. 这时候要
    # 重启炉石
    # choose_hero_count会在每一次开始留牌时重置
    choose_hero_count += 1
    if choose_hero_count >= 20:
        return FSM_ERROR

    time.sleep(2)
    click.match_opponent()
    time.sleep(1)
    return FSM_MATCHING


def MatchingAction():
    print_out()
    loop_count = 0
    print("==========================in MatchingAction==========================")
    while True:
        if quitting_flag:
            sys.exit(0)

        time.sleep(STATE_CHECK_INTERVAL)

        click.commit_error_report()

        ok = update_log_state()
        if ok:
            if not log_state.is_end:
                return FSM_CHOOSING_CARD

        curr_state = get_screen.get_state()
        if curr_state == FSM_CHOOSING_HERO:
            return FSM_CHOOSING_HERO

        loop_count += 1
        if loop_count >= 60:
            warn_print("Time out in Matching Opponent")
            return FSM_ERROR


def ChoosingCardAction():
    global choose_hero_count
    choose_hero_count = 0
    print("===========================in ChoosingCardAction===========================")
    print_out()
    time.sleep(21)
    loop_count = 0
    has_print = 0
    init()
    time.sleep(5)
    while True:
        ok = update_log_state()

        if not ok:
            return FSM_ERROR
        strategy_state = StrategyState(log_state)
        strategy_state.debug_print_out()
        time.sleep(3)
        if log_state.game_num_turns_in_play > 0:
            return FSM_BATTLING
        if log_state.is_end:
            return FSM_QUITTING_BATTLE

        strategy_state = StrategyState(log_state)
        strategy_state.debug_print_out()
        time.sleep(3)
        # return FSM_BATTLING

        hand_card_num = strategy_state.my_hand_card_num

        # 等待被替换的卡牌 ZONE=HAND
        # 注意后手时幸运币会作为第五张卡牌算在手牌里, 故只取前四张手牌
        # 但是后手时 hand_card_num 仍然是 5
        for my_hand_index, my_hand_card in \
                enumerate(strategy_state.my_hand_cards[:4]):
            detail_card = my_hand_card.detail_card

            if detail_card is None:
                should_keep_in_hand = \
                    my_hand_card.current_cost <= REPLACE_COST_BAR
            else:
                should_keep_in_hand = \
                    detail_card.keep_in_hand(strategy_state, my_hand_index)

            if not has_print:
                debug_print(f"手牌-[{my_hand_index}]({my_hand_card.name})"
                            f"是否保留: {should_keep_in_hand}")

            if not should_keep_in_hand:
                click.replace_starting_card(my_hand_index, hand_card_num)

        has_print = 1

        click.commit_choose_card()

        loop_count += 1
        if loop_count >= 60:
            warn_print("Time out in Choosing Opponent")
            return FSM_ERROR
        time.sleep(STATE_CHECK_INTERVAL)

good_dic = {}


def get_best_solution(strategy_state, action_list, k):
    max_val = 0
    best_action = []
    temp_val = 0
    temp_action = 0
    global good_dic
    
    if strategy_state.get_hash() in good_dic:
        # print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk", k)
        return good_dic[strategy_state.get_hash()]
    # print("-----------------------k is ", k, " ------------------------------------------")
    # k += 1
    # print("in get_best_solution action_list len is ", len(action_list))
    for actions in action_list:
        for action in actions:
            temp_val = 0
            states = []
            # print("in get_best_solution actions len is ", len(actions))
            # action.show_action()
            temp_state = copy.deepcopy(strategy_state)
            temp_val, states = action.do_action(temp_state)
            # print("temp_val ", temp_val)
            # print("states0 ", states)
            if temp_val == 999999:
                return 999999, [action]
            # print("strategy_state.my_last_mana is :", strategy_state.my_last_mana)
            # print("temp_state.my_last_mana is :", temp_state.my_last_mana)
            if len(states) == 0:
                continue
            
            # best_action.append(action)
            # if temp_val > max_val:
            #     max_val = temp_val
            # temp_best_action = best_action
            # temp_best_action = [action]
            for index, state in enumerate(states):
                # print("in get_best_solution states len is ", len(states)) 
                # # print("in get_best_solution states hero power status is ", state.)  
                # state.debug_print_out()
                temp_action_list = state.get_action_list()
                temp_val1, temp_actions = get_best_solution(state, temp_action_list, k)
                if temp_val1 == 999999:
                    return 999999, ([action] + temp_actions)
                # print("temp_val ", temp_val)
                # print("temp_val1 ", temp_val1)
                temp_val += temp_val1
                if temp_val > max_val:
                    max_val = temp_val
                    best_action = ([action] + temp_actions)
                temp_val -= temp_val1
    # print("return now, max_val is ", max_val, " best_action is ", len(best_action))
    # for ac in best_action:
    #     ac.show_action()
    if strategy_state.get_hash() not in good_dic:
        good_dic[strategy_state.get_hash()] = (max_val, best_action)
    elif good_dic[strategy_state.get_hash()][0] < max_val:
        good_dic[strategy_state.get_hash()] = (max_val, best_action)
    return max_val, best_action


def test_battle():
    global log_state
    check_name()
    init()
    update_log_state()
    strategy_state = StrategyState(log_state)
    action_list = strategy_state.get_action_list()
    from datetime import datetime
    strategy_state.debug_print_out()
    # now = datetime.now()
    # current_time = now.strftime("%Y-%m-%d %H:%M:%S") + "." + now.strftime("%S")
    # for actions in action_list:
    #     if not actions:
    #         continue
    #     for action in actions:
    #         action.show_action()
    # print("当前时间1：", current_time)
    max_val, best_action = get_best_solution(strategy_state, action_list, 0)
    # now = datetime.now()
    # current_time = now.strftime("%Y-%m-%d %H:%M:%S") + "." + now.strftime("%S")
    # print("当前时间2：", current_time)
    # print("max_val is ", max_val)
    for action in best_action:
        action.show_action()
        # break

def Battling():
    global win_count
    global log_state
    global good_dic
    print_out()
    
    not_mine_count = 0
    mine_count = 0
    last_controller_is_me = False
    global g_is_single
    print("===========================in Battling===========================, g_is_single is :", g_is_single)
    while True:
        if quitting_flag:
            sys.exit(0)
        # if (g_is_single == 1) or (g_is_single == 2):
        #     time.sleep(30)
        # time.sleep(2)
        ok = update_log_state()
        if not ok:
            print("===========================update_log_state err in Battling===========================")
            return FSM_ERROR

        if log_state.is_end:
            if log_state.my_entity.query_tag("PLAYSTATE") == "WON":
                win_count += 1
                info_print("你赢得了这场对战")
            else:
                info_print("你输了")
            return FSM_QUITTING_BATTLE
        
        # 在对方回合等就行了
        if not log_state.is_my_turn:
            print("========================not my turn=========================")
            
            last_controller_is_me = False
            mine_count = 0
            not_mine_count += 1
            if not_mine_count >= 400:
                warn_print("Time out in Opponent's turn")
                return FSM_ERROR
            time.sleep(5)
            continue

        # 接下来考虑在我的回合的出牌逻辑
        print("========================start sleep=========================")
        time.sleep(3)
        print("========================end sleep=========================")
        # if (g_is_single == 1) or (g_is_single == 2):
        #     time.sleep(5)
        #     update_log_state()
        # 如果是这个我的回合的第一次操作
        update_log_state()
        if log_state.is_end:
            if log_state.my_entity.query_tag("PLAYSTATE") == "WON":
                win_count += 1
                info_print("你赢得了这场对战")
            else:
                info_print("你输了")
            return FSM_QUITTING_BATTLE
        if not last_controller_is_me:
            time.sleep(2)
            # 在游戏的第一个我的回合, 发一个你好
            # game_num_turns_in_play在每一个回合开始时都会加一, 即
            # 后手放第一个回合这个数是2
            if log_state.game_num_turns_in_play <= 2:
                click.emoj(0)
            else:
                # 在之后每个回合开始时有概率发表情
                if random.random() < EMOJ_RATIO:
                    click.emoj()

        last_controller_is_me = True
        not_mine_count = 0
        mine_count += 1

        if mine_count >= 20:
            if mine_count >= 40:
                return FSM_ERROR
            click.end_turn()
            click.commit_error_report()
            click.cancel_click()
            time.sleep(STATE_CHECK_INTERVAL)
        time.sleep(1)
        # ok = update_log_state()
        # ok = update_log_state()
        ok = update_log_state()
        strategy_state = StrategyState(log_state)
        # 
        if log_state.is_end:
            time.sleep(1)
            continue
        strategy_state.debug_print_out()
        good_dic = {}
        try:
            action_list = strategy_state.get_action_list()
            max_val, best_action = get_best_solution(strategy_state, action_list, 0)
        except:
            print("err=======================================================================================")
            import shutil
            global save_path
            # 源文件路径
            source_file = save_path

            # 目标文件路径
            destination_file = 'Power.log1'

            # 复制文件
            shutil.copy(source_file, destination_file)
            return FSM_ERROR
        if len(best_action) == 0:
            click.end_turn()
            time.sleep(STATE_CHECK_INTERVAL)
            continue
        best_action = best_action[0]
        strategy_state = StrategyState(log_state)
        if best_action.is_in_hand:
            if best_action.hand_index == -2:
                if strategy_state.my_hero_power.exhausted or strategy_state.my_last_mana < 2:
                    click.end_turn()
                    continue
                else:
                    index = -1
            else:
                index = best_action.hand_index
            args = []
            if best_action.put_index != -3:
                args.append(best_action.put_index)
            elif best_action.point_oppo != -3:
                args.append(best_action.point_oppo)
            elif best_action.point_self != -3:
                args.append(best_action.point_self)
            else:
                args.append(0)
                # print("err in action !!!!!!!!!!!!!!!!!!!!!!!!!!")
                # best_action.show_action()
                # click.end_turn()
                # time.sleep(STATE_CHECK_INTERVAL)
            strategy_state.use_best_entity(index, args)
            continue
        else:
            index = best_action.battle_index
            oppo_index = best_action.point_oppo
            strategy_state.my_entity_attack_oppo(index, oppo_index)
        # # 考虑要不要出牌
        # index, args = strategy_state.best_h_index_arg()

        # # index == -1 代表使用技能, -2 代表不出牌
        # if index != -2:
        #     strategy_state.use_best_entity(index, args)
        #     continue

        # 如果不出牌, 考虑随从怎么打架
        # my_index, oppo_index = strategy_state.get_best_attack_target()

        # # my_index == -1代表英雄攻击, -2 代表不攻击
        # if my_index != -2:
        #     strategy_state.my_entity_attack_oppo(my_index, oppo_index)
        # else:
        #     print("======================================================================================================================================================")
        #     time.sleep(1)
        #     update_log_state()
        #     strategy_state = StrategyState(log_state)
        #     index, args = strategy_state.best_h_index_arg()
        #     my_index, oppo_index = strategy_state.get_best_attack_target()
        #     if index == -2:
        #         click.end_turn()
        #         time.sleep(STATE_CHECK_INTERVAL)
        #     else:
        #         continue
            # else:
            #     click.end_turn()
            #     time.sleep(STATE_CHECK_INTERVAL)


def QuittingBattle():
    print_out()
    global g_is_single
    print("==========================in QuittingBattle==========================, g_is_single is", g_is_single)
    time.sleep(5)
    
    loop_count = 0
    # return FSM_CHOOSING_CARD
    while True:
        if quitting_flag:
            sys.exit(0)

        state = get_screen.get_state()
        if g_is_single == 1:
            g_is_single += 1
            click.cancel_click()
            click.test_click()
            click.commit_error_report()
            import zlh.zlh_click
            time.sleep(5)
            zlh.zlh_click.test_single_game_start_click()
            print("11111111111111111111111111111111111111111111111111")
            time.sleep(1)
            zlh.zlh_click.test_single_chose_hero_oppo_x_click(3)
            time.sleep(1)
            zlh.zlh_click.test_single_chose_hero_oppo_x_click(3)
            time.sleep(1)
            zlh.zlh_click.test_single_chose_hero_oppo_x_click(3)
            time.sleep(1)
            zlh.zlh_click.test_single_chose_hero_oppo_x_click(3)
            print("222222222222222222222222222222222222222222222222222")
            time.sleep(1)
            zlh.zlh_click.test_single_game_start_click()
            print("333333333333333333333333333333333333333333333333333")
            time.sleep(3)
            return FSM_MATCHING
        elif g_is_single == 2:
            print("44444444444444444444444444444444444444444444444444444444444444")
            time.sleep(3)
            click.cancel_click()
            click.test_click()
            click.test_click()
            click.test_click()
            click.test_click()
            click.test_click()
            click.test_click()
            time.sleep(1)
            click.commit_error_report()
            import zlh.zlh_click
            zlh.zlh_click.add_new_hunter_cards_from_single()
            g_is_single = False
            return FSM_MAIN_MENU
        print("55555555555555555555555555555555555555555555555555555555")
        if state in [FSM_CHOOSING_HERO, FSM_LEAVE_HS]:
            print("66666666666666666666666666666666666666666666666666")
            return state
        click.cancel_click()
        click.test_click()
        click.commit_error_report()

        loop_count += 1
        if loop_count >= 15:
            return FSM_ERROR

        time.sleep(STATE_CHECK_INTERVAL)


def GoBackHSAction():
    global FSM_state
    print("==========================in GoBackHSAction==========================")
    print_out()
    time.sleep(3)

    while not get_screen.test_hs_available():
        if quitting_flag:
            sys.exit(0)
        click.enter_HS()
        time.sleep(10)

    # 有时候炉石进程会直接重写Power.log, 这时应该重新创建文件操作句柄
    init()

    return FSM_WAIT_MAIN_MENU


def MainMenuAction():
    print("==========================in MainMenuAction==========================")
    print_out()

    time.sleep(3)

    while True:
        if quitting_flag:
            sys.exit(0)

        click.enter_battle_mode()
        time.sleep(5)

        state = get_screen.get_state()

        # 重新连接对战之类的
        if state == FSM_BATTLING:
            ok = update_log_state()
            if ok and log_state.available:
                return FSM_BATTLING
        if state == FSM_CHOOSING_HERO:
            return FSM_CHOOSING_HERO


def WaitMainMenu():
    print("==========================in WaitMainMenu==========================")
    print_out()
    while get_screen.get_state() != FSM_MAIN_MENU:
        click.click_middle()
        time.sleep(5)
    return FSM_MAIN_MENU


def HandleErrorAction():
    print("==========================in HandleErrorAction==========================")
    print_out()

    if not get_screen.test_hs_available():
        return FSM_LEAVE_HS
    else:
        click.commit_error_report()
        click.click_setting()
        time.sleep(0.5)
        # 先尝试点认输
        click.left_click(960, 380)
        time.sleep(2)

        get_screen.terminate_HS()
        time.sleep(STATE_CHECK_INTERVAL)

        return FSM_LEAVE_HS


def FSM_dispatch(next_state):
    dispatch_dict = {
        FSM_LEAVE_HS: GoBackHSAction,
        FSM_MAIN_MENU: MainMenuAction,
        FSM_CHOOSING_HERO: ChoosingHeroAction,
        FSM_MATCHING: MatchingAction,
        FSM_CHOOSING_CARD: ChoosingCardAction,
        FSM_BATTLING: Battling,
        FSM_ERROR: HandleErrorAction,
        FSM_QUITTING_BATTLE: QuittingBattle,
        FSM_WAIT_MAIN_MENU: WaitMainMenu,
    }

    if next_state not in dispatch_dict:
        error_print("Unknown state!")
        sys.exit()
    else:
        return dispatch_dict[next_state]()

def AutoHS_automata(is_single=0):
    global FSM_state
    global g_is_single
    g_is_single = is_single
    # init()
    if get_screen.test_hs_available():
        hs_hwnd = get_screen.get_HS_hwnd()
        get_screen.move_window_foreground(hs_hwnd)
        time.sleep(0.5)
    # FSM_state = FSM_CHOOSING_CARD
    # read_data_x()
    # read_data_y()
    while 1:
        if quitting_flag:
            sys.exit(0)
        if FSM_state == "":
            if g_is_single == 1 or g_is_single == 2:
                time.sleep(15)
            else:
                time.sleep(10)
            FSM_state = get_screen.get_state()
        FSM_state = FSM_dispatch(FSM_state)


if __name__ == "__main__":
    test_battle()
