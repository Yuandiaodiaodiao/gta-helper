import numpy as np


def trim_iterative(frame):
    for start_y in range(1, frame.shape[0]):
        if np.sum(frame[:start_y]) > 10:
            start_y -= 1
            break
        if start_y == frame.shape[0]:
            if len(frame.shape) == 2:
                return np.zeros((0, 0))
            else:
                return np.zeros((0, 0, 0))
    for trim_bottom in range(1, frame.shape[0]):
        if np.sum(frame[-trim_bottom:]) > 10:
            break

    for start_x in range(1, frame.shape[1]):
        if np.sum(frame[:, :start_x]) > 10:
            start_x -= 1
            break
    for trim_right in range(1, frame.shape[1]):
        if np.sum(frame[:, -trim_right:]) > 10:
            break

    end_y = frame.shape[0] - trim_bottom + 1
    end_x = frame.shape[1] - trim_right + 1

    # print('iterative cropping x:{}, w:{}, y:{}, h:{}'.format(start_x, end_x - start_x, start_y, end_y - start_y))
    return frame[start_y:end_y, start_x:end_x]
