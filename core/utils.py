
def ted(state):
    try:
        return state
    except IndexError:
        return None


def find_mic_detail(status, pos):
    if pos == 2:
        tmp = status.split()
        tmp.pop(1)
        tmp.pop(0)
        res = ' '.join(tmp)
        return res
    if pos == 1:
        tmp = status.split()
        tmp.pop(0)
        res = ' '.join(tmp)
        return res
