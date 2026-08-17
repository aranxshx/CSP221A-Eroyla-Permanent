from abc import ABC, abstractmethod

class Robot(ABC):
    manufacturer = "Ritwal"
    population = 0

    def __init__(self, name, battery=100):
        self.name = name
        self.battery = 0
        self.battery = battery
        Robot.population += 1

    @property
    def battery(self):
        return self._battery

    @battery.setter
    def battery(self, value):
        if value < 0:
            self._battery = 0
        elif value > 100:
            self._battery = 100
        else:
            self._battery = value

    def __str__(self):
        return f"{self.name} ({self.battery}% battery)"

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r}, battery={self.battery!r})"

    @abstractmethod
    def perform_task(self):
        pass

if __name__ == "__main__":
    r1 = Robot("Bot1", battery=150)