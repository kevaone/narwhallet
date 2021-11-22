from enum import IntEnum


class EWalletKind(IntEnum):
    NORMAL = 0
    READ_ONLY = 1
    SEED_PROTECTED = 2
    WATCH = 3
