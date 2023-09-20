import sys
sys.path.append(r"..")
from card.basic_card import *
import statistics
import copy
import strategy
BrandonKitkouski_used_before = 0
# 护甲商贩
class ArmorVendor(MinionNoPoint):
    value = 2
    keep_in_hand_bool = True


# 神圣惩击
class HolySmite(SpellPointOppo):
    wait_time = 2
    # 加个bias,一是包含了消耗的水晶的代价，二是包含了消耗了手牌的代价
    bias = -2

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        best_oppo_index = -1
        best_delta_h = 0

        for oppo_index, oppo_minion in enumerate(state.oppo_minions):
            if not oppo_minion.can_be_pointed_by_spell:
                continue
            temp_delta_h = oppo_minion.delta_h_after_damage(3) + cls.bias
            if temp_delta_h > best_delta_h:
                best_delta_h = temp_delta_h
                best_oppo_index = oppo_index

        return best_delta_h, best_oppo_index


# 倦怠光波
class WaveOfApathy(SpellNoPoint):
    wait_time = 2
    bias = -4

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        tmp = 0

        for minion in state.oppo_minions:
            tmp += minion.attack - 1

        return tmp + cls.bias,


# 噬骨殴斗者
class BonechewerBrawler(MinionNoPoint):
    value = 2
    keep_in_hand_bool = True


# 暗言术灭
class ShadowWordDeath(SpellPointOppo):
    wait_time = 1.5
    bias = -6

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        best_oppo_index = -1
        best_delta_h = 0

        for oppo_index, oppo_minion in enumerate(state.oppo_minions):
            if oppo_minion.attack < 5:
                continue
            if not oppo_minion.can_be_pointed_by_spell:
                continue

            tmp = oppo_minion.heuristic_val + cls.bias
            if tmp > best_delta_h:
                best_delta_h = tmp
                best_oppo_index = oppo_index

        return best_delta_h, best_oppo_index


# 神圣化身
class Apotheosis(SpellPointMine):
    bias = -6

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        best_delta_h = 0
        best_mine_index = -1

        for my_index, my_minion in enumerate(state.my_minions):
            if not my_minion.can_be_pointed_by_spell:
                continue

            tmp = cls.bias + 3 + (my_minion.health + 2) / 4 + \
                  (my_minion.attack + 1) / 2
            if my_minion.can_attack_minion:
                tmp += my_minion.attack / 4
            if tmp > best_delta_h:
                best_delta_h = tmp
                best_mine_index = my_index

        return best_delta_h, best_mine_index


# 亡首教徒
class DeathsHeadCultist(MinionNoPoint):
    value = 1
    keep_in_hand_bool = True


# 噬灵疫病
class DevouringPlague(SpellNoPoint):
    wait_time = 4
    bias = -4  # 把吸的血直接算进bias

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        curr_h = state.heuristic_value

        delta_h_sum = 0
        sample_times = 5

        for i in range(sample_times):
            tmp_state = state.copy_new_one()
            for j in range(4):
                tmp_state.random_distribute_damage(1, [i for i in range(tmp_state.oppo_minion_num)], [])

            delta_h_sum += tmp_state.heuristic_value - curr_h

        return delta_h_sum / sample_times + cls.bias,


# 狂傲的兽人
class OverconfidentOrc(MinionNoPoint):
    value = 3
    keep_in_hand_bool = True


# 神圣新星
class HolyNova(SpellNoPoint):
    bias = -8

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        return cls.bias + sum([minion.delta_h_after_damage(2)
                               for minion in state.oppo_minions]),


