from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class MenuCallBack(CallbackData, prefix="menu"):
    level: int
    menu_name: str
    category: int | None = None
    page: int = 1
    zodiac_id: int | None = None
    date: str | None = None


def get_user_main_btns(*, level: int, sizes: tuple[int]= (1,)):

    keyboard = InlineKeyboardBuilder()
    btns = {
        "Сatalog ⭐": "catalog",
        "About us ℹ": "about",
    }

    for text, menu_name in btns.items():
        if menu_name == 'catalog':
            keyboard.add(InlineKeyboardButton(text=text,
                    callback_data=MenuCallBack(level=level+1, menu_name=menu_name).pack()))
        else:
            keyboard.add(InlineKeyboardButton(text=text,
                    callback_data=MenuCallBack(level=level, menu_name=menu_name).pack()))
            
    return keyboard.adjust(*sizes).as_markup() 


def get_user_catalog_btns(*, level: int, categories: list, sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text="Back",
                                      callback_data=MenuCallBack(level=level-1, menu_name="main").pack()))
    
    for category in categories:
        keyboard.add(InlineKeyboardButton(text=category.name,
                                          callback_data=MenuCallBack(level=level+1,menu_name=category.name, category=category.id).pack()))

    return keyboard.adjust(*sizes).as_markup()



def get_zodiacs_btns(
    *,
    level: int,
    category: int,
    page: int,
    pagination_btns: dict,
    zodiac_id: int,
    sizes: tuple[int] = (2,)
):

    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text="Back",
                                            callback_data=MenuCallBack(level=level-1, menu_name="catalog").pack()))
    keyboard.add(InlineKeyboardButton(text="Select ⭐",
                                      callback_data=MenuCallBack(level=level + 1, menu_name="dates", zodiac_id=zodiac_id).pack()))

    keyboard.adjust(*sizes)

    row=[]
    for text, menu_name in pagination_btns.items():
        if menu_name == "next":
            row.append(InlineKeyboardButton(text=text,
                                            callback_data=MenuCallBack(
                                                level=level,
                                                menu_name=menu_name,
                                                category=category,
                                                page=page + 1).pack()))
            
        elif menu_name == "previous":
            row.append(InlineKeyboardButton(text=text,
                                            callback_data=MenuCallBack(
                                                level=level,
                                                menu_name=menu_name,
                                                category=category,
                                                page=page - 1).pack()))

    return keyboard.row(*row).as_markup()


def get_user_dates_btns(*, level: int, dates: list, zodiac_id: int, sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text="Back",
                                      callback_data=MenuCallBack(level=level-2, menu_name="catalog").pack())) #, zodiac_id=zodiac_id
    
    for date in dates:
        keyboard.add(InlineKeyboardButton(text=date.name,
                                          callback_data=MenuCallBack(level=level+1, menu_name="show_horoscope", zodiac_id=zodiac_id, date=date.name).pack())) #date=date.id

    return keyboard.adjust(*sizes).as_markup()


def get_callback_btns(*, btns: dict[str, str], sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()

    for text, data in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

    return keyboard.adjust(*sizes).as_markup()



