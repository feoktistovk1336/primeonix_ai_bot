from aiogram import Router, F
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery

from database.db import (
    activate_tariff,
    get_subscription_info,
    get_tariff_info,
    get_feature_limit,
    get_daily_usage
)
from keyboards import tariffs_menu


router = Router()


TARIFFS_FOR_PAYMENT = {
    "💎 Start Premium": {
        "code": "start_premium",
        "title": "Start Premium",
        "stars": 30,
        "days": 30,
        "description": "+2 генерации в день к каждому блоку"
    },
    "➕ Plus": {
        "code": "plus",
        "title": "Plus",
        "stars": 50,
        "days": 30,
        "description": "+4 генерации в день к каждому блоку"
    },
    "🔥 VIP": {
        "code": "vip",
        "title": "VIP",
        "stars": 100,
        "days": 30,
        "description": "+7 генераций в день к каждому блоку + лучше картинки"
    },
    "👑 Premium": {
        "code": "premium",
        "title": "Premium",
        "stars": 160,
        "days": 30,
        "description": "+10 генераций в день + premium картинки"
    },
    "🚀 PRO": {
        "code": "pro",
        "title": "PRO",
        "stars": 500,
        "days": 30,
        "description": "Безлимитный доступ ко всем функциям"
    }
}


@router.message(F.text.in_({"💎 Подписка", "💎 PRO"}))
async def subscription(message: Message):
    await message.answer(
        "💎 Подписка\n\n"
        "Выбери тариф:\n\n"
        "💎 Start Premium — 30 Stars\n"
        "+2 генерации в день к каждому блоку.\n\n"
        "➕ Plus — 50 Stars\n"
        "+4 генерации в день к каждому блоку.\n\n"
        "🔥 VIP — 100 Stars\n"
        "+7 генераций в день + лучше картинки.\n\n"
        "👑 Premium — 160 Stars\n"
        "+10 генераций в день + premium картинки.\n\n"
        "🚀 PRO — 500 Stars\n"
        "Безлимитный доступ ко всем функциям.",
        reply_markup=tariffs_menu
    )


@router.message(F.text.in_(list(TARIFFS_FOR_PAYMENT.keys())))
async def buy_tariff(message: Message):
    tariff = TARIFFS_FOR_PAYMENT[message.text]

    await message.answer_invoice(
        title=f"Тариф {tariff['title']}",
        description=tariff["description"],
        payload=f"tariff:{tariff['code']}:{tariff['days']}",
        currency="XTR",
        prices=[
            LabeledPrice(
                label=tariff["title"],
                amount=tariff["stars"]
            )
        ],
        provider_token=""
    )


@router.pre_checkout_query()
async def pre_checkout(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


@router.message(F.successful_payment)
async def successful_payment(message: Message):
    payment = message.successful_payment
    payload = payment.invoice_payload

    if not payload.startswith("tariff:"):
        await message.answer("❌ Неизвестный платёж.")
        return

    _, tariff_code, days = payload.split(":")

    await activate_tariff(
        user_id=message.from_user.id,
        tariff=tariff_code,
        days=int(days)
    )

    await message.answer(
        "✅ Оплата прошла успешно\n\n"
        f"Тариф активирован: {tariff_code}\n"
        f"Срок: {days} дней"
    )


@router.message(F.text == "📊 Моя подписка")
async def my_subscription(message: Message):
    user_id = message.from_user.id

    info = await get_subscription_info(user_id)
    tariff = await get_tariff_info(user_id)

    features = [
        ("content_factory", "✍️ Посты"),
        ("post_image", "🖼 Картинки"),
        ("content_pack", "🚀 Контент-пак"),
        ("rewrite", "✍️ Rewrite"),
        ("brand_rewrite", "🎭 Brand Voice")
    ]

    limits_text = ""

    for feature, title in features:
        limit = await get_feature_limit(user_id, feature)
        used = await get_daily_usage(user_id, feature)

        if tariff["unlimited"]:
            limits_text += f"{title}: безлимит\n"
        else:
            limits_text += f"{title}: {used}/{limit} в день\n"

    await message.answer(
        "📊 Моя подписка\n\n"
        f"Тариф: {tariff['title']}\n"
        f"Осталось дней: {info['days_left']}\n"
        f"Дата окончания: {info['pro_until'] or 'нет'}\n\n"
        "Лимиты:\n"
        f"{limits_text}"
    )