# 狂乱
class Hysteria(SpellPointOppo):
    wait_time = 5
    bias = -9  # 我觉得狂乱应该要能力挽狂澜
    keep_in_hand_bool = False

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        best_delta_h = 0
        best_arg = 0
        sample_times = 10

        if state.oppo_minion_num == 0 or state.oppo_minion_num + state.my_minion_num == 1:
            return 0, -1

        for chosen_index, chosen_minion in enumerate(state.oppo_minions):
            if not chosen_minion.can_be_pointed_by_spell:
                continue

            delta_h_count = 0

            for i in range(sample_times):
                tmp_state = state.copy_new_one()
                tmp_chosen_index = chosen_index

                while True:
                    another_index_list = [j for j in range(tmp_state.oppo_minion_num + tmp_state.my_minion_num)]
                    another_index_list.pop(tmp_chosen_index)
                    if len(another_index_list) == 0:
                        break
                    another_index = another_index_list[random.randint(0, len(another_index_list) - 1)]

                    # print("another index: ", another_index)
                    if another_index >= tmp_state.oppo_minion_num:
                        another_minion = tmp_state.my_minions[another_index - tmp_state.oppo_minion_num]
                        if another_minion.get_damaged(chosen_minion.attack):
                            tmp_state.my_minions.pop(another_index - tmp_state.oppo_minion_num)
                    else:
                        another_minion = tmp_state.oppo_minions[another_index]
                        if another_minion.get_damaged(chosen_minion.attack):
                            tmp_state.oppo_minions.pop(another_index)
                            if another_index < tmp_chosen_index:
                                tmp_chosen_index -= 1

                    if chosen_minion.get_damaged(another_minion.attack):
                        # print("h:", tmp_state.heuristic_value, state.heuristic_value)
                        tmp_state.oppo_minions.pop(tmp_chosen_index)
                        break

                    # print("h:", tmp_state.heuristic_value, state.heuristic_value)

                delta_h_count += tmp_state.heuristic_value - state.heuristic_value

            delta_h_count /= sample_times
            # print("average delta_h:", delta_h_count)
            if delta_h_count > best_delta_h:
                best_delta_h = delta_h_count
                best_arg = chosen_index

        return best_delta_h + cls.bias, best_arg


# 暗言术毁
class ShadowWordRuin(SpellNoPoint):
    bias = -8
    keep_in_hand_bool = False

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        return cls.bias + sum([minion.heuristic_val
                               for minion in state.oppo_minions
                               if minion.attack >= 5]),


# 除奇致胜
class AgainstAllOdds(SpellNoPoint):
    bias = -9
    keep_in_hand_bool = False

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        return cls.bias + \
               sum([minion.heuristic_val
                    for minion in state.oppo_minions
                    if minion.attack % 2 == 1]) - \
               sum([minion.heuristic_val
                    for minion in state.my_minions
                    if minion.attack % 2 == 1]),


# 锈骑劫匪
class RuststeedRaider(MinionNoPoint):
    value = 3
    keep_in_hand_bool = False
    # TODO: 也许我可以为突袭随从专门写一套价值评判?


# 泰兰佛丁
class TaelanFordring(MinionNoPoint):
    value = 3
    keep_in_hand_bool = False


# 凯恩血蹄
class CairneBloodhoof(MinionNoPoint):
    value = 6
    keep_in_hand_bool = False


# 吃手手鱼
class MutanusTheDevourer(MinionNoPoint):
    value = 5
    keep_in_hand_bool = False


# 灵魂之镜
class SoulMirror(SpellNoPoint):
    wait_time = 5
    bias = -16
    keep_in_hand_bool = False

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        copy_number = min(7 - state.my_minion_num, state.oppo_minion_num)
        h_sum = 0
        for i in range(copy_number):
            h_sum += state.oppo_minions[i].heuristic_val

        return h_sum + cls.bias,


# 戈霍恩之血
class BloodOfGhuun(MinionNoPoint):
    value = 8
    keep_in_hand_bool = False

class ArcaneShot(SpellPointOppo):
    wait_time = 2
    # 加个bias,一是包含了消耗的水晶的代价，二是包含了消耗了手牌的代价
    bias = -2.5

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        best_oppo_index = -1
        best_delta_h = 0
        if state.oppo_hero.can_be_pointed_by_spell:
           best_delta_h = state.oppo_hero.delta_h_after_damage(2) + cls.bias

        for oppo_index, oppo_minion in enumerate(state.oppo_minions):
            if not oppo_minion.can_be_pointed_by_spell:
                continue
            temp_delta_h = oppo_minion.delta_h_after_damage(2) + cls.bias
            if temp_delta_h > best_delta_h:
                best_delta_h = temp_delta_h
                best_oppo_index = oppo_index

        return best_delta_h, best_oppo_index


    @classmethod
    def delta_h_after_direct(cls, action, state):
        index = action.hand_index
        del state.my_hand_cards[index]
        oppo_index = action.point_oppo
        state.pay_mana(1)  
        if oppo_index == -1:
            state.oppo_hero.get_damaged(2)
            return state.oppo_hero.delta_h_after_damage(2), [state]
        
        val = state.oppo_minions[oppo_index].delta_h_after_damage(2)
        if state.oppo_minions[oppo_index].get_damaged(2):
            del state.oppo_minions[oppo_index]
        return val, [state]
    
    @classmethod
    def get_all_actions(cls, state, index, is_in_hand):
        actions = []
        if not is_in_hand:
            return actions
        if state.my_last_mana < state.my_hand_cards[index].current_cost:
            return actions
        if state.oppo_hero.can_be_pointed_by_spell:
            action = strategy.Action()
            action.set_spell_atk_hero(state, index, 2)
            actions.append(action)
        for oppo_index, oppo_minion in enumerate(state.oppo_minions):
            if not oppo_minion.can_be_pointed_by_spell:
                continue
            action = strategy.Action()
            action.set_spell_atk_minon(state, index, oppo_index, 2)
            actions.append(action)
        return actions
        

#惩罚 -水晶（1：1） - 卡牌（1：1） - 被动（0.5）

#奖励 +过牌（1：1） + 冷冻（1：1）

# 爆炸陷阱
class BrandonKitkouski(SpellNoPoint):
   
    bias = -3
    
    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        global BrandonKitkouski_used_before
        print("in BrandonKitkouski BrandonKitkouski_used_before is ", BrandonKitkouski_used_before)
        if BrandonKitkouski_used_before == 0:
            BrandonKitkouski_used_before = 1;
            return 1000000,
        if BrandonKitkouski_used_before == 1:
            for entity in state.my_graveyard:
                if entity.name == "爆炸陷阱":
                    return cls.bias + sum([minion.delta_h_after_damage(2)
                               for minion in state.oppo_minions]) + state.oppo_hero.delta_h_after_damage(2),
            return -99999999,
        return cls.bias + sum([minion.delta_h_after_damage(2)
                               for minion in state.oppo_minions]) + state.oppo_hero.delta_h_after_damage(2),
    
    @classmethod
    def delta_h_after_direct(cls, action, state):
        index = action.hand_index
        if state.my_hand_cards[index].current_cost > state.my_last_mana:
            return -9999, [state]
        state.pay_mana(state.my_hand_cards[index].current_cost)
        
        val = cls.best_h_and_arg(state, 0)[0]
        if val == -99999999:
            return -9999, [state]
        del state.my_hand_cards[index]
        return val, [state]

    @classmethod
    def get_all_actions(cls, state, index, is_in_hand):
        if cls.best_h_and_arg(state, index)[0] ==  -99999999:
            return []
        return cls.get_all_actions_nopoint_cls(state, index, is_in_hand, 2)

#快速射击
class QuickShot(SpellPointOppo):
    wait_time = 2
    # 加个bias,一是包含了消耗的水晶的代价，二是包含了消耗了手牌的代价
    bias = -3

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        best_oppo_index = -1
        best_delta_h = 0
        if state.my_hand_card_num == 1:
            cls.value += 10
        if state.oppo_hero.can_be_pointed_by_spell:
           best_delta_h = state.oppo_hero.delta_h_after_damage(3) + cls.bias

        for oppo_index, oppo_minion in enumerate(state.oppo_minions):
            if not oppo_minion.can_be_pointed_by_spell:
                continue
            temp_delta_h = oppo_minion.delta_h_after_damage(3) + cls.bias
            if temp_delta_h > best_delta_h:
                best_delta_h = temp_delta_h
                best_oppo_index = oppo_index

        return best_delta_h, best_oppo_index

    @classmethod
    def delta_h_after_direct(cls, action, state):
        index = action.hand_index
        if state.my_hand_cards[index].current_cost > state.my_last_mana:
            return -9999, [state]
        state.pay_mana(state.my_hand_cards[index].current_cost)
        del state.my_hand_cards[index]
        add_val = 0
        if len(state.my_hand_cards) == 0:
            print("------------------------------------------------------------------------------------------------------------------------------------------")
            add_val = 999
        oppo_index = action.point_oppo
        if oppo_index == -1:
            val = state.oppo_hero.delta_h_after_damage(3) + add_val + cls.bias
            state.oppo_hero.get_damaged(3)
            return val, [state]
        
        val = state.oppo_minions[oppo_index].delta_h_after_damage(3) + add_val + cls.bias
        if state.oppo_minions[oppo_index].get_damaged(3):
            del state.oppo_minions[oppo_index]
        return val, [state]


    @classmethod
    def get_all_actions(cls, state, index, is_in_hand):
        actions = []
        if not is_in_hand:
            return actions
        if state.my_last_mana < state.my_hand_cards[index].current_cost:
            return actions
        if state.oppo_hero.can_be_pointed_by_spell:
            action = strategy.Action()
            action.set_spell_atk_hero(state, index, 3)
            actions.append(action)
        for oppo_index, oppo_minion in enumerate(state.oppo_minions):
            if not oppo_minion.can_be_pointed_by_spell:
                continue
            action = strategy.Action()
            action.set_spell_atk_minon(state, index, oppo_index, 3)
            actions.append(action)
        return actions
 
