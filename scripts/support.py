import math
import sys
from os import walk
import pygame

import shaders


def import_folder(path: str, size: float) -> [pygame.Surface]:
    """
    :param path: path to the folder
    :param size: size of the images imported
    :return: a list of surfaces containg all images in the folder
    """
    surface_list = []

    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            image_surf = pygame.transform.scale_by(image_surf, size)
            surface_list.append(image_surf)

    return surface_list


def distance(a: tuple, b: tuple) -> float:
    """
    :param a: first position
    :param b: second position
    :return: euclidian distance between a and b
    """
    if not isinstance(a, tuple):
        raise TypeError(f'A should be of type tuple and not {type(a)}')
    if not isinstance(b, tuple):
        raise TypeError(f'B should be of type tuple and not {type(b)}')

    return math.sqrt(sum((a[i] - b[i]) ** 2 for i in range(2)))


def fadeTransitionStart(screen: pygame.Surface, shader: shaders.Shader=None, duration: int=150):
    """
    Fades the screen to black slowly
    :param screen: screen to do the transition
    :param shader: shader to do the transition
    """
    # create black surface
    blackGradient = pygame.Surface((screen.get_width(), screen.get_height()))
    blackGradient.fill('black')
    # slowly increase alpha to create the transition effect
    for a in range(duration):
        blackGradient.set_alpha(a)
        screen.blit(blackGradient, (0, 0))
        # if there is a shader use it else just update the display
        if shader is None:
            pygame.display.update()
        else:
            shader.render(screen)
        # wait 5 ms between each iteration
        pygame.time.delay(5)


def fadeTransitionEnd(screen: pygame.Surface, shader: shaders.Shader=None, duration: int=180):
    """
    Fades from black to the original screen slowly
    :param screen: screen to do the transition
    :param shader: shader to do the transition
    """
    # copy the screen and show it every frame before the black surface,
    # this is to prevent the screen to be 'erased' at the beginning of the transition
    background = screen.copy()
    # create black surface
    blackGradient = pygame.Surface((screen.get_width(), screen.get_height()))
    blackGradient.fill('black')
    # slowly decrease alpha to create the transition effect
    for a in range(duration, -1, -3):
        blackGradient.set_alpha(a)
        screen.blit(background, (0, 0))
        screen.blit(blackGradient, (0, 0))
        # if there is a shader use it else just update the display
        if shader is None:
            pygame.display.update()
        else:
            shader.render(screen)
        # wait 5 ms between each iteration
        pygame.time.delay(5)


def slideTransitionStart(screen: pygame.Surface, surface: pygame.Surface, shader: shaders.Shader=None):
    """
    Does a sliding transition for the surface onto the screen from the bottom
    :param screen: screen to do the transition
    :param surface: surface to translate from bottom to center
    :param shader: shader to do the transition
    """
    # copy the screen and show it every frame before the black surface,
    # this is to prevent the screen to be 'erased' at the beginning of the transition
    background = screen.copy()
    rect = screen.get_rect(topleft=screen.get_rect().bottomleft)

    screen.blit(surface, rect)
    h = screen.get_height() // 6

    # translate the surface with an ease out effect from bottom to top
    while rect.y > 0:
        screen.blit(background, (0, 0))
        screen.blit(surface, rect)

        # if there is a shader use it else just update the display
        if shader is None:
            pygame.display.update()
        else:
            shader.render(screen)

        # slowly decrease the amount of vertical change to the surface for the ease out
        rect.y -= h
        h -= h // 6

        # wait 5 ms between each iteration
        pygame.time.delay(5)


def slideTransitionEnd(screen: pygame.Surface, surface: pygame.Surface, shader: shaders.Shader=None):
    """
    Does a sliding transition for the surface to disappear at the bottom of the screen
    :param screen: screen to do the transition
    :param surface: surface to translate from center to below the bottom
    :param shader: shader to do the transition
    """
    # copy the screen and show it every frame before the black surface,
    # this is to prevent the screen to be 'erased' at the beginning of the transition
    background = screen.copy()
    rect = screen.get_rect()

    screen.blit(surface, rect)
    j = screen.get_height() // 6

    # translate the surface with an ease in effect from top to bottom
    while rect.y < screen.get_height():
        screen.blit(background, (0, 0))
        screen.blit(surface, rect)

        # if there is a shader use it else just update the display
        if shader is None:
            pygame.display.update()
        else:
            shader.render(screen)

        # slowly increase the amount of vertical change to the surface for the ease in
        rect.y += j
        j += j // 6

        # wait 5 ms between each iteration
        pygame.time.delay(5)


