from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from config import settings
from keyboards import (
    main_menu,
    admin_main_menu,
    create_menu,
    content_menu,
    profile_menu,
    style_menu,
    goal_menu,
    subscription_menu,
    admin_menu,
    prime_panel_menu,
    admin_content_center_menu,
    admin_telegram_menu,
    admin_instagram_menu,
    prime_funnel_hub_menu,
    admin_broadcast_menu,
    admin_users_menu,
    admin_limits_menu,
    admin_queue_menu,
    prime_content_hub_menu,
    admin_stats_menu,
    admin_checks_menu,
    prime_system_hub_menu,
)
from database.db import (
    get_tariff_info,
    get_subscription_info,
    get_feature_limit,
    get_referral_stats,
    get_daily_usage,
    get_stats,
    get_all_limits,
)
from handlers.content import ContentState
from handlers.admin import AdminState, is_admin

router = Router()


def home_kb(user_id: int):
    return admin_main_menu if settings.ADMIN_ID is not None and user_id == settings.ADMIN_ID else main_menu


CONTENT_ACTIONS = {
    "✍️ Пост": "post",
    "🖼 Пост + картинка": "image_post",
    "🖼 Пост с картинкой": "image_post",  # old compatibility
    "🎠 Карусель": "carousel",
    "🎬 Reels": "reels",
    "📦 Контент-пак": "content_pack",
    "🚀 Контент-пак": "content_pack",  # old compatibility
}

GOAL_NORMALIZE = {
    "🔥 Продажа": "продать продукт или услугу",
    "🔥 Продать": "продать продукт или услугу",
    "🧠 Экспертность": "показать экспертность и доверие",
    "💬 Вовлечение": "вызвать комментарии и реакции",
    "💬 Вовлечь": "вызвать комментарии и реакции",
    "🚀 Прогрев": "прогреть аудиторию к покупке",
    "🚀 Прогреть": "прогреть аудиторию к покупке",
}


