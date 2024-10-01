from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import (
    orm_change_banner_image,
    orm_get_categories,
    orm_add_zodiac,
    orm_delete_zodiac,
    orm_get_info_pages,
    orm_get_zodiac,
    orm_get_zodiacs,
    orm_update_zodiac,
)

from filters.chat_types import ChatTypeFilter, IsAdmin

from kbds.inline import get_callback_btns
from kbds.reply import get_keyboard


admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())


ADMIN_KB = get_keyboard(
    "Add zodiac sign",
    "Assortment",
    "Add/Change Banner",
    placeholder="Select an action",
    sizes=(2,),
)


@admin_router.message(Command("admin"))
async def admin_features(message: types.Message):
    await message.answer("What do you want to do?", reply_markup=ADMIN_KB)


@admin_router.message(F.text == 'Assortment')
async def admin_features(message: types.Message, session: AsyncSession):
    categories = await orm_get_categories(session)
    btns = {category.name : f'category_{category.id}' for category in categories}
    await message.answer("Select category", reply_markup=get_callback_btns(btns=btns))


@admin_router.callback_query(F.data.startswith('category_'))
async def starring_at_zodiac(callback: types.CallbackQuery, session: AsyncSession):
    category_id = callback.data.split('_')[-1]
    for zodiac in await orm_get_zodiacs(session, int(category_id)):
        await callback.message.answer_photo(
            zodiac.image,
            caption=f"<strong>{zodiac.name}</strong>",
            reply_markup=get_callback_btns(
                btns={
                    "Delete": f"delete_{zodiac.id}",
                    "Change": f"change_{zodiac.id}",
                },
                sizes=(2,)
            ),
        )
    await callback.answer()
    await callback.message.answer("OK, here is the list of zodiac signs ⏫")


@admin_router.callback_query(F.data.startswith("delete_"))
async def delete_zodiac_callback(callback: types.CallbackQuery, session: AsyncSession):
    zodiac_id = callback.data.split("_")[-1]
    await orm_delete_zodiac(session, int(zodiac_id))

    await callback.answer("Zodiac sign removed")
    await callback.message.answer("Zodiac sign removed!")


################# Micro FSM for loading/changing banners ############################

class AddBanner(StatesGroup):
    image = State()

# We send a list of information pages of the bot and enter the sending state photo
@admin_router.message(StateFilter(None), F.text == 'Add/Change Banner')
async def add_image2(message: types.Message, state: FSMContext, session: AsyncSession):
    pages_names = [page.name for page in await orm_get_info_pages(session)]
    await message.answer(f"Send a photo of the banner.\nIn the description, please indicate for which page:\
                         \n{', '.join(pages_names)}")
    await state.set_state(AddBanner.image)


