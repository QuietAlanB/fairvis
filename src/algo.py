# `ro_*` indicates that external modules may only read the variable.
# `wo_*` indicates, conversely, a write-only value for external use.
ro_display_ready = False
wo_display_done = False
ro_iterations = 0
ro_comparisons = 0
ro_swaps = 0

# since the algorithms are meant to run in a seperate thread, it is necessary to
# create a mechanism for requesting their termination.
# in order to terminate the running algorithm thread, set this to `True`.
wo_terminate = False

# for internal use only.
def _algo_init():
        global ro_display_ready
        global wo_display_done
        global ro_iterations
        global ro_comparisons
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
def _algo_greater(a, b):
        return _algo_compare(a, b) == a

# for internal use only.
def _algo_swap(lst, ind_a, ind_b):
        global ro_swaps

        tmp = lst[ind_a]
        lst[ind_a] = lst[ind_b]
        lst[ind_b] = tmp
        ro_swaps += 1

def bubble_sort(lst):
        global ro_display_ready
        global wo_display_done
        global ro_iterations
        global wo_terminate
        
        _algo_init()
        
        for _ in lst:
                for i in range(1, len(lst)):
                        ro_iterations += 1

                        if wo_terminate:
                                wo_terminate = False
                                return
                        
                        if _algo_greater(lst[i - 1], lst[i]):
                                _algo_swap(lst, i - 1, i)

                                ro_display_ready = True
                                while not wo_display_done:
                                        continue
                                ro_display_ready = False
                                wo_display_done = False

def bogo_sort(lst):
        pass