@router.message(F.text == "⬅️ Главное меню")
async def v2_home(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Главное меню 👇", reply_markup=home_kb(message.from_user.id))


@router.message(F.text.in_({"🚀 Создать", "📦 Создать", "🚀 Создать контент", "⬅️ Назад в создание"}))
async def v2_create(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "🚀 <b>Создать</b>\n\n"
        "Выбери формат. Стили больше не дублируются внутри каруселей и картинок — они задаются в AI Профиле.",
        reply_markup=create_menu,
        parse_mode="HTML",
    )


@router.message(F.text == "🛠 Инструменты")
async def v2_tools(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "🛠 <b>Инструменты</b>\n\n"
        "Идеи, хуки, лид-магнит, rewrite, CTA, серия постов и анализ.",
        reply_markup=content_menu,
        parse_mode="HTML",
    )


@router.message(F.text.in_(CONTENT_ACTIONS.keys()))
async def v2_choose_content(message: Message, state: FSMContext):
    await state.clear()
    action = CONTENT_ACTIONS[message.text]
    # Дефолтный визуальный стиль. Пользователь меняет его в AI Профиль → Стиль бренда.
    await state.update_data(action=action, visual_style="primeonix", visual_style_title="PrimeOnix AI")
    await state.set_state(ContentState.waiting_goal)
    await message.answer(
        "🎯 <b>Цель контента</b>\n\n"
        "Выбери цель один раз. Она применится к выбранному формату.",
        reply_markup=goal_menu,
        parse_mode="HTML",
    )


@router.message(ContentState.waiting_goal, F.text.in_(GOAL_NORMALIZE.keys()))
async def v2_goal_selected(message: Message, state: FSMContext):
    await state.update_data(content_goal=GOAL_NORMALIZE[message.text])
    await state.set_state(ContentState.waiting_prompt)
    data = await state.get_data()
    action = data.get("action")
    examples = {
        "post": "Например: продай консультацию по нейросетям для бизнеса",
        "image_post": "Например: пост о том, как AI экономит 5 часов в неделю",
        "carousel": "Например: 7 ошибок в создании Reels и как их исправить",
        "reels": "Например: сценарий Reels про промпты для бизнеса",
        "content_pack": "Например: контент-пак для Instagram эксперта по AI",
    }
    await message.answer(
        "Отлично. Теперь напиши тему или промпт 👇\n\n"
        f"{examples.get(action, 'Например: AI-контент для Instagram и Telegram')}"
    )


@router.message(F.text == "🧠 AI Профиль")
async def v2_profile(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "🧠 <b>AI Профиль</b>\n\n"
        "Здесь задаётся стиль бренда, цель контента, аудитория, CTA, ниша и оффер.\n"
        "Важно: стили визуала теперь только здесь, а не внутри каждой карусели.",
        reply_markup=profile_menu,
        parse_mode="HTML",
    )


@router.message(F.text.in_({"🎭 Стиль бренда", "🎭 Стиль", "⬅️ Назад в профиль"}))
async def v2_brand_style(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "🎭 <b>Стиль бренда</b>\n\n"
        "Выбери визуальный стиль или обучи AI своему стилю.\n"
        "Этот стиль будет применяться к постам, картинкам, каруселям и Reels.",
        reply_markup=style_menu,
        parse_mode="HTML",
    )


@router.message(F.text.in_({"🎯 Цель контента"}))
async def v2_profile_goal(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "🎯 <b>Цель контента</b>\n\n"
        "Эта настройка нужна, чтобы не дублировать кнопки внутри каждого раздела.\n"
        "Для конкретной генерации цель также можно выбрать перед вводом темы.",
        reply_markup=goal_menu,
        parse_mode="HTML",
    )


@router.message(F.text == "📊 Кабинет")
async def v2_cabinet(message: Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    tariff = await get_tariff_info(user_id)
    sub = await get_subscription_info(user_id)
    ref_stats = await get_referral_stats(user_id)
    bot_username = getattr(settings, "BOT_USERNAME", None) or "PrimeOnixBot"
    ref_link = f"https://t.me/{bot_username}?start=ref_{user_id}"

    features = [
        ("content_factory", "✍️ Посты"),
        ("post_image", "🖼 Картинки"),
        ("content_pack", "📦 Контент-пак"),
        ("rewrite", "✍️ Rewrite"),
        ("brand_rewrite", "🎭 Brand Voice"),
    ]
    limits_text = ""
    for feature, title in features:
        used = await get_daily_usage(user_id, feature)
        if tariff.get("unlimited"):
            limits_text += f"{title}: {used}/∞\n"
        else:
            limit = await get_feature_limit(user_id, feature)
            limits_text += f"{title}: {used}/{limit}\n"

    await message.answer(
        "📊 <b>Личный кабинет</b>\n\n"
        f"👤 ID: <code>{user_id}</code>\n"
        f"💎 Тариф: <b>{tariff.get('title', 'FREE')}</b>\n"
        f"⏳ Осталось дней: {sub.get('days_left', 0)}\n"
        f"📅 Окончание: {sub.get('pro_until') or 'нет'}\n\n"
        f"🎁 Приглашено друзей: {ref_stats.get('total_referrals', 0)}\n"
        f"🎁 Бонусных дней: {ref_stats.get('premium_days', 0)}\n\n"
        "📈 <b>Лимиты на сегодня:</b>\n"
        f"{limits_text}\n"
        "🔗 <b>Твоя реферальная ссылка:</b>\n"
        f"<code>{ref_link}</code>\n\n"
        "Нажми на ссылку/удержи, чтобы скопировать.",
        reply_markup=home_kb(user_id),
        parse_mode="HTML",
    )


@router.message(F.text == "💎 PRO")
async def v2_pro(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "💎 <b>Подписка PrimeOnix</b>\n\n"
        "Выбери тариф. PRO открывает максимум функций: картинки, карусели, Reels, воронки и автопостинг.",
        reply_markup=subscription_menu,
        parse_mode="HTML",
    )


# ============================================================
# ADMIN V2
# ============================================================

@router.message(F.text.in_({"👑 Админ", "⬅️ Назад в админку"}))
async def v2_admin(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("❌ Нет доступа")
        return
    await state.clear()
    await message.answer("👑 <b>Админ-панель</b>\n\nУправление пользователями, PRO, лимитами, рассылками и системой.", reply_markup=admin_menu, parse_mode="HTML")


@router.message(F.text.in_({"👑 PRIME PANEL", "🚀 PRIME PANEL", "⬅️ Назад в PRIME PANEL"}))
async def v2_prime_panel(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("❌ Нет доступа")
        return
    await state.clear()
    await message.answer(
        "👑 <b>PRIME PANEL V2</b>\n\n"
        "Главный пульт управления.\n\n"
        "Логика:\n"
        "• Telegram отдельно\n"
        "• Instagram отдельно\n"
        "• IG → TG воронки отдельно\n"
        "• Админка управляет n8n, лимитами, PRO, рассылками и статистикой.",
        reply_markup=prime_panel_menu,
        parse_mode="HTML",
    )


ADMIN_HUBS = {
    "📣 Контент Центр": ("📣 Контент Центр", "Единый центр создания материалов для Telegram, Instagram и контент-паков.", admin_content_center_menu),
    "📢 Telegram": ("📢 Telegram", "Посты, картинки, серии, лид-магниты, очередь и статистика Telegram.", admin_telegram_menu),
    "📲 Instagram": ("📲 Instagram", "Посты, карусели, Reels, pipeline, автопостинг и статистика Instagram.", admin_instagram_menu),
    "🎯 Воронки IG→TG": ("🎯 Воронки IG → TG", "Reels/карусель/пост → кодовое слово → DM → Telegram-материал.", prime_funnel_hub_menu),
    "📬 Рассылки": ("📬 Рассылки", "Рассылки всем, PRO, FREE, сегментам и по воронкам.", admin_broadcast_menu),
    "👥 Пользователи": ("👥 Пользователи", "Поиск пользователей, выдача PRO, блокировка и история.", admin_users_menu),
    "💎 Подписки и лимиты": ("💎 Подписки и лимиты", "Тарифы, лимиты, бонусы, PRO и проверки подписки.", admin_limits_menu),
    "📦 Очередь": ("📦 Очередь", "Очередь публикаций, отложенные посты, ошибки и повтор.", admin_queue_menu),
    "🤖 AI Лаборатория": ("🤖 AI Лаборатория", "Viral Reels, Viral Carousels, Hook Generator, Lead Magnet Lab, Prompt Tester.", prime_content_hub_menu),
    "📈 Статистика": ("📈 Статистика", "Пользователи, генерации, лимиты, подписки, воронки и ошибки n8n.", admin_stats_menu),
    "🧪 Проверки": ("🧪 Проверки", "Проверка n8n, OpenRouter, Telegram, Instagram, Image и Video Generator.", admin_checks_menu),
    "⚙️ Система": ("⚙️ Система", "API, webhooks, каналы, ссылки, логи и backup.", prime_system_hub_menu),
}


@router.message(F.text.in_(ADMIN_HUBS.keys()))
async def v2_admin_hub(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("❌ Нет доступа")
        return
    await state.clear()
    title, desc, keyboard = ADMIN_HUBS[message.text]
    await message.answer(f"{title}\n\n{desc}\n\nВыбери действие 👇", reply_markup=keyboard)


@router.message(F.text == "💎 Выдать PRO")
async def v2_grant_pro(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    await state.clear()
    await state.set_state(AdminState.waiting_pro_user_id)
    await message.answer("💎 Выдать PRO\n\nОтправь user_id пользователя.")


@router.message(F.text == "⚙️ Лимиты")
async def v2_limits_legacy(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    await state.clear()
    limits = await get_all_limits()
    await message.answer(
        "⚙️ Лимиты FREE в день\n\n"
        f"✍️ Посты: {limits.get('content_factory')}\n"
        f"🧠 Rewrite: {limits.get('rewrite')}\n"
        f"🎭 Brand Voice: {limits.get('brand_rewrite')}\n"
        f"🖼 Картинки: {limits.get('post_image')}\n"
        f"📦 Контент-пак: {limits.get('content_pack')}\n\n"
        "Подробное управление: PRIME PANEL → Подписки и лимиты.",
        reply_markup=admin_limits_menu,
    )


@router.message(F.text == "📊 Статистика")
async def v2_stats_legacy(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    await state.clear()
    data = await get_stats()
    await message.answer(
        "📊 Статистика\n\n"
        f"👥 Пользователей: {data.get('total_users')}\n"
        f"💎 PRO: {data.get('total_pro')}\n"
        f"⚡ Генераций: {data.get('total_generations')}\n\n"
        "Подробная статистика: PRIME PANEL → Статистика.",
        reply_markup=admin_stats_menu,
    )


# Все глубокие кнопки админки должны отвечать, а не молчать.
ADMIN_ACTION_HINTS = {
    "TG: Пост": "WF-01 Telegram Post",
    "TG: Создать пост": "WF-01 Telegram Post",
    "TG: Пост + картинка": "WF-02 Telegram Post + Image",
    "TG: Серия постов": "WF-03 Telegram Series",
    "TG: Лид-магнит": "WF-04 Telegram Lead Magnet",
    "TG: Автопостинг": "WF-14 Auto Posting",
    "TG: Очередь": "WF-14 Auto Posting",
    "TG: Статистика": "WF-18 Analytics",
    "IG: Пост": "WF-05 Instagram Post",
    "IG: Карусель": "WF-06 Instagram Carousel",
    "IG: Reels": "WF-07 Instagram Reels",
    "IG: Контент-план": "WF-08 Instagram Content Plan",
    "IG: Подключение": "Instagram API setup",
    "IG: Pipeline Test": "WF-19 System Health Check",
    "IG: Автопостинг": "WF-14 Auto Posting",
    "IG: Очередь": "WF-14 Auto Posting",
    "IG: Статистика": "WF-18 Analytics",
    "🎬 Reels → Telegram": "WF-09 Funnel Reels to Telegram",
    "🎠 Карусель → Telegram": "WF-10 Funnel Carousel to Telegram",
    "📷 Пост → Telegram": "WF-11 Funnel Post to Telegram",
    "🎁 Лид-магнит → Telegram": "WF-12 Lead Magnet Delivery",
    "📨 DM Funnel": "WF-13 DM Funnel Handler",
    "📊 Статистика воронок": "WF-18 Analytics",
    "📬 Новая рассылка": "WF-15 Broadcasts",
    "Рассылка всем": "WF-15 Broadcasts",
    "Рассылка PRO": "WF-15 Broadcasts",
    "Рассылка FREE": "WF-15 Broadcasts",
    "Рассылка по сегменту": "WF-15 Broadcasts",
    "Запланированные рассылки": "WF-15 Broadcasts",
    "История рассылок": "WF-15 Broadcasts",
    "Список пользователей": "User Manager",
    "Найти пользователя": "User Manager",
    "Забрать PRO": "WF-17 User PRO Manager",
    "Изменить тариф": "WF-17 User PRO Manager",
    "Заблокировать": "User Manager",
    "История пользователя": "User Manager",
    "Тарифы": "WF-16 Limits",
    "Лимиты FREE": "WF-16 Limits",
    "Лимиты Plus": "WF-16 Limits",
    "Лимиты Premium": "WF-16 Limits",
    "Лимиты PRO": "WF-16 Limits",
    "Выдать бонусы": "WF-16 Limits",
    "Сбросить лимиты": "WF-16 Limits",
    "Проверить подписку": "WF-16 Limits",
    "Очередь публикаций": "WF-14 Auto Posting",
    "Отложенные посты": "WF-14 Auto Posting",
    "Ошибки публикаций": "WF-14 Auto Posting",
    "Готово к публикации": "WF-14 Auto Posting",
    "Повторить публикацию": "WF-14 Auto Posting",
    "Viral Reels": "AI Lab",
    "Viral Carousels": "AI Lab",
    "Hook Generator": "AI Lab",
    "Lead Magnet Lab": "AI Lab",
    "AI Agent": "AI Lab",
    "Prompt Tester": "AI Lab",
    "Статистика пользователей": "WF-18 Analytics",
    "Статистика генераций": "WF-18 Analytics",
    "Статистика лимитов": "WF-18 Analytics",
    "Статистика подписок": "WF-18 Analytics",
    "Статистика воронок": "WF-18 Analytics",
    "Ошибки n8n": "WF-18 Analytics",
    "🧪 Проверить n8n": "WF-19 System Health Check",
    "Проверить OpenRouter": "WF-19 System Health Check",
    "Проверить Telegram Bot": "WF-19 System Health Check",
    "Проверить Instagram API": "WF-19 System Health Check",
    "Проверить Image Generator": "WF-19 System Health Check",
    "Проверить Video Generator": "WF-19 System Health Check",
    "OpenRouter API": "System Settings",
    "Telegram Bot Token": "System Settings",
    "Instagram API": "System Settings",
    "n8n Webhooks": "System Settings",
    "Каналы": "System Settings",
    "Ссылки": "System Settings",
    "Логи": "System Settings",
    "Backup": "System Settings",
}


@router.message(F.text.in_(ADMIN_ACTION_HINTS.keys()))
async def v2_admin_action_stub(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("❌ Нет доступа")
        return
    await state.clear()
    await message.answer(
        f"✅ <b>{message.text}</b>\n\n"
        f"Маршрут подключён.\n"
        f"n8n/workflow: <code>{ADMIN_ACTION_HINTS[message.text]}</code>\n\n"
        "Следующий шаг — привязать рабочий n8n webhook к этому действию.",
        reply_markup=prime_panel_menu,
        parse_mode="HTML",
    )

@router.message(F.text.in_(GOAL_NORMALIZE.keys()))
async def v2_goal_button_outside_generation(message: Message, state: FSMContext):
    # Если цель нажали в AI Профиле, а не во время генерации — просто подтверждаем.
    await state.clear()
    await message.answer(
        f"✅ Цель контента выбрана: {message.text}\n\n"
        "Теперь открой «🚀 Создать» и выбери формат. Цель можно будет подтвердить перед генерацией.",
        reply_markup=create_menu,
    )
