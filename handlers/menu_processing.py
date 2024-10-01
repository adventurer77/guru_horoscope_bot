from aiogram.types import InputMediaPhoto
from sqlalchemy.ext.asyncio import AsyncSession

# from api.api_horoscope import get_daily_horoscope, get_monthly_horoscope, get_weekly_horoscope
from database.orm_query import (
    orm_get_banner,
    orm_get_categories,
    orm_get_dates,
    orm_get_zodiacs,
)
from kbds.inline import (
    get_user_catalog_btns,
    get_user_dates_btns,
    get_user_main_btns,
    get_zodiacs_btns,
)
from utils.paginator import Paginator


async def main_menu(session, level, menu_name):
    banner = await orm_get_banner(session, menu_name)
    image = InputMediaPhoto(media=banner.image, caption=banner.description)

    kbds = get_user_main_btns(level=level)

    return image, kbds


async def catalog(session, level, menu_name):
    banner = await orm_get_banner(session, menu_name)
    image = InputMediaPhoto(media=banner.image, caption=banner.description)

    categories = await orm_get_categories(session)
    kbds = get_user_catalog_btns(level=level, categories=categories)

    return image, kbds


def pages(paginator: Paginator):
    btns = dict()
    if paginator.has_previous():
        btns["◀ Previous"] = "previous"

    if paginator.has_next():
        btns["Next ▶"] = "next"

    return btns


async def zodiacs(session, level, category, page):

    zodiacs = await orm_get_zodiacs(session, category_id=category)

    paginator = Paginator(zodiacs, page=page)
    zodiac = paginator.get_page()[0]

    image = InputMediaPhoto(
        media=zodiac.image,
        caption=f"<strong>{zodiac.name}</strong>\
                \n<strong>Zodiac {paginator.page} of {paginator.pages}</strong>",
    )

    pagination_btns = pages(paginator)

    kbds = get_zodiacs_btns(
        level=level,
        category=category,
        page=page,
        pagination_btns=pagination_btns,
        zodiac_id=zodiac.id,
    )

    return image, kbds


async def dates(session, level, menu_name, zodiac_id):
    banner = await orm_get_banner(session, menu_name)
    image = InputMediaPhoto(media=banner.image, caption=banner.description)

    dates = await orm_get_dates(session)
    kbds = get_user_dates_btns(
        level=level,
        dates=dates,
        zodiac_id=zodiac_id,
    )

    return image, kbds


async def get_menu_content(
    session: AsyncSession,
    level: int,
    menu_name: str,
    category: int | None = None,
    page: int | None = None,
    zodiac_id: int | None = None,
    # date: str | None = None,
):

    if level == 0:
        return await main_menu(session, level, menu_name)
    elif level == 1:
        return await catalog(session, level, menu_name)
    elif level == 2:
        return await zodiacs(session, level, category, page)
    elif level == 3:
        return await dates(session, level, menu_name, zodiac_id)
    # elif level == 4:  # Step 4 to show horoscope based on zodiac and date
    #     return await show_horoscope(session, zodiac_id, date)


# async def show_horoscope(session, zodiac_id: int, date: str):

#     zodiac = await orm_get_zodiac(session, zodiac_id=zodiac_id)

#     if date == "WEEKLY":
#         horoscope = get_weekly_horoscope(zodiac.name)
#         #  Display the horoscope message
#         horoscope_message = f"*Horoscope for {zodiac.name} on {date}:*\n\n{horoscope['data']['horoscope_data']}\n\n*Week*: {horoscope['data']["week"]}"
#     elif date == "MONTHLY":
#         horoscope = get_monthly_horoscope(zodiac.name)
#         #  Display the horoscope message
#         horoscope_message = f"*Horoscope for {zodiac.name} on {date}:*\n\nChallenging days: {horoscope['data']['challenging_days']}\n{horoscope['data']['horoscope_data']}"
#     else:
#     # Generate or fetch horoscope for the selected zodiac sign and date
#         horoscope = get_daily_horoscope(zodiac.name, date)

#         # Display the horoscope message
#         horoscope_message = f"*Horoscope for {zodiac.name} on {date}:*\n\n{horoscope['data']['horoscope_data']}"

#     media = InputMediaPhoto(
#         media=zodiac.image,
#         caption=horoscope_message, parse_mode= "Markdown"
#     )

#     return media, None