# 致命射击
class DeadlyShot(SpellNoPoint):
    bias = -5

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        if state.oppo_minion_num == 0:
            return -999, 
        return cls.bias + statistics.mean([minion.heuristic_val
                               for minion in state.oppo_minions]),

    @classmethod
    def delta_h_after_direct(cls, action, state):
        index = action.hand_index
        states = []
        values = cls.bias
        oppo_num = len(state.oppo_minions)
        if oppo_num == 0:
            return -9999, [state]
        for oppo_index, oppo_minion in enumerate(state.oppo_minions):
            statex = copy.deepcopy(state)
            statex.pay_mana(state.my_hand_cards[index].current_cost)
            val = statex.oppo_minions[oppo_index].heuristic_val
            del statex.oppo_minions[oppo_index]
            del statex.my_hand_cards[index]
            values += val
            states.append(statex)
        values /= oppo_num
        del state.my_hand_cards[index]
        return values, states
    
    @classmethod
    def get_all_actions(cls, state, index, is_in_hand):
        return cls.get_all_actions_nopoint_cls(state, index, is_in_hand, 3)


# 动物伙伴
class AnimalCompanion(SpellNoPoint):
    bias = -4
    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        return cls.bias + (10 + 9 + 7) / 3,

    @classmethod
    def delta_h_after_direct(cls, action, state):
        index = action.hand_index
        if state.my_last_mana < state.my_hand_cards[index].current_cost:
            return -999, [state]
        del state.my_hand_cards[index]
        states = []
        values = (6 + 5 + 3) / 3 + cls.bias
        import strategy_entity
        
        # s1 = strategy_entity.StrategyMinion(attack = 4, taunt = 1, max_health = 4)
        state1 = copy.deepcopy(state)
        s1 = strategy_entity.StrategyMinion(card_id = 'NEW1_032', zone = 'PLAY', zone_pos = state1.my_minion_num + 1,
                 current_cost = 3, overload = 0, is_mine = 1,
                 attack = 4, max_health = 4,
                 taunt = 1, exhausted = 1)
        state1.my_minions.append(s1)
        state1.pay_mana(3)
        # s2 = strategy_entity.StrategyMinion(attack = 4, rush = 1, max_health = 2)
        state2 = copy.deepcopy(state)
        s2 = strategy_entity.StrategyMinion(card_id = 'NEW1_034', zone = 'PLAY', zone_pos = state2.my_minion_num + 1,
                 current_cost = 3, overload = 0, is_mine = 1,
                 attack = 4, max_health = 2,
                 exhausted = 1)
        state2.my_minions.append(s2)
        state2.pay_mana(3)
        # s3 = strategy_entity.StrategyMinion(attack = 2, max_healt = 4)
        state3 = copy.deepcopy(state)
        s3 = strategy_entity.StrategyMinion(card_id = 'NEW1_033', zone = 'PLAY', zone_pos = state3.my_minion_num + 1,
                 current_cost = 3, overload = 0, is_mine = 1,
                 attack = 2, max_health = 4, exhausted = 1)
        state3.my_minions.append(s3)
        state3.pay_mana(3)
        states = [state1 ,state2, state3]
        return values, states
    
    @classmethod
    def get_all_actions(cls, state, index, is_in_hand):
        return cls.get_all_actions_nopoint_cls(state, index, is_in_hand, 3)

