import numpy as np

print("Reloaded ImageTransform")

rng = np.random.default_rng()

def naive_channel_delta(color_a, color_b):
    r_a, g_a, b_a = color_a
    r_b, g_b, b_b = color_b
    return (abs(int(r_a) - int(r_b)) +
            abs(int(g_a) - int(g_b)) +
            abs(int(b_a) - int(b_b)))

def channel_squared_delta(color_a, color_b):
    r_a, g_a, b_a = color_a
    r_b, g_b, b_b = color_b
    return (pow(int(r_a) - int(r_b), 2) +
            pow(int(g_a) - int(g_b), 2) +
            pow(int(b_a) - int(b_b), 2))

def channel_squared_delta_inv(color_a, color_b):
    csd = channel_squared_delta(color_a, color_b)
    if csd == 0:
        return csd
    return 1.0/csd

def swap_pixels_if_needed(source_array, target_array, coord_a, coord_b, transfer_function=channel_squared_delta):
    r_a, c_a = coord_a
    r_b, c_b = coord_b
    source_a = np.array(source_array[r_a, c_a])
    source_b = np.array(source_array[r_b, c_b])
    target_a = target_array[r_a, c_a]
    target_b = target_array[r_b, c_b]
    
    curr_error = (transfer_function(source_a, target_a) +
                  transfer_function(source_b, target_b))
    swap_error = (transfer_function(source_a, target_b) +
                  transfer_function(source_b, target_a))
    
    if curr_error > swap_error:
        source_array[r_a, c_a], source_array[r_b, c_b] = source_b, source_a
        return 1
    return 0

coords_tmp = []
for r in range(512):
    for c in range(512):
        coords_tmp.append((r,c))
        
coords = np.asarray(coords_tmp)

def reshuffle():
    global shuffled_coords
    shuffled_coords = rng.permutation(coords)

reshuffle()

def pixel_transform(working_array, target_array, transfer_function, progress_widget=None):
    # Validate that both arrays have the same shape
    if target_array.shape != working_array.shape:
        return

    # For each loop:
        # Generate pixel pairs for tests
        # Use swap_if_needed on pairs
    for i in range(25):
        reshuffle()
        swaps = 0
        for i_c in range(512 * 512):
            swaps += swap_pixels_if_needed(working_array, target_array, coords[i_c], shuffled_coords[i_c], transfer_function)
        # print(swaps)
        if progress_widget != None:
            progress_widget.value = i
        if swaps == 0:
            return

def pixel_transform_continuous(working_array, target_array, transfer_function, progress_widget=None):
    # Validate that both arrays have the same shape
    if target_array.shape != working_array.shape:
        return

    for i in range(6553600):
        coords = rng.integers(0, 512, (2, 2))
        # print(coords)
        # return
        swap_pixels_if_needed(working_array, target_array, coords[0], coords[1], transfer_function)
        # print(swaps)
        if progress_widget != None and i % 13107 == 0:
            progress_widget.value = i / 262144.0
