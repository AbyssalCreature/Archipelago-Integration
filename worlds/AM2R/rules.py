import itertools
from typing import Union
from BaseClasses import MultiWorld, CollectionState
from .options import MetroidsRequired, MetroidsAreChecks, get_option_value


class AM2RLogic:
    player: int

    def __init__(self, world: MultiWorld, player: int):
        self.player = player

    def AM2R_can_bomb(self, state: CollectionState) -> bool:
        return state.has_any({'Bombs', 'Power Bombs'}, self.player)

    def AM2R_can_jump(self, state: CollectionState) -> bool:
        return state.has_any({'Hi Jump', 'Space Jump', 'Bombs'}, self.player)

    def AM2R_can_fly(self, state: CollectionState) -> bool:
        return state.has_any({'Bombs', 'Space Jump'}, self.player)

    def AM2R_can_spider(self, state: CollectionState) -> bool:
        return state.has('Spiderball', self.player) \
            or self.AM2R_can_fly(state)

    def AM2R_can_schmove(self, state: CollectionState) -> bool:
        return self.AM2R_can_spider(state) \
            or state.has('Hi Jump', self.player)

    def AM2R_has_ballspark(self, state: CollectionState) -> bool:
        return state.has_all({'Speed Booster', 'Spring Ball'}, self.player)

    def AM2R_can_down(self, state: CollectionState) -> bool:
        amount = get_option_value(MultiWorld, self.player, "MetroidsRequired")

        if MetroidsAreChecks == MetroidsAreChecks.option_exclude_A6 or MetroidsAreChecks.option_include_A6:
            return state.has("Metroid", self.player, amount) \
                and state.has_all({"Speed Booster", "Ice Beam", "Super Missile", "Screw Attack"}, self.player) \
                and self.AM2R_can_fly(state) and self.AM2R_can_bomb(state)
        else:
            return state.has_all({"Speed Booster", "Ice Beam", "Super Missile", "Screw Attack"}, self.player) \
                and self.AM2R_can_fly(state) and self.AM2R_can_bomb(state)

    def AM2R_can_lab(self, state: CollectionState) -> bool:
        amount = get_option_value(MultiWorld, self.player, "MetroidsRequired")

        if MetroidsAreChecks == MetroidsAreChecks.option_include_A6:
            amount += 5
            return state.has("Metroid", self.player, amount) \
                and state.has_all({"Speed Booster", "Ice Beam", "Super Missile", "Screw Attack"}, self.player) \
                and self.AM2R_can_fly(state) and self.AM2R_can_bomb(state)
        elif MetroidsAreChecks == MetroidsAreChecks.option_exclude_A6:
            return state.has("Metroid", self.player, amount) \
                and state.has_all({"Speed Booster", "Ice Beam", "Super Missile", "Screw Attack"}, self.player) \
                and self.AM2R_can_fly(state) and self.AM2R_can_bomb(state)
        else:
            return state.has_all({"Speed Booster", "Ice Beam", "Super Missile", "Screw Attack"}, self.player) \
                and self.AM2R_can_fly(state) and self.AM2R_can_bomb(state)