import math, decimal, datetime
from PIL import Image
from pathlib import Path

dec = decimal.Decimal
BASE_DIR = Path(__file__).resolve().parent
IMG_DIR = BASE_DIR / "moon_images"


def position(now=None): 
    if now is None: 
        now = datetime.datetime.now()

    diff = now - datetime.datetime(2001, 1, 1)
    days = dec(diff.days) + (dec(diff.seconds) / dec(86400))
    lunations = dec("0.20439731") + (days * dec("0.03386319269"))

    return lunations % dec(1)

def phase(pos): 
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
        7: "Waning Crescent"
    }
    phase_name = phases[int(index) & 7]
    filename = f"{phase_name.replace(' ', '_').lower()}.jpg"
    image_path = IMG_DIR / filename
    return phase_name, image_path


def moon_phase_for_date(date_str):
    #date_str is the time we get from the user though ui ( it is defined there)

    try:
        input_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        pos=position(input_date)
        phase_name = phase(pos)
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return




    
    
    """return phase_name, f"moon_images/{phase_name.replace(' ', '_').lower()}.jpg"  # Path to the image"""
    """""

def display_image(image_path):
    try:
        img = Image.open(image_path)
        img.show()  # Display the image
    except FileNotFoundError:
        print(f"Image not found: {image_path}")

def main(): 
    # Ask the user to input a date
    user_input = input("Enter a date (YYYY-MM-DD): ")
    
    # Convert the user input to a datetime object
    try:
        input_date = datetime.datetime.strptime(user_input, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return
    
    pos = position(input_date)  # Use the input date instead of current date
    phasename, image_path = phase(pos)

    roundedpos = round(float(pos), 3)
    print(f"{phasename} ({roundedpos})")
    print(f"{pos: .2%} illuminated")
    
    # Display the corresponding image
    display_image(image_path)
    """
"""""
if __name__ == "__main__": 
    main()
    """
