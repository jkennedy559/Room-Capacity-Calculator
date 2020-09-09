from itertools import product


class Room:
    def __init__(self, length, width):
        self.coordinates_dict = dict.fromkeys(product(range(length + 1), range(width + 1)), 'Empty')
        self.person_count = 0
        self.add_person(Person((0, 0)))

    def add_person(self, person):
        """Adds a person to the room if no one else in the person's safety perimeter"""
        checks = [check for check in person.buffer if check in self.coordinates_dict.keys()]
        person_checks = []
        for buffer_check in checks:
            if isinstance(self.coordinates_dict.get(buffer_check), Person):
                person_checks.append(True)
            else:
                person_checks.append(False)
        if any(person_checks):
            return False
        else:
            self.coordinates_dict.update({person.location: person})
            self.person_count += 1
            return True

    def maximise_people(self):
        """Add people to the room until no more can be added safely"""
        # TODO List of all available coordinates currently without a person
        # TODO Try and add a new person to any of these coordinates, if successfully repeat else return person count
        while True:
            coords = self.coordinates_dict.keys()
            available = [position for position in coords if not isinstance(self.position, Person)]

        pass


class Person:
    def __init__(self, location):
        self.location = location
        self.buffer = self.define_buffer_coordinates(location)

    def define_buffer_coordinates(self, location):
        buffer_coords = []
        adjustments = [(0, 1), (0, -1), (1, 0), (1, -1), (-1, 0), (-1, 1), (-1, -1), (1, 1)]
        for adjustment in adjustments:
            adj_length, adj_width = adjustment
            coord_length, coord_width = location
            buffer_coords.append((coord_length + adj_length, coord_width + adj_width))
        return buffer_coords


if __name__ == '__main__':
    room = Room(1, 3)
