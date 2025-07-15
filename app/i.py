# Файл содержит импорты для наиболее часто-используемых моделей
# импортируйте его в начале работы с manage.py shell

import curses
import locale
import numbers
from collections import *
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from functools import reduce

from django.conf import settings
from django.db import models
from django.db.models import *
from django.db.models import base as django_db_models_base

from base.models import *
from core.choices import *
from core.controllers import *
from core.lib import *
from core.models import *

locale.setlocale(locale.LC_ALL, "")
code = locale.getpreferredencoding()

stdscr = curses.initscr()
_max_results, _ = stdscr.getmaxyx()
_max_results -= 10
curses.endwin()


def iget(self, *args, **kwargs):
    manager = self._meta.managers[0]

    if len(args) == 1 and len(kwargs) == 0:
        name = args[0]
        if isinstance(name, numbers.Number):
            q = Q(pk=name)
        else:
            char_field_names = [
                f.name for f in self._meta.fields if type(f) == models.fields.CharField
            ]
            q = reduce(
                lambda acc, field_name: acc
                | Q(**{"{}__contains".format(field_name): name}),
                char_field_names,
                Q(),
            )
    elif len(args) != 0:
        raise ValueError(
            "Передавайте в iget либо один аргумент либо используйте именованные параметры"
        )
    else:
        q = Q(**kwargs)

    objects_count = manager.filter(q).count()
    if objects_count == 1:
        obj = manager.get(q)
        print(obj)
        return obj
    elif objects_count == 0:
        print("Нет подходящих записей")
        return None
    else:
        obj = prompt_option(
            "Найдено несколько записей.\n\nВыберите:",
            [{"value": obj, "title": str(obj)} for obj in manager.filter(q)],
        )
        print(obj)
        return obj


django_db_models_base.ModelBase.iget = iget


def prompt_option(prompt, options):
    def character(stdscr):
        if len(options) > _max_results:
            return None

        attributes = {}
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        attributes["normal"] = curses.color_pair(1)

        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
        attributes["highlighted"] = curses.color_pair(2)

        c = 0  # last character read
        option = 0  # the current option that is marked
        while c != 10:  # Enter in ascii
            stdscr.erase()
            stdscr.addstr("{}\n".format(prompt), curses.A_UNDERLINE)
            for i in range(len(options)):
                if i == option:
                    attr = attributes["highlighted"]
                else:
                    attr = attributes["normal"]
                stdscr.addstr("{0}. ".format(i + 1))
                stdscr.addstr(
                    "#{} {}\n".format(options[i]["value"].pk, options[i]["title"]), attr
                )
            c = stdscr.getch()
            if c == curses.KEY_UP and option > 0:
                option -= 1
            elif c == curses.KEY_DOWN and option < len(options) - 1:
                option += 1

        return options[option]["value"]

    result = curses.wrapper(character)
    if result is None:
        print(
            "Найдено {} записей. Это более {} записей, помещающихся на экране. Уточните критерий отбора.".format(
                len(options), _max_results
            )
        )
        print(
            "Показаны первые 200 опций:\n{}".format(
                "\n".join([str(x["title"]) for x in options])
            )
        )
        return options[0]["value"]

    return result


def tabs(*args, **kwargs):
    separator = kwargs.get("separator", "\t")
    return separator.join([str(a).strip().replace(separator, " ") for a in args])


def stub():
    return lambda: None
