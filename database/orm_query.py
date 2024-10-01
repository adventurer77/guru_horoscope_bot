from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Banner, Category, Date, Zodiac, User



############### Working with banners (information pages) ###############

async def orm_add_banner_description(session: AsyncSession, data: dict):
    #Add new or change existing ones by name
    #menu: main, about, dates, catalog
    query = select(Banner)
    result = await session.execute(query)
    if result.first():
        return
    session.add_all([Banner(name=name, description=description) for name, description in data.items()]) 
    await session.commit()


async def orm_change_banner_image(session: AsyncSession, name: str, image: str):
    query = update(Banner).where(Banner.name == name).values(image=image)
    await session.execute(query)
    await session.commit()


async def orm_get_banner(session: AsyncSession, page: str):
    query = select(Banner).where(Banner.name == page)
    result = await session.execute(query)
    return result.scalar()


async def orm_get_info_pages(session: AsyncSession):
    query = select(Banner)
    result = await session.execute(query)
    return result.scalars().all()


############################ Category ######################################

async def orm_get_categories(session: AsyncSession):
    query = select(Category)
    result = await session.execute(query)
    return result.scalars().all()

async def orm_create_categories(session: AsyncSession, categories: list):
    query = select(Category)
    result = await session.execute(query)
    if result.first():
        return
    session.add_all([Category(name=name) for name in categories]) 
    await session.commit()



############################ Dates ######################################

async def orm_get_dates(session: AsyncSession):
    query = select(Date)
    result = await session.execute(query)
    return result.scalars().all()

async def orm_create_dates(session: AsyncSession, dates: list):
    query = select(Date)
    result = await session.execute(query)
    if result.first():
        return
    session.add_all([Date(name=name) for name in dates]) 
    await session.commit()

############ Administrator: add/edit/delete zodiac sign ########################


async def orm_add_zodiac(session: AsyncSession, data: dict):
    obj = Zodiac(
        name=data["name"],
        image=data["image"],
        category_id=int(data["category"]),
        
    )
    session.add(obj)
    await session.commit()


async def orm_get_zodiacs(session: AsyncSession, category_id):
    query = select(Zodiac).where(Zodiac.category_id == int(category_id))
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_zodiac(session: AsyncSession, zodiac_id: int):
    query = select(Zodiac).where(Zodiac.id == zodiac_id)
    result = await session.execute(query)
    return result.scalar()


async def orm_update_zodiac(session: AsyncSession, zodiac_id: int, data):
    query = (
        update(Zodiac)
        .where(Zodiac.id == zodiac_id)
        .values(
            name=data["name"],
            image=data["image"],
            category_id=int(data["category"]),
        )
    )
    await session.execute(query)
    await session.commit()


async def orm_delete_zodiac(session: AsyncSession, zodiac_id: int):
    query = delete(Zodiac).where(Zodiac.id == zodiac_id)
    await session.execute(query)
    await session.commit()

##################### Adding a user to the database #####################################

async def orm_add_user(
    session: AsyncSession,
    user_id: int,
    first_name: str | None = None,
    last_name: str | None = None,
    phone: str | None = None,
):
    query = select(User).where(User.user_id == user_id)
    result = await session.execute(query)
    if result.first() is None:
        session.add(
            User(user_id=user_id, first_name=first_name, last_name=last_name, phone=phone)
        )
        await session.commit()




