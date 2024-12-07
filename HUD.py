import pygame as pg

class HUD():
    def __init__(self, screen, total_sugar, sugar_spout, buckets, level_count, gravity):
       self.screen = screen
       self.total_sugar = total_sugar
       self.sugar_spout = sugar_spout
       self.buckets = buckets
       self.level_count = level_count
       self.gravity = gravity


    
    def draw(self):
        total_sugar_text = self.font.render(f"Total Sugar: {self.total_sugar}", True, pg.Color('white'))
        self.screen.blit(total_sugar_text, (10, 10))

        # Draw count of sugar
        y_offset = 40
        for i, bucket in enumerate(self.buckets):
            bucket_sugar = bucket.collected_sugar
            needed_sugar = bucket.needed_sugar
            bucket_text = self.font.render(f"Bucket {i+1}: {bucket_sugar}/{needed_sugar}", True, pg.Color('white'))
            self.screen.blit(bucket_text, (10, y_offset))
            y_offset += 30


# Draw sugar left in spout
        spout_sugar_text = self.font.render(f"Spout Sugar: {self.spout_sugar}", True, pg.Color('white'))
        self.screen.blit(spout_sugar_text, (10, y_offset))
        
# Draw Level
        level_text = self.font.render(f"Level: {self.level_count}", True, pg.Color('white'))
        self.screen.blit(level_text, (10, y_offset + 30))
        
# Draw Gravity Direction
        gravity_text = self.font.render(f"Gravity: {self.gravity_direction}", True, pg.Color('white'))
        self.screen.blit(gravity_text, (10, y_offset + 60))


    def update(self, total_sugar, spout_sugar, buckets, level_count, gravity_direction):
# Update
        self.total_sugar = total_sugar
        self.spout_sugar = spout_sugar
        self.buckets = buckets
        self.level_count = level_count
        self.gravity_direction = gravity_direction