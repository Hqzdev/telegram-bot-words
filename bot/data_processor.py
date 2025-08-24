"""
Модуль для обработки и форматирования данных опроса
"""

import re
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
                    # Используем display_text если есть, иначе обычный text
                    option_text = option.get("display_text", option.get("text", ""))
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
                # Используем display_text если есть, иначе обычный text
                return option.get("display_text", option.get("text", ""))
        
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
                        # Используем display_text если есть, иначе обычный text
                        option_text = option.get("display_text", option.get("text", ""))
                        break
                
                # Добавляем комментарий, если есть
                if option_id in comments and comments[option_id]:
                    # Для опции "Другое" объединяем display_text с комментарием
                    if option_id == "q3_2_other":
                        option_text = f"{option_text} {comments[option_id]}"
                    else:
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
                        # Используем display_text если есть, иначе обычный text
                        formatted_options.append(option.get("display_text", option.get("text", "")))
                        break
            
            return "; ".join(formatted_options)
        
        return str(answer)
    
    def validate_answer(self, question_id: str, answer: Any) -> bool:
        """Проверить валидность ответа"""
        question_type = self.survey_manager.get_question_type(question_id)
        
        if question_type.value == "text":
            if not isinstance(answer, str) or answer.strip() == "":
                return False
            
            # Проверяем дополнительную валидацию
            validation_type = self.survey_manager.get_question_validation(question_id)
            if validation_type:
                return self._validate_by_type(validation_type, answer)
            
            return True
        
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
    
    def _validate_by_type(self, validation_type: str, value: str) -> bool:
        """Валидация по типу"""
        if validation_type == "email":
            return self._validate_email(value)
        elif validation_type == "phone":
            return self._validate_phone(value)
        elif validation_type == "number":
            return self._validate_number(value)
        elif validation_type == "full_name":
            return self._validate_full_name(value)
        elif validation_type == "telegram_username":
            return self._validate_telegram_username(value)
        elif validation_type == "cadastral_number":
            return self._validate_cadastral_number(value)
        return True
    
    def _validate_email(self, email: str) -> bool:
        """Валидация email адреса"""
        # Простая проверка на наличие @ и точки
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_pattern, email.strip()))
    
    def _validate_phone(self, phone: str) -> bool:
        """Валидация номера телефона"""
        # Убираем все пробелы, скобки, дефисы и плюсы
        cleaned_phone = re.sub(r'[\s\(\)\-\+]', '', phone)
        # Проверяем, что остались только цифры и длина от 10 до 15 символов
        return cleaned_phone.isdigit() and 10 <= len(cleaned_phone) <= 15
    
    def _validate_number(self, number: str) -> bool:
        """Валидация числового значения"""
        try:
            # Пробуем преобразовать в float (поддерживает десятичные числа)
            float(number.strip())
            return True
        except ValueError:
            return False
    
    def _validate_full_name(self, full_name: str) -> bool:
        """Валидация ФИО (минимум 3 слова)"""
        # Убираем лишние пробелы и считаем слова
        words = [word.strip() for word in full_name.split() if word.strip()]
        return len(words) >= 3
    
    def _validate_telegram_username(self, username: str) -> bool:
        """Валидация имени в Telegram (обязательно @)"""
        # Проверяем, что есть символ @
        return '@' in username.strip()
    
    def _validate_cadastral_number(self, cadastral: str) -> bool:
        """Валидация кадастрового номера (только цифры и двоеточия)"""
        # Убираем лишние пробелы
        cadastral = cadastral.strip()
        
        # Проверяем, что строка содержит только цифры и двоеточия
        # И что есть хотя бы одна цифра и одно двоеточие
        if not cadastral:
            return False
        
        # Проверяем, что строка состоит только из цифр и двоеточий
        if not re.match(r'^[\d:]+$', cadastral):
            return False
        
        # Проверяем, что есть хотя бы одна цифра
        if not re.search(r'\d', cadastral):
            return False
        
        # Проверяем, что есть хотя бы одно двоеточие
        if ':' not in cadastral:
            return False
        
        return True
    
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



