import random
import numpy as np

SEED = 42

# Backwards-compatible alias used by some modules
RANDOM_SEED = SEED

DEFAULT_COUNTRY_ID = 1

# Pattern 1

CASH_STRUCTURING_ACCOUNTS = 20

MIN_STRUCTURING_TXNS = 6
MAX_STRUCTURING_TXNS = 8

MIN_STRUCTURING_AMOUNT = 150000
MAX_STRUCTURING_AMOUNT = 199999

STRUCTURING_WINDOW_HOURS = 72

# Pattern 2

LATE_NIGHT_ACCOUNTS = 30

MIN_LATE_NIGHT_TXNS = 2
MAX_LATE_NIGHT_TXNS = 4

MIN_LATE_NIGHT_AMOUNT = 500000
MAX_LATE_NIGHT_AMOUNT = 2000000

# ============================================================
# Pattern 3 : Account Takeover
# ============================================================

ACCOUNT_TAKEOVER_ACCOUNTS = 25

MIN_ACCOUNT_TAKEOVER_TXNS = 1
MAX_ACCOUNT_TAKEOVER_TXNS = 3

MIN_ACCOUNT_TAKEOVER_AMOUNT = 300000
MAX_ACCOUNT_TAKEOVER_AMOUNT = 1500000

random.seed(SEED)
np.random.seed(SEED)

# ============================================================
# Pattern 6 : Dormant Account Reactivation
# ============================================================

DORMANT_REACTIVATION_ACCOUNTS = 20

MIN_DORMANT_TXNS = 2
MAX_DORMANT_TXNS = 4

MIN_DORMANT_AMOUNT = 250000
MAX_DORMANT_AMOUNT = 1000000

MIN_DORMANT_DAYS = 90
MAX_DORMANT_DAYS = 180