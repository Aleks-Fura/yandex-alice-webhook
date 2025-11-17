from flask import Flask, request, jsonify
import logging
import random

app = Flask(__name__)

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Варианты приветствий (3 шт)
GREETINGS = [
    "Доброе утро, Савенька! Как твоё настроение?",
    "Привет, Сав! Ну что, как дела сегодня?",
    "Эй, Савенька! Расскажи, как настроение?"
]

# Варианты для хорошего настроения (3 шт) - с матерными словами
GOOD_MOOD_RESPONSES = [
    "Ура, Савенька! Я так рада! Сегодня будет замечательный день - ты всё успеешь, всё получится, и энергии хватит на всё! Вперёд покорять мир! Вкл muzu!",
    "Заебись! Вот это я понимаю! С таким настроем горы свернёшь! Держи энергию и вперёд, Сав! Вкл muzu!",
    "Пиздато! Отличный настрой на день! Сегодня точно всё будет огонь! Поглади делать дела! Вкл muzu!"
]

# Варианты для плохого настроения (3 шт)
BAD_MOOD_RESPONSES = [
    "Эх, Савенька, не грусти! Знаешь, что поможет? Три подтягивания на турнике - и мир сразу заиграет новыми красками! Эндорфины разгонят хандру, обещаю!",
    "Бывает, Сав! Слушай, сделай одну простую вещь: выпей стакан холодной воды и сделай пару глубоких вдохов. Потом турник - и сразу полетаешь! Я в тебя верю!",
    "Понимаю, бывает такие дни. Но ты же знаешь рецепт: движение! Даже пара подтягиваний запустит химию счастья в мозгу. Давай, Савенька, ты сильная!"
]

# Вариант для неопределённого ответа - с возвратом к вопросу
CLARIFY_RESPONSES = [
    "Хм, что-то я не поняла! Ну давай, говори конкретно: настроение-то как? Хорошо или плохо?",
    "Эээ, погоди, это что было? Отвечай нормально: как настроение, Сав? Хорошо или не очень?",
    "Стоп-стоп, я запуталась! Давай ещё раз: настроение отличное или так себе?"
]

# Ответ по умолчанию для хорошего настроения (используется после 2 попыток)
DEFAULT_GOOD_RESPONSE = "Окей, понял! Ну тогда иди делай! Вкл muzu!"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        logger.info(f"Received request: {data}")
        
        # Получаем текущее состояние сессии
                logger.info(f"State object: {data.get('state', {})}")
        session_state = data.get('state', {}).get('session', {})
        attempts = session_state.get('attempts', 0)
                logger.info(f"Session state: {session_state}, attempts: {attempts}")
        
        # Извлекаем текст и intent
        request_data = data.get('request', {})
        intent = request_data.get('nlu', {}).get('intents', {})
        
        # Проверяем, является ли это новой сессией
        if data.get('session', {}).get('new', False):
            # Новая сессия - приветствие
            text = random.choice(GREETINGS)
            new_state = {'attempts': 0}
            end_session = False
        elif 'good_mood' in intent:
            # Позитивный ответ - выбираем из хороших вариантов
            text = random.choice(GOOD_MOOD_RESPONSES)
            new_state = {'attempts': 0}
            end_session = True
        elif 'bad_mood' in intent:
            # Негативный ответ - выбираем из плохих вариантов
            text = random.choice(BAD_MOOD_RESPONSES)
            new_state = {'attempts': 0}
            end_session = True
        else:
            # Неопределённый ответ - проверяем количество попыток
            if attempts >= 2:
                # После 2 попыток уточнения - принимаем как хорошее настроение
                text = DEFAULT_GOOD_RESPONSE
                new_state = {'attempts': 0}
                end_session = True
            else:
                # Просим уточнить
                text = random.choice(CLARIFY_RESPONSES)
                new_state = {'attempts': attempts + 1}
                end_session = False
        
        response = {
            'response': {
                'text': text,
                'end_session': end_session
            },
            'session_state': new_state,
            'version': '1.0'
        }
        
        logger.info(f"Sending response: {response}")
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({
            'response': {
                'text': 'Ой, что-то пошло не так! Попробуй ещё раз.',
                'end_session': True
            },
            'version': '1.0'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
