import click
import keyboard
import sys
import random

from card.basic_card import MinionNoPoint
from log_state import *
from log_op import *
from strategy_entity import *

user_input = ""

class Action():
    is_in_hand = False
    hand_index = -3
    put_index = -3
    is_in_battle = False
    battle_index = -3
    point_self = -3
    point_oppo = -3
    cost_damage = 0
    cost_heal = 0
    
    def show_action(cls):
        print("=========================================")
        print("is_in_hand: ", cls.is_in_hand)
        print("hand_index: ", cls.hand_index)
        print("put_index: ", cls.put_index)
        print("is_in_battle: ", cls.is_in_battle)
        print("battle_index: ", cls.battle_index)
        print("point_self: ", cls.point_self)
        print("point_oppo: ", cls.point_oppo)
        print("cost_damage: ", cls.cost_damage)
        print("cost_heal: ", cls.cost_heal)
        print("=========================================")
        print("")
    
    def set_in_hand(cls):
        cls.is_in_hand = True

    def set_in_battle(cls):
        cls.is_in_battle = True

    def set_hero_atk_hero(cls, state):
        cls.is_in_hand = True
        cls.hand_index = -1
        cls.point_oppo = -1
        cls.cost_damage = state.my_hero.attack

    def set_hero_atk_minion(cls, state, index):
        cls.is_in_hand = True
        cls.hand_index = -1
        cls.point_oppo = index
        cls.cost_damage = state.my_hero.attack


    def set_hero_power(cls, state, index, damage):
        cls.is_in_hand = True
        cls.hand_index = -2
        cls.point_oppo = index
        cls.cost_damage = damage

    def set_default_minion(cls, state, hand_card_index):
        delta_h, *args = MinionNoPoint.best_h_and_arg(state, hand_card_index)
        cls.is_in_hand = True
        cls.hand_index = hand_card_index

    def set_minion_atk_hero(cls, state, index, damage):
        cls.is_in_battle = True
        cls.battle_index = index
        cls.point_oppo = -1
        cls.cost_damage = damage

    def set_minion_put_nopoint(cls, state, my_index, pt_index):
        cls.is_in_hand = True
        cls.hand_index = my_index
        cls.put_index = pt_index
        
    def set_minion_put_point(cls, state, my_index, pt_index, point_index):
        cls.is_in_hand = True
        cls.hand_index = my_index
        cls.put_index = pt_index
        cls.point_oppo = point_index

    def set_spell_atk_hero(cls, state, index, damage):
        cls.is_in_hand = True
        cls.hand_index = index
        cls.point_oppo = -1
        cls.cost_damage = damage
        
    def set_spell_atk_minon(cls, state, my_index, oppo_index, damage):
        cls.is_in_hand = True
        cls.hand_index = my_index
        cls.point_oppo = oppo_index
        cls.cost_damage = damage

    def set_spell_point_self_minon(cls, state, my_index, minion_index, add_atk, add_health):
        cls.is_in_hand = True
        cls.hand_index = my_index
        cls.point_self = minion_index
        cls.cost_damage = add_atk
        cls.cost_heal = add_health

    def set_use_nopoint_spell(cls, state, my_index):
        cls.is_in_hand = True
        cls.hand_index = my_index
        
    def set_use_nopoint_weapon(cls, state, my_index):
        cls.is_in_hand = True
        cls.hand_index = my_index

    def set_minion_atk_minion(cls, state, index, oppo_index, damage):
        cls.is_in_battle = True
        cls.battle_index = index
        cls.point_oppo = oppo_index
        cls.cost_damage = damage

    def do_action(cls, state):
        detail_card = None
        if cls.is_in_hand:
            if cls.hand_index == -2:
                from card.standard_card import Hero_power_cost_dec_num
                if state.my_last_mana < (2 - Hero_power_cost_dec_num):
                    return 0, []
                state.my_hero_power.exhausted = True
                val = state.oppo_hero.delta_h_after_damage(2)
                state.oppo_hero.get_damaged(2)
                return val, [state]
            if cls.hand_index == -1:
                if state.my_hero.exhausted:
                    return 0, []
                if cls.point_oppo == -1:
                    val = state.oppo_hero.delta_h_after_damage(cls.cost_damage)
                    state.oppo_hero.get_damaged(cls.cost_damage)
                elif cls.point_oppo >= 0 and cls.point_oppo <= 6:
                    val_add = state.oppo_minions[cls.point_oppo].delta_h_after_damage(cls.cost_damage)
                    if state.my_hero.health - state.oppo_minions[cls.point_oppo].attack <= 0:
                        return -99999, [state]
                    val_dec = state.my_hero.delta_h_after_damage(state.oppo_minions[cls.point_oppo].attack)
                    state.my_hero.get_damaged(state.oppo_minions[cls.point_oppo].attack)
                    if state.oppo_minions[cls.point_oppo].get_damaged(cls.cost_damage):
                        del state.oppo_minions[cls.point_oppo]
                    val = val_add -val_dec
                state.my_hero.exhausted = 1
                if state.my_weapon:
                    state.my_weapon.durability -= 1
                    val -= state.my_weapon.attack
                    state.my_weapon = None
                return val, [state]
            if cls.hand_index >= 0 and cls.hand_index <= 6:
                if state.my_hand_cards[cls.hand_index].current_cost > state.my_last_mana:
                    return 0, []
                detail_card = state.my_hand_cards[cls.hand_index].detail_card
        elif cls.is_in_battle:
            detail_card = state.my_minions[cls.battle_index].detail_card
        if detail_card:
            return detail_card.delta_h_after_direct(cls, state)
        # print("????????????????????????????")
        if cls.is_in_battle:
            if cls.point_oppo == -1:
                val = state.oppo_hero.delta_h_after_damage(cls.cost_damage)
                state.oppo_hero.get_damaged(cls.cost_damage)
                state.my_minions[cls.battle_index].exhausted = 1
                return val, [state]
            if cls.point_oppo >= 0 and cls.point_oppo <= 6:
                val = state.oppo_minions[cls.point_oppo].delta_h_after_damage(cls.cost_damage)
                oppo_val = state.oppo_minions[cls.point_oppo].get_damaged(cls.cost_damage)
                my_val = state.my_minions[cls.battle_index].get_damaged(state.oppo_minions[cls.point_oppo].attack)
                state.my_minions[cls.battle_index].exhausted = 1
                if oppo_val:
                    del state.oppo_minions[cls.point_oppo]
                if my_val:
                    del state.my_minions[cls.battle_index]
                return val, [state]
            # if cls.point_self == -1:
            #     val = state.my_hero.delta_h_after_heal(cls.cost_heal)
            #     state.my_hero.get_heal(cls.cost_heal)
            #     return val, [state]
            # if cls.point_self >= 0 and cls.point_self <= 6:
            #     val = state.my_minions[cls.point_self].delta_h_after_heal(cls.cost_heal)
            #     state.my_minions[cls.point_self].get_heal(cls.cost_heal)
            #     return val, [state]
                # state.my_hero.delta_h_after_damage()
        else:
            print("err in unknow hand card!")
            return 0, [state]
        


