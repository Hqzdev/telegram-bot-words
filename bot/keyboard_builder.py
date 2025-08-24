"""
Модуль для построения клавиатур и кнопок
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from typing import List, Dict, Any
from bot.survey_manager import SurveyManager, QuestionType

class KeyboardBuilder:
    """Построитель клавиатур"""
    
    def __init__(self, survey_manager: SurveyManager):
        self.survey_manager = survey_manager
    
    def build_welcome_keyboard(self) -> InlineKeyboardMarkup:
        """Построить клавиатуру приветствия"""
        keyboard = [
            [InlineKeyboardButton("Перейти к вопросам", callback_data="start_survey")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    def build_single_choice_keyboard(self, question_id: str) -> InlineKeyboardMarkup:
        """Построить клавиатуру для одиночного выбора"""
        options = self.survey_manager.get_question_options(question_id)
        keyboard = []
        
        for option in options:
            button_text = option.get("text", "")
            callback_data = f"single_choice:{question_id}:{option.get('id', '')}"
            keyboard.append([InlineKeyboardButton(button_text, callback_data=callback_data)])
        
        return InlineKeyboardMarkup(keyboard)
    
    def build_multi_choice_keyboard(self, question_id: str, user_id: int) -> InlineKeyboardMarkup:
        """Построить клавиатуру для множественного выбора"""
        options = self.survey_manager.get_question_options(question_id)
        current_selections = self.survey_manager.get_multi_choice_selections(user_id)
        keyboard = []
        
        for option in options:
            option_id = option.get("id", "")
            button_text = option.get("text", "")
            
            # Добавляем маркер выбора
            if option_id in current_selections:
                button_text = f"✅ {button_text}"
            else:
                button_text = f"⬜ {button_text}"
            
            callback_data = f"multi_choice_toggle:{question_id}:{option_id}"
            keyboard.append([InlineKeyboardButton(button_text, callback_data=callback_data)])
        
        # Кнопка "Готово"
        keyboard.append([InlineKeyboardButton("Готово", callback_data=f"multi_choice_done:{question_id}")])
        
        return InlineKeyboardMarkup(keyboard)
    
    def build_comment_prompt_keyboard(self, question_id: str, option_id: str, is_required: bool = True) -> InlineKeyboardMarkup:
        """Построить клавиатуру для запроса комментария"""
        keyboard = []
        
        if not is_required:
            # Если комментарий необязательный, добавляем кнопку "Пропустить"
            keyboard.append([InlineKeyboardButton("Пропустить", callback_data=f"skip_comment:{question_id}:{option_id}")])
        
        return InlineKeyboardMarkup(keyboard) if keyboard else None
    
    def build_text_input_keyboard(self) -> ReplyKeyboardMarkup:
        """Построить клавиатуру для текстового ввода"""
        # Для текстового ввода используем обычную клавиатуру
        keyboard = []
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    




