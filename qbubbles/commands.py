from typing import List, Tuple, Optional

from qbubbles.sprites import Sprite

from qbubbles.registry import Registry

from qbubbles.exceptions import ParserError

SPRITE = 0


class CommandParser(object):
    def __init__(self, command):
        import shlex
        self._cmdSplit = shlex.split(command, comments=True, posix=True)
        self.commmand = self._cmdSplit[0]
        if "=" in self.command:
            raise ParserError("Command cannot contain '='")
        self.kwargs, self.args = self._parse_params(*self._cmdSplit[1:])

    def _parse_params(self, *params):
        kwargs = {}
        args = []
        params: List[str]
        for param in params:
            if "=" in param:
                key, value = param.split("=", 1)
                kwargs[key] = value
            else:
                args.append(param)
        return kwargs, args

    def execute(self, command, *args, **kwargs):
        args: List[str]
        args2 = []
        command_class: BaseCommand = Registry.get_command(command)
        for index in range(0, len(command_class.args)):
            if command_class.args[index] == int:
                if args[index].isnumeric():
                    args2.append(int(args[index]))
                    continue
                return ParserError(f"Invalid type for argument {index}, it's not an integer")
            elif command_class.args[index] == float:
                if args[index].isdigit():
                    args2.append(float(args[index]))
                    continue
                return ParserError(f"Invalid type for argument {index}, it's not a float'")
            elif command_class.args[index] == SPRITE:
                if args[index] in [s.get_sname() for s in Registry.get_sprites()]:
                    args.append(Registry.get_sprite(args[index]))
                    continue
                if args[index].count(":") == 1:
                    return ParserError(f"No such sprite: {repr(args[index])}")
                return ParserError(f"Invalid type for argument {index}")
            else:
                raise ParserError(f"Invalid Command Argument type: {repr(command_class.args[index])}")
        command_class.execute(*args2, **kwargs)


class BaseCommand(object):
    def __init__(self):
        self.args = []

    def execute(self, *args, **kwargs) -> Optional[Tuple[str, str, bool]]:
        pass

    def get_description(self) -> str:
        pass

    def allow_helppage(self) -> str:
        pass

    def get_help(self) -> str:
        pass


class TeleportCommand(BaseCommand):
    def __init__(self):
        super(TeleportCommand, self).__init__()
        self.args = [int, int, SPRITES]

    def execute(self, x, y, sprites):
        pass