class Button:
    def __init__(self, image: pygame.image, pos: (int, int), text_input: str, font: pygame.font,
                 base_color: str, hovering_color: str):
        """
        The button is a button that can do actions when pressed
        :param image: image to be displayed being the button, if set to None the text will be displayed instead
        :param pos: center of the button
        :param text_input: text to be shown
        :param font: font to be used for the text
        :param base_color: color of the text
        :param hovering_color: color of the text when hovering the slider with the mouse
        """
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

        self.changeColor()

    def checkForInput(self):
        position = pygame.mouse.get_pos()
        if self.rect.left < position[0] < self.rect.right and self.rect.top < position[1] < self.rect.bottom:
            return True
        return False

    def changeColor(self):
        position = pygame.mouse.get_pos()
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


class CheckButton:
    def __init__(self, image: pygame.image, pos: (int, int), text_input: str, start_value: bool, font: pygame.font,
                 base_color: str, hovering_color: str):
        """
        The Check button is like an ON/OFF button its value is either True or False and can be toggled by clicking it
        :param image: image to be displayed being the button, if set to None the text will be displayed instead
        :param pos: center of the button
        :param text_input: text to be shown
        :param start_value: initial value of the button
        :param font: font to be used for the text
        :param base_color: color of the text
        :param hovering_color: color of the text when hovering the slider with the mouse
        """
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

        self.box = pygame.Rect(0, 0, self.text_rect.height, self.text_rect.height)
        self.box.center = (self.x_pos + self.text_rect.width / 1.8, self.y_pos)
        self.cross_rect = self.box.inflate(-6, -6)

        self.value = start_value

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)

        screen.blit(self.text, self.text_rect)
        pygame.draw.rect(screen, self.base_color, self.box, 8)

        if self.value:
            pygame.draw.line(screen, self.base_color, (self.cross_rect.left + 4, self.cross_rect.top + 4),
                             (self.cross_rect.right - 4, self.cross_rect.bottom - 4), 8)
            pygame.draw.line(screen, self.base_color, (self.cross_rect.left + 4, self.cross_rect.bottom - 4),
                             (self.cross_rect.right - 4, self.cross_rect.top + 4), 8)

        self.changeColor()

    def checkForInput(self):
        position = pygame.mouse.get_pos()
        if self.rect.left < position[0] < self.rect.right and self.rect.top < position[1] < self.rect.bottom:
            self.value = not self.value
            return self.value

    def changeColor(self):
        position = pygame.mouse.get_pos()
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


class InputButton:
    def __init__(self, image: pygame.image, pos: (int, int), text_input: str, key_input: int, font: pygame.font,
                 base_color: str, hovering_color: str):
        """
        The Input button is a button that stores a key when pressed
        :param image: image to be displayed being the button, if set to None the text will be displayed instead
        :param pos: center of the button
        :param text_input: text to be shown
        :param key_input: initial value
        :param font: font to be used for the text
        :param base_color: color of the text
        :param hovering_color: color of the text when hovering the slider with the mouse
        """
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = str(text_input)
        self.key_input = pygame.key.name(key_input).upper()
        self.text = self.font.render(self.text_input + self.key_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.is_hovered = False
        self.is_active = False
        self.key = key_input

        self.exitInputButton = Button(None, (pygame.display.get_surface().get_width()/2, pygame.display.get_surface().get_height()/1.1),
                                      'EXIT', font, self.base_color, self.hovering_color)

    def update(self, screen: pygame.Surface):
        """
        Updates the button's color and position based on its stored value
        :param screen: screen to display the button
        """
        self.text_rect.centerx = self.x_pos - (len(self.key_input) * 20) / 2
        screen.blit(self.text, self.text_rect)

        self.changeColor()

    def isHovered(self):
        position = pygame.mouse.get_pos()
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,self.rect.bottom):
            return True
        return False

    def checkForInput(self):
        """
        If the button is pressed it takes the next key the user presses and stores it
        """
        # check if button is clicked
        position = pygame.mouse.get_pos()
        if self.rect.left < position[0] < self.rect.right and self.rect.top < position[1] < self.rect.bottom:
            key = None
            # wait for input
            while key is None:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            key = self.key_input
                        else:
                            key = pygame.key.name(event.key)
                    if event.type == pygame.MOUSEBUTTONDOWN and self.exitInputButton.checkForInput():
                        key = self.key_input

            # store input key as its pygame attribute if it is a valid key
            try:
                self.key = getattr(pygame, "K_" + key.lower())
                self.key_input = key.upper()
            except:
                try:
                    self.key = getattr(pygame, "K_" + key.upper())
                    self.key_input = key.upper()
                except:
                    raise(ValueError(f'Invalid Key Selection : "{key}"'))

    def changeColor(self):
        position = pygame.mouse.get_pos()
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input + self.key_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input + self.key_input, True, self.base_color)


