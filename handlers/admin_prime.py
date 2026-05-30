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
    prime_stats_menu,
    prime_checks_menu,
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
        "Это отдельный раздел с метриками. Выбери, какую статистику посмотреть 👇",
        prime_stats_menu,
    ),
    "🧪 Проверки": (
        "🧪 <b>Проверки</b>\n\n"
        "Это отдельный раздел диагностики связей. Нажимаешь кнопку — проверяем конкретную интеграцию 👇",
        prime_checks_menu,
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


@router.message(F.text.in_({"👑 Админ", "👑 PRIME PANEL", "🚀 PRIME PANEL"}))
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
    "🕒 Запланированные": "Раздел запланированных рассылок. Здесь будут будущие рассылки и расписание.",
    "📜 История рассылок": "История рассылок: дата, сегмент, текст, отправлено, ошибки.",
    "⚙️ Лимиты FREE": "Настройка лимитов FREE: посты, картинки, rewrite, карусели, Reels.",
    "⚙️ Лимиты PRO": "Настройка лимитов PRO: расширенные лимиты, воронки, автопостинг, приоритет.",
    "👥 Статистика пользователей": "Показывает: всего, новые, активные, FREE, PRO, заблокированные.",
    "⚡ Статистика генераций": "Показывает генерации: посты, картинки, карусели, Reels, лид-магниты.",
    "💎 Статистика подписок": "Показывает подписки: FREE, Plus, Premium, PRO, истекающие, оплаты.",
    "📈 Статистика лимитов": "Показывает использование лимитов по тарифам и пользователям.",
    "🎯 Статистика воронок": "Показывает funnel_id, переходы IG→TG, keyword, выдачи лид-магнитов.",
    "📲 Статистика Instagram": "Показывает Instagram-материалы, карусели, Reels и ошибки публикаций.",
    "📢 Статистика Telegram": "Показывает Telegram-посты, лид-магниты, подписчиков и активность.",
    "🚨 Ошибки n8n": "Показывает ошибки workflow, таймауты, неудачные публикации и повторы.",
    "🧪 Проверить n8n": "Проверка доступности n8n system webhook.",
    "🧪 Проверить Image Generator": "Проверка генерации картинок через OpenRouter/image workflow.",
    "🧪 Проверить Video Generator": "Проверка видео workflow для Reels.",
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

    # Real diagnostics must call n8n/Telegram immediately, not show old placeholder text.
    if message.text == "🧪 Проверить n8n":
        from services.n8n_client import ping_n8n
        await message.answer("🧪 Проверяю n8n system webhook...")
        result = await ping_n8n()
        if result.get("ok"):
            await message.answer(
                "✅ n8n отвечает.\n\n"
                f"HTTP status: {result.get('status')}\n"
                f"Ответ: {result.get('text') or result.get('raw')}",
                reply_markup=prime_checks_menu,
            )
        else:
            await message.answer(
                "❌ n8n не ответил как надо.\n\n"
                f"Ошибка: {result.get('error')}\n"
                f"Детали: {result.get('message') or result.get('raw') or result.get('data')}",
                reply_markup=prime_checks_menu,
            )
        return

    if message.text == "🧪 Проверить Telegram Bot":
        me = await message.bot.get_me()
        await message.answer(
            "✅ Telegram Bot отвечает.\n\n"
            f"@{me.username}\n"
            f"ID: {me.id}",
            reply_markup=prime_checks_menu,
        )
        return

    if message.text in {"🧪 Проверить OpenRouter", "🧪 Проверить IG Pipeline", "🧪 Проверить Image Generator", "🧪 Проверить Video Generator"}:
        from services.n8n_client import call_n8n
        action_map = {
            "🧪 Проверить OpenRouter": "check_openrouter",
            "🧪 Проверить IG Pipeline": "check_instagram_pipeline",
            "🧪 Проверить Image Generator": "check_image_generator",
            "🧪 Проверить Video Generator": "check_video_generator",
        }
        await message.answer(f"🧪 Отправляю тест: {message.text}...")
        result = await call_n8n({
            "action": action_map[message.text],
            "source": "telegram_bot",
            "platform": "instagram" if "IG" in message.text else "telegram",
            "message": "PrimeOnix integration diagnostic test",
        }, timeout=45)
        if result.get("ok"):
            await message.answer(
                "✅ Проверка прошла.\n\n"
                f"HTTP status: {result.get('status')}\n"
                f"Ответ: {result.get('text') or result.get('raw')}",
                reply_markup=prime_checks_menu,
            )
        else:
            await message.answer(
                "❌ Проверка не прошла.\n\n"
                f"Ошибка: {result.get('error')}\n"
                f"Детали: {result.get('message') or result.get('raw') or result.get('data')}",
                reply_markup=prime_checks_menu,
            )
        return

    if message.text == "🔗 Webhooks n8n":
        from services.n8n_client import n8n_config_status
        ok, missing, cfg = n8n_config_status({"action": "ping"})
        lines = ["🔗 <b>Webhooks n8n</b>", "", f"Статус: {'✅ настроено' if ok else '⚠️ не хватает ' + ', '.join(missing)}", ""]
        for key, value in cfg.items():
            lines.append(f"• {key}: {'✅' if value else '❌'}")
        await message.answer("\n".join(lines), reply_markup=prime_checks_menu, parse_mode="HTML")
        return

    section_keyboard = prime_panel_menu
    text_info = ADMIN_ACTION_TEXTS[message.text]
    if message.text in {"👥 Статистика пользователей", "⚡ Статистика генераций", "💎 Статистика подписок", "📈 Статистика лимитов", "🎯 Статистика воронок", "📲 Статистика Instagram", "📢 Статистика Telegram", "🚨 Ошибки n8n"}:
        section_keyboard = prime_stats_menu
    elif message.text in {"🧪 Проверить n8n", "🧪 Проверить OpenRouter", "🧪 Проверить Telegram Bot", "🧪 Проверить IG Pipeline", "🧪 Проверить Image Generator", "🧪 Проверить Video Generator", "🔗 Webhooks n8n", "📜 Логи"}:
        section_keyboard = prime_checks_menu
    elif message.text in {"🕒 Запланированные", "📜 История рассылок"}:
        section_keyboard = prime_broadcast_menu
    elif "Telegram" in text_info or "TG" in text_info:
        section_keyboard = prime_telegram_hub_menu
    elif "Instagram" in text_info or "IG" in text_info:
        section_keyboard = prime_instagram_hub_menu
    elif "Funnel" in text_info or "funnel" in text_info or "ворон" in text_info.lower():
        section_keyboard = prime_funnel_hub_menu
    elif "Broadcast" in text_info or "рассыл" in text_info.lower():
        section_keyboard = prime_broadcast_menu
    elif "лимит" in text_info.lower() or "PRO" in message.text:
        section_keyboard = prime_limits_menu

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
