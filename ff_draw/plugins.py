import typing

if typing.TYPE_CHECKING:
    from ff_draw.main import FFDraw


class FFDrawPlugin:
    main: 'FFDraw'

    def __init__(self, main):
        self.main = main

    def __init_subclass__(cls, **kwargs):
        super(FFDrawPlugin, cls).__init_subclass__()
        plugins.append(cls)

    def update(self, main: 'FFDraw'):
        pass

    def process_command(self, data: dict) -> bool:
        return False


plugins: list[typing.Type[FFDrawPlugin]] = []
