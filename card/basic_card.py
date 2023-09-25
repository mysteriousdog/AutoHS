import random
import time
from abc import ABC, abstractmethod
import click
from constants.constants import *
from print_info import *
import strategy

class Card(ABC):
    # 用来指示是否在留牌阶段把它留下, 默认留下
    # 在 keep_in_hand 中返回
    keep_in_hand_bool = True

    @classmethod
    def keep_in_hand(cls, state, hand_card_index):
        return cls.keep_in_hand_bool

    # 用来指示这张卡的价值, 在 best_h_and_arg 中返回.
    # 如果为 0 则代表未设置, 会根据卡牌费用等信息区估算价值.
    # 一些功能卡不能用一个简单的数值去评判价值, 应针对其另写
    # 函数
    value = 0

    # 返回两个东西,第一项是使用这张卡的\delta h,
    # 之后是是用这张卡的最佳参数,参数数目不定
    # 参数是什么呢,比如一张火球术,参数就是指示你
    # 是要打脸还是打怪
    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        return cls.value,

    @classmethod
    @abstractmethod
    def use_with_arg(cls, state, card_index, *args):
        pass

    @classmethod
    @abstractmethod
    def get_card_type(cls):
        pass


class SpellCard(Card):
    wait_time = BASIC_SPELL_WAIT_TIME

    @classmethod
    def get_card_type(cls):
        return CARD_SPELL


class SpellNoPoint(SpellCard):
    @classmethod
    def use_with_arg(cls, state, card_index, *args):
        click.choose_and_use_spell(card_index, state.my_hand_card_num)
        click.cancel_click()
        time.sleep(cls.wait_time)
    
    @classmethod
    def get_all_actions_nopoint_cls(cls, state, index, is_in_hand, cost):
        actions = []
        if not is_in_hand:
            return actions
        if state.my_last_mana < state.my_hand_cards[index].current_cost:
            return actions
        action = strategy.Action()
        action.set_use_nopoint_spell(state, index)
        actions.append(action)
        return actions


class SpellPointOppo(SpellCard):
    @classmethod
    def use_with_arg(cls, state, card_index, *args):
        if len(args) == 0:
            hand_card = state.my_hand_cards[card_index]
            warn_print(f"Receive 0 args in using SpellPointOppo card {hand_card.name}")
            return

        oppo_index = args[0]
        click.choose_card(card_index, state.my_hand_card_num)
        if oppo_index >= 0:
            click.choose_opponent_minion(oppo_index, state.oppo_minion_num)
        else:
            click.choose_oppo_hero()
        click.cancel_click()
        time.sleep(cls.wait_time)


class SpellPointMine(SpellCard):
    @classmethod
    def use_with_arg(cls, state, card_index, *args):
        if len(args) == 0:
            hand_card = state.my_hand_cards[card_index]
            warn_print(f"Receive 0 args in using SpellPointMine card {hand_card.name}")
            return

        mine_index = args[0]
        click.choose_card(card_index, state.my_hand_card_num)
        click.choose_my_minion(mine_index, state.my_minion_num)
        click.cancel_click()
        time.sleep(cls.wait_time)
    
    @classmethod
    def get_all_actions(cls, state, index, is_in_hand):
        actions = []
        if not is_in_hand:
            return actions
        if state.my_last_mana < state.my_hand_cards[index].current_cost:
            return actions

        for oppo_index, oppo_minion in enumerate(state.my_minions):
            if not oppo_minion.can_be_pointed_by_spell:
                continue
            action = strategy.Action()
            action.set_spell_atk_minon(state, index, oppo_index, 3)
            actions.append(action)
        return actions


