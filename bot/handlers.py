"""
Обработчики команд и сообщений бота
"""

import logging
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler,
    ContextTypes, filters
)
from bot.survey_manager import SurveyManager, QuestionType
from bot.keyboard_builder import KeyboardBuilder
from bot.data_processor import DataProcessor
from bot.google_sheets import GoogleSheetsManager
from bot.config import Config

logger = logging.getLogger(__name__)

class SurveyHandlers:
    """Обработчики опроса"""
    
    def __init__(self):
        self.config = Config()
        self.survey_manager = SurveyManager()
        self.keyboard_builder = KeyboardBuilder(self.survey_manager)
        self.data_processor = DataProcessor(self.survey_manager)
        # Инициализируем Google Sheets только при необходимости
        self.sheets_manager = None
    
    def _get_sheets_manager(self):
        """Получить менеджер Google Sheets (ленивая инициализация)"""
        if self.sheets_manager is None:
            self.sheets_manager = GoogleSheetsManager(self.config)
        return self.sheets_manager
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        user_id = update.effective_user.id
        
        # Очищаем предыдущее состояние пользователя
        self.survey_manager.clear_user_state(user_id)
        
        # Отправляем приветственное сообщение
        welcome_message = self.survey_manager.get_welcome_message()
        keyboard = self.keyboard_builder.build_welcome_keyboard()
        
        await update.message.reply_text(
            welcome_message,
            reply_markup=keyboard
        )
    
    async def handle_callback_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик callback запросов"""
        query = update.callback_query
        await query.answer()
        
        user_id = update.effective_user.id
        data = query.data
        
        if data == "start_survey":
            await self._start_survey(update, context)
        
        elif data == "restart_survey":
            await self._restart_survey(update, context)
        
        elif data.startswith("single_choice:"):
            await self._handle_single_choice(update, context, data)
        
        elif data.startswith("multi_choice_toggle:"):
            await self._handle_multi_choice_toggle(update, context, data)
        
        elif data.startswith("multi_choice_done:"):
            await self._handle_multi_choice_done(update, context, data)
        
        elif data.startswith("skip_comment:"):
            await self._handle_skip_comment(update, context, data)
    
    async def handle_text_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик текстовых сообщений"""
        user_id = update.effective_user.id
        text = update.message.text
        
        # Проверяем, ожидается ли комментарий
        if self.survey_manager.is_waiting_for_comment(user_id):
            await self._handle_comment_input(update, context, text)
            return
        
        # Проверяем, ожидается ли текстовый ответ
        current_question = self.survey_manager.get_current_question(user_id)
        if current_question != "start" and current_question != "completed":
            question_type = self.survey_manager.get_question_type(current_question)
            if question_type == QuestionType.TEXT:
                await self._handle_text_answer(update, context, text)
                return
        
        # Если не в процессе опроса, предлагаем начать
        await update.message.reply_text(
            "Для начала опроса используйте команду /start",
            reply_markup=self.keyboard_builder.build_restart_keyboard()
        )
    
    async def _start_survey(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Начать опрос"""
        user_id = update.effective_user.id
        
        # Устанавливаем первый вопрос
        self.survey_manager.set_current_question(user_id, "q1_1")
        
        # Отправляем первый вопрос
        await self._send_question(update, context, "q1_1")
    
    async def _restart_survey(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Перезапустить опрос"""
        user_id = update.effective_user.id
        
        # Очищаем состояние
        self.survey_manager.clear_user_state(user_id)
        
        # Начинаем заново
        await self._start_survey(update, context)
    
    async def _handle_single_choice(self, update: Update, context: ContextTypes.DEFAULT_TYPE, data: str):
        """Обработчик одиночного выбора"""
        user_id = update.effective_user.id
        _, question_id, option_id = data.split(":", 2)
        
        # Получаем информацию об опции
        options = self.survey_manager.get_question_options(question_id)
        selected_option = None
        for option in options:
            if option.get("id") == option_id:
                selected_option = option
                break
        
        if not selected_option:
            return
        
        # Проверяем, нужен ли комментарий
        comment_required = selected_option.get("comment_required", False)
        comment_type = selected_option.get("comment_type", "none")
        
        if comment_required and comment_type != "none":
            # Устанавливаем ожидание комментария
            comment_question = selected_option.get("comment_question", "Укажите дополнительную информацию:")
            self.survey_manager.set_waiting_for_comment(user_id, option_id, comment_question)
            
            # Запрашиваем комментарий
            keyboard = self.keyboard_builder.build_comment_prompt_keyboard(
                question_id, option_id, comment_required
            )
            
            await update.callback_query.edit_message_text(
                comment_question,
                reply_markup=keyboard
            )
        else:
            # Сохраняем ответ и переходим к следующему вопросу
            self.survey_manager.save_answer(user_id, question_id, option_id)
            self.survey_manager.move_to_next_question(user_id)
            
            # Отправляем следующий вопрос
            next_question = self.survey_manager.get_current_question(user_id)
            if next_question == "completed":
                await self._complete_survey(update, context)
            else:
                await self._send_question(update, context, next_question)
    
    async def _handle_multi_choice_toggle(self, update: Update, context: ContextTypes.DEFAULT_TYPE, data: str):
        """Обработчик переключения множественного выбора"""
        user_id = update.effective_user.id
        _, question_id, option_id = data.split(":", 2)
        
        # Переключаем выбор
        current_selections = self.survey_manager.get_multi_choice_selections(user_id)
        is_selected = option_id in current_selections
        
        self.survey_manager.save_multi_choice_selection(user_id, option_id, not is_selected)
        
        # Обновляем клавиатуру
        keyboard = self.keyboard_builder.build_multi_choice_keyboard(question_id, user_id)
        
        await update.callback_query.edit_message_reply_markup(reply_markup=keyboard)
    
    async def _handle_multi_choice_done(self, update: Update, context: ContextTypes.DEFAULT_TYPE, data: str):
        """Обработчик завершения множественного выбора"""
        user_id = update.effective_user.id
        _, question_id = data.split(":", 1)
        
        # Получаем выбранные опции
        selected_options = self.survey_manager.get_multi_choice_selections(user_id)
        
        if not selected_options:
            await update.callback_query.edit_message_text(
                "Пожалуйста, выберите хотя бы один вариант.",
                reply_markup=self.keyboard_builder.build_multi_choice_keyboard(question_id, user_id)
            )
            return
        
        # Проверяем, нужны ли комментарии для выбранных опций
        options_needing_comments = []
        for option_id in selected_options:
            if self.survey_manager.get_option_requires_comment(question_id, option_id):
                options_needing_comments.append(option_id)
        
        if options_needing_comments:
            # Запрашиваем комментарии
            option_id = options_needing_comments[0]
            comment_question = self.survey_manager.get_option_comment_question(question_id, option_id)
            if not comment_question:
                comment_question = "Укажите дополнительную информацию:"
            
            self.survey_manager.set_waiting_for_comment(user_id, option_id, comment_question)
            
            keyboard = self.keyboard_builder.build_comment_prompt_keyboard(
                question_id, option_id, True
            )
            
            await update.callback_query.edit_message_text(
                comment_question,
                reply_markup=keyboard
            )
        else:
            # Сохраняем ответ и переходим к следующему вопросу
            self.survey_manager.save_answer(user_id, question_id, selected_options)
            self.survey_manager.clear_multi_choice_selections(user_id)
            self.survey_manager.move_to_next_question(user_id)
            
            # Отправляем следующий вопрос
            next_question = self.survey_manager.get_current_question(user_id)
            if next_question == "completed":
                await self._complete_survey(update, context)
            else:
                await self._send_question(update, context, next_question)
    
    async def _handle_comment_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
        """Обработчик ввода комментария"""
        user_id = update.effective_user.id
        option_id = self.survey_manager.get_waiting_option_id(user_id)
        
        if not option_id:
            return
        
        # Сохраняем комментарий
        current_question = self.survey_manager.get_current_question(user_id)
        current_answer = self.survey_manager.get_all_answers(user_id).get(current_question, {})
        
        if isinstance(current_answer, dict):
            if "comments" not in current_answer:
                current_answer["comments"] = {}
            current_answer["comments"][option_id] = text
        else:
            # Если ответ еще не словарь, создаем его
            current_answer = {
                "options": [option_id] if isinstance(current_answer, list) else [current_answer],
                "comments": {option_id: text}
            }
        
        self.survey_manager.save_answer(user_id, current_question, current_answer)
        
        # Очищаем ожидание комментария
        self.survey_manager.clear_waiting_for_comment(user_id)
        
        # Переходим к следующему вопросу
        self.survey_manager.move_to_next_question(user_id)
        
        # Отправляем следующий вопрос
        next_question = self.survey_manager.get_current_question(user_id)
        if next_question == "completed":
            await self._complete_survey(update, context)
        else:
            await self._send_question(update, context, next_question)
    
    async def _handle_skip_comment(self, update: Update, context: ContextTypes.DEFAULT_TYPE, data: str):
        """Обработчик пропуска комментария"""
        user_id = update.effective_user.id
        _, question_id, option_id = data.split(":", 2)
        
        # Очищаем ожидание комментария
        self.survey_manager.clear_waiting_for_comment(user_id)
        
        # Переходим к следующему вопросу
        self.survey_manager.move_to_next_question(user_id)
        
        # Отправляем следующий вопрос
        next_question = self.survey_manager.get_current_question(user_id)
        if next_question == "completed":
            await self._complete_survey(update, context)
        else:
            await self._send_question(update, context, next_question)
    
    async def _handle_text_answer(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
        """Обработчик текстового ответа"""
        user_id = update.effective_user.id
        current_question = self.survey_manager.get_current_question(user_id)
        
        # Сохраняем ответ
        self.survey_manager.save_answer(user_id, current_question, text)
        
        # Переходим к следующему вопросу
        self.survey_manager.move_to_next_question(user_id)
        
        # Отправляем следующий вопрос
        next_question = self.survey_manager.get_current_question(user_id)
        if next_question == "completed":
            await self._complete_survey(update, context)
        else:
            await self._send_question(update, context, next_question)
    
    async def _send_question(self, update: Update, context: ContextTypes.DEFAULT_TYPE, question_id: str):
        """Отправить вопрос пользователю"""
        question_text = self.survey_manager.get_question_text(question_id)
        question_type = self.survey_manager.get_question_type(question_id)
        
        # Проверяем, есть ли callback_query (для inline кнопок)
        has_callback_query = update.callback_query is not None
        
        if question_type == QuestionType.TEXT:
            # Для текстовых вопросов отправляем новое сообщение
            keyboard = self.keyboard_builder.build_text_input_keyboard()
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=question_text,
                reply_markup=keyboard
            )
        else:
            # Для вопросов с выбором используем inline клавиатуру
            if question_type == QuestionType.SINGLE_CHOICE:
                keyboard = self.keyboard_builder.build_single_choice_keyboard(question_id)
            else:
                keyboard = self.keyboard_builder.build_multi_choice_keyboard(question_id, update.effective_user.id)
            
            if has_callback_query:
                # Если есть callback_query, редактируем сообщение
                await update.callback_query.edit_message_text(
                    question_text,
                    reply_markup=keyboard
                )
            else:
                # Если нет callback_query, отправляем новое сообщение
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=question_text,
                    reply_markup=keyboard
                )
    
    async def _complete_survey(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Завершить опрос"""
        user_id = update.effective_user.id
        
        try:
            # Форматируем данные для Google Sheets
            survey_data = self.data_processor.format_answers_for_sheets(user_id)
            
            # Записываем в Google Sheets
            sheets_manager = self._get_sheets_manager()
            sheets_manager.append_survey_data(survey_data)
            
            # Отправляем сообщение об успешном завершении
            completion_message = (
                "Спасибо за участие в опросе! Ваши ответы успешно сохранены. "
                "Мы свяжемся с вами для дальнейших консультаций."
            )
            
            if update.callback_query is not None:
                await update.callback_query.edit_message_text(
                    completion_message,
                    reply_markup=self.keyboard_builder.build_restart_keyboard()
                )
            else:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=completion_message,
                    reply_markup=self.keyboard_builder.build_restart_keyboard()
                )
            
            # Очищаем состояние пользователя
            self.survey_manager.clear_user_state(user_id)
            
        except Exception as e:
            logger.error(f"Ошибка при сохранении данных: {e}")
            if update.callback_query is not None:
                await update.callback_query.edit_message_text(
                    "Произошла ошибка при сохранении данных. Пожалуйста, попробуйте позже.",
                    reply_markup=self.keyboard_builder.build_restart_keyboard()
                )
            else:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Произошла ошибка при сохранении данных. Пожалуйста, попробуйте позже.",
                    reply_markup=self.keyboard_builder.build_restart_keyboard()
                )

def setup_handlers(application: Application):
    """Настройка обработчиков"""
    handlers = SurveyHandlers()
    
    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", handlers.start_command))
    application.add_handler(CallbackQueryHandler(handlers.handle_callback_query))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.handle_text_message))