class StrategyState:
    def __init__(self, log_state=None):
        self.oppo_minions = []
        self.oppo_graveyard = []
        self.my_minions = []
        self.my_hand_cards = []
        self.my_graveyard = []

        self.my_hero = None
        self.my_hero_power = None
        self.can_use_power = False
        self.my_weapon = None
        self.oppo_hero = None
        self.oppo_hero_power = None
        self.oppo_weapon = None
        self.oppo_hand_card_num = 0

        self.my_total_mana = int(log_state.my_entity.query_tag("RESOURCES"))
        self.my_used_mana = int(log_state.my_entity.query_tag("RESOURCES_USED"))
        self.my_temp_mana = int(log_state.my_entity.query_tag("TEMP_RESOURCES"))

        for entity in log_state.entity_dict.values():
            if entity.query_tag("ZONE") == "HAND":
                if log_state.is_my_entity(entity):
                    hand_card = entity.generate_strategy_entity(log_state)
                    self.my_hand_cards.append(hand_card)
                else:
                    self.oppo_hand_card_num += 1

            elif entity.zone == "PLAY":
                if entity.cardtype == "MINION":
                    minion = entity.generate_strategy_entity(log_state)
                    if log_state.is_my_entity(entity):
                        self.my_minions.append(minion)
                    else:
                        self.oppo_minions.append(minion)

                elif entity.cardtype == "HERO":
                    hero = entity.generate_strategy_entity(log_state)
                    if log_state.is_my_entity(entity):
                        self.my_hero = hero
                    else:
                        self.oppo_hero = hero

                elif entity.cardtype == "HERO_POWER":
                    hero_power = entity.generate_strategy_entity(log_state)
                    if log_state.is_my_entity(entity):
                        self.my_hero_power = hero_power
                    else:
                        self.oppo_hero_power = hero_power

                elif entity.cardtype == "WEAPON":
                    weapon = entity.generate_strategy_entity(log_state)
                    if log_state.is_my_entity(entity):
                        self.my_weapon = weapon
                    else:
                        self.oppo_weapon = weapon

            elif entity.zone == "GRAVEYARD":
                if log_state.is_my_entity(entity):
                    self.my_graveyard.append(entity)
                else:
                    self.oppo_graveyard.append(entity)

        self.my_minions.sort(key=lambda temp: temp.zone_pos)
        self.oppo_minions.sort(key=lambda temp: temp.zone_pos)
        self.my_hand_cards.sort(key=lambda temp: temp.zone_pos)

    # def __eq__(self, other):
    #     return True
    
    def get_hash(self):
        res = []
        hand_cards = []
        for card in self.my_hand_cards:
            hand_cards.append(card.name)
        
        res.append(tuple(hand_cards))
        status = [self.my_hero.health, self.my_hero.attack, self.my_hero.exhausted, self.my_hero_power.exhausted, self.my_last_mana]
        res.append(tuple(status))
        minions = []
        for minion in self.my_minions:
            minions.append((minion.name, minion.attack, minion.health, minion.exhausted))
        res.append(tuple(minions))
        oppo_minions = []
        for minion in self.oppo_minions:
            oppo_minions.append((minion.name, minion.attack, minion.health))
        res.append(tuple(oppo_minions))
        oppo_hero = [self.oppo_hero.health]
        res.append(tuple(oppo_hero))
        return tuple(res)

    def get_action_list(self):
        res = []
        actions = []
        if self.my_hero.can_attack:
            # print(" my hero can attack!")
            if self.oppo_hero.can_be_pointed_by_minion:
                action = Action()
                action.set_hero_atk_hero(self)
                actions.append(action)
            for oppo_index, oppo_minion in enumerate(self.oppo_minions):
                if oppo_minion.can_be_pointed_by_minion:
                    action = Action()
                    action.set_hero_atk_minion(self, oppo_index)
                    actions.append(action)
            res.append(actions)
        # hero_power
        # print("!!!!!!!!!!!!!!!!!!!!!!!!!!self.my_hero_power.exhausted is", self.my_hero_power.exhausted)
        # if self.my_last_mana > 0:
        from card.standard_card import Hero_power_cost_dec_num
        if not self.my_hero_power.exhausted and self.my_last_mana >= (2 - Hero_power_cost_dec_num):
            # print(" my hero power can attack!")
            actions = []
            action = Action()
            action.set_hero_power(self, -1, 2)
            actions.append(action)
            res.append(actions)
        for hand_card_index, hand_card in enumerate(self.my_hand_cards):
            if hand_card.current_cost > self.my_last_mana:
                continue

            detail_card = hand_card.detail_card
            actions = []
            if detail_card is None:
                if hand_card.cardtype == CARD_MINION and not hand_card.battlecry:
                    action = Action()
                    action.set_default_minion(self, hand_card_index)
                    actions.append(action)

                else:
                    continue
            else:
                actions = detail_card.get_all_actions(self, hand_card_index, True)

            res.append(actions)
        touchable_oppo_minions = self.touchable_oppo_minions
        has_taunt = self.oppo_has_taunt
        for battle_card_index, battle_card in enumerate(self.my_minions):
            # print("battle_card_index is :", battle_card_index)
            if not battle_card.can_attack_minion:
                continue
            actions = []
            if not has_taunt and battle_card.can_beat_face and self.oppo_hero.can_be_pointed_by_minion:
            # if self.oppo_hero.can_be_pointed_by_minion:
                action = Action()
                action.set_minion_atk_hero(self, battle_card_index, battle_card.attack)
                actions.append(action)
            for oppo_index, oppo_min in enumerate(self.oppo_minions):
                if oppo_min not in touchable_oppo_minions:
                    continue
                action = Action()
                action.set_minion_atk_minion(self, battle_card_index, oppo_index, battle_card.attack)
                actions.append(action)
            res.append(actions)
        return res


    def debug_print_battlefield(self):
        if not DEBUG_PRINT:
            return

        debug_print("对手英雄:")
        debug_print("    " + str(self.oppo_hero))
        debug_print(f"技能:")
        debug_print("    " + self.oppo_hero_power.name)
        if self.oppo_weapon:
            debug_print("头上有把武器:")
            debug_print("    " + str(self.oppo_weapon))
        if self.oppo_minion_num > 0:
            debug_print(f"对手有{self.oppo_minion_num}个随从:")
            for minion in self.oppo_minions:
                debug_print("    " + str(minion))
        else:
            debug_print(f"对手没有随从")
        debug_print(f"总卡费启发值: {self.oppo_heuristic_value}")

        debug_print()

        debug_print("我的英雄:")
        debug_print("    " + str(self.my_hero))
        debug_print(f"技能:")
        debug_print("    " + self.my_hero_power.name)
        if self.my_weapon:
            debug_print("头上有把武器:")
            debug_print("    " + str(self.my_weapon))
        if self.my_minion_num > 0:
            debug_print(f"我有{self.my_minion_num}个随从:")
            for minion in self.my_minions:
                debug_print("    " + str(minion))
        else:
            debug_print("我没有随从")
        debug_print(f"总卡费启发值: {self.my_heuristic_value}")

    def debug_print_out(self):
        global user_input
        if not DEBUG_PRINT:
            return

        debug_print(f"对手墓地:")
        debug_print("    " + ", ".join([entity.name for entity in self.oppo_graveyard]))
        debug_print(f"对手有{self.oppo_hand_card_num}张手牌")

        self.debug_print_battlefield()
        debug_print()

        debug_print(f"水晶: {self.my_last_mana}/{self.my_total_mana}")
        debug_print(f"我有{self.my_hand_card_num}张手牌:")
        for hand_card in self.my_hand_cards:
            debug_print(f"    [{hand_card.zone_pos}] {hand_card.name} {hand_card.card_id}"
                        f"cost:{hand_card.current_cost}")
        debug_print(f"我的墓地:")
        debug_print("    " + ", ".join([entity.name for entity in self.my_graveyard]))


        infolist = []
        total_mana = self.my_last_mana
        self.my_hero.health
        hero_info = [0, 0, total_mana, 1, 2, 4, self.my_hero.attack, self.my_hero.health, 0]
        if self.my_hero.attack > 0:
            hero_info.append(1)
            hero_info.append(1)
        else:
            hero_info.append(0)
            hero_info.append(0)
        hero_info.append(self.my_hero.attack)
        hero_info.append(0)
        power_info = [2, 0, total_mana, 1, 1, 1, 2, 0, 0, 0, 1, 2, 0]
        infolist.append(hero_info)
        infolist.append(power_info)
       
        for hand_card in self.my_hand_cards:
            card_type = -1
            atk = 0
            put = 0
            ptmin = 0
            pthero = 0
            damage = 0
            protect = 0
            health = 0
            if isinstance(hand_card, StrategyMinion):
                card_type = 2
                atk = hand_card.attack
                health = hand_card.health
                put = 1
                if hand_card.name == "冰川裂片":
                    ptmin = 1
                    pthero = 1
                elif hand_card.name == "吸血蚊":
                    damage = 3
                    protect = 3
            elif isinstance(hand_card, StrategySpell):
                card_type = 1
                if hand_card.name == "秘法射擊":
                    atk = 2
                    damage = atk
                    ptmin = 1
                elif hand_card.name == "爆炸陷阱":
                    atk = 2
                    damage = atk
                elif hand_card.name == "快速射擊":
                    ptmin = 1
                    pthero
                    atk = 3
                    damage = atk
            elif isinstance(hand_card, StrategyWeapon):
                card_type = 3
                atk = hand_card.attack
                health = hand_card.durability
            else:
                card_type = -1
            temp = [hand_card.current_cost, 1, total_mana, 1, 1, card_type, atk, health, put, ptmin, pthero, damage, protect]
           
            infolist.append(temp)
       

        for my_minion in self.my_minions:
            atk = my_minion.attack
            health = my_minion.health
            protect = 0
            damage = atk
            if my_minion.taunt:
                protect = health
            if my_minion.exhausted:
                damage = 0
            temp = [0, 0, total_mana, 1, 2, 2, atk, health, 0, 0, 0, damage, protect]
            infolist.append(temp)

       
        oppo_hero = [0, 0, total_mana, 2, 2, 4, self.oppo_hero.attack, self.oppo_hero.health, 0, 0, 0, 0, 0]
        infolist.append(oppo_hero)
        oppo_power_name = self.oppo_hero_power.name
        oppo_hero_cost = 2
        oppo_hero_atk = 0
        oppo_hero_health = 0
        oppo_hero_ptmin = 0
        oppo_hero_pthero = 0
        oppo_hero_damage = 0
        oppo_hero_protect = 0
        if oppo_power_name == "次级治疗术":
            oppo_hero_ptmin = 1
            oppo_hero_pthero = 1
            oppo_hero_protect = 2
        elif oppo_power_name == "图腾召唤":
            oppo_hero_atk = 1
            oppo_hero_health = 1
            oppo_hero_protect = 1
        elif oppo_power_name == "稳固射击":
            oppo_hero_atk = 2
            oppo_hero_pthero = 1
            oppo_hero_damage = 2

        oppo_hero_power = [oppo_hero_cost, 0, total_mana, 2, 1, 1, oppo_hero_atk, oppo_hero_health, 0, oppo_hero_ptmin, oppo_hero_pthero, oppo_hero_damage, oppo_hero_protect]
        infolist.append(oppo_hero_power)

        for opo_minion in self.oppo_minions:
            atk = opo_minion.attack
            health = opo_minion.health
            protect = 0
            damage = 0
            if opo_minion.taunt:
                protect = health
            temp = [0, 0, total_mana, 2, 2, 2, atk, health, 0, 0, 0, atk, protect]
            infolist.append(temp)
        print("user_input now is: ", user_input)
        res = []
        if user_input != "":
            user_input = user_input.strip()
            user_input_list = user_input.split()
            for inp in user_input_list:
                res.append(int(inp))
            infolist.append(res)
            user_input = ""

        # debug_print(infolist)
        return infolist
    @property
    def my_last_mana(self):
        return self.my_total_mana - self.my_used_mana + self.my_temp_mana
    
    def pay_mana(self, mana_num):
        if mana_num + self.my_used_mana - self.my_total_mana > 0:
            print("err in  pay_mana!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!, mana_num is :", mana_num, "my_used_mana is ", self.my_used_mana, " my_total_mana is :", self.my_total_mana)
            return False
        self.my_used_mana += mana_num
        return True

    @property
    def oppo_minion_num(self):
        return len(self.oppo_minions)

    @property
    def my_minion_num(self):
        return len(self.my_minions)

    @property
    def my_hand_card_num(self):
        return len(self.my_hand_cards)

    # 用卡费体系算启发值
    @property
    def oppo_heuristic_value(self):
        total_h_val = self.oppo_hero.heuristic_val
        if self.oppo_weapon:
            total_h_val += self.oppo_weapon.heuristic_val
        for minion in self.oppo_minions:
            total_h_val += minion.heuristic_val
        return total_h_val

    @property
    def my_heuristic_value(self):
        total_h_val = self.my_hero.heuristic_val
        if self.my_weapon:
            total_h_val += self.my_weapon.heuristic_val
        for minion in self.my_minions:
            total_h_val += minion.heuristic_val
        return total_h_val

    @property
    def heuristic_value(self):
        return round(self.my_heuristic_value - self.oppo_heuristic_value, 3)

    @property
    def min_cost(self):
        minium = 100
        for hand_card in self.my_hand_cards:
            minium = min(minium, hand_card.current_cost)
        return minium

    @property
    def my_total_spell_power(self):
        return sum([minion.spell_power for minion in self.my_minions])

    @property
    def my_detail_hero_power(self):
        return self.my_hero_power.detail_hero_power

    @property
    def touchable_oppo_minions(self):
        ret = []

        for oppo_minion in self.oppo_minions:
            if oppo_minion.taunt and oppo_minion.can_be_pointed_by_minion:
                ret.append(oppo_minion)

        if len(ret) == 0:
            for oppo_minion in self.oppo_minions:
                if oppo_minion.can_be_pointed_by_minion:
                    ret.append(oppo_minion)

        return ret

    @property
    def oppo_has_taunt(self):
        for oppo_minion in self.oppo_minions:
            if oppo_minion.taunt and not oppo_minion.stealth:
                return True

        return False

    @property
    def my_total_attack(self):
        count = 0
        for my_minion in self.my_minions:
            if my_minion.can_beat_face:
                count += my_minion.attack

        if self.my_hero.can_attack:
            count += self.my_hero.attack

        return count

    def fetch_uni_entity(self, uni_index):
        if 0 <= uni_index < 7:
            return self.my_minions[uni_index]
        elif uni_index == 9:
            return self.my_hero
        elif 10 <= uni_index < 17:
            return self.oppo_minions[uni_index]
        elif uni_index == 19:
            return self.oppo_hero
        else:
            error_print(f"Get invalid uni_index: {uni_index}")
            sys.exit(-1)

    def fight_between(self, oppo_index, my_index):
        oppo_minion = self.oppo_minions[oppo_index]
        my_minion = self.my_minions[my_index]

        if oppo_minion.get_damaged(my_minion.attack):
            self.oppo_minions.pop(oppo_index)

        if my_minion.get_damaged(oppo_minion.attack):
            self.my_minions.pop(my_index)

    def random_distribute_damage(self, damage, oppo_index_list, my_index_list):
        if len(oppo_index_list) == len(my_index_list) == 0:
            return

        random_x = random.randint(0, len(oppo_index_list) + len(my_index_list) - 1)

        if random_x < len(oppo_index_list):
            oppo_index = oppo_index_list[random_x]
            minion = self.oppo_minions[oppo_index]
            if minion.get_damaged(damage):
                self.oppo_minions.pop(oppo_index)
        else:
            my_index = my_index_list[random_x - len(oppo_index_list)]
            minion = self.my_minions[my_index]
            if minion.get_damaged(damage):
                self.my_minions.pop(my_index)

    def get_best_attack_target(self):
        touchable_oppo_minions = self.touchable_oppo_minions
        has_taunt = self.oppo_has_taunt
        beat_face_win = self.my_total_attack >= self.oppo_hero.health

        max_delta_h_val = 0
        max_my_index = -2
        max_oppo_index = -2
        min_attack = 0

        # 枚举每一个己方随从
        for my_index, my_minion in enumerate(self.my_minions):
            if not my_minion.can_attack_minion:
                continue
            print("can attack is================================================================= ", my_minion.name)
            # 如果没有墙,自己又能打脸,应该试一试
            if not has_taunt \
                    and my_minion.can_beat_face \
                    and self.oppo_hero.can_be_pointed_by_minion:
                if beat_face_win:
                    debug_print(f"攻击决策: [{my_index}]({my_minion.name})->"
                                f"[-1]({self.oppo_hero.name}) "
                                f"斩杀了")
                    return my_index, -1

                tmp_delta_h = self.oppo_hero.delta_h_after_damage(my_minion.attack)

                debug_print(f"攻击决策: [{my_index}]({my_minion.name})->"
                            f"[-1]({self.oppo_hero.name}) "
                            f"delta_h_val:{tmp_delta_h}")

                if tmp_delta_h > max_delta_h_val:
                    max_delta_h_val = tmp_delta_h
                    max_my_index = my_index
                    max_oppo_index = -1
                    min_attack = 999

            for oppo_minion in touchable_oppo_minions:
                oppo_index = oppo_minion.zone_pos - 1

                tmp_delta_h = 0
                tmp_delta_h -= my_minion.delta_h_after_damage(oppo_minion.attack)
                tmp_delta_h += oppo_minion.delta_h_after_damage(my_minion.attack)

                debug_print(f"攻击决策：[{my_index}]({my_minion.name})->"
                            f"[{oppo_index}]({oppo_minion.name}) "
                            f"delta_h_val: {tmp_delta_h}")

                if tmp_delta_h > max_delta_h_val or \
                        tmp_delta_h == max_delta_h_val and my_minion.attack < min_attack:
                    max_delta_h_val = tmp_delta_h
                    max_my_index = my_index
                    max_oppo_index = oppo_index
                    min_attack = my_minion.attack

        # 试一试英雄攻击
        if self.my_hero.can_attack:
            if not has_taunt and self.oppo_hero.can_be_pointed_by_minion:
                if beat_face_win:
                    debug_print(f"攻击决策: [-1]({self.my_hero.name})->"
                                f"[-1]({self.oppo_hero.name}) "
                                f"斩杀了")
                    return -1, -1

            for oppo_minion in touchable_oppo_minions:
                oppo_index = oppo_minion.zone_pos - 1

                tmp_delta_h = 0
                tmp_delta_h += oppo_minion.delta_h_after_damage(self.my_hero.attack)
                tmp_delta_h -= self.my_hero.delta_h_after_damage(oppo_minion.attack)
                if self.my_weapon is not None:
                    tmp_delta_h -= self.my_weapon.attack

                debug_print(f"攻击决策: [-1]({self.my_hero.name})->"
                            f"[{oppo_index}]({oppo_minion.name}) "
                            f"delta_h_val: {tmp_delta_h}")

                if tmp_delta_h >= max_delta_h_val:
                    max_delta_h_val = tmp_delta_h
                    max_my_index = -1
                    max_oppo_index = oppo_index

        debug_print(f"最终决策: max_my_index: {max_my_index}, "
                    f"max_oppo_index: {max_oppo_index}")

        return max_my_index, max_oppo_index

    def my_entity_attack_oppo(self, my_index, oppo_index):
        if my_index == -1:
            if oppo_index == -1:
                click.hero_beat_hero()
            else:
                click.hero_beat_minion(oppo_index, self.oppo_minion_num)
        else:
            if oppo_index == -1:
                click.minion_beat_hero(my_index, self.my_minion_num)
            else:
                click.minion_beat_minion(my_index, self.my_minion_num,
                                         oppo_index, self.oppo_minion_num)

    def copy_new_one(self):
        # TODO: 有必要deepcopy吗
        tmp = copy.deepcopy(self)
        for i in range(self.oppo_minion_num):
            tmp.oppo_minions[i] = copy.deepcopy(self.oppo_minions[i])
        for i in range(self.my_minion_num):
            tmp.my_minions[i] = copy.deepcopy(self.my_minions[i])
        for i in range(self.my_hand_card_num):
            tmp.my_hand_cards[i] = copy.deepcopy(self.my_hand_cards[i])
        return tmp

    def best_h_index_arg(self):
        debug_print()
        best_delta_h = 0
        best_index = -2
        best_args = []

        # 考虑使用手牌
        for hand_card_index, hand_card in enumerate(self.my_hand_cards):
            delta_h = 0
            args = []

            if hand_card.current_cost > self.my_last_mana:
                debug_print(f"卡牌-[{hand_card_index}]({hand_card.name}) 跳过")
                continue

            detail_card = hand_card.detail_card
            print("now card name is ", hand_card.name, " id is : ", hand_card.card_id)
            if detail_card is None:
                if hand_card.cardtype == CARD_MINION and not hand_card.battlecry:
                    delta_h, *args = MinionNoPoint.best_h_and_arg(self, hand_card_index)
                    debug_print(f"卡牌-[{hand_card_index}]({hand_card.name}) "
                                f"delta_h: {delta_h}, *args: {[]} (默认行为) ")
                else:
                    debug_print(f"卡牌[{hand_card_index}]({hand_card.name})无法评判")
            else:
                delta_h, *args = detail_card.best_h_and_arg(self, hand_card_index)
                debug_print(f"卡牌-[{hand_card_index}]({hand_card.name}) "
                            f"delta_h: {delta_h}, *args: {args} (手写行为)")

            if delta_h > best_delta_h:
                best_delta_h = delta_h
                best_index = hand_card_index
                best_args = args

        # 考虑使用英雄技能
        if self.my_last_mana >= 2 and \
                self.my_detail_hero_power and \
                not self.my_hero_power.exhausted:
            hero_power = self.my_detail_hero_power

            delta_h, *args = hero_power.best_h_and_arg(self, -1)

            debug_print(f"技能-[ ]({self.my_hero_power.name}) "
                        f"delta_h: {delta_h} "
                        f"*args: {args}")

            if delta_h > best_delta_h:
                best_index = -1
                best_args = args
        else:
            debug_print(f"技能-[ ]({self.my_hero_power.name}) 跳过")

        debug_print(f"决策结果: best_delta_h:{best_delta_h}, "
                    f"best_index:{best_index}, best_args:{best_args}")
        debug_print()
        return best_index, best_args

    def use_best_entity(self, index, args):
        if index == -1:
            debug_print("将使用技能")
            hero_power = self.my_detail_hero_power
            hero_power.use_with_arg(self, -1, *args)
        else:
            self.use_card(index, *args)

    # 会返回这张卡的cost
    def use_card(self, index, *args):
        hand_card = self.my_hand_cards[index]
        detail_card = hand_card.detail_card
        debug_print(f"将使用卡牌[{index}] {hand_card.name}")

        if detail_card is None:
            MinionNoPoint.use_with_arg(self, index, *args)
        else:
            detail_card.use_with_arg(self, index, *args)

        self.my_hand_cards.pop(index)
        return hand_card.current_cost


# if __name__ == "__main__":
#     # keyboard.add_hotkey("ctrl+q", sys.exit)

#     log_iter = log_iter_func(HEARTHSTONE_POWER_LOG_PATH)
#     state = LogState()

#     while True:
#         log_container = next(log_iter)
#         if log_container.length > 0:
#             for x in log_container.message_list:
#                 update_state(state, x)
#             strategy_state = StrategyState(state)
#             strategy_state.debug_print_out()

#             with open("game_state_snapshot.txt", "w", encoding="utf8") as f:
#                 f.write(str(state))

#             mine_index, oppo_index = strategy_state.get_best_attack_target()
#             debug_print(f"我的决策是: mine_index: {mine_index}, oppo_index: {oppo_index}")

#             if mine_index != -1:
#                 if oppo_index == -1:
#                     click.minion_beat_hero(mine_index, strategy_state.my_minion_num)
#                 else:
#                     click.minion_beat_minion(mine_index, strategy_state.my_minion_num,
#                                              oppo_index, strategy_state.oppo_minion_num)
