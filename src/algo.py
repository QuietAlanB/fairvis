import math
import numpy
import pygame
import copy

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
ro_display_arr_queue = []

def _algo_init():
        global ro_display_ready
        global wo_display_done
        global ro_comparisons
        global ro_swaps
        global ro_algo_done
        global ro_display_swap_queue
        global ro_display_cmp_queue
        global ro_display_arr_queue
        global ro_verify_max_correct
        
        ro_display_ready = False
        wo_display_done = False
        ro_comparisons = 0
        ro_swaps = 0
        ro_algo_done = False
        ro_display_swap_queue.clear()
        ro_display_cmp_queue.clear()
        ro_display_arr_queue.clear()
        ro_verify_max_correct = 0

def _algo_play_sound(lst, ind):
        sin_array = None
        try:
                sin_array = numpy.array(
                        2048 * numpy.sin(2.0 * numpy.pi * 350 * (lst[ind] / max(lst)) * numpy.arange(1800) / 1800)
                ).astype(numpy.int16)

                sound_array = numpy.c_[sin_array, sin_array]
                sound = pygame.sndarray.make_sound(sound_array)

                #sound.set_volume(0.8)

                sound.play(0, 36) # dont change
                sound.fadeout(36) # dont change

        except ZeroDivisionError:
                pass

def _algo_play_verify_sound(lst, ind):
        sin_array = numpy.array(
                4096 * numpy.sin(2.0 * numpy.pi * 700 * (lst[ind] / max(lst)) * numpy.arange(3600) / 3600)
        ).astype(numpy.int16)

        sound_array = numpy.c_[sin_array, sin_array]
        sound = pygame.sndarray.make_sound(sound_array)

        #sound.set_volume(0.8)

        sound.play(0, 100)
        sound.fadeout(100)

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

# only for visuals, no other use currently
def _access_other_array(lst, ind):
        global ro_display_arr_queue

        _algo_play_sound(lst, ind)
        ro_display_arr_queue.clear()
        ro_display_arr_queue.append(ind)

def _algo_greater(lst, ind_lhs, ind_rhs):
        cmp = _algo_compare(lst, ind_lhs, ind_rhs)
        return cmp == lst[ind_lhs] and cmp != lst[ind_rhs]

def _algo_greater_equal(lst, ind_lhs, ind_rhs):
        return _algo_compare(lst, ind_lhs, ind_rhs) == lst[ind_lhs]

def _algo_radix_digit(str, max_digits):
        if (len(str) == max_digits):
                return str
        
        diff = max_digits - len(str)
        new_str = ("0" * diff) + str
        return new_str

def _algo_bubble_sort_radix_one(lst, iter):        
        for j in range(1, len(lst) - iter):
                if lst[j][2] < lst[j - 1][2]:
                        temp = lst[j]
                        lst[j] = lst[j - 1]
                        lst[j - 1] = temp

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

def radix_sort_lsd(lst):
        global wo_terminate
        global ro_algo_done

        _algo_init()

        max_digits = len(str(max(lst)))
        buckets = lst
        next_buckets = []

        for cur_digit_ind in range(max_digits - 1, -1, -1):
                for i, elem in enumerate(buckets):
                        if wo_terminate:
                                wo_terminate = False
                                return
                        
                        str_elem = _algo_radix_digit(str(elem), max_digits)

                        cur_digit = int(str_elem[cur_digit_ind])
                        next_buckets.append([i, elem, cur_digit])

                        _access_other_array(lst, i)
                        _algo_render()

                for i in range(len(lst)):
                        _algo_bubble_sort_radix_one(next_buckets, i)
                        _algo_play_sound(next_buckets[i], 1)

                        lstcpy = copy.deepcopy(lst)
                        for i in range(len(lst)):
                                lst[i] = next_buckets[i][1]
                        _algo_render()
                        for i in range(len(lst)):
                                lst[i] = lstcpy[i]

                buckets = [int(b[1]) for b in next_buckets]
                for i, _ in enumerate(lst):
                        lst[i] = buckets[i]
                next_buckets.clear()

        ro_algo_done = True
        _algo_verify(lst)