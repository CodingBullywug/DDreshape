import numpy as np

def PoolByteArray2NumpyArray(pool_byte_array_string):
    return np.array(pool_byte_array_string[14:-1].split(',')).astype(np.uint8)

def PoolIntArray2NumpyArray(pool_int_array_string):
    return np.array(pool_int_array_string[13:-1].split(',')).astype(np.int64)

def PoolVector2Array2NumpyArray(pool_vector2_array_string, dtype=np.float):
    if not pool_vector2_array_string[17:-1].strip(): # Check if empty
        np_array = np.array([], dtype=dtype)
    else:
        np_array = np.array(pool_vector2_array_string[17:-1].split(',')).astype(dtype)
    return np_array.reshape(int(np_array.shape[0]/2),2)

def Vector22NumpyArray(vector2_string, dtype=np.float):
    return np.array(vector2_string[8:-1].split(',')).astype(dtype)

def NumpyArray2PoolByteArray(numpy_array):
    return 'PoolByteArray(' + ', '.join(list(numpy_array.astype(np.str))) + ')'

def NumpyArray2PoolIntArray(numpy_array):
    return 'PoolIntArray(' + ', '.join(list(numpy_array.astype(np.str))) + ')'

def NumpyArray2PoolVector2Array(numpy_array):
    return 'PoolVector2Array(' + ', '.join(list(numpy_array.flatten().astype(np.str))) + ')'

def NumpyArray2Vector2(numpy_array):
    return 'Vector2(' + ', '.join(list(numpy_array.astype(np.str))) + ')'

def NumpyByteArray2NumpyBitArray(np_byte_array, width, height):
    np_bit_str = ''.join(["{0:08b}".format(b) for b in np_byte_array])
    np_bit_flat = np.asarray(list(np_bit_str)).astype(np.uint8)
    np_bit_array = np.fliplr(np_bit_flat.reshape(len(np_byte_array),8)).reshape(len(np_bit_flat))[0:(width*height)].reshape(height, width)
    return np_bit_array

def NumpyBitArray2NumpyByteArray(np_bit_array):
    np_bit_array_flat = np_bit_array.flatten()
    np_bit_array_flat_padded = np.pad(np_bit_array_flat, (0,int(np.ceil(len(np_bit_array_flat)/8)*8-len(np_bit_array_flat))), mode='constant', constant_values=0) # Pad with zeros in the end to match byte size. Must be divisible by 8.
    np_bit_array_flat_padded_flipped = np.fliplr(np_bit_array_flat_padded.reshape(int(len(np_bit_array_flat_padded)/8),8))
    np_byte_array = np.asarray([int(''.join(list(row)),2) for row in np_bit_array_flat_padded_flipped.astype(str)])
    return np_byte_array