# 狼人渗透者
class WorgenInfiltrator(MinionNoPoint):
    value = 3 - 2
    keep_in_hand_bool = True

    @classmethod
    def delta_h_after_direct(cls, action, state):
        # if action.is_in_hand:
        #     index = action.hand_index
        #     state.oppo_minions.append(state.my_minions[index])
        #     del state.my_minions[index]
        #     return cls.value
        if action.is_in_hand:
            return cls.delta_h_after_direct_hand_no_point( action, state)
        if action.is_in_battle:
            return cls.delta_h_after_direct_cls( action, state)
    
    @classmethod
    def get_all_actions(cls, state, index, is_in_hand):
        if is_in_hand:
           return cls.get_all_actions_MinionNoPoint_inhand(state, index, is_in_hand)
        else:
            return cls.get_all_actions_MinionNoPoint_inbattle(state, index, is_in_hand)
        
# 荆棘谷猛虎
class Tiger(MinionNoPoint):
    value = 10 - 5 - 1 + 2
    keep_in_hand_bool = False

    @classmethod
    def delta_h_after_direct(cls, action, state):
        if action.is_in_hand:
            return cls.delta_h_after_direct_hand_no_point( action, state)
        if action.is_in_battle:
            return cls.delta_h_after_direct_cls( action, state)
    
    @classmethod
    def get_all_actions(cls, state, index, is_in_hand):
        if is_in_hand:
           return cls.get_all_actions_MinionNoPoint_inhand(state, index, is_in_hand)
        else:
            return cls.get_all_actions_MinionNoPoint_inbattle(state, index, is_in_hand)


#翡翠天爪枭 
class JadeSkyClawOwl(MinionNoPoint):
    value = 3 -2
    keep_in_hand_bool = True

    @classmethod
    def delta_h_after_direct(cls, action, state):
        if action.is_in_hand:
            return cls.delta_h_after_direct_hand_no_point( action, state)
        if action.is_in_battle:
            return cls.delta_h_after_direct_cls( action, state)
    
    @classmethod
    def get_all_actions(cls, state, index, is_in_hand):
        if is_in_hand:
           return cls.get_all_actions_MinionNoPoint_inhand(state, index, is_in_hand)
        else:
            return cls.get_all_actions_MinionNoPoint_inbattle(state, index, is_in_hand)

# 冰川裂片
class GlacialShard(MinionPointOppo):
    keep_in_hand_bool = True
    value = 3 - 2
    @classmethod
    def utilize_delta_h_and_arg(cls, state, hand_card_index):
        best_h = cls.value + state.oppo_hero.heuristic_val / 10
        best_oppo_index = -1

        for oppo_index, oppo_minion in enumerate(state.oppo_minions):
            if not oppo_minion.can_be_pointed_by_minion:
                continue

            delta_h = cls.value +  oppo_minion.heuristic_val / 2
            if delta_h > best_h:
                best_h = delta_h
                best_oppo_index = oppo_index

        return best_h, state.my_minion_num, best_oppo_index

    @classmethod
    def delta_h_after_direct(cls, action, state):
        if action.is_in_hand:
            res = cls.value
            if action.point_oppo != -1:
                res += state.oppo_minions[action.point_oppo].heuristic_val / 2
            state.pay_mana(state.my_hand_cards[action.hand_index].current_cost)
            state.my_hand_cards[action.hand_index].exhausted = 1
            state.my_minions.append(state.my_hand_cards[action.hand_index])
            del state.my_hand_cards[action.hand_index]
            return res, [state]
        if action.is_in_battle:
            return cls.delta_h_after_direct_cls( action, state)


    @classmethod
    def get_all_actions(cls, state, index, is_in_hand):
        if is_in_hand:
            point_index = cls.utilize_delta_h_and_arg(state, 0)[2]
            return cls.get_all_actions_MinionPoint_inhand(state, index, is_in_hand, point_index)
        #    return cls.delta_h_after_direct_hand_no_point(state, index, is_in_hand)
        else:
            return cls.get_all_actions_MinionNoPoint_inbattle(state, index, is_in_hand)

