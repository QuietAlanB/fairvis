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

# upon `_algo_render()`, the main thread must render the current state of the
# list being sorted.
# in order to display changes in state (swaps, comparisons), it must look into
# these lists and use the info accordingly.
# upon writing `True` to `wo_display_done`, these are cleared.
ro_display_swap_queue = []
ro_display_cmp_queue = []

def _algo_init():
        global ro_display_ready
        global wo_display_done
        global ro_iterations
        global ro_comparisons
        global ro_swaps
        global ro_display_swap_queue
        global ro_display_cmp_queue
        
        ro_display_ready = False
        wo_display_done = False
        ro_iterations = 0
        ro_comparisons = 0
        ro_swaps = 0
        ro_display_swap_queue = []
        ro_display_cmp_queue = []

def _algo_compare(lst, ind_a, ind_b):
        global ro_comparisons
        global ro_display_cmp_queue

        ro_comparisons += 1
        ro_display_cmp_queue.append((ind_a, ind_b))
        return max(lst[ind_a], lst[ind_b])

def _algo_greater(lst, ind_lhs, ind_rhs):
        cmp = _algo_compare(lst, ind_lhs, ind_rhs)
        return cmp == lst[ind_lhs] and cmp != lst[ind_rhs]

def _algo_greater_equal(lst, ind_lhs, ind_rhs):
        return _algo_compare(lst, ind_lhs, ind_rhs) == lst[ind_lhs]

def _algo_render():
        global ro_display_ready
        global wo_display_done
        global ro_display_cmp_queue
        global ro_display_swap_queue
        
        ro_display_ready = True
        
        while not wo_display_done:
                continue
        
        ro_display_ready = False
        wo_display_done = False

        ro_display_cmp_queue.clear()
        ro_display_swap_queue.clear()

def _algo_swap(lst, ind_a, ind_b):
        global ro_swaps
        global ro_display_swap_queue

        tmp = lst[ind_a]
        lst[ind_a] = lst[ind_b]
        lst[ind_b] = tmp
        ro_swaps += 1
        ro_display_swap_queue.append((ind_a, ind_b))

def bubble_sort(lst):
        global ro_iterations
        global wo_terminate
        
        _algo_init()
        
        for _ in lst:
                for i in range(1, len(lst)):
                        ro_iterations += 1
                        if wo_terminate:
                                wo_terminate = False
                                return
                        
                        if _algo_greater(lst, i - 1, i):
                                _algo_swap(lst, i - 1, i)
                                
                        _algo_render()

def insertion_sort(lst):
        global ro_iterations
        global wo_terminate

        _algo_init()

        for i, _ in enumerate(lst):
                for j in range(i, 0, -1):
                        ro_iterations += 1
                        if wo_terminate:
                                wo_terminate = False
                                return
                        
                        if _algo_greater(lst, j - 1, j):
                                _algo_swap(lst, j - 1, j)
                                
                        _algo_render()

def gnome_sort(lst):
        global ro_iterations
        global wo_terminate

        _algo_init()

        pos = 0
        while pos < len(lst):
                ro_iterations += 1
                if wo_terminate:
                        wo_terminate = False
                        return
                
                if pos == 0 or _algo_greater_equal(lst, pos, pos - 1):
                        pos += 1
                else:
                        _algo_swap(lst, pos, pos - 1)
                        pos -= 1

                _algo_render()
