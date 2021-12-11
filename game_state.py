from enum import auto, Enum


#lower on the list is higher in render stack
#CORPSE at lowest level
class GameState(Enum):
    LOOP = auto()
    PONDER = auto()