# 吸血蚊
class LifeDrinker(MinionNoPoint):
    value = 6 - 5
    keep_in_hand_bool = False

    @classmethod
    def utilize_delta_h_and_arg(cls, state, hand_card_index):
        if state.oppo_hero.health <= 15:
            cls.value += 1
        if state.my_hero.health <= 27:
            cls.value += 0.5
        if state.my_hero.health <= 15:
            cls.value += 1
        if state.my_hero.health <= 10:
            cls.value += 1
        if state.my_hero.health <= 5:
            cls.value += 1
        return cls.value, state.my_minion_num


    @classmethod
    def delta_h_after_direct(cls, action, state):
        if action.is_in_hand:
            return (cls.delta_h_after_direct_hand_no_point( action, state)[0] + cls.utilize_delta_h_and_arg(state, 0)[0]), [state]

        if action.is_in_battle:
            return cls.delta_h_after_direct_cls( action, state)
    
    @classmethod
    def get_all_actions(cls, state, index, is_in_hand):
        if is_in_hand:
           return cls.get_all_actions_MinionNoPoint_inhand(state, index, is_in_hand)
        else:
            return cls.get_all_actions_MinionNoPoint_inbattle(state, index, is_in_hand)
        


# 恐狼前锋
class DireWolfAlpha(MinionNoPoint):
    keep_in_hand_bool = True
    value = 4 - 3

    @classmethod
    def utilize_delta_h_and_arg(cls, state, hand_card_index):
        if state.my_minion_num == 1:
            cls.value += 1
        elif state.my_minion_num > 1:
            cls.value += 2
        return cls.value, state.my_minion_num - 1

    @classmethod
    def delta_h_after_direct(cls, action, state):
        if action.is_in_hand:
            return cls.delta_h_after_direct_hand_no_point( action, state)[0] + cls.utilize_delta_h_and_arg(state, 0)[0], [state]

        if action.is_in_battle:
            return cls.delta_h_after_direct_cls( action, state)
    
    @classmethod
    def get_all_actions(cls, state, index, is_in_hand):
        if is_in_hand:
           return cls.get_all_actions_MinionNoPoint_inhand(state, index, is_in_hand)
        else:
            return cls.get_all_actions_MinionNoPoint_inbattle(state, index, is_in_hand)

# 战利品贮藏者
class LootHoarder(MinionNoPoint):
    keep_in_hand_bool = True
    value = 3 - 3

    @classmethod
    def utilize_delta_h_and_arg(cls, state, hand_card_index):
        cls.value += (10 - state.my_hand_card_num) / 2
        return cls.value, state.my_minion_num

    @classmethod
    def delta_h_after_direct(cls, action, state):
        if action.is_in_hand:
            return (cls.delta_h_after_direct_hand_no_point( action, state)[0] + cls.utilize_delta_h_and_arg(state, 0)[0] / 2), [state]

        if action.is_in_battle:
            return (cls.delta_h_after_direct_cls( action, state)[0] + cls.utilize_delta_h_and_arg(state, 0)[0] / 2), [state]
    
    @classmethod
    def get_all_actions(cls, state, index, is_in_hand):
        if is_in_hand:
           return cls.get_all_actions_MinionNoPoint_inhand(state, index, is_in_hand)
        else:
            return cls.get_all_actions_MinionNoPoint_inbattle(state, index, is_in_hand)

# 精灵龙
class FaerieDragon(MinionNoPoint):
    keep_in_hand_bool = True
    value = 5 - 3

    @classmethod
    def utilize_delta_h_and_arg(cls, state, hand_card_index):
        if state.oppo_hero_power.name == "火球术" or state.oppo_hero_power.name == "次级治疗术" or state.oppo_hero_power.name == "生命分流":
            cls.value += 1
        return cls.value, state.my_minion_num

    @classmethod
    def delta_h_after_direct(cls, action, state):
        if action.is_in_hand:
            return (cls.delta_h_after_direct_hand_no_point( action, state)[0] + cls.utilize_delta_h_and_arg(state, 0)[0]), [state]

        if action.is_in_battle:
            return cls.delta_h_after_direct_cls( action, state)
    
    @classmethod
    def get_all_actions(cls, state, index, is_in_hand):
        if is_in_hand:
           return cls.get_all_actions_MinionNoPoint_inhand(state, index, is_in_hand)
        else:
            return cls.get_all_actions_MinionNoPoint_inbattle(state, index, is_in_hand)

