from card.basic_card import Coin
from card.standard_card import *
from card.classic_card import *
from card.hero_power_card import *

ID2CARD_DICT = {
    # 特殊项-幸运币
    "COIN": Coin,

    # 英雄技能
    "TOTEMIC_CALL": TotemicCall,
    "LESSER_HEAL": LesserHeal,
    "BALLISTA_SHOT": BallistaShot,

    # 标准模式-牧师
    "YOP_032": ArmorVendor,  # 护甲商贩
    "CORE_CS1_130": HolySmite,  # 神圣惩击
    "CS1_130": HolySmite,  # 神圣惩击
    "SCH_250": WaveOfApathy,  # 倦怠光波
    "BT_715": BonechewerBrawler,  # 噬骨殴斗者
    "CORE_EX1_622": ShadowWordDeath,  # 暗言术：灭
    "EX1_622": ShadowWordDeath,  # 暗言术：灭
    "BT_257": Apotheosis,  # 神圣化身
    "BAR_026": DeathsHeadCultist,  # 亡首教徒
    "BAR_311": DevouringPlague,  # 噬灵疫病
    "BT_730": OverconfidentOrc,  # 狂傲的兽人
    "CORE_CS1_112": HolyNova,  # 神圣新星
    "CS1_112": HolyNova,  # 神圣新星
    "YOP_006": Hysteria,  # 狂乱
    "CORE_EX1_197": ShadowWordRuin,  # 暗言术：毁
    "EX1_197": ShadowWordRuin,  # 暗言术：毁
    "WC_014": AgainstAllOdds,  # 除奇致胜
    "BT_720": RuststeedRaider,  # 锈骑劫匪
    "CS3_024": TaelanFordring,  # 泰兰·弗丁
    "EX1_110": CairneBloodhoof,  # 凯恩·血蹄
    "CORE_EX1_110": CairneBloodhoof,  # 凯恩·血蹄
    "WC_030": MutanusTheDevourer,  # 吞噬者穆坦努斯
    "BT_198": SoulMirror,  # 灵魂之镜
    "DMF_053": BloodOfGhuun,  # 戈霍恩之血


    # 标准模式-猎人
    "CORE_DS1_185" : ArcaneShot, # 奥数射击
    "CORE_EX1_610" : BrandonKitkouski, # 爆炸陷阱
    "CORE_BRM_013" : QuickShot, # 快速射击
    "CORE_EX1_617" : DeadlyShot, # 致命射击
    "CORE_NEW1_031" : AnimalCompanion, # 动物伙伴
    "CORE_EX1_010" : WorgenInfiltrator, # 狼人渗透者
    "CORE_UNG_205" : GlacialShard, # 冰川裂片
    "CORE_GIL_622" : LifeDrinker, # 吸血蚊
    "CORE_EX1_162" : DireWolfAlpha, # 恐狼前锋
    "CORE_EX1_096" : LootHoarder, # 战利品贮藏者
    "CORE_NEW1_023" : FaerieDragon, # 精灵龙
    "CORE_SCH_713" : CultNeophyte, # 异教低阶牧师
    "CORE_EX1_284" : BlueDrogen, # 碧蓝幼龙
    "CORE_EX1_028" : Tiger, #荆棘谷猛虎
    "CS3_037" : JadeSkyClawOwl, #翡翠天爪枭 

    #标准模式-法师
    "CORE_UNG_018" : FlamingFountain, # 烈焰喷泉
    "CORE_BOT_453" : spark, # 电火花
    "CORE_EX1_289" : IceBarrier, # 寒冰护体
    "CORE_UNG_928" : TarCreeper, # 焦油蠕行者
    "CORE_CS2_023" : Esotericintelligence, #秘法智力
    "CORE_EX1_007" : PainfulServantMonk, #苦痛侍僧
    "CORE_CS2_179" : MasterSenjinYudun, #森金御盾大师
    "CORE_CS2_029" : FireBall, # 火球术
    "CORE_CS2_028" : SnowStorm, # 暴风雪
    "CORE_KAR_076" : FireSourceTransmissionGate, # 火源传送门


    # 经典模式
    "VAN_CS2_042": FireElemental,
    "VAN_EX1_562": Onyxia,
    "VAN_EX1_248": FeralSpirit,
    "VAN_EX1_246": Hex,
    "VAN_EX1_238": LightingBolt,
    "VAN_EX1_085": MindControlTech,
    "VAN_EX1_284": AzureDrake,
    "VAN_EX1_259": LightningStorm,
    "VAN_CS2_189": ElvenArcher,
    "VAN_CS2_117": EarthenRingFarseer,
    "VAN_EX1_097": Abomination,
    "VAN_NEW1_021": DoomSayer,
    "VAN_NEW1_041": StampedingKodo,
    "VAN_EX1_590": BloodKnight,
    "VAN_EX1_247": StormforgedAxe,
}
