#############################################################
# Module Name: Sugar Pop level Module
# Project: Sugar Pop Program
# Date: Nov 17, 2024
# By: Brett W. Huffman
# Description: The level implementation of the sugar pop game
#############################################################

import json
import os

class Level:
    def __init__(self, level_file=None):
        """
        Initialize a Level object.

        :param level_file: Path to the JSON file for the level. If None, an empty level is created.
        """
        self.level_file = level_file
        self.data = {
            "number_sugar_grains": 0,
            "statics": [],
            "buckets": [],
            "time_to_complete_level": 0,
        }
        
        if level_file:
            self.load_level(level_file)

    def load_level(self, level_file):
        """
        Load a level from a JSON file.

        :param level_file: Path to the JSON file to load the level from.
        """
        if not os.path.isfile(level_file):
            print(f"Level file not found: {level_file}")
            self.data = {}
            return

        try:
            with open(level_file, 'r') as f:
                self.data = json.load(f)

            # Validate the loaded data
            if not isinstance(self.data, dict):
                raise ValueError("Level data is not a dictionary.")
            
            self.statics = self.data.get("statics", [])
            self.buckets = self.data.get("buckets", [])

        except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
            print(f"Error loading level: {e}")
            self.data = {}

    def save_level(self, level_file=None):
        """
        Save the current level to a JSON file.

        :param level_file: Path to save the level. If None, uses the current level_file.
        """
        if level_file:
            self.level_file = level_file

        if not self.level_file:
            raise ValueError("No file specified to save the level.")

        try:
            with open(self.level_file, 'w') as f:
                json.dump(self.data, f, indent=4)
        except Exception as e:
            print(f"Error saving level: {e}")

    def add_static_box(self, x1, y1, x2, y2, color='white', line_width=2, friction=0.5, restitution=0.5):
        """
        Add a static box to the level.

        :param x1, y1, x2, y2: Coordinates for the static box.
        :param color: Color of the box (default is white).
        :param line_width: Line width for the box.
        :param friction: Friction value for the box.
        :param restitution: Restitution value for the box.
        """
        self.data["statics"].append({
            "x1": x1,
            "y1": y1,
            "x2": x2,
            "y2": y2,
            "color": color,
            "line_width": line_width,
            "friction": friction,
            "restitution": restitution,
        })

    def add_bucket(self, x, y, width, height, needed_sugar):
        """
        Add a bucket to the level.

        :param x: X-coordinate of the bucket.
        :param y: Y-coordinate of the bucket.
        :param width: Width of the bucket.
        :param height: Height of the bucket.
        :param needed_sugar: Amount of sugar needed to fill the bucket.
        """
        self.data["buckets"].append({
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "needed_sugar": needed_sugar
        })

    def set_number_sugar_grains(self, count):
        """
        Set the total number of sugar grains for the level.

        :param count: Total number of sugar grains.
        """
        self.data["number_sugar_grains"] = count

    def set_time_to_complete(self, time_in_seconds):
        """
        Set the time to complete the level.

        :param time_in_seconds: Time in seconds to complete the level.
        """
        self.data["time_to_complete_level"] = time_in_seconds

