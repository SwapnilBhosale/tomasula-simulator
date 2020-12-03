from enum import Enum


class ScoreBoardStage(Enum):
    FETCH = 0
    ISSUE = 1
    READ = 2
    EXECUTE = 3
    WRITE = 4
