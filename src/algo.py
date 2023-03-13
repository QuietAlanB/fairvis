# `ro_*` indicates that external modules may only read the variable.
# `wo_*` indicates, conversely, a write-only value for external use.
ro_display_ready = False
wo_display_done = False
ro_iterations = 0
ro_comparisons = 0
ro_swaps = 0

# for internal use only.
def _algo_init():
    global ro_display_ready
    global wo_display_done
    global ro_iterations
    global ro_checks
    global ro_swaps
    
    ro_display_ready = False
    wo_display_done = False
    ro_iterations = 0
    ro_comparisons = 0
    ro_swaps = 0

# for internal use only.
def _algo_compare(a, b):
    global ro_comparisons

    ro_comparisons += 1
    return max(a, b)

# for internal use only.
def _algo_swap(a, b):
    global ro_swaps

    tmp = a
    a = b
    b = tmp
    ro_swaps += 1

def bubble_sort(ilist):
    global ro_display_ready
    global wo_display_done
    global ro_iterations
    
    _algo_init()

    for _ in ilist:
        for i in range(len(ilist) - 1):
            if _algo_compare(ilist[i - 1], ilist[i]) == ilist[i - 1]:
                _algo_swap(ilist[i - 1], ilist[i])
                
            ro_iterations += 1
            ro_display_ready = True
            while not wo_display_done:
                continue
