#importing necessary  modules
import pygame, math, random
from .exceptions import *
pygame.init()
#function to create a random rgb tuple(r,g,b)
def randomRGB():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


#Font object will define a font, which can then be used to generete text
class Font:
    "A class that is used to create sand store settings to create text"
    def __init__(self, size, color = None, shadow = None):
        self.size = size
        self.color = color
        self.shadow = shadow

    #changing the color of the text
    def change_color(self, color):
        "Changes the color of the font to given color"
        self.color = color

    #changing the shadow
    def change_shadow(self, shadow):
        "Changes the shadow of the font to given shadow"
        self.shadow = shadow

    #changing the size
    def change_size(self, size):
        "Changes font size to given size"
        self.size = size
    #PREVIOUS FUNCTIONS ONLY WORK IF THE TEXT
    #IS GENERATED EVERY TIME IN THE GAME LOOP
    #OR ELSE YOU'LL HAVE TO REGENERATE IT

    def generate_text(self, text: str):
        """
        Generate a Surface object of the perfect size containing some text
        Accordingly to the Font attributes
        """
        #we define the size of the jumps for the 3 different fonts
        if self.size == "small":
            x_increment = 6
            y_increment = 12
        elif self.size == "medium":
            x_increment = 17
            y_increment = 35
        elif self.size == "large":
            x_increment = 33
            y_increment = 65

        #we create a big surface, we'll "downscale" it later
        TextSurface = pygame.Surface((500, 500))
        #we fill it with a non used color, we'll key it out later
        if self.color == (255, 255, 255):
            text_chroma_color = (255, 0, 0)
            TextSurface.fill(text_chroma_color)
        else:
            text_chroma_color = (255, 255, 255)
            TextSurface.fill(text_chroma_color)

        #the text starts at (0, 0) and as you progress thru lines and rows they increase
        text_x = 0
        text_y = 0
        #we get the lines
        lines = text.split("\n")
        #longest line will be use when "downscaling" the surface
        longest_line = max(list([len(line) for line in lines]))

        #iteration thorugh the lines and rows + blitting
        #the letters when we encounter them
        for line in lines:
            for char in line:
                #if the char is a space we skip it but increase the x
                if char == " ":
                    text_x += x_increment
                else:
                    #this is where we handle errors like using unsupported characters
                    try:
                        letter = pygame.image.load("engine/Pixel_Text/"+ self.size + "/" + char + ".png")
                    except FileNotFoundError:
                        raise NotSupportedTextCharacter
                    #then we blit the letter
                    TextSurface.blit(letter, (text_x, text_y))
                    text_x += x_increment
                    #we repeat
            #we go back to the first raw and we go tho the next line
            text_x = 0
            text_y += y_increment
        #we create a nwe surface with the perfect size and blit the text over there
        newTextSurface = pygame.Surface((longest_line * x_increment ,len(lines) * y_increment))
        newTextSurface.blit(TextSurface, (0, 0))

        #if color is specified, we replace black with the color
        if self.color:
            newTextSurface_array = pygame.PixelArray(newTextSurface)
            newTextSurface_array.replace([0, 0, 0], self.color)
            newTextSurface = newTextSurface_array.make_surface()

        # then we set the chroma key of the surface
        newTextSurface.set_colorkey(text_chroma_color)

        #then we create some text the same way, it will be the shadow
        #if one is specified
        if self.shadow:
            ShadowSurface = pygame.Surface((500, 500))
            #we set the chroma key to an unused color
            if self.shadow[2] == (255, 255, 255):
                shadow_chroma_color = (255, 0, 0)
                ShadowSurface.fill(shadow_chroma_color)
            else:
                shadow_chroma_color = (255, 255, 255)
                ShadowSurface.fill(shadow_chroma_color)

            text_x = 0
            text_y = 0
            lines = text.split("\n")
            longest_line = max(list([len(line) for line in lines]))
            #we generate the text on the shadow surface
            for line in lines:
                for char in line:
                    if char == " ":
                        text_x += x_increment
                    else:
                        try:
                            letter = pygame.image.load("engine/Pixel_Text/"+ self.size + "/" + char + ".png")
                        except FileNotFoundError:
                            raise NotSupportedTextCharacter
                        ShadowSurface.blit(letter, (text_x, text_y))
                        text_x += x_increment
                text_x = 0
                text_y += y_increment
            #we create a new surface with the perfect size and blit the text over there
            newShadowSurface = pygame.Surface((longest_line * x_increment ,len(lines) * y_increment))
            newShadowSurface.blit(ShadowSurface, (0, 0))

            #if a color is specified, we change black to that color
            if self.shadow[2]:
                newShadowSurface_array = pygame.PixelArray(newShadowSurface)
                newShadowSurface_array.replace((0, 0, 0), self.shadow[2])
                newShadowSurface = newShadowSurface_array.make_surface()

            newShadowSurface.set_colorkey(shadow_chroma_color)

            #now we put those things togheter
            #first we create a surface that can hold both the shadow and the text
            #we know that the extra size given by the shadow is dependent on angle and distance
            x_comp = math.cos(math.radians(self.shadow[0])) * self.shadow[1]
            x_offs = abs(x_comp)
            y_comp = math.sin(math.radians(self.shadow[0])) * self.shadow[1]
            y_offs = abs(y_comp)
            finalSurface = pygame.Surface((newTextSurface.get_width() + x_offs, newTextSurface.get_height() + y_offs))

            final_chroma_color = (0, 0, 0)
            #we make sure that we don't key out any used color
            #or text will be invisible
            while final_chroma_color == self.color or final_chroma_color == self.shadow[2]:
                final_chroma_color = randomRGB()
            finalSurface.fill(final_chroma_color)

            #we define if the shadow is higher/lower and left/right
            #of the text, so we either blit the shadow in the
            #top left and move the text accordingly or blit the text
            #top left and move the shadow accordingly
            #this allows for shadows at 360 degrees
            if x_comp >= 0:
                text_x = 0
                shadow_x = x_offs
            else:
                shadow_x = 0
                text_x = x_offs

            if y_comp >= 0:
                text_y = 0
                shadow_y = y_offs
            else:
                shadow_y = 0
                text_y = y_offs

            #then we blit the shadow first, then the text
            finalSurface.blit(newShadowSurface, (shadow_x, shadow_y))
            finalSurface.blit(newTextSurface, (text_x, text_y))
            finalSurface.set_colorkey(final_chroma_color)
        else: #if the shadow was not specified, we just return the text surface
            finalSurface = pygame.Surface((newTextSurface.get_width(), newTextSurface.get_height()))
            finalSurface.fill(text_chroma_color)
            finalSurface.set_colorkey(text_chroma_color)
            finalSurface.blit(newTextSurface, (0, 0))

        return finalSurface #we return our pygame.Surface()
