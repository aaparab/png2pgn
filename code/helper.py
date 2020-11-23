##############################
#####  Helper functions  #####
##############################

# This is a list of helper functions related to
# file read/write and converting pgn to np array, etc.

from PIL import Image
import numpy as np
import os

piece_to_num_dict = {
    'P': 1,
    'N': 2,
    'B': 3,
    'R': 4,
    'Q': 5,
    'K': 6,
    'p': -1,
    'n': -2,
    'b': -3,
    'r': -4,
    'q': -5,
    'k': -6
}


num_dict_to_piece = {
    1: 'P', 
    2: 'N', 
    3: 'B', 
    4: 'R', 
    5: 'Q', 
    6: 'K', 
    -1: 'p', 
    -2: 'n', 
    -3: 'b', 
    -4: 'r', 
    -5: 'q', 
    -6: 'k', 
}


piece_to_list = {
    'P': [0]*7 + [1] + [0]*5,
    'N': [0]*8 + [1] + [0]*4,
    'B': [0]*9 + [1] + [0]*3,
    'R': [0]*10 + [1] + [0]*2,
    'Q': [0]*11 + [1] + [0]*1,
    'K': [0]*12 + [1],
    'p': [0]*5 + [1] + [0]*7,
    'n': [0]*4 + [1] + [0]*8,
    'b': [0]*3 + [1] + [0]*9,
    'r': [0]*2 + [1] + [0]*10,
    'q': [0]*1 + [1] + [0]*11,
    'k': [1] + [0]*12
}


def fpath_to_pgn(fpath):
    """Slices the pgn string from file path.
    """
    return fpath.split('/')[-1].split('.jpeg')[0]


def pgn_to_np_array(pgn):
    """Convert pgn string to a 64x64 numpy array.
    Dictionary:
        Empty: 0
        WPawn: 1
        WKnight: 2
        WBishop: 3
        WRook: 4
        WQueen: 5
        WKing: 6
        BPawn: -1
        BKnight: -2
        BBishop: -3
        BRook: -4
        BQueen: -5
        BKing: -6
    """
    board = []
    for s in pgn.split('-'):
        row = []
        for ch in s:
            if ch in piece_to_num_dict.keys():
                row.append(piece_to_num_dict[ch])
            else:
                row += [0]*int(ch)
        assert len(row) == 8, 'Length of row != 8.'
        board.append(row)
    return np.array(board)


def pgn_to_dc_vector(png):
    """Converts a pgn string to a dummy-coded vector of size 1 x 832 (64x13)
    Dictionary:
        Empty: 0
        WPawn: 1
        WKnight: 2
        WBishop: 3
        WRook: 4
        WQueen: 5
        WKing: 6
        BPawn: -1
        BKnight: -2
        BBishop: -3
        BRook: -4
        BQueen: -5
        BKing: -6
    """
    vector = []
    for s in png.split('-'):
        for ch in s:
            if ch in piece_to_num_dict.keys():
                vector += piece_to_list[ch]
            else:
                vector += ([0]*6 + [1] + [0]*6)*int(ch)
    return np.array(vector).reshape(1, 832)


def dc_vector_to_np_array(vector):
    """Converts a dummy-coded vector of size 832 = 64x13
    into a numpy array representing the chessboard.
    """
    vector = vector.reshape(64, 13)
    array = [i-6 for v in vector for i, pos in enumerate(v) if pos]
    array = np.array(array).reshape(8, 8)
    return array


def get_X(fpaths):
    """Generates a numpy vector of size len(fpaths) x 480_000. 
    
    Normalization is done by dividing each value by the maximum, i.e., 255.
    """
    x_array = np.array([], dtype=np.float32).reshape((0, 480_000))
    for f in fpaths:
        im = Image.open(f)
        arr = np.asarray(im).reshape(1, 480_000)
        x_array = np.append(x_array, arr, axis=0)
    return x_array/255.

def get_Y(fpaths):
    """Generates a numpy vector of size len(fpaths) x 832. 
    """
    y_array = np.array([], dtype=np.float32).reshape((0, 832))
    for f in fpaths:
        pgn = fpath_to_pgn(f)
        vec = pgn_to_dc_vector(pgn)
        y_array = np.append(y_array, vec, axis=0)
    return y_array