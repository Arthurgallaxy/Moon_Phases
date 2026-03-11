#Importing libraries
import math, decimal, datetime
from PIL import Image
from pathlib import Path

dec = decimal.Decimal

#Define directory paths for the image files
BASE_DIR = Path(__file__).resolve().parent
IMG_DIR = BASE_DIR / "moon_images"

#Create the MoonPhaseCalculator class
class MoonPhaseCalculator:
    def __init__(self, img_dir):
        self.img_dir = Path(img_dir)

#Return the percentage of lumination
    @staticmethod
    def position(now=None):
        if now is None:
            now = datetime.datetime.now()

        diff = now - datetime.datetime(2001, 1, 1)
        days = dec(diff.days) + (dec(diff.seconds) / dec(86400))
        lunations = dec("0.20439731") + (days * dec("0.03386319269"))

        return lunations % dec(1)

#Method for the moon phase
    def phase(self, pos):
        index = (pos * dec(8)) + dec("0.5")
        index = math.floor(index)

        phases = {
            0: "New Moon",
            1: "Waxing Crescent",
            2: "First Quarter",
            3: "Waxing Gibbous",
            4: "Full Moon",
            5: "Waning Gibbous",
            6: "Last Quarter",
            7: "Waning Crescent",
        }

        phase_name = phases[int(index) & 7]
        filename = f"{phase_name.replace(' ', '_').lower()}.jpg"
        image_path = self.img_dir / filename

        return phase_name, image_path

#Converts a string into a daytime object
    @staticmethod
    def parse_date(date_str):
        return datetime.datetime.strptime(date_str, "%Y-%m-%d")

#Final calculation for the moonphase and error handeling
    def moon_phase_for_date(self, date_str):
        try:
            input_date = self.parse_date(date_str)
            pos = self.position(input_date)
            return self.phase(pos)
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return None




