
from pymjengine.engine.tile import Tile
from pymjengine.engine.mj_constants import MJConstants




class Player:

    ACTION_TAKE_STR = "TAKE"
    ACTION_CHOW_STR = "CHOW"
    ACTION_PONG_STR = "PONG"
    ACTION_KONG_STR = "KONG"
    ACTION_PLAY_STR = "PLAY"
    ACTION_TIN_STR = "TIN"
    ACTION_HU_STR = "HU" 
    ACTION_NONE_STR = "NONE" 

    def __init__(self, uuid, name="No Name"):
        self.name = name
        self.uuid = uuid
        self.ask_act = MJConstants.Action.NONE
        self.is_hu = False
        self.active_info = False
        self.hand_tiles = []
        self.action_histories = []


    def add_hand_tile(self, tile):
        self.hand_tiles += [tile]

    def add_hand_tiles(self, tiles):
        self.hand_tiles += tiles

    def clear_hand_tiles(self):
        self.hand_tiles = []

    def is_hu(self):
        return self.is_hu

    def set_hu(self, bHu):
        self.is_hu = bHu

    def is_active(self):
        return self.active_info

    def set_active(self, bActive):
        self.active_info = bActive
    
    def set_ask_act(self, act):
        self.ask_act = act
        
    def get_ask_act(self):
        #print("get_ask_act:{}".format(self.ask_act))
        return self.ask_act

    def add_action_history(self, kind ):
        history = None
        history = self.__get_history_node(kind)
        history = self.__add_uuid_on_history(history)
        self.action_histories.append(history)

    def clear_action_histories(self):
        self.action_histories = []

    def clear_active_info(self):
        self.active_info = False

    def get_handtile_ids(self):
        tile_ids = [tile.to_id() for tile in self.hand_tiles]
        return [tile_ids]

    def serialize(self):
        tile_ids = [tile.to_id() for tile in self.hand_tiles]
        return [
            self.name, self.uuid, self.hand_tiles, tile_ids,\
            self.action_histories[::],self.active_info
        ]

    @classmethod
    def deserialize(self, serial):
        tile_ids = [Tile.from_id(tid) for tid in serial[3]]
        player = self(serial[1], serial[0])
        if len(tile_ids)!=0: player.add_hand_tiles(tile_ids)
        player.action_histories = serial[4]
        player.active_info = serial[5]
        return player


    def __get_history_node(self, kind):
        if kind == MJConstants.Action.TAKE:
            return { "action" : self.ACTION_TAKE_STR }
        elif kind == MJConstants.Action.CHOW:
            return { "action" : self.ACTION_CHOW_STR }
        elif kind == MJConstants.Action.PONG:
            return { "action" : self.ACTION_PONG_STR }
        elif kind == MJConstants.Action.KONG:
            return { "action" : self.ACTION_KONG_STR }
        elif kind == MJConstants.Action.PLAY:
            return { "action" : self.ACTION_PLAY_STR }
        elif kind == MJConstants.Action.TIN:
            return { "action" : self.ACTION_TIN_STR }
        elif kind == MJConstants.Action.HU:
            return { "action" : self.ACTION_HU_STR }
        else:
            return { "action" : self.ACTION_NONE_STR }
 

    def __add_uuid_on_history(self, history):
        history["uuid"] = self.uuid
        return history
