
def readin_time (text : str):
    words = list(text.split(' '))
    _time = (len(words) / 125)
    return round(_time , 2)
