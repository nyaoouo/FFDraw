import typing

import imgui

from nylib.utils.win32 import memory as ny_mem

if typing.TYPE_CHECKING:
    from . import XivMem


class TerritoryInfo:
    def __init__(self, main: 'XivMem'):
        self.main = main
        self.handle = main.handle
        self.p_territory, = main.scanner.find_point('0f ? ? * * * * 85 ? 48 89 5c 24')
        self.p_weather, = main.scanner.find_point('48 ? ? * * * * f3 ? ? ? ? 41 ? ? ? 48 ? ? ? ? ? ? 0f ? ? 48 ff 60')

    @property
    def territory_id(self):
        return ny_mem.read_uint(self.handle, self.p_territory)

    @property
    def layer_id(self):
        return ny_mem.read_uint(self.handle, self.p_territory + 4)

    @property
    def map_id(self):
        return ny_mem.read_uint(self.handle, self.p_territory + 8)

    @property
    def weather_id(self):
        return ny_mem.read_ubyte(self.handle, self.p_weather + 9)

    @property
    def weather_is_content(self):
        return ny_mem.read_ubyte(self.handle, self.p_weather + 0x14) == 1

    def render_debug(self):
        imgui.text(f'territory_id: {self.territory_id}')
        imgui.text(f'layer_id: {self.layer_id}')
        imgui.text(f'map_id: {self.map_id}')
        imgui.text(f'weather_id: {self.weather_id}')
        imgui.text(f'weather_is_content: {self.weather_is_content}')

