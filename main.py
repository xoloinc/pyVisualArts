#!/usr/bin/env python
#
#  Copyright (c) 2013, 2015, Corey Goldberg
#
#  Dev: https://github.com/cgoldberg/py-slideshow
#  License: GPLv3


import argparse
import random
import os
import pyglet
import pyglet_ffmpeg
from Lib.filesystem import getPaths

global step,img

pyglet_ffmpeg.load_ffmpeg()
player = pyglet.media.Player()
player.eos_action = 'pause'
source = pyglet.media.StreamingSource()
step=-1
mediatype="video"
video_x = 0
screens = pyglet.canvas.get_display().get_screens()
display = pyglet.canvas.get_display()
window = pyglet.window.Window(fullscreen=True,screen=screens[2])
pyglet.gl.glClearColor(1,1,1,1)

def is_video(file):
    extension = os.path.splitext(file)[1]
    return extension == '.mp4'

def next_file():
    global step
    step = step+1
    return image_paths[step % len(image_paths)]

def handle_player():    
    file = next_file()
    if is_video(file):
        play_video(file)
    else:
        play_image(file)

def play_video(file):
    global mediatype,video_x
    mediatype="video"
    player.eos_action = 'loop'
    MediaLoad = pyglet.media.load(file, streaming=True)
    player.queue(MediaLoad)
    player.play()
    player.seek(1)
    player.pause()
    video_x = window.width
    update_video_in()

def play_image(file):
    global mediatype, sprite, img
    mediatype="img"
    img = pyglet.image.load(file)
    sprite = pyglet.sprite.Sprite(img)
    sprite.scale = get_scale(window, img)
    sprite.x = window.width
    sprite.y = ((window.height - (int(img.height*sprite.scale)))/2)
    update_pan_in()
    
def update_video_in(dt='no'):
    global video_x
    if(video_x>0):
        video_x-=10
        pyglet.clock.schedule_once(update_video_in, 1/240.0)
    else:
        player.seek(0)
        player.play()

def update_video_out(dt='no'):
    global video_x
    player.seek(1)
    if(video_x>-window.width):
        video_x-=10
        pyglet.clock.schedule_once(update_video_out, 1/240.0)
    else:
        next_image()
    
def update_pan_in(dt='no'):
    
    if (sprite.x>((window.width - (int(img.width*sprite.scale)))/2)):
        sprite.x=sprite.x-15
        pyglet.clock.schedule_once(update_pan_in, 1/240.0)
    else:
        sprite.x=((window.width - (int(img.width*sprite.scale)))/2)
        pyglet.clock.schedule_once(update_pan_out, 6.0)

def update_pan_out(dt='no'):
    if (sprite.x>-window.width):
        sprite.x=sprite.x-15
        pyglet.clock.schedule_once(update_pan_out, 1/240.0)
    else:
        next_image()

def get_scale(window, image):
    if image.width > image.height:
        scale = float(window.width) / image.width
    else:
        scale = float(window.height) / image.height
    return scale

def next_image(dt="no"):
    handle_player()


#platform = window.get_platform()


@player.event
def on_player_eos():
    update_video_out()




@window.event
def on_draw():
    global video_x
    window.clear()
    if (mediatype == "video"):
        if player.source and player.source.video_format:
           scale = get_scale(window, player.source.video_format)
           #player.get_texture().blit(((window.width - (int(player.source.video_format.width*scale)))/2), ((window.height - (int(player.source.video_format.height*scale)))/2),width=window.width,height=player.source.video_format.height*scale)
           player.get_texture().blit(video_x, ((window.height - (int(player.source.video_format.height*scale)))/2),width=window.width,height=player.source.video_format.height*scale)
    else:
        sprite.draw()


if __name__ == '__main__':
    #_pan_speed_x, _pan_speed_y, _zoom_speed = update_pan_zoom_speeds()
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', help='directory of images',
                        nargs='?', default=os.getcwd())
    args = parser.parse_args()
    image_paths = getPaths.get_image_paths(args.dir)
    handle_player()
    pyglet.app.run()
    