# 异教低阶牧师
class CultNeophyte(MinionNoPoint):
    keep_in_hand_bool = True
    value = 5 - 3

    @classmethod
    def utilize_delta_h_and_arg(cls, state, hand_card_index):
        if state.my_total_mana >= 3:
            cls.value += 0.5
        if state.oppo_hero_power.name == "火球术" or state.oppo_hero_power.name == "次级治疗术" or state.oppo_hero_power.name == "生命分流":
            cls.value += 0.5
        return cls.value, state.my_minion_num
    
    @classmethod
    def delta_h_after_direct(cls, action, state):
        if action.is_in_hand:
            return (cls.delta_h_after_direct_hand_no_point( action, state)[0] + cls.utilize_delta_h_and_arg(state, 0)[0]), [state]

        if action.is_in_battle:
            return cls.delta_h_after_direct_cls( action, state)
    
    @classmethod
    def get_all_actions(cls, state, index, is_in_hand):
        if is_in_hand:
           return cls.get_all_actions_MinionNoPoint_inhand(state, index, is_in_hand)
        else:
            return cls.get_all_actions_MinionNoPoint_inbattle(state, index, is_in_hand)

# 碧蓝幼龙
class BlueDrogen(MinionNoPoint):
    value = 10 - 6
    keep_in_hand_bool = False

    @classmethod
    def utilize_delta_h_and_arg(cls, state, hand_card_index):
        cls.value += (10 - state.my_hand_card_num) / 2
        return cls.value, state.my_minion_num

    @classmethod
    def delta_h_after_direct(cls, action, state):
        if action.is_in_hand:
            return (cls.delta_h_after_direct_hand_no_point( action, state)[0] + cls.utilize_delta_h_and_arg(state, 0)[0]), [state]

        if action.is_in_battle:
            return cls.delta_h_after_direct_cls( action, state)
    
    @classmethod
    def get_all_actions(cls, state, index, is_in_hand):
        if is_in_hand:
           return cls.get_all_actions_MinionNoPoint_inhand(state, index, is_in_hand)
        else:
            return cls.get_all_actions_MinionNoPoint_inbattle(state, index, is_in_hand)
    


############################################################
# 烈焰喷泉
class FlamingFountain(SpellPointOppo):
    wait_time = 2
    # 加个bias,一是包含了消耗的水晶的代价，二是包含了消耗了手牌的代价
    bias = -2

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        best_oppo_index = -1
        best_delta_h = 0
        if state.oppo_hero.can_be_pointed_by_spell:
           best_delta_h = state.oppo_hero.delta_h_after_damage(2) + cls.bias

        for oppo_index, oppo_minion in enumerate(state.oppo_minions):
            if not oppo_minion.can_be_pointed_by_spell:
                continue
            temp_delta_h = oppo_minion.delta_h_after_damage(2) + cls.bias
            if temp_delta_h > best_delta_h:
                best_delta_h = temp_delta_h
                best_oppo_index = oppo_index

        return best_delta_h, best_oppo_index
    
# 电火花
class spark(SpellPointOppo):
    wait_time = 2
    # 加个bias,一是包含了消耗的水晶的代价，二是包含了消耗了手牌的代价
    bias = -2

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        best_oppo_index = -1
        best_delta_h = 0
        temp_opoo_minion = None
        for oppo_index, oppo_minion in enumerate(state.oppo_minions):
            temp_opoo_minion = oppo_minion
            if not oppo_minion.can_be_pointed_by_spell:
                continue
            temp_delta_h = oppo_minion.delta_h_after_damage(1) + cls.bias
            if temp_opoo_minion != None:
                temp_delta_h += temp_opoo_minion.delta_h_after_damage(1) + cls.bias
            try:
                temp_delta_h += state.oppo_minions[oppo_index + 1].delta_h_after_damage(1) + cls.bias
            except:
                if temp_delta_h > best_delta_h:
                    best_delta_h = temp_delta_h
                    best_oppo_index = oppo_index

            if temp_delta_h > best_delta_h:
                best_delta_h = temp_delta_h
                best_oppo_index = oppo_index

        return best_delta_h, best_oppo_index

