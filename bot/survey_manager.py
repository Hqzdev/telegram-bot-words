"""
Менеджер опроса - управление состоянием и логикой анкеты
"""

import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

class QuestionType(Enum):
    """Типы вопросов"""
    TEXT = "text"
    SINGLE_CHOICE = "single_choice"
    MULTI_CHOICE = "multi_choice"

@dataclass
class SurveyState:
    """Состояние опроса пользователя"""
    user_id: int
    current_question: str = "start"
    answers: Dict[str, Any] = field(default_factory=dict)
    multi_choice_selections: List[str] = field(default_factory=list)
    waiting_for_comment: Optional[str] = None
    comment_question: Optional[str] = None

class SurveyManager:
    """Менеджер опроса"""
    
    def __init__(self, config_file: str = "survey_config.json"):
        self.config = self._load_config(config_file)
        self.states: Dict[int, SurveyState] = {}
    
    def _load_config(self, config_file: str) -> Dict[str, Any]:
        """Загрузить конфигурацию опроса"""
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_user_state(self, user_id: int) -> SurveyState:
        """Получить состояние пользователя"""
        if user_id not in self.states:
            self.states[user_id] = SurveyState(user_id=user_id)
        return self.states[user_id]
    
    def get_welcome_message(self) -> str:
        """Получить приветственное сообщение"""
        return ("Уважаемый землевладелец, благодарим за активность и стремление к сотрудничеству! "
                "Информация необходима для формирования общего понимания ситуации и дальнейших консультаций "
                "по развитию с/х бизнеса, улучшения его эффективности на территории нашего поселения. "
                "Уважаемый землевладелец, просим ответить на ряд вопросов в анкете.")
    
    def get_question(self, question_id: str) -> Optional[Dict[str, Any]]:
        """Получить вопрос по ID"""
        return self.config.get("questions", {}).get(question_id)
    
    def get_question_text(self, question_id: str) -> str:
        """Получить текст вопроса"""
        question = self.get_question(question_id)
        return question.get("text", "") if question else ""
    
    def get_question_type(self, question_id: str) -> QuestionType:
        """Получить тип вопроса"""
        question = self.get_question(question_id)
        if not question:
            return QuestionType.TEXT
        
        type_str = question.get("type", "text")
        try:
            return QuestionType(type_str)
        except ValueError:
            return QuestionType.TEXT
    
    def get_question_options(self, question_id: str) -> List[Dict[str, Any]]:
        """Получить варианты ответов для вопроса"""
        question = self.get_question(question_id)
        return question.get("options", []) if question else []
    
    def get_next_question(self, question_id: str) -> str:
        """Получить следующий вопрос"""
        question = self.get_question(question_id)
        return question.get("next", "completed") if question else "completed"
    
    def save_answer(self, user_id: int, question_id: str, answer: Any):
        """Сохранить ответ пользователя"""
        state = self.get_user_state(user_id)
        state.answers[question_id] = answer
    
    def save_multi_choice_selection(self, user_id: int, option_id: str, selected: bool):
        """Сохранить выбор в множественном выборе"""
        state = self.get_user_state(user_id)
        if selected and option_id not in state.multi_choice_selections:
            state.multi_choice_selections.append(option_id)
        elif not selected and option_id in state.multi_choice_selections:
            state.multi_choice_selections.remove(option_id)
    
    def get_multi_choice_selections(self, user_id: int) -> List[str]:
        """Получить текущие выборы множественного выбора"""
        state = self.get_user_state(user_id)
        return state.multi_choice_selections.copy()
    
    def clear_multi_choice_selections(self, user_id: int):
        """Очистить выборы множественного выбора"""
        state = self.get_user_state(user_id)
        state.multi_choice_selections.clear()
    
    def set_waiting_for_comment(self, user_id: int, option_id: str, comment_question: str):
        """Установить ожидание комментария"""
        state = self.get_user_state(user_id)
        state.waiting_for_comment = option_id
        state.comment_question = comment_question
    
    def clear_waiting_for_comment(self, user_id: int):
        """Очистить ожидание комментария"""
        state = self.get_user_state(user_id)
        state.waiting_for_comment = None
        state.comment_question = None
    
    def is_waiting_for_comment(self, user_id: int) -> bool:
        """Проверить, ожидается ли комментарий"""
        state = self.get_user_state(user_id)
        return state.waiting_for_comment is not None
    
    def get_comment_question(self, user_id: int) -> Optional[str]:
        """Получить вопрос для комментария"""
        state = self.get_user_state(user_id)
        return state.comment_question
    
    def get_waiting_option_id(self, user_id: int) -> Optional[str]:
        """Получить ID опции, для которой ожидается комментарий"""
        state = self.get_user_state(user_id)
        return state.waiting_for_comment
    
    def move_to_next_question(self, user_id: int):
        """Перейти к следующему вопросу"""
        state = self.get_user_state(user_id)
        state.current_question = self.get_next_question(state.current_question)
        state.waiting_for_comment = None
        state.comment_question = None
    
    def get_current_question(self, user_id: int) -> str:
        """Получить текущий вопрос"""
        state = self.get_user_state(user_id)
        return state.current_question
    
    def set_current_question(self, user_id: int, question_id: str):
        """Установить текущий вопрос"""
        state = self.get_user_state(user_id)
        state.current_question = question_id
    
    def is_survey_completed(self, user_id: int) -> bool:
        """Проверить, завершен ли опрос"""
        state = self.get_user_state(user_id)
        return state.current_question == "completed"
    
    def get_all_answers(self, user_id: int) -> Dict[str, Any]:
        """Получить все ответы пользователя"""
        state = self.get_user_state(user_id)
        return state.answers.copy()
    
    def clear_user_state(self, user_id: int):
        """Очистить состояние пользователя"""
        if user_id in self.states:
            del self.states[user_id]
    
    def get_option_requires_comment(self, question_id: str, option_id: str) -> bool:
        """Проверить, требует ли опция комментария"""
        options = self.get_question_options(question_id)
        for option in options:
            if option.get("id") == option_id:
                return option.get("comment_required", False)
        return False
    
    def get_option_comment_type(self, question_id: str, option_id: str) -> str:
        """Получить тип комментария для опции"""
        options = self.get_question_options(question_id)
        for option in options:
            if option.get("id") == option_id:
                return option.get("comment_type", "none")
        return "none"
    
    def get_option_comment_question(self, question_id: str, option_id: str) -> Optional[str]:
        """Получить вопрос для комментария опции"""
        options = self.get_question_options(question_id)
        for option in options:
            if option.get("id") == option_id:
                return option.get("comment_question")
        return None
