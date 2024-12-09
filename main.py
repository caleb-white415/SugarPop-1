#############################################################
# Module Name: Sugar Pop Main Module
# Project: Sugar Pop Program
# Date: Nov 17, 2024
# By: Brett W. Huffman
# Description: The main implementation of the sugar pop game
#############################################################


import pygame as pg
import pymunk  # Import Pymunk library
import sys
from settings import *
import random
import statics
import dynamic_item
import sugar_grain
import bucket
import level
import message_display
import HUD
from sound_class import SoundManager


class Game:
    def __init__(self) -> None:
        pg.init()
        pg.mixer.init()
        self.sound_class = SoundManager()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.iter = 0
        
        
        self.font = pg.font.SysFont(None, 36)  

        self.FPS = 60
        self.current_level = 1
        self.level_complete = False
        self.space = pymunk.Space()
        self.space.gravity = (0, -9)  
        self.space.iterations = 30 
        self.is_paused = False

        self.drawing_lines = []
        self.sugar_grains = []
        self.buckets = []
        self.statics = []
        self.total_sugar_count = None
        self.level_spout_position = None
        self.level_grain_dropping = None
        self.mouse_down = False
        self.current_line = None
        self.message_display = message_display.MessageDisplay(font_size=72)
        self.gravity_up = False
        self.exploded = False

        
        
        self.intro_image = pg.image.load("./images/SugarPop.png").convert() 
        
        scale_height = self.intro_image.get_height() * WIDTH / self.intro_image.get_width()
        self.intro_image = pg.transform.scale(self.intro_image, (WIDTH, int(scale_height)))  
        
        pg.time.set_timer(LOAD_NEW_LEVEL, 2000)  

    def explode(self):
        self.exploded = True

    def load_level(self, levelnumber=0):
        
        for item in self.sugar_grains:
            item.delete() 
        for item in self.drawing_lines:
            item.delete() 
        for item in self.buckets:
            item.delete() 
        for item in self.statics:
            item.delete() 
        self.sugar_grains = []
        self.drawing_lines = []  
        self.buckets = []
        self.statics = []
        self.data = {}  
        self.level_spout_position = (0, 0) 
        self.current_level += 0
 
        new_level = LEVEL_FILE_NAME.replace("X", str(levelnumber))
        self.level = level.Level(new_level)
        
        
        if not self.level or not self.level.data:
            return False
        else:  
            self.level_grain_dropping = False
            self.level_spout_position = (
            self.data.get('spout_x', 0),  # Default to 0 if 'spout_x' is missing
            self.data.get('spout_y', 0)   # Default to 0 if 'spout_y' is missing
            )

            self.build_main_walls()

            # Load buckets
            for nb in self.level.data['buckets']:
                self.buckets.append(bucket.Bucket(self.space, nb['x'], nb['y'], nb['width'], nb['height'], nb['needed_sugar']))
                
            # Load static items
            for nb in self.level.data['statics']:
                self.statics.append(statics.StaticItem(self.space, nb['x1'], nb['y1'], nb['x2'], nb['y2'], nb['color'], nb['line_width'], nb['friction'], nb['restitution']))
                self.total_sugar_count = self.level.data['number_sugar_grains']
                pg.time.set_timer(START_FLOW, 5 * 1000)  # 5 seconds
                self.message_display.show_message("Level Up", 10)
                self.level_complete = False
                return True

    def build_main_walls(self):
        '''Build the walls, ceiling, and floor of the screen'''
        # Floor
        floor = statics.StaticItem(self.space, 0, 0, WIDTH, 0, 'red', 5)
        self.statics.append(floor)
        # Left Wall
        left_wall = statics.StaticItem(self.space, 0, 0, 0, HEIGHT, 'red')
        self.statics.append(left_wall)
        # Right Wall
        right_wall = statics.StaticItem(self.space, WIDTH, 0, WIDTH, HEIGHT, 'red')
        self.statics.append(right_wall)
        # Ceiling
        ceiling = statics.StaticItem(self.space, 0, HEIGHT, WIDTH, HEIGHT, 'red')
        self.statics.append(ceiling)
    
    def check_all_buckets_exploded(self):
        """
        Check if all buckets have exploded.
        """
        for bucket in self.buckets:
            if not bucket.exploded:  
                return False  
            return True  


    def update(self):
        '''Update the program physics'''
        
        if self.is_paused:
            return
        
        
        self.iter += 1
        
        
        delta_time = self.clock.tick(FPS) / 1000.0  

       
        time_step = min(delta_time, MAX_TIME_STEP)

        
        self.space.step(time_step)
        
        if self.iter == 60:
            self.iter = 0

        pg.display.set_caption(f'fps: {self.clock.get_fps():.1f}')
        
        
        if self.iter % 20 == 0:
            
            self.message_display.update()
            
    
        for bucket in self.buckets:
            if bucket.count >= bucket.needed_sugar:
                bucket.explode(self.sugar_grains)  
            if not bucket.exploded:  
                bucket.exploded = True
            else:
                bucket.count_reset() 


        if not self.level_complete and self.check_all_buckets_exploded():
            self.level_complete = True
            self.message_display.show_message("Level Complete!", 3)
            pg.time.set_timer(LOAD_NEW_LEVEL, 2000)  

           
        for grain in self.sugar_grains:
                for bucket in self.buckets:
                    bucket.collect(grain)
                
            # Drop sugar if needed
        if self.level_grain_dropping:
                # Create new sugar to drop
                new_sugar = sugar_grain.sugar_grain(self.space, self.level_spout_position[0], self.level_spout_position[1], 0.1)
                self.sugar_grains.append(new_sugar)
                # Check if it's time to stop
                if len(self.sugar_grains) >= self.total_sugar_count:
                    self.level_grain_dropping = False

    def draw_hud(self):
        """Draw the HUD displaying the number of grains."""
        # Prepare the text surface
        if self.total_sugar_count:
            text_surface = self.font.render(f'{self.total_sugar_count - len(self.sugar_grains)}', True, (255, 255, 255))
            # Draw the text surface on the screen
            self.screen.blit(text_surface, (10, 10))  # Position at top-left corner

    def draw(self):
        '''Draw the overall game. Should call individual item draw() methods'''
        # Clear the screen
        self.screen.fill('black')

        # Only show the intro screen if we haven't loaded a level yet
        if self.intro_image:
            self.screen.blit(self.intro_image, (0, 0))  # Draw the intro image
    
        for bucket in self.buckets:
            bucket.draw(self.screen)

        # Draw each sugar grain
        for grain in self.sugar_grains:
            grain.draw(self.screen)

        # Draw the current dynamic line
        if self.current_line is not None:
            self.current_line.draw(self.screen)
        
        # Draw the user-drawn lines
        for line in self.drawing_lines:
            line.draw(self.screen)
            
        # Draw any static items
        for static in self.statics:
            static.draw(self.screen)

        # Draw the nozzle (Remember to subtract y from the height)
        if self.level_spout_position:
            pg.draw.line(
                self.screen, 
                (255, 165, 144), 
                (self.level_spout_position[0], HEIGHT - self.level_spout_position[1] - 10), 
                (self.level_spout_position[0], HEIGHT - self.level_spout_position[1]), 
                5
            )
        
        # Draw the heads-up display
        self.draw_hud()

        # Show any messages needed        
        self.message_display.draw(self.screen)

        # Update the display
        pg.display.update()

    def check_events(self):
        '''Check for keyboard and mouse events'''
        for event in pg.event.get():
            if event.type == EXIT_APP or event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

            # Implementing level restart
            elif event.type == pg.KEYDOWN and event.key == pg.K_r:
                self.current_level -= 1
                pg.time.set_timer(LOAD_NEW_LEVEL, 100)  # Load level

            
            # Implementing a pause
            elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                if self.is_paused:
                    self.is_paused = False        
                else:
                    self.message_display.show_message("Paused", 2)  # Show Paused
                    self.is_paused = True
                
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.mouse_down = True
                # Get mouse position and start a new dynamic line
                mouse_x, mouse_y = pg.mouse.get_pos()
                self.current_line = dynamic_item.DynamicItem(self.space, 'blue')
                self.current_line.add_vertex(mouse_x, mouse_y)
                
            elif event.type == pg.MOUSEBUTTONUP:
                self.mouse_down = False
                if self.current_line:
                    self.drawing_lines.append(self.current_line)
                    self.current_line = None
                
            elif event.type == pg.MOUSEMOTION and self.mouse_down:
                # Get mouse position
                mouse_x, mouse_y = pg.mouse.get_pos()
                if mouse_x == 0 or mouse_x == WIDTH or mouse_y == 0 or mouse_y == HEIGHT:
                    self.mouse_down = False
                if self.current_line and self.iter % 10 == 0:
                    self.current_line.add_vertex(mouse_x, mouse_y)

            elif event.type == START_FLOW:
                self.level_grain_dropping = True
                # Disable the timer after the first trigger
                pg.time.set_timer(START_FLOW, 0)
                
            elif event.type == LOAD_NEW_LEVEL:
                pg.time.set_timer(LOAD_NEW_LEVEL, 0)  
                self.intro_image = None
                self.current_level += 1
                if not self.load_level(self.current_level):
                    self.message_display.show_message("You Win!", 5)  
                    
                else:
                    self.message_display.show_message(f"Level {self.current_level} Start!", 2)
                    
    def run(self):
        '''Run the main game loop'''
        while True:
            self.check_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)


def main():
    game = Game()
    game.run()

if __name__ == '__main__':
    main()
