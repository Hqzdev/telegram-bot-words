"""
Модуль для обработки и форматирования данных опроса
"""

from typing import List, Dict, Any
from bot.survey_manager import SurveyManager

class DataProcessor:
    """Обработчик данных опроса"""
    
    def __init__(self, survey_manager: SurveyManager):
        self.survey_manager = survey_manager
    
    def format_answers_for_sheets(self, user_id: int) -> List[List[str]]:
        """Форматировать ответы для записи в Google Sheets"""
        answers = self.survey_manager.get_all_answers(user_id)
        formatted_data = []
        
        # Проходим по всем вопросам в конфигурации
        for question_id, question_data in self.survey_manager.config.get("questions", {}).items():
            question_text = question_data.get("text", "")
            answer = answers.get(question_id, "")
            
            # Форматируем ответ в зависимости от типа вопроса
            formatted_answer = self._format_answer(question_id, answer)
            
            # Добавляем строку в данные
            formatted_data.append([question_text, formatted_answer])
        
        return formatted_data
    
    def _format_answer(self, question_id: str, answer: Any) -> str:
        """Форматировать ответ для отображения"""
        if not answer:
            return ""
        
        question_type = self.survey_manager.get_question_type(question_id)
        
        if question_type.value == "text":
            return str(answer)
        
        elif question_type.value == "single_choice":
            return self._format_single_choice_answer(question_id, answer)
        
        elif question_type.value == "multi_choice":
            return self._format_multi_choice_answer(question_id, answer)
        
        return str(answer)
    
    def _format_single_choice_answer(self, question_id: str, answer: Any) -> str:
        """Форматировать ответ одиночного выбора"""
        if isinstance(answer, dict):
            # Если ответ содержит выбор и комментарий
            selected_option = answer.get("option", "")
            comment = answer.get("comment", "")
            
            # Находим текст выбранной опции
            options = self.survey_manager.get_question_options(question_id)
            option_text = ""
            for option in options:
                if option.get("id") == selected_option:
                    option_text = option.get("text", "")
                    break
            
            # Формируем ответ
            result = option_text
            if comment:
                result += f" - {comment}"
            
            return result
        
        # Если ответ - просто ID опции
        options = self.survey_manager.get_question_options(question_id)
        for option in options:
            if option.get("id") == answer:
                return option.get("text", "")
        
        return str(answer)
    
    def _format_multi_choice_answer(self, question_id: str, answer: Any) -> str:
        """Форматировать ответ множественного выбора"""
        if isinstance(answer, dict):
            # Если ответ содержит выборы и комментарии
            selected_options = answer.get("options", [])
            comments = answer.get("comments", {})
            
            formatted_options = []
            options = self.survey_manager.get_question_options(question_id)
            
            for option_id in selected_options:
                # Находим текст опции
                option_text = ""
                for option in options:
                    if option.get("id") == option_id:
                        option_text = option.get("text", "")
                        break
                
                # Добавляем комментарий, если есть
                if option_id in comments and comments[option_id]:
                    option_text += f" - {comments[option_id]}"
                
                formatted_options.append(option_text)
            
            return "; ".join(formatted_options)
        
        # Если ответ - просто список ID опций
        if isinstance(answer, list):
            options = self.survey_manager.get_question_options(question_id)
            formatted_options = []
            
            for option_id in answer:
                for option in options:
                    if option.get("id") == option_id:
                        formatted_options.append(option.get("text", ""))
                        break
            
            return "; ".join(formatted_options)
        
        return str(answer)
    
    def validate_answer(self, question_id: str, answer: Any) -> bool:
        """Проверить валидность ответа"""
        question_type = self.survey_manager.get_question_type(question_id)
        
        if question_type.value == "text":
            return isinstance(answer, str) and answer.strip() != ""
        
        elif question_type.value == "single_choice":
            options = self.survey_manager.get_question_options(question_id)
            valid_ids = [option.get("id") for option in options]
            return answer in valid_ids
        
        elif question_type.value == "multi_choice":
            if isinstance(answer, list):
                options = self.survey_manager.get_question_options(question_id)
                valid_ids = [option.get("id") for option in options]
                return all(option_id in valid_ids for option_id in answer)
            elif isinstance(answer, dict):
                return "options" in answer and isinstance(answer["options"], list)
        
        return False
    
    def get_required_fields(self, question_id: str) -> List[str]:
        """Получить список обязательных полей для вопроса"""
        question_type = self.survey_manager.get_question_type(question_id)
        
        if question_type.value == "text":
            return ["text"]
        
        elif question_type.value == "single_choice":
            options = self.survey_manager.get_question_options(question_id)
            required_fields = ["option"]
            
            # Проверяем, есть ли обязательные комментарии
            for option in options:
                if option.get("comment_required", False):
                    required_fields.append("comment")
                    break
            
            return required_fields
        
        elif question_type.value == "multi_choice":
            return ["options"]
        
        return []