# The handler for canceling and resetting the state should always be here,
# after we have just reached state number 1 (elementary sequence of filters)
@admin_router.message(StateFilter("*"), Command("cancel"))
@admin_router.message(StateFilter("*"), F.text.casefold() == "cancel")
async def cancel_handler_banner(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer("Action cancelled", reply_markup=ADMIN_KB)

# Add/change the image in the table (there are already pages recorded by name:
# main, catalog, about, dates
@admin_router.message(AddBanner.image, F.photo)
async def add_banner(message: types.Message, state: FSMContext, session: AsyncSession):
    image_id = message.photo[-1].file_id
    for_page = message.caption.strip()
    pages_names = [page.name for page in await orm_get_info_pages(session)]
    if for_page not in pages_names:
        await message.answer(f"Please enter a normal page title, for example:\
                         \n{', '.join(pages_names)}")
        return
    await orm_change_banner_image(session, for_page, image_id,)
    await message.answer("Banner added/changed.")
    await state.clear()

# ловим некоррекный ввод
@admin_router.message(AddBanner.image)
async def add_banner2(message: types.Message, state: FSMContext):
    await message.answer("Send a photo of the banner or cancel")

#########################################################################################



######################### FSM for adding/changing zodiac signs by admin ###################

class AddZodiac(StatesGroup):
    name = State()
    category = State()
    image = State()

    zodiac_for_change = None

    texts = {
        "AddZodiac:name": "Please re-enter the name:",
        "AddZodiac:category": "Please select the category again ⬆️",
        "AddZodiac:image": "This state is the last one, so...",
    }


# We enter the state of waiting for the input name
@admin_router.callback_query(StateFilter(None), F.data.startswith("change_"))
async def change_zodiac_callback(
    callback: types.CallbackQuery, state: FSMContext, session: AsyncSession
):
    zodiac_id = callback.data.split("_")[-1]

    zodiac_for_change = await orm_get_zodiac(session, int(zodiac_id))

    AddZodiac.zodiac_for_change = zodiac_for_change

    await callback.answer()
    await callback.message.answer(
        "Enter the name of the zodiac sign", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddZodiac.name)


# We enter the state of waiting for the input name
@admin_router.message(StateFilter(None), F.text == "Add zodiac sign")
async def add_zodiac(message: types.Message, state: FSMContext, session: AsyncSession):
    await message.answer(
        "Enter the name of the zodiac sign", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddZodiac.name)


# The handler for canceling and resetting the state should always be here,
# after we have just reached state number 1 (elementary sequence of filters)
@admin_router.message(StateFilter("*"), Command("cancel"))
@admin_router.message(StateFilter("*"), F.text.casefold() == "cancel")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    if AddZodiac.zodiac_for_change:
        AddZodiac.zodiac_for_change = None
    await state.clear()
    await message.answer("Actions cancelled", reply_markup=ADMIN_KB)


# Go back one step (to the previous state)
@admin_router.message(StateFilter("*"), Command("back"))
@admin_router.message(StateFilter("*"), F.text.casefold() == "back")
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state == AddZodiac.name:
        await message.answer(
            'There is no previous step, or enter the name of the zodiac sign or write "cancel"'
        )
        return

    previous = None
    for step in AddZodiac.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(
                f"Ok, you are back to the previous step. \n {AddZodiac.texts[previous.state]}"
            )
            return
        previous = step


# We catch data for the name state and then change the state to category
@admin_router.message(AddZodiac.name, F.text)
async def add_name(message: types.Message, state: FSMContext, session: AsyncSession):
    # Leave the name unchanged
    if message.text == "." and AddZodiac.zodiac_for_change:
        await state.update_data(name=AddZodiac.zodiac_for_change.name)
    else:
        if not (3 <= len(message.text) <= 150):
            await message.answer(
            "The name of the zodiac sign must not exceed 150 characters and be shorter than 3 characters." 
            "Re-enter the name"
            )
            return

        await state.update_data(name=message.text)

    categories = await orm_get_categories(session)
    btns = {category.name : str(category.id) for category in categories}
    await message.answer("Select category", reply_markup=get_callback_btns(btns=btns))
    await state.set_state(AddZodiac.category)


#  Handler to catch invalid inputs for state name
@admin_router.message(AddZodiac.name)
async def add_name2(message: types.Message, state: FSMContext):
    await message.answer("You have entered invalid data, please enter the text of the zodiac sign name.")


# Catch the category selection callback
@admin_router.callback_query(AddZodiac.category)
async def category_choice(callback: types.CallbackQuery, state: FSMContext , session: AsyncSession):
    if int(callback.data) in [category.id for category in await orm_get_categories(session)]:
        await callback.answer()
        await state.update_data(category=callback.data)
        await callback.message.answer("Upload Zodiac Sign Image")
        await state.set_state(AddZodiac.image)
    else:
        await callback.message.answer('Select a category from the buttons.')
        await callback.answer()

# We catch any incorrect actions except for pressing the category selection button
@admin_router.message(AddZodiac.category)
async def category_choice2(message: types.Message, state: FSMContext):
    await message.answer("Select a category from the buttons.")


# We catch data for the image state and then exit the states
@admin_router.message(AddZodiac.image, or_f(F.photo, F.text == "."))
async def add_image(message: types.Message, state: FSMContext, session: AsyncSession):
    # Leave the photo unchanged
    if message.text and message.text == "." and AddZodiac.zodiac_for_change:
        await state.update_data(image=AddZodiac.zodiac_for_change.image)

    elif message.photo:
        await state.update_data(image=message.photo[-1].file_id)
    else:
        await message.answer("Send a photo zodiac sign")
        return
    data = await state.get_data()
    try:
        if AddZodiac.zodiac_for_change:
            await orm_update_zodiac(session, AddZodiac.zodiac_for_change.id, data)
        else:
            await orm_add_zodiac(session, data)
        await message.answer("Zodiac sign added/changed", reply_markup=ADMIN_KB)
        await state.clear()

    except Exception as e:
        await message.answer(
            f"Error: \n{str(e)}\n",
            reply_markup=ADMIN_KB,
        )
        await state.clear()

    AddZodiac.zodiac_for_change = None

# We catch all other incorrect behavior for this state
@admin_router.message(AddZodiac.image)
async def add_image2(message: types.Message, state: FSMContext):
    await message.answer("Send a photo zodiac sign")




