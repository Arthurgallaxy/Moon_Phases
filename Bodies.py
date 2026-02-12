  def __init__(self, latitude, longitude, alive=True, date_time=None):
        # Initialize the cat's properties
        self.latitude = latitude
        self.longitude = longitude
        self.alive = alive
        self.date_time = date_time

    def set_position(self, latitude, longitude):
        # Update the cat's latitude and longitude
        self.latitude = latitude
        self.longitude = longitude

    def check_alive(self):
        # Check if the cat is alive
        return self.alive

    def set_date_time(self, date_time):
        # Set or update the observation time
        self.date_time = date_time