class Slider:
    def __init__(self, pos: (int, int), text_input: str, range: (int, int), font: pygame.font.Font,
                 base_color: str, exterior_color: str, interior_color: str, hovering_color: str, ball_color: str,
                 size: int, startVal: float, custom: dict=None):
        """
        :param pos: center of the slider
        :param text_input: text to be displayed next to the value
        :param range: range of value
        :param font: font to be used for the text
        :param base_color: color of the text
        :param exterior_color: color of the exterior part of the slider
        :param interior_color: color of the interior part of the slider
        :param hovering_color: color of the text when hovering the slider with the mouse
        :param ball_color: color of the ball
        :param size: size of the slider
        :param startVal: starting value of the slider
        :param custom: custom text to value dictionary, maps the ouput value to a text in the dict
        """
        self.base_color, self.exterior_color, self.interior_color, self.hovering_color, self.ball_color = base_color, exterior_color, interior_color, hovering_color, ball_color

        # main rectangle of the slider (the biggest one)
        self.slider = pygame.Surface((100 * size, 16.666 * size))
        self.slider.fill(self.exterior_color)
        self.rect = self.slider.get_rect(center=(pos[0], pos[1]))

        # second rectangle of the slider (smaller one in which the ball is)
        self.slider_small_rect = self.rect.inflate(-13.333 * size, -13.333 * size)
        self.slider_small = pygame.Surface((self.slider_small_rect.width, self.slider_small_rect.height))
        self.slider_small.fill(self.interior_color)

        # slider ball that you can drag around
        self.slider_ball = pygame.Rect(self.slider_small_rect.left, self.slider_small_rect.top - 2.08333 * size,
                                       8.333 * size, 8.333 * size)

        self.x_pos = pos[0]
        self.y_pos = pos[1]

        # range of value
        self.range = range

        self.font = font

        # text to be displayed above the slider
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos - 13.333 * size))

        # value of the slider
        self.value = startVal
        self.slider_ball.centerx = self.ballPosFromValue()

        # custom text/value dictionnary
        self.custom = custom

    def checkForInput(self):
        """
        Updates the position of the ball if the mouse drags it
        """
        mPos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mPos) and pygame.mouse.get_pressed()[0]:
            if self.slider_small_rect.left < mPos[0] < self.slider_small_rect.right:
                self.slider_ball.centerx = mPos[0]

    def update(self, screen: pygame.Surface, getInput=True):
        """
        :param screen: current display
        Updates the ball position, text displayed and value
        """
        if getInput:
            self.checkForInput()

        # show slider
        pygame.draw.rect(screen, self.exterior_color, self.rect, border_radius=50)  # exterior rect
        screen.blit(self.slider_small, self.slider_small_rect)  # interior rect
        pygame.draw.circle(screen, self.ball_color, self.slider_ball.center, self.slider_ball.width / 1.5)  # ball
        if self.custom is None:
            self.text_rect.centerx = self.x_pos - (len(str(round(self.value))) * 20) / 2
        else:
            self.text_rect.centerx = self.x_pos - (len(": " + self.custom[round(self.value)]) * 20) / 2
        self.changeColor()  # update color
        screen.blit(self.text, self.text_rect)  # show text

        self.value = self.valueFromBallPos()  # update value

    def changeColor(self):
        """
        Makes the color of the text change if the mouse is over it
        :param position: position of the thing you want to test is over the text
        """
        position = pygame.mouse.get_pos()
        if self.rect.left < position[0] < self.rect.right and self.rect.top < position[1] < self.rect.bottom:
            if self.custom is None:
                self.text = self.font.render(self.text_input + ": " + str(round(self.value)), True,
                                             self.hovering_color)
            else:
                self.text = self.font.render(self.text_input + ": " + self.custom[round(self.value)], True,
                                         self.hovering_color)
        else:
            if self.custom is None:
                self.text = self.font.render(self.text_input + ": " + str(round(self.value)), True,
                                             self.base_color)
            else:
                self.text = self.font.render(self.text_input + ": " + self.custom[round(self.value)], True,
                                             self.base_color)

    def valueFromBallPos(self):
        """
        :return: the value from the ball position mapped to the value range
        """
        # ball position on the slider converted to percentage
        value = ((self.slider_ball.centerx - self.slider_small_rect.left) /
                 (self.slider_small_rect.right - self.slider_small_rect.left))

        # map percentage on the value range
        value = value * (self.range[1] - self.range[0]) + self.range[0]

        return value

    def ballPosFromValue(self):
        """
        :return: ball position on the slider from the value
        """
        # value converted to percentage = (value - minimum value) / value range
        value = (self.value - self.range[0]) / (self.range[1] - self.range[0])
        # then mapped onto the slider's width
        pos = self.slider_small_rect.width * value + self.slider_small_rect.left

        return pos
