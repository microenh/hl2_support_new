from enum import Enum, auto

EVENT = '<<EVENT>>'

class ThetisEvent(Enum):

    QUIT = auto()
    TURN = auto()
    BUTTON = auto()
    FREQA = auto()
    STEP = auto()

if __name__ == '__main__':
    t = ThetisEvent
