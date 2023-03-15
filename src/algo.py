import math
import numpy
import pygame

# `ro_*` indicates that external modules may only read the variable.
# `wo_*` indicates, conversely, a write-only value for external use.
ro_display_ready = False
wo_display_done = False
ro_comparisons = 0
ro_swaps = 0
ro_algo_done = False

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
        global ro_comparisons
        global ro_swaps
        global ro_algo_done
        global ro_display_swap_queue
        global ro_display_cmp_queue
        global ro_verify_max_correct
        
        ro_display_ready = False
        wo_display_done = False
        ro_comparisons = 0
        ro_swaps = 0
        ro_algo_done = False
        ro_display_swap_queue.clear()
        ro_display_cmp_queue.clear()
        ro_verify_max_correct = 0

def _algo_play_sound(lst, ind):
        buffer = numpy.cos(2 * numpy.pi * numpy.arange(0, 4410, 0.1) * (600 + lst[ind] / max(lst) * 700) / 4410).astype(numpy.float32)
        sound = pygame.mixer.Sound(buffer)
        sound.play(0, 10)

def _algo_play_verify_sound(lst, ind):
        buffer = 0.5 * numpy.cos(8 * numpy.pi * numpy.arange(0, 4410, 0.1) * (600 + lst[ind] / max(lst) * 700) / 4410).astype(numpy.float32)
        sound = pygame.mixer.Sound(buffer)
        sound.play(0, 10)

def _algo_verify(lst):
        global ro_verify_max_correct

        for i in range(1, len(lst)):
                _algo_play_verify_sound(lst, i)
                if lst[i - 1] > lst[i]:
                        return
                ro_verify_max_correct += 1
                _algo_render()
        
def _algo_compare(lst, ind_a, ind_b):
        global ro_comparisons
        global ro_display_cmp_queue

        ro_comparisons += 1
        ro_display_cmp_queue.append((ind_a, ind_b))
        _algo_play_sound(lst, ind_a)
        _algo_play_sound(lst, ind_b)
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
        global wo_terminate
        global ro_algo_done
        
        _algo_init()
        
        for i, _ in enumerate(lst):
                for j in range(1, len(lst) - i):
                        if wo_terminate:
                                wo_terminate = False
                                return
                        
                        if _algo_greater(lst, j - 1, j):
                                _algo_swap(lst, j - 1, j)
                                
                        _algo_render()
        ro_algo_done = True
        _algo_verify(lst)

def insertion_sort(lst):
        global wo_terminate
        global ro_algo_done

        _algo_init()

        for i, _ in enumerate(lst):
                for j in range(i, 0, -1):
                        if wo_terminate:
                                wo_terminate = False
                                return
                        
                        if _algo_greater(lst, j - 1, j):
                                _algo_swap(lst, j - 1, j)
                                
                        _algo_render()
        ro_algo_done = True
        _algo_verify(lst)

def gnome_sort(lst):
        global wo_terminate
        global ro_algo_done

        _algo_init()

        pos = 0
        while pos < len(lst):
                if wo_terminate:
                        wo_terminate = False
                        return
                
                if pos == 0 or _algo_greater_equal(lst, pos, pos - 1):
                        pos += 1
                else:
                        _algo_swap(lst, pos, pos - 1)
                        pos -= 1

                _algo_render()
        ro_algo_done = True
        _algo_verify(lst)

def selection_sort(lst):
        global wo_terminate
        global ro_algo_done

        _algo_init()

        for i in range(len(lst) - 1):
                smallest = i
                for j in range(i + 1, len(lst)):
                        if wo_terminate:
                                wo_terminate = False
                                return

                        if _algo_greater(lst, smallest, j):
                                smallest = j
                        
                        _algo_render()
                        
                _algo_swap(lst, i, smallest)
                _algo_render()
        ro_algo_done = True
        _algo_verify(lst)

def comb_sort(lst):
        global wo_terminate
        global ro_algo_done

        _algo_init()

        gap = len(lst)
        shrink = 1.2
        sorted = False
        while not sorted:
                gap = math.floor(gap / shrink)
                if gap <= 1:
                        gap = 1
                        sorted = True
                for i in range(len(lst) - gap):
                        if wo_terminate:
                                wo_terminate = False
                                return
                        
                        sm = gap + i
                        if _algo_greater(lst, i, sm):
                                _algo_swap(lst, i, sm)
                                
                        _algo_render()
        ro_algo_done = True
        _algo_verify(lst)