class MinionCard(Card):
    @classmethod
    def get_card_type(cls):
        return CARD_MINION

    @classmethod
    def basic_delta_h(cls, state, hand_card_index):
        if state.my_minion_num >= 7:
            return -20000
        else:
            return 0

    @classmethod
    def utilize_delta_h_and_arg(cls, state, hand_card_index):
        if cls.value != 0:
            return cls.value, state.my_minion_num
        else:
            # 费用越高的应该越厉害吧
            hand_card = state.my_hand_cards[hand_card_index]
            delta_h = hand_card.current_cost / 2 + 1

            if state.my_hero.health <= 10 and hand_card.taunt:
                delta_h *= 1.5

            return delta_h, state.my_minion_num  # 默认放到最右边

    @classmethod
    def combo_delta_h(cls, state, hand_card_index):
        h_sum = 0

        for my_minion in state.my_minions:
            # 有末日就别下怪了
            if my_minion.card_id == "VAN_NEW1_021":
                h_sum += -1000

            # 有飞刀可以多下怪
            if my_minion.card_id == "VAN_NEW1_019":
                h_sum += 0.5

        return h_sum

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        delta_h, *args = cls.utilize_delta_h_and_arg(state, hand_card_index)
        if len(args) == 0:
            args = [state.my_minion_num]

        delta_h += cls.basic_delta_h(state, hand_card_index)
        delta_h += cls.combo_delta_h(state, hand_card_index)
        return (delta_h,) + tuple(args)
    
    @classmethod
    def delta_h_after_direct_cls(cls, action, state):
        if action.is_in_battle:
            if action.point_oppo == -1:
                oppo_atk = 0
                oppo_minion = state.oppo_hero
                val_del = 0
            else:
                oppo_minion = state.oppo_minions[action.point_oppo]
                oppo_atk = oppo_minion.attack
            me = state.my_minions[action.battle_index]
            if me.exhausted and me.attackable_by_rush == 0:
                return 0, [state]
            if action.point_oppo != -1:
                val_del = me.delta_h_after_damage(oppo_atk)
            
            val_add = oppo_minion.delta_h_after_damage(me.attack)
            oppo_minion.get_damaged(me.attack)
            me.exhausted = 1
            me.attackable_by_rush = 0
            if oppo_minion.health <= 0:
                if action.point_oppo == -1:
                    return 999999, [state]
                else:
                    del state.oppo_minions[action.point_oppo]
            if me.get_damaged(oppo_atk):
                del state.my_minions[action.battle_index]
            val = val_add - val_del
            # print("=============================val_add is ", val_add, " val_del is ", val_del, "oppo index is ", action.point_oppo)
            return val , [state]

    @classmethod
    def delta_h_after_direct_hand_no_point(cls, action, state):
        if action.is_in_hand:
            index = action.hand_index
            state.my_minions.append(state.my_hand_cards[index])
            if state.my_minions[-1].charge:
                state.my_minions[-1].exhausted = 0
            else:
                state.my_minions[-1].exhausted = 1
            if state.my_minions[-1].rush:
                state.my_minions[-1].attackable_by_rush = 1
            state.pay_mana(state.my_hand_cards[index].current_cost)
            del state.my_hand_cards[index]
            return cls.value, [state]
        else:
            return 0, []
    
    @classmethod
    def get_all_actions_MinionNoPoint_inbattle(cls, state, index, is_in_hand):
        actions = []
        if is_in_hand:
            return actions
        touchable_oppo_minions = state.touchable_oppo_minions
        has_taunt = state.oppo_has_taunt
        my_minion = state.my_minions[index]
        if not has_taunt \
                and my_minion.can_beat_face \
                and state.oppo_hero.can_be_pointed_by_minion:
            action = strategy.Action()
            action.set_minion_atk_hero(state, index, my_minion.attack)
            actions.append(action)
        for oppo_index, oppo_minion in enumerate(state.oppo_minions):
            if oppo_minion not in touchable_oppo_minions:
                continue
            if oppo_minion.can_be_pointed_by_minion:
                action = strategy.Action()
                action.set_minion_atk_minion(state, index, oppo_index, my_minion.attack)
                actions.append(action)
        return actions


class MinionNoPoint(MinionCard):
    @classmethod
    def use_with_arg(cls, state, card_index, *args):
        gap_index = args[0]
        click.choose_card(card_index, state.my_hand_card_num)
        click.put_minion(gap_index, state.my_minion_num)
        click.cancel_click()
        time.sleep(BASIC_MINION_PUT_INTERVAL)
        
    @classmethod
    def get_all_actions_MinionNoPoint_inhand(cls, state, index, is_in_hand):
        actions = []
        if not is_in_hand:
            return actions
        cost = state.my_hand_cards[index].current_cost
        if state.my_last_mana < cost:
            return actions
        
        # state.pay_mana(cost)
        action = strategy.Action()
        action.set_minion_put_nopoint(state, index, state.my_minion_num)
        actions.append(action)
        return actions


