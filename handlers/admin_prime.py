from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from handlers.admin import is_admin
from keyboards import (
    admin_menu,
    prime_panel_menu,
    prime_funnel_hub_menu,
    prime_content_hub_menu,
    prime_publish_hub_menu,
    prime_instagram_hub_menu,
    prime_agents_hub_menu,
    prime_system_hub_menu,
    prime_telegram_hub_menu,
    prime_broadcast_menu,
    prime_users_menu,
    prime_limits_menu,
    prime_publish_hub_menu,
)


router = Router()


PRIME_PANEL_TEXT = (
    "👑 <b>PRIME PANEL</b>\n\n"
    "Это главный пульт твоей AI-SMM системы.\n\n"
    "Логика проекта:\n"
    "• <b>Telegram-бот</b> — ты управляешь и одобряешь\n"
    "• <b>n8n</b> — выполняет автоматизацию\n"
    "• <b>Instagram</b> — даёт трафик\n"
    "• <b>Telegram</b> — удерживает, прогревает и продаёт\n\n"
    "Чтобы не было хаоса, всё собрано по блокам 👇"
)


SYSTEM_MAP_TEXT = (
    "🧭 <b>Карта PRIME-системы</b>\n\n"
    "Вот что куда относится:\n\n"
    "🔗 <b>Воронки IG→TG</b>\n"
    "Создаёт связку: Reels/карусель/лид-магнит → кодовое слово → DM → Telegram-пост.\n\n"
    "🧠 <b>Генерация контента</b>\n"
    "Viral Reels, карусели, хуки, лид-магниты, AI-агенты.\n\n"
    "📦 <b>Очередь и публикации</b>\n"
    "Сохранить материал, подготовить к публикации, запланировать, отправить в TG/IG.\n\n"
    "📲 <b>Instagram / AutoPost</b>\n"
    "Проверка n8n/IG pipeline, подготовка Reels, отправка в Instagram, DM funnel.\n\n"
    "🤖 <b>Агенты и аналитика</b>\n"
    "AI-стратег, viral analyzer, анализ связок и улучшение контента.\n\n"
    "⚙️ <b>Система</b>\n"
    "Проверки n8n, Instagram, API и технических связок."
)


HUBS = {
    "🧭 Карта системы": (SYSTEM_MAP_TEXT, prime_panel_menu),
    "📣 Контент Центр": (
        "📣 <b>Контент Центр</b>\n\n"
        "Быстро создаём отдельные материалы: Telegram, Instagram, Reels, карусели, лид-магниты.\n\n"
        "Выбери формат 👇",
        prime_content_hub_menu,
    ),
    "📢 Telegram": (
        "📢 <b>Telegram</b>\n\n"
        "Отдельная ветка для Telegram: посты, картинки, серии, лид-магниты, прогрев и автопостинг.",
        prime_telegram_hub_menu,
    ),
    "📲 Instagram": (
        "📲 <b>Instagram</b>\n\n"
        "Отдельная ветка для Instagram: посты, карусели, Reels, обложки, caption и автопостинг.",
        prime_instagram_hub_menu,
    ),
    "🎯 Воронки IG→TG": (
        "🎯 <b>Воронки IG → TG</b>\n\n"
        "Instagram даёт охват → человек пишет кодовое слово → Telegram выдаёт конкретный материал.\n\n"
        "Выбери формат входа 👇",
        prime_funnel_hub_menu,
    ),
    "📬 Рассылки": (
        "📬 <b>Рассылки</b>\n\n"
        "Рассылки всем, PRO, FREE, по сегментам и по воронкам.",
        prime_broadcast_menu,
    ),
    "👥 Пользователи": (
        "👥 <b>Пользователи</b>\n\n"
        "Поиск пользователей, выдача PRO, бонусы, блокировка, история.",
        prime_users_menu,
    ),
    "💎 Подписки и лимиты": (
        "💎 <b>Подписки и лимиты</b>\n\n"
        "Выдача PRO, лимиты тарифов, бонусные генерации и сброс лимитов.",
        prime_limits_menu,
    ),
    "📦 Очередь": (
        "📦 <b>Очередь</b>\n\n"
        "Публикации, отложка, ошибки, готовые материалы и повтор публикаций.",
        prime_publish_hub_menu,
    ),
    "🤖 AI Лаборатория": (
        "🤖 <b>AI Лаборатория</b>\n\n"
        "Viral Reels, карусели, хуки, лид-магниты и тест промптов.",
        prime_agents_hub_menu,
    ),
    "📈 Статистика": (
        "📈 <b>Статистика</b>\n\n"
        "Пользователи, генерации, лимиты, подписки, воронки, Instagram, Telegram и ошибки n8n.",
        prime_system_hub_menu,
    ),
    "🧪 Проверки": (
        "🧪 <b>Проверки</b>\n\n"
        "Быстрая диагностика: n8n, OpenRouter, Telegram Bot, Instagram Pipeline.",
        prime_system_hub_menu,
    ),
    "⚙️ Система": (
        "⚙️ <b>Система</b>\n\n"
        "Технические настройки: webhooks, API, логи, интеграции и backup.",
        prime_system_hub_menu,
    ),
}


