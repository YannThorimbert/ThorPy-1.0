from __future__ import division

from pygame.rect import Rect

from thorpy.elements._sliderutils._dragger import DraggerX, DraggerY
from thorpy.elements.element import Element
from thorpy.elements._sliderutils._shifters import Plus, Minus
from thorpy.miscgui.reaction import Reaction, ConstantReaction
from thorpy.miscgui import constants, functions, parameters, style, painterstyle


class _Slider(object):
    """Not to be instanciated, not an element."""

    def __init__(self, length, limvals=None):
        limvals = parameters.LIMVALS if limvals is None else limvals
        self._length = length
        self._limvals = limvals
        self._shift = self.val_to_pix(1, 0)

    def get_width_val(self):
        return self._limvals[1] - self._limvals[0]

    def pix_to_val(self, pix, x0):
        fraction = float((pix - x0)) / self._length
        return self._limvals[0] + fraction * self.get_width_val()

    def val_to_pix(self, val, x0):
        fraction = float(val - self._limvals[0]) / self.get_width_val()
        return int(round(fraction * self._length + x0))

    def _refresh_shift(self):
        self._shift = self.val_to_pix(1, 0)



class _GraphicalSlider(_Slider, Element):

    def __init__(self, length, limvals=None, text="", elements=None,
                 normal_params=None):
        limvals = parameters.LIMVALS if limvals is None else limvals
        self._plus = None
        self._minus = None
        Element.__init__(self, text, elements, normal_params)
        _Slider.__init__(self, length, limvals)
        self.current_state.autoghost = False
##        self._set_wheel_reaction(parameters.BUTTON_UNPRESS_EVENT,
##                                {"button": parameters.WHEELUP_BUTTON})
##        self._set_unwheel_reaction(parameters.BUTTON_PRESS_EVENT,
##                                  {"button": parameters.WHEELDOWN_BUTTON})
        self._setup()
        self.active_wheel = False

    def get_storer_rect(self):
        return self.get_family_rect(constants.STATE_NORMAL)

    def move(self, shift):
        value_before = self.get_value()
        Element.move(self, shift)
        if self.get_value() != value_before:
            self._drag_element.place_at(value_before)

##    def _set_wheel_reaction(self, typ, args=None):
##        if not args:
##            args = {}
##        reac_wheelup = Reaction(typ, self._reaction_wheel, args,
##                                name=constants.REAC_WHEELUP)
##
##    def _set_unwheel_reaction(self, typ, args=None):
##        if not args:
##            args = {}
##        reac_wheeldown = Reaction(typ, self._reaction_unwheel, args,
##                                  name=constants.REAC_WHEELDOWN)
##
##    def _reaction_wheel(self, event):
##        if self.active_wheel:
##            if self.collide(event.pos, self.current_state_key):
##                self._drag_element.shift(parameters.WHEEL_SLIDER_SHIFT)
##
##    def _reaction_unwheel(self, event):
##        if self.active_wheel:
##            if self.collide(event.pos, self.current_state_key):
##                self._drag_element.shift(-parameters.WHEEL_SLIDER_SHIFT)

    def _setup(self):
        pass

    def _press_plus(self):
        # change state, blit and update
        functions.keypress(self._plus, constants.STATE_PRESSED)
        self._drag_element.shift()

    def _press_minus(self):
        # change state, blit and update
        functions.keypress(self._minus, constants.STATE_PRESSED)
        self._drag_element.shift(-1)

    def _add_buttons(self, size=None):
        size = style.SMALL_SIZE if size is None else size
        # _plus
        self._plus = Plus(text="+")
        self._plus.set_painter(painterstyle.DEF_PAINTER(size=size))
        self._plus.finish()
        self._plus.drag = self._drag_element
        reac_plus = ConstantReaction(constants.THORPY_EVENT,
                                     self._plus._reaction_time,
                                     {"name":constants.EVENT_TIME},
                                     name=constants.REAC_MOUSE_REPEAT)
        self.add_reaction(reac_plus)
        # _minus
        self._minus = Minus(text="-")
        self._minus.set_painter(painterstyle.DEF_PAINTER(size=size))
        self._minus.finish()
        self._minus.drag = self._drag_element
        reac_minus = ConstantReaction(constants.THORPY_EVENT,
                                     self._plus._reaction_time,
                                     {"name":constants.EVENT_TIME},
                                     name=constants.REAC_MOUSE_REPEAT+0.1)
        self.add_reaction(reac_minus)
        self.add_elements([self._plus, self._minus])
        # reactions to mouse _press (!= reactions to key _press):
        self._plus.reactions[constants.REAC_PRESSED +0.1] = ConstantReaction(
            constants.THORPY_EVENT,
            self._drag_element.shift,
            {"name":constants.EVENT_PRESS, "el": self.plus})
        self._minus.reactions[constants.REAC_PRESSED +0.1] = ConstantReaction(
            constants.THORPY_EVENT,
            self._drag_element.shift,
            {"name":constants.EVENT_PRESS, "el": self.minus},
            {"sign":-1})
        self._reactions[constants.REAC_PRESSED + 0.1] = ConstantReaction(
            constants.THORPY_EVENT,
            self._drag_element.shift,
            {"name":constants.EVENT_PRESS, "el": self.plus})
        self._reactions[constants.REAC_PRESSED + 0.1] = ConstantReaction(
            constants.THORPY_EVENT,
            self._drag_element.shift,
            {"name":constants.EVENT_PRESS, "el": self.minus},
            {"sign":-1})

