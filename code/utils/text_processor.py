from cltk.stem.lat import _checkremove_que
from cltk.text.lat import replace_jv

punctuation = ["'", '"', "!", "&", "(", ")", ";", ":", ",", ".", "?", "[", "]"]

def split_punct(text, punct):
    split_text = []
    for item in text:
        punct_ind = item.split(punct)
        if len(punct_ind)>1:
            
            punct_ind.insert(1, punct)
        split_text = split_text + punct_ind
    return (split_text)
            
def split_chars(text, punctuation):
    for punct in punctuation:
        text = split_punct(text, punct)
    text[:] = [word for word in text if word !=""]
    return(text)

def process_text(text, jvque_toggle=True):
    proc_text = text.lower()
    if jvque_toggle == True:
        proc_text = replace_jv(proc_text)
    proc_text = proc_text.strip()
    proc_text = proc_text.split(" ")
    proc_text = split_chars(proc_text, punctuation)
    if jvque_toggle == True:
        proc_text = [_checkremove_que(word)[0] for word in proc_text]
    return(proc_text)
