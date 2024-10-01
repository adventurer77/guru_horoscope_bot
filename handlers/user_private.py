from aiogram import F, types, Router
from aiogram.filters import CommandStart

from sqlalchemy.ext.asyncio import AsyncSession
from kbds.inline import MenuCallBack
from filters.chat_types import ChatTypeFilter

from aiogram.types import InputMediaPhoto

from database.orm_query import orm_get_zodiac
from handlers.menu_processing import get_menu_content


from api.api_horoscope import (
    get_daily_horoscope,
    get_monthly_horoscope,
    get_weekly_horoscope,
)
from kbds.inline import MenuCallBack

from aiogram.types import InputMediaPhoto


user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(["private"]))


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message, session: AsyncSession):
    media, reply_markup = await get_menu_content(session, level=0, menu_name="main")

    await message.answer_photo(
        media.media, caption=media.caption, reply_markup=reply_markup
    )


async def show_horoscope(
    callback: types.CallbackQuery, session: AsyncSession, zodiac_id: int, date: str
):
    zodiac = await orm_get_zodiac(session, zodiac_id=zodiac_id)

    if date == "WEEKLY":
        horoscope = get_weekly_horoscope(zodiac.name)
        horoscope_data = horoscope['data']['horoscope_data']
        period_info = f"*Horoscope for {zodiac.name} on {date}:*\
                        \n*Week*: {horoscope['data']['week']}"
    elif date == "MONTHLY":
        horoscope = get_monthly_horoscope(zodiac.name)
        horoscope_data = horoscope['data']['horoscope_data']
        period_info = f"*Horoscope for {zodiac.name} on {date}:*\
                        \n*Challenging days:* {horoscope['data']['challenging_days']}\
                        \n*Standout days:* {horoscope['data']["standout_days"]}\
                        \n*Month:* {horoscope['data']["month"]}"
    else:
        horoscope = get_daily_horoscope(zodiac.name, date)
        horoscope_data = horoscope['data']['horoscope_data']
        period_info = f"*Horoscope for {zodiac.name} on {date}:*"

    # First message: photo + title
    media = InputMediaPhoto(
        media=zodiac.image,
        caption=period_info,
        parse_mode="Markdown"
    )
    await callback.message.edit_media(media=media)

    # The second message: the text of the horoscope
    await callback.message.answer(horoscope_data, parse_mode="Markdown")


@user_private_router.callback_query(MenuCallBack.filter())
async def user_menu(
    callback: types.CallbackQuery, callback_data: MenuCallBack, session: AsyncSession
):

    if (
        callback_data.menu_name == "show_horoscope"
        and callback_data.zodiac_id
        and callback_data.date
    ):
        await show_horoscope(
            callback,
            session,
            zodiac_id=callback_data.zodiac_id,
            date=callback_data.date,
        )

    else:

        media, reply_markup = await get_menu_content(
            session,
            level=callback_data.level,
            menu_name=callback_data.menu_name,
            category=callback_data.category,
            page=callback_data.page,
            zodiac_id=callback_data.zodiac_id,  # Include zodiac_id for zodiac and horoscope steps
            # date=callback_data.date,  # Include date for horoscope step
        )

        await callback.message.edit_media(media=media, reply_markup=reply_markup)
    await callback.answer()



# Checking the message for the maximum number of characters under the photo
# if date == "WEEKLY":
    #     horoscope = get_weekly_horoscope(zodiac.name)
    #     horoscope_message = f"*Horoscope for {zodiac.name} on {date}:*\n\n{horoscope['data']['horoscope_data']}\n\n*Week*: {horoscope['data']['week']}"
    # elif date == "MONTHLY":
    #     horoscope = get_monthly_horoscope(zodiac.name)
    #     horoscope_message = f"*Horoscope for {zodiac.name} on {date}:*\n\nChallenging days: {horoscope['data']['challenging_days']}\n{horoscope['data']['horoscope_data']}"
    # else:
    #     horoscope = get_daily_horoscope(zodiac.name, date)
    #     horoscope_message = f"*Horoscope for {zodiac.name} on {date}:*\n\n{horoscope['data']['horoscope_data']}"

    # max_caption_length = 1024
    # if len(horoscope_message) > max_caption_length:
    #     # Split message into multiple parts
    #     media = InputMediaPhoto(media=zodiac.image)
    #     await callback.message.edit_media(media=media)

    #     await callback.message.answer(horoscope_message, parse_mode="Markdown")
    # else:
    #     # If the message is within the limit, send it normally
    #     media = InputMediaPhoto(
    #         media=zodiac.image, caption=horoscope_message, parse_mode="Markdown"
    #     )
    #     await callback.message.edit_media(media=media)
