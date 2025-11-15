from flask import Flask, request, jsonify
import logging
import random

app = Flask(__name__)

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Варианты приветствий (3 шт)
GREETINGS = [
    "Доброе утро, Сашенька! Как твоё настроение?",
    "Привет, Саш! Ну что, как дела сегодня?",
    "Эй, Сашенька! Расскажи, как настроение?"
]

# Варианты для хорошего настроения (3 шт) - с матерными словами
GOOD_MOOD_RESPONSES = [
    "Ура, Сашенька! Я так рада! Сегодня будет замечательный день - ты всё успеешь, всё получится, и энергии хватит на всё! Вперёд покорять мир! Включаю Европа Плюс!",
    "Заебись! Вот это я понимаю! С таким настроем горы свернёшь! Держи энергию и вперёд, Саш! Включаю музыку!",
    "Пиздато! Отличный настрой на день! Сегодня точно всё будет огонь! Погнали делать дела! Включаю Европа Плюс!"
]

# Варианты для плохого настроения (3 шт)
BAD_MOOD_RESPONSES = [
    "Эх, Сашенька, не грусти! Знаешь, что поможет? Три подтягивания на турнике - и мир сразу заиграет новыми красками! Эндорфины разгонят хандру, обещаю. Давай, ты справишься! А потом включу тебе музыку для настроения!",
    "Бывает, Саш! Слушай, сделай одну простую вещь: выпей стакан холодной воды и сделай пару глубоких вдохов. Потом турник - и сразу полегчает! Я в тебя верю!",
    "Понимаю, бывают такие дни. Но ты же знаешь рецепт: движение! Даже пара подтягиваний запустит химию счастья в мозгу. Давай, Сашенька, ты сильный! А я включу что-нибудь бодрое!"
]

# Вариант для неопределённого ответа - с возвратом к вопросу
CLARIFY_RESPONSES = [
    "Хм, что-то я не поняла! Ну давай, говори конкретно: настроение-то как? Хорошо или плохо?",
    "Эээ, погоди, это что было? Отвечай нормально: как настроение, Саш? Хорошо или не очень?",
    "Стоп-стоп, я запуталась! Давай ещё раз: настроение отличное или так себе?",
    "Непонятно как-то! Саш, ну скажи просто: дела хорошо или плохо?"
]

@app.route('/')
def index():
    return 'Yandex Alice Webhook Server is running!'

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        logger.info(f"Received request: {data}")
        
        # Проверяем наличие интента
        intents = data.get('request', {}).get('nlu', {}).get('intents', {})
        
        # Для первого запуска - отправляем приветствие
        if data.get('session', {}).get('new', False):
            text = random.choice(GREETINGS)
        # Определяем ответ на основе интента
        elif 'mood_excellent' in intents:
            text = random.choice(GOOD_MOOD_RESPONSES)
        elif 'mood_bad' in intents:
            text = random.choice(BAD_MOOD_RESPONSES)
        else:
            # Неопределённый ответ - просим уточнить
            text = random.choice(CLARIFY_RESPONSES)
        
        response = {
            'response': {
                'text': text,
                'end_session': False  # Не заканчиваем сессию, чтобы был повтор
            },
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
    app.run(host='0.0.0.0', port=10000)