class MinionPointAllMinions(MinionCard):
    @classmethod
    def use_with_arg(cls, state, card_index, *args):
        gap_index = args[0]
        oppo_index = args[1]
        my_index = args[2]

        click.choose_card(card_index, state.my_hand_card_num)
        click.put_minion(gap_index, state.my_minion_num)
        if oppo_index >= 0:
            click.choose_opponent_minion(oppo_index, state.oppo_minion_num)
        elif my_index >= 0:
            click.choose_my_minion(my_index, state.my_minion_num + 1)
        click.cancel_click()
        time.sleep(BASIC_MINION_PUT_INTERVAL)

class MinionPointOppo(MinionCard):
    @classmethod
    def use_with_arg(cls, state, card_index, *args):
        gap_index = args[0]
        oppo_index = args[1]

        click.choose_card(card_index, state.my_hand_card_num)
        click.put_minion(gap_index, state.my_minion_num)
        if oppo_index >= 0:
            click.choose_opponent_minion(oppo_index, state.oppo_minion_num)
        else:
            click.choose_oppo_hero()
        click.cancel_click()
        time.sleep(BASIC_MINION_PUT_INTERVAL)
    
    @classmethod
    def get_all_actions_MinionPoint_inhand(cls, state, index, is_in_hand, point_index):
        actions = []
        if not is_in_hand:
            return actions
        cost = state.my_hand_cards[index].current_cost
        if state.my_last_mana < cost:
            return actions
        
        # state.pay_mana(cost)
        action = strategy.Action()
        action.set_minion_put_point(state, index, state.my_minion_num, point_index)
        actions.append(action)
        return actions


class MinionPointMine(MinionCard):
    @classmethod
    def use_with_arg(cls, state, card_index, *args):
        gap_index = args[0]
        my_index = args[1]

        click.choose_card(card_index, state.my_hand_card_num)
        click.put_minion(gap_index, state.my_minion_num)
        if my_index >= 0:
            # 这时这个随从已经在场上了, 其他随从已经移位了
            click.choose_my_minion(my_index, state.my_minion_num + 1)
        else:
            click.choose_my_hero()
        click.cancel_click()
        time.sleep(BASIC_MINION_PUT_INTERVAL)


class WeaponCard(Card):
    @classmethod
    def get_card_type(cls):
        return CARD_WEAPON

    @classmethod
    def use_with_arg(cls, state, card_index, *args):
        click.choose_and_use_spell(card_index, state.my_hand_card_num)
        click.cancel_click()
        time.sleep(BASIC_WEAPON_WAIT_TIME)

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        if state.my_weapon:
            return 0,
        else:
            return cls.value,
    # TODO: 还什么都没实现...
    @classmethod
    def get_all_actions_nopoint_weapon(cls, state, index, cost):
        actions = []
        if state.my_last_mana < state.my_hand_cards[index].current_cost:
            return actions
        action = strategy.Action()
        action.set_use_nopoint_weapon(state, index)
        actions.append(action)
        return actions


class HeroPowerCard(Card):
    @classmethod
    def get_card_type(cls):
        return CARD_HERO_POWER


# 幸运币
class Coin(SpellNoPoint):
    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        best_delta_h = 0

        for another_index, hand_card in enumerate(state.my_hand_cards):
            delta_h = 0

            if hand_card.current_cost != state.my_last_mana + 1:
                continue
            if hand_card.is_coin:
                continue

            detail_card = hand_card.detail_card
            if detail_card is None:
                if hand_card.cardtype == CARD_MINION and not hand_card.battlecry:
                    delta_h = MinionNoPoint.best_h_and_arg(state, another_index)[0]
            else:
                delta_h = detail_card.best_h_and_arg(state, another_index)[0]

            delta_h -= 2  # 如果跳费之后能使用的卡显著强于不跳费的卡, 就跳币
            best_delta_h = max(best_delta_h, delta_h)

        return best_delta_h,
    
    @classmethod
    def get_all_actions(cls, state, index, is_in_hand):
        return cls.get_all_actions_nopoint_cls(state, index, is_in_hand, 0)
    
    @classmethod
    def delta_h_after_direct(cls, action, state):
        del state.my_hand_cards[action.hand_index]
        state.pay_mana(-1)
        return 1, [state]