##    def _get_no_slide_rect(self):
##        """Returns size without slide_rect"""
##        wh_slide = self._get_slide_rect().size
##        wh = self.get_fus_rect().size
##        return (wh[0] - wh_slide[0], wh[1] - wh_slide[1])


class SliderX(_GraphicalSlider):

    def __init__(self,
                 length,
                 limvals=None,
                 text="",
                 elements=None,
                 normal_params=None,
                 initial_value=None):
        if limvals[0] <= initial_value <= limvals[1]: #will be False if initial_value is None
            self.initial_value = initial_value
        else:
            if initial_value is not None:
                functions.debug_msg("Initial value for slider was not in the\
                                    limvals range. Auto set to limvals[0].")
            self.initial_value = limvals[0]
        self._drag_element = DraggerX(self)
        super(SliderX, self).__init__(length, limvals, text, elements)
        self._drag_element.finish()
        self.add_elements(list([self._drag_element]))

    def finish(self):
        Element.finish(self)
        self._drag_element.set_center((None, self.get_fus_center()[1]))
        for state in self._states:
            self._states[state].refresh_ghost_rect()
        self._setup()
        self._drag_element.place_at(self.initial_value)

    def _setup(self, height=None, dragsize=None):
        height = style.SLIDER_THICK if height is None else height
        dragsize = style.SLIDERX_DRAG_SIZE if dragsize is None else dragsize
        self._height = height
        size = (self._length + dragsize[0] + style.SLIDER_MARGINS[0], height)
        painter = functions.obtain_valid_painter(
            painterstyle.DEF_PAINTER,
            pressed=True,
            color=style.DEF_COLOR2,
            size=size)
        self.set_painter(painter)
        dp = functions.obtain_valid_painter(
            painterstyle.DEF_PAINTER,
            pressed=False,
            size=dragsize)
        try:
            drag_x = self.val_to_pix(self.initial_value,
                                     self.get_fus_topleft()[0]) + 1
            self._drag_element.change_painter(dp, autopress=False)
            self._drag_element.set_center((drag_x, self.get_fus_center()[1]))
        except AttributeError:
            drag_x = self.val_to_pix(self.initial_value,
                                     self.get_ghost_topleft()[0]) + 1
            self._drag_element.set_painter(dp, autopress=False)
            self._drag_element.set_center((drag_x, self.get_ghost_center()[1]))
        self._drag_element.set_free(y=False)
        self.englobe_childrens()

    def _get_slide_rect(self):
        slide_rect = Rect((0, 0), (self._length, self._height))
        try:
            slide_rect.center = self.get_fus_center()
        except AttributeError:
            slide_rect.center = self.get_ghost_center()
        return slide_rect

    def get_value(self):
        x0 = self._get_slide_rect().x
        val = self.pix_to_val(self._drag_element.get_fus_center()[0], x0)
        if val < self._limvals[0]:
            return self._limvals[0]
        elif val > self._limvals[1]:
            return self._limvals[1]
        else:
            return val

    def _add_buttons(self, size=None):
        _GraphicalSlider._add_buttons(self, size)
        rect = self.get_fus_rect()
        self._minus.set_center((-2 + rect.left - size[0] // 2, rect.centery))
        self._plus.set_center((2 + rect.right + size[0] // 2, rect.centery))
        self.englobe_childrens()
        self._add_buttons_reactions()

    def _add_buttons_reactions(self):
        """Add reactions to keyboard _press and unpress"""
        pass

    def get_size(self, state=None):
        """Special get_size method for sliders.
        Could be named get_family_size().
        """
        return self.get_family_rect(state).size


class SliderY(_GraphicalSlider):

    def __init__(self,
                 length,
                 limvals=None,
                 text="",
                 elements=None,
                 normal_params=None):
        self._height = None
        self._drag_element = DraggerY(self)
        super(SliderY, self).__init__(length, limvals, text, elements,
                                      normal_params)
        self._drag_element.finish()
        self.add_elements(list([self._drag_element]))
        self.englobe_childrens()

    def finish(self):
        Element.finish(self)
        self._drag_element.set_center((self.get_fus_center()[0], None))
        self.misc_refresh()

    def misc_refresh(self):
        self._refresh_shift()

    def _get_slide_rect(self):
        slide_rect = Rect((0, 0), (self._height, self._length))
        slide_rect.center = self.get_fus_rect().center
        return slide_rect

    def get_value(self):
        y0 = self._get_slide_rect().y
        val = self.pix_to_val(self._drag_element.get_fus_center()[1], y0)
        if val < self._limvals[0]:
            return self._limvals[0]
        elif val > self._limvals[1]:
            return self._limvals[1]
        else:
            return val

    def get_factor(self):
        value = self.get_value()
        return 1. - (self._limvals[1] - value) / self._limvals[1]

    def _add_buttons(self, size=None):
        _GraphicalSlider._add_buttons(self, size)
        rect = self.get_fus_rect()
        pos = (rect.centerx, rect.bottom + style.SLIDER_MARGINS[1] + size[1]/2)
        self._minus.set_center(pos)
        pos = (rect.centerx, rect.top - style.SLIDER_MARGINS[1] - size[1]/2)
        self._plus.set_center(pos)
        self.englobe_childrens()
        self._add_buttons_reactions()

    def _add_buttons_reactions(self):
        pass

    def _get_theo_size(self, buttonsize, dragsize, length, margins=None,
                       surplus=False):
        """Returns the theoretical future total size of self. The reason for
        this method to exist is that it provides a way to guess the size before
        the graphical parts are created by calling self.finish().
        <surplus> : get only the size surplus due to buttons.
        """
        margins = style.SLIDER_MARGINS[0] if margins is None else margins
        w = max(buttonsize[0], dragsize[0])
        actual_length = length + dragsize[1] + 2 * margins
        if buttonsize[0] != 0:  # (0, 0) button size means no buttons
            buttons_growth = 2 * buttonsize[1] + 2 * margins
        else:
            buttons_growth = 0
        h = actual_length + buttons_growth
        if surplus:
            h -= length
        return (w, h)
