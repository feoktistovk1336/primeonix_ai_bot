from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from config import settings
from keyboards import (
    main_menu,
    admin_main_menu,
    create_menu,
    content_menu,
    publish_plan_menu,
    subscription_menu,
    profile_menu,
    ig_tg_funnel_menu,
)

router = Router()


def _home_kb(user_id: int):
    return admin_main_menu if user_id == settings.ADMIN_ID else main_menu


PRO_TEXT = (
    "💎 <b>PrimeOnix PRO</b>\n\n"
    "Выбери тариф ниже. Оплата через Telegram Stars.\n\n"
    "💎 <b>Start Premium</b> — 30 Stars / 30 дней\n"
    "+2 генерации в день к каждому блоку.\n\n"
    "➕ <b>Plus</b> — 50 Stars / 30 дней\n"
    "+4 генерации в день к каждому блоку.\n\n"
    "🔥 <b>VIP</b> — 100 Stars / 30 дней\n"
    "+7 генераций в день + улучшенные картинки.\n\n"
    "👑 <b>Premium</b> — 160 Stars / 30 дней\n"
    "+10 генераций в день + premium-картинки.\n\n"
    "🚀 <b>PRO</b> — 500 Stars / 30 дней\n"
    "Максимальный доступ ко всем функциям.\n\n"
    "Нажми тариф кнопкой ниже 👇"
)


@router.message(F.text.in_({"🚀 Создать", "🚀 Создать контент", "📦 Создать", "⬅️ Назад в создание"}))
async def ui_create(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "🚀 <b>Создать контент</b>\n\n"
        "Генерация контента: посты, карусели, Reels, картинки и AI-инструменты.",
        reply_markup=create_menu,
        parse_mode="HTML",
    )


@router.message(F.text.in_({"🛠 Инструменты", "🛠 AI-инструменты", "📚 Контент"}))
async def ui_tools(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "🛠 <b>Инструменты</b>\n\n"
        "Хуки, идеи, лид-магниты, rewrite, CTA, анализ и серии постов.",
        reply_markup=content_menu,
        parse_mode="HTML",
    )


@router.message(F.text.in_({"📲 Публикации", "📅 План и публикации", "⬅️ Назад в публикации"}))
async def ui_publish(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "📲 <b>Публикации</b>\n\n"
        "Здесь связки Instagram → Telegram, пакеты публикаций, очередь и отложенные задачи.",
        reply_markup=publish_plan_menu,
        parse_mode="HTML",
    )


@router.message(F.text == "💎 PRO")
async def ui_pro(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(PRO_TEXT, reply_markup=subscription_menu, parse_mode="HTML")


@router.message(F.text == "🧠 AI Профиль")
async def ui_profile(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "🧠 <b>AI Профиль</b>\n\n"
        "Здесь бот запоминает твою нишу, стиль, аудиторию, оффер и CTA.\n"
        "Чем лучше профиль — тем точнее посты, Reels и карусели.",
        reply_markup=profile_menu,
        parse_mode="HTML",
    )


@router.message(F.text == "🔗 IG→TG Воронка")
async def ui_ig_tg(message: Message, state: FSMContext):
    await state.clear()
    from handlers.ig_tg_funnel import IgTgFunnelState, IG_TG_INTRO_TEXT
    await state.set_state(IgTgFunnelState.waiting_type)
    await message.answer(IG_TG_INTRO_TEXT, reply_markup=ig_tg_funnel_menu, parse_mode="HTML")


@router.message(F.text.in_({"📲 Instagram пакет", "📲 Отправить в Instagram"}))
async def ui_instagram_package(message: Message, state: FSMContext):
    await state.clear()
    from handlers.prime_autopost import _send_last_to_n8n_publish
    await _send_last_to_n8n_publish(message, "publish_instagram", "instagram", "Instagram пакет")


@router.message(F.text.in_({"📣 Telegram пакет", "📣 Отправить в Telegram"}))
async def ui_telegram_package(message: Message, state: FSMContext):
    await state.clear()
    from handlers.prime_autopost import _send_last_to_n8n_publish
    await _send_last_to_n8n_publish(message, "publish_telegram", "telegram", "Telegram пакет")


@router.message(F.text == "⬅️ Главное меню")
async def ui_home(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Главное меню 👇", reply_markup=_home_kb(message.from_user.id))
