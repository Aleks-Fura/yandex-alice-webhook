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

# Новый навык "Я дома" - встреча дома после работы
@app.route('/home-welcome', methods=['POST'])
def home_welcome():
    try:
        data = request.json
        logger.info(f"Received home welcome request: {data}")
        
                GREETINGS_ALONE = [
            "Наконец-то! Ну как там, выжил на этом заводе?",
            "О, ты вернулся! Как день прошел? Расскажи, что там творилось?",
            "Привет-привет! Ну что, как прошла смена?"
        ]
        
        # Варианты заботливых ответов (рандомно)
        CARE_RESPONSES = [
            "Держись, я тебя понимаю. Слушай, давай по плану: сначала в душ марш, никаких 'пять минуточек на кровати'. Потом готовишь ужин, кушаешь и НЕ ЗАБУДЬ витамины! А уже после можешь залипать в ютубы.",
            "Ну что поделать, работа такая. Короче, вот что: душ сейчас же, потом на кухню. Приготовишь что-нибудь нормальное, поешь, витамины выпей - и только тогда можешь расслабляться. Понял меня?",
            "Эх, бывает и хуже. Ладно, давай действуй: первым делом - душ, освежись. Затем ужин готовь, и обязательно витамины не пропусти! А там уже можешь делать что хочешь.",
            "Понимаю-понимаю. Но расслабляться рано! Сначала душ принимаешь, потом идешь готовить. Поел - витамины выпил, запомнил? И только после этого разрешаю валяться с телефоном.",
            "Ничего, завтра будет полегче. А сейчас слушай сюда: в душ немедленно, потом готовишь ужин. За ужином витамины - это святое! И уже потом можешь ютубчики свои включать."
        ]
        
        # Варианты саркастических ответов для гостей (рандомно)
        GUEST_RESPONSES = [
            "Ааа, понятно... Ну что ж, придется потесниться. Надеюсь, это ненадолго. Располагайтесь, я тут в углу посижу.",
            "Мда, вот так сюрприз. Ладно уж, так и быть, я потерплю. Только не привыкай часто с компанией приходить, а?",
            "Хм, интересно. Ну ничего, держу себя в руках. Хотя предупреждать можно было заранее, между прочим.",
            "О как! Гости, значит. Ладно, не буду мешать, постараюсь вести себя прилично. Но это особый случай, учти.",
            "Вот это поворот... Ну окей, буду культурной. Надеюсь, долго засиживаться не будете?"
        ]
        
        # Получаем текст запроса
        user_text = data.get('request', {}).get('original_utterance', '').lower()
        
        # Проверяем на "мы" в запросе
        if 'мы' in user_text or data.get('session', {}).get('new', False):
            if data.get('session', {}).get('new', False):
                # Первый запуск - проверяем на "мы"
                if 'мы' in user_text:
                    text = "Ого, а ты не один? И кто же это с тобой?"
                    session_state = 'waiting_for_name'
                else:
                    text = random.choice(GREETINGS_ALONE)
                    session_state = 'waiting_for_response'
            elif data.get('session_state', {}).get('state') == 'waiting_for_name':
                # Получили имя гостя
                text = random.choice(GUEST_RESPONSES)
                session_state = 'done'
            elif data.get('session_state', {}).get('state') == 'waiting_for_response':
                # Получили ответ о самочувствии - даем заботливый совет
                text = random.choice(CARE_RESPONSES)
                session_state = 'done'
            else:
                text = "Хорошо, отдыхай!"
                session_state = 'done'
        
        response = {
            'response': {
                'text': text,
                'end_session': session_state == 'done'
            },
            'session_state': {
                'state': session_state
            },
            'version': '1.0'
        }
        
        logger.info(f"Sending home welcome response: {response}")
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error processing home welcome request: {str(e)}")
        return jsonify({
            'response': {
                'text': 'Ой, что-то пошло не так! Попробуй ещё раз.',
                'end_session': True
            },
            'version': '1.0'
        }), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
