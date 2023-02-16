#!/usr/bin/env python3

import cProfile as profile
import pstats
from pstats import SortKey

from exercise_2 import simulate

output = "./exercise_2.pstats"
profile.run("simulate('389125467', max_value=1000000, stop=1000)", output)

p = pstats.Stats(output)
p.sort_stats(SortKey.CUMULATIVE).print_stats(10)
