#imorting necessary modules
import pygame, os
from .exceptions import *

class _Animation:
    "A class to store one animation, path"
    def __init__(self, path, frames_duration, loop = True):
        #the list is going to hold a status for each frame
        #example: run_o for 3 frames and run_1 for 4 is-->
        #["run_0", "run_0", "run_0", "run_1", "run_1", "run_1", "run_1"]
        self.data = []
        #the path is the path to the folder, example, for the running animation
        #the path would be "animations/player/run" with no slash at the end
        self.path = path
        #we get the animation name from the folder name
        self.name = path.split("/")[-1]
        #we set the duration to 0 and increase it later
        self.duration = 0
        #weather or not it should loop
        self.loop = loop

        #we iterate for the different frame durations, example [7, 7]
        #and we add the first frame 7 times, the second frames 7 times
        #and we have an animation of 14 frames in total
        #the name of the animation HAS to be in the format [animation name]_[order number].png
        n = 0
        for frame_duration in frames_duration:
            image_id = self.name + "_" + str(n)
            self.duration += frame_duration
            for i in range(frame_duration):
                self.data.append(image_id)
            n +=1


class AnimationDatabase:
    "A class to store animation data about an object/entity, with useful methods to modify it's status"
    def __init__(self):
        #the object has currently no animation, it's at frame 0 and doesn't have a status so no animation will play
        self.animations = {}
        self.frame = 0
        self.status = None
    #with this we can load animations and add them to the animations dictionary
    #giving it a folder path(ie. "animations/player/run"), frame durations (ie. [7,7])
    # and telling it to loop or not we can create a new animation and add it to the
    #dictonary, the key for it will be it's name, or the folder name(ie. "run")
    def add_animation(self, path, frames_duration, loop = True):
        a = _Animation(path, frames_duration, loop)
        self.animations[a.name] = a
    #The update function simply updates the frame we should render every time
    #it is called y the get_current_image which is called every frame so no need to
    #call it yourself
    def _update(self):
        if self.frame < self.animations[self.status].duration - 1:
            self.frame += 1
        else:
            if self.animations[self.status].loop:
                self.frame = 0
            else:
                pass
    #with this we can change the animation of the entity
    #if the animation id isn't found, an AnimationIDNotFound exception
    #will be raised
    def change_animation(self, new_animation):
        #if the animation id is available, then go on
        #else raise an exception
        if new_animation in self.animations:
            pass
        else:
            raise AnimationIDNotFound
        #then we check if the action isn't already playing, if it's not
        #we reset the frame to 0 and the status to the new animation
        #we reset from 0 so it starts from the beginning and to avoid
        #IndexError: list index out of range
        if self.status != new_animation:
            self.status = new_animation
            self.frame = 0
    #this gets the current frame name without the ".png" or path behind it
    #it is called by the get_current_image so no need to call it yourself
    def _get_current_frame(self):
        #it searches for the current status in the dictionary and gets the animation
        #then access its data and then goes to the right frame number in the list
        return self.animations[self.status].data[self.frame]
    def get_current_image(self):
        #it updates the frame number and then gives you the full path to the image
        #which you can use
        #if the function is called 60 times per second you'll get variable that changes every 1/60th of a second
        #and have an animation
        self._update()
        return self.animations[self.status].path + "/" + self._get_current_frame() + ".png"
