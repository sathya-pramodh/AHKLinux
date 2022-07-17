class TokenStream:
    def __init__(self, stream_list):
        self._value = stream_list
        self._cur_val = 0

    def next(self):
        if self._cur_val == len(self._value):
            return
        ret_elem = self._value[self._cur_val]
        self._cur_val += 1
        return ret_elem
