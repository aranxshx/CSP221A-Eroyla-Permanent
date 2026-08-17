import logging

logging.basicConfig(level=logging.INFO)
from abc import ABC, abstractmethod
from functools import wraps

# 1.6 decorator using functools.wraps
def log_action(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        logging.info(f"{self.name} is starting task: {func.__name__}...")
        result = func(self, *args, **kwargs)
        logging.info(f"{self.name} finished task: {func.__name__}")
        return result
    return wrapper

# 1.4 custom exception
class InsufficientBatteryError(Exception):
    def __init__(self, name, required, available):
        message = f"{name} needs {required}% battery for this task, but only has {available}%."
        super().__init__(message)
        self.name = name
        self.required = required
        self.available = available

# 1.1 robot abstract base class
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

    def use_battery(self, amount):
        if amount > self.battery:
            raise InsufficientBatteryError(self.name, amount, self.battery)
        self.battery -= amount

    # 1.7 alternative constructor
    @classmethod
    def from_config(cls, config):
        return cls(name=config["name"], battery=config.get("battery", 100))

    @abstractmethod
    def perform_task(self):
        pass

# 1.2 subclass - coffeeblenderrobot 
class CoffeeBlenderRobot(Robot):
    def __init__(self, name, battery=100, bean_supply=50):
        super().__init__(name, battery)
        self.bean_supply = bean_supply

    @log_action 
    def perform_task(self):
        cost = 20
        self.use_battery(cost)
        self.bean_supply -= 5
        return f"{self.name} brewed a coffee. Beans remaining: {self.bean_supply}."

# 1.2 subclass - dispenserrobot
class DispenserRobot(Robot):
    def __init__(self, name, battery=100, cup_supply=50):
        super().__init__(name, battery)
        self.cup_supply = cup_supply

    def perform_task(self):
        cost = 10
        self.use_battery(cost)
        self.cup_supply -= 1
        return f"{self.name} dispensed a cup. Cups remaining: {self.cup_supply}."

# 1.3 fleet report - polymorphism in practice
def fleet_report(robots):
    print("--- Fleet Report ---")
    for robot in robots:
        print(str(robot))

# 1.5 full try/except/else/finally
def run_task_safely(robot, **kwargs):
    try:
        result = robot.perform_task(**kwargs)
    except InsufficientBatteryError as e:
        logging.error(e)
    else:
        print(result)
    finally:
        print(f"[{robot.name}] Current battery: {robot.battery}%")

# 1.8 mutable class attribute trap - buggy
class BuggyOrderTracker:
    orders = []

    def add_order(self, order):
        self.orders.append(order)

# 1.8 mutable class attribute trap - fixed
class FixedOrderTracker:
    def __init__(self):
        self.orders = []

    def add_order(self, order):
        self.orders.append(order)

if __name__ == "__main__":
    blender = CoffeeBlenderRobot("Brew-Bot", battery=100)
    dispenser = DispenserRobot("Cup-Bot", battery=100)
    weak_dispenser = DispenserRobot("Weak-Bot", battery=5)

    fleet = [blender, dispenser, weak_dispenser]
    fleet_report(fleet)

    print()
    print("--- Running Tasks ---")
    run_task_safely(blender)
    print()
    run_task_safely(dispenser)
    print()
    run_task_safely(weak_dispenser)

    print()
    fleet_report(fleet)

    print()
    print("--- Buggy version ---")
    t1 = BuggyOrderTracker()
    t2 = BuggyOrderTracker()
    t1.add_order("Order A")
    print("t1 orders:", t1.orders)
    print("t2 orders:", t2.orders)

    print("--- Fixed version ---")
    f1 = FixedOrderTracker()
    f2 = FixedOrderTracker()
    f1.add_order("Order A")
    print("f1 orders:", f1.orders)
    print("f2 orders:", f2.orders)

    print()
    print("--- from_config demo ---")
    config = {"name": "Config-Bot", "battery": 30}
    config_blender = CoffeeBlenderRobot.from_config(config)
    print(str(config_blender))
    print(type(config_blender))