PRIME_SECTIONS = {
    "📈 Analytics": (
        "📈 <b>Analytics</b>\n\n"
        "Раздел аналитики контента, роста и воронок.\n\n"
        "Будем отслеживать:\n"
        "• охваты\n"
        "• сохранения\n"
        "• переходы в Telegram\n"
        "• лучшие темы\n"
        "• лучшие хуки\n"
        "• связки, которые стоит повторять\n\n"
        "Пока это информационный блок. Реальные метрики подключим после автопостинга."
    ),
}


@router.message(F.text.in_({"👑 PRIME PANEL", "🚀 PRIME PANEL"}))
async def open_prime_panel(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("❌ Нет доступа")
        return

    await state.clear()
    await message.answer(PRIME_PANEL_TEXT, reply_markup=prime_panel_menu, parse_mode="HTML")


@router.message(F.text == "⬅️ Назад в PRIME PANEL")
async def back_to_prime_panel(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    await state.clear()
    await message.answer(PRIME_PANEL_TEXT, reply_markup=prime_panel_menu, parse_mode="HTML")


@router.message(F.text.in_(HUBS.keys()))
async def open_prime_hub(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("❌ Нет доступа")
        return

    await state.clear()
    text, keyboard = HUBS[message.text]

    if message.text in {"🎯 Воронки IG→TG", "🔗 Воронки IG→TG"}:
        from handlers.ig_tg_funnel import IgTgFunnelState
        await state.set_state(IgTgFunnelState.waiting_type)

    await message.answer(text, reply_markup=keyboard, parse_mode="HTML")


@router.message(F.text.in_(PRIME_SECTIONS.keys()))
async def prime_panel_section(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("❌ Нет доступа")
        return

    await state.clear()
    await message.answer(PRIME_SECTIONS[message.text], reply_markup=prime_system_hub_menu, parse_mode="HTML")


ADMIN_ACTION_TEXTS = {
    "📢 Telegram пост": "WF Telegram Post: текст для Telegram.",
    "🖼 TG пост + картинка": "WF Telegram Post + Image: текст + картинка для Telegram.",
    "📚 Серия постов": "WF Telegram Series: серия постов для канала.",
    "🎁 Лид-магниты TG": "WF Lead Magnet: промпты, чек-лист, инструкция или мини-гайд.",
    "🚀 Прогрев TG": "WF Telegram Warm-up: welcome, доверие, экспертность, боль, решение, продажа.",
    "🚀 Автопостинг TG": "WF Telegram Auto Posting: публикация/отложка в Telegram.",
    "📷 Instagram пост": "WF Instagram Post: caption + visual + hashtags.",
    "🎠 Instagram карусель": "WF Instagram Carousel: cover + 8 слайдов + caption.",
    "🎬 Instagram Reels": "WF Instagram Reels: hook + script + cover + video prompt.",
    "📅 Контент-план": "WF Content Plan: 7/14/30 дней.",
    "🚀 Автопостинг IG": "WF Instagram Auto Posting: публикация в IG после подключения API.",
    "🎬 Reels → Telegram": "WF Funnel Reels → Telegram: Reels + keyword + DM + TG material.",
    "🎠 Карусель → Telegram": "WF Funnel Carousel → Telegram: карусель + CTA + TG material.",
    "📷 Пост → Telegram": "WF Funnel Post → Telegram: пост + keyword + TG material.",
    "🎁 Лид-магнит → Telegram": "WF Lead Magnet Delivery: выдача материала по funnel_id.",
    "📨 DM Funnel": "WF DM Funnel Handler: keyword → ответ → ссылка в Telegram.",
    "🧭 Все funnel_id": "Список и статистика funnel_id. Подключим к БД/n8n.",
    "📬 Новая рассылка": "WF Broadcast: новая рассылка.",
    "📣 Рассылка всем": "WF Broadcast: всем пользователям.",
    "💎 Рассылка PRO": "WF Broadcast: только PRO.",
    "🆓 Рассылка FREE": "WF Broadcast: только FREE.",
    "🎯 Рассылка по сегменту": "WF Broadcast: выбранный сегмент/воронка.",
    "👥 Список пользователей": "Админ: список пользователей. Подключим пагинацию.",
    "🔎 Найти пользователя": "Админ: поиск пользователя по ID/username.",
    "🚫 Забрать PRO": "Админ: забрать PRO у пользователя.",
    "➕ Выдать бонусы": "Админ: добавить бонусные генерации/дни.",
    "🔄 Сбросить лимиты": "Админ: сбросить лимиты пользователя.",
    "📊 Проверить подписку": "Админ: проверка тарифа и лимитов пользователя.",
    "🧪 Проверить OpenRouter": "Проверка OpenRouter через n8n/system webhook.",
    "🧪 Проверить Telegram Bot": "Проверка Telegram Bot статуса.",
    "🔗 Webhooks n8n": "Список webhook-переменных Railway/n8n.",
    "📜 Логи": "Логи ошибок и последних запусков.",
}


@router.message(F.text.in_(ADMIN_ACTION_TEXTS.keys()))
async def admin_action_placeholder(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("❌ Нет доступа")
        return

    await state.clear()

    if message.text in {"📬 Новая рассылка", "📣 Рассылка всем", "💎 Рассылка PRO", "🆓 Рассылка FREE", "🎯 Рассылка по сегменту"}:
        from handlers.admin import AdminState
        await state.set_state(AdminState.waiting_broadcast_text)
        await message.answer(
            f"📬 <b>{message.text}</b>\n\n"
            "Отправь текст рассылки. После подключения n8n этот маршрут сможет отправлять по выбранному сегменту.",
            reply_markup=prime_broadcast_menu,
            parse_mode="HTML",
        )
        return

    section_keyboard = prime_panel_menu
    text_info = ADMIN_ACTION_TEXTS[message.text]
    if "Telegram" in text_info or "TG" in text_info:
        section_keyboard = prime_telegram_hub_menu
    elif "Instagram" in text_info or "IG" in text_info:
        section_keyboard = prime_instagram_hub_menu
    elif "Funnel" in text_info or "funnel" in text_info or "ворон" in text_info.lower():
        section_keyboard = prime_funnel_hub_menu
    elif "Broadcast" in text_info:
        section_keyboard = prime_broadcast_menu

    await message.answer(
        f"✅ <b>{message.text}</b>\n\n"
        f"{text_info}\n\n"
        "Маршрут подготовлен. Когда вставим рабочий n8n webhook, эта кнопка будет запускать отдельный workflow.",
        reply_markup=section_keyboard,
        parse_mode="HTML",
    )


@router.message(F.text == "⬅️ Назад в админку")
async def back_to_admin_from_prime(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    await state.clear()
    await message.answer("👑 Админ-панель", reply_markup=admin_menu)
