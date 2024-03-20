import json
from field import Field

class Map:
    """
    represents the map for the game world
    """

    def __init__(self):
        self._width = 0
        self._height = 0
        self.fields = []

    def show_area(self, xcoord, ycoord, color, viewrange):
        ant_coord = (xcoord, ycoord)
        coordList = []
        for y in range(ycoord + viewrange, ycoord - viewrange - 1, -1):
            for x in range(xcoord - viewrange, xcoord + viewrange + 1):
                if (x, y) != ant_coord:
                    fieldType = Field.type

                    if fieldType == "ground":
                        if Field.food > 0:
                            coordList.append({"x-coordinates": x, "y-coordinates": y, "state": "food"})
                        elif Field.ants > 0:
                            if Field.hive == color:
                                coordList.append({"x-coordinates": x, "y-coordinates": y, "state": "home"})
                            else:
                                coordList.append({"x-coordinates": x, "y-coordinates": y, "state": "foe"})
                        else:
                            coordList.append({"x-coordinates": x, "y-coordinates": y, "state": "empty"})
                    if fieldType == "water":
                        coordList.append({"x-coordinates": x, "y-coordinates": y, "state": "water"})
                    if fieldType == "hive":
                        if Field.hive == color:
                            coordList.append({"x-coordinates": x, "y-coordinates": y, "state": "home"})
                    else:
                            coordList.append({"x-coordinates": x, "y-coordinates": y, "state": "hill"})
    def show_map(self):
        """
        show the map
        :return: the map
        """

        fieldType = Field.type
        for y in range(self._height, -1):
            for x in range(self._width):
                if fieldType == "ground":
                    if Field.food > 0:
                        self.fields.append({"x-coordinates": x, "y-coordinates": y, "state": {"Food": Field.food}})
                    elif Field.ants > 0:
                        self.fields.append({"x-coordinates": x, "y-coordinates": y, "state": {"Ant-Color": Field.ants}})
                    else:
                        self.fields.append({"x-coordinates": x, "y-coordinates": y, "state": {"Empty": "empty"}})
                elif fieldType == "water":
                    self.fields.append({"x-coordinates": x, "y-coordinates": y, "state": {"Water": "water"}})
                elif fieldType == "hive":
                    self.fields.append({"x-coordinates": x, "y-coordinates": y, "state": {"Hive-color": Field.hive}})
        return self.fields


if __name__ == '__main__':
    map = Map()

    print(map.show_map())

