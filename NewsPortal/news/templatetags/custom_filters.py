from django import template

register = template.Library()

BLACKLIST = ['Telescope', 'bad_word_2']


@register.filter()
def censor(text):
    text = text.split()
    censored_text = text
    for b in BLACKLIST:
        for n, w in enumerate(text):
            if w.lower() == b.lower():
                censored_text[n] = text[n][0] + '*' * (len(text[n]) - 1)
    censored_text = " ".join(censored_text)

    return censored_text