IceBarrier_used = 0
# 寒冰护体
class IceBarrier(SpellNoPoint):
    bias = -4
    bias += 8
    
    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        global IceBarrier_used
        if IceBarrier_used == 1:
            return -11111,
        if IceBarrier_used == 0:
            IceBarrier_used = 1
        if state.my_hero.health <= 20:
            return cls.bias + 1,
        if state.my_hero.health <= 15:
            return cls.bias + 1.5,
        if state.my_hero.health <= 10:
            return cls.bias + 3,
        if state.my_hero.health <= 5:
            return cls.bias + 990,
        return cls.bias, 

# 焦油蠕行者
class TarCreeper(MinionNoPoint):
    value = 7
    keep_in_hand_bool = True

    @classmethod
    def utilize_delta_h_and_arg(cls, state, hand_card_index):
        if state.my_minion_num > 0:
             return cls.value + 0.5, state.my_minion_num
        if state.my_hero.health <= 15:
            return cls.value + 1.5, state.my_minion_num
        if state.my_hero.health <= 10:
            return cls.value + 3, state.my_minion_num
        if state.my_hero.health <= 5:
            return cls.value + 8, state.my_minion_num
        return cls.value, state.my_minion_num

# 秘法智力
class Esotericintelligence(SpellNoPoint):
    bias = -4
    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        best_oppo_index = -1
        best_delta_h = 0
        best_delta_h += cls.bias + (7 - state.my_hand_card_num) * 1.8

        return best_delta_h, 

# 苦痛侍僧
class PainfulServantMonk(MinionNoPoint):
    value = 4
    keep_in_hand_bool = True

    @classmethod
    def utilize_delta_h_and_arg(cls, state, hand_card_index):
        
        return cls.value + (8 - state.my_hand_card_num) * 1.8, state.my_minion_num
    
#森金御盾大师
class MasterSenjinYudun(MinionNoPoint):
    value = 9.5
    keep_in_hand_bool = True

    @classmethod
    def utilize_delta_h_and_arg(cls, state, hand_card_index):
        if state.my_minion_num >= 1:
            cls.value += 1
        if state.my_hero.health <= 15:
            return cls.value + 1.5, state.my_minion_num
        if state.my_hero.health <= 10:
            return cls.value + 3, state.my_minion_num
        if state.my_hero.health <= 5:
            return cls.value + 20, state.my_minion_num
        return cls.value, state.my_minion_num

# 火球术
class FireBall(SpellPointOppo):
    wait_time = 2
    # 加个bias,一是包含了消耗的水晶的代价，二是包含了消耗了手牌的代价
    bias = -5

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        best_oppo_index = -1
        best_delta_h = 0
        if state.oppo_hero.can_be_pointed_by_spell:
           best_delta_h = state.oppo_hero.delta_h_after_damage(6) + cls.bias

        for oppo_index, oppo_minion in enumerate(state.oppo_minions):
            if not oppo_minion.can_be_pointed_by_spell:
                continue
            temp_delta_h = oppo_minion.delta_h_after_damage(6) + cls.bias
            if temp_delta_h > best_delta_h:
                best_delta_h = temp_delta_h
                best_oppo_index = oppo_index

        return best_delta_h, best_oppo_index

# 暴风雪
class SnowStorm(SpellNoPoint):
    bias = -7
    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        return cls.bias + sum([minion.delta_h_after_damage(2) + 1
                               for minion in state.oppo_minions]),

# 火源传送门
class FireSourceTransmissionGate(SpellPointOppo):
    wait_time = 2
    # 加个bias,一是包含了消耗的水晶的代价，二是包含了消耗了手牌的代价
    bias = -8 + 10

    @classmethod
    def best_h_and_arg(cls, state, hand_card_index):
        best_oppo_index = -1
        best_delta_h = 0
        if state.oppo_hero.can_be_pointed_by_spell:
           best_delta_h = state.oppo_hero.delta_h_after_damage(6) + cls.bias

        for oppo_index, oppo_minion in enumerate(state.oppo_minions):
            if not oppo_minion.can_be_pointed_by_spell:
                continue
            temp_delta_h = oppo_minion.delta_h_after_damage(6) + cls.bias
            if temp_delta_h > best_delta_h:
                best_delta_h = temp_delta_h
                best_oppo_index = oppo_index

        return best_delta_h, best_oppo_index
