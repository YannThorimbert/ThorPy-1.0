from thorpy.elements.clickable import Clickable

def make_button(text, func=None, params=None):
    button = Clickable(text)
    button.finish()
    button.scale_to_title()
    if func:
        button.user_func = func
    if params:
        button.user_params = params
    return button