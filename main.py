from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return 'Yandex Alice Webhook Server is running!'

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        logger.info(f'Received request: {data}')
        
        # Проверяем наличие интента
        intents = data.get('request', {}).get('nlu', {}).get('intents', {})
        
        # Определяем ответ на основе интента
        if 'mood_excellent' in intents:
            text = "Ура, Сашенька! Я так рада! Сегодня будет замечательный день - ты всё успеешь, всё получится, и энергии хватит на всё! Вперёд покорять мир! Включаю Европа Плюс!"
        elif 'mood_bad' in intents:
            text = "Эх, Сашенька, не грусти! Знаешь, что поможет? Три подтягивания на турнике - и мир сразу заиграет новыми красками! Эндорфины разгонят хандру, обещаю. Давай, ты справишься! А потом включу тебе музыку для настроения!"
        else:
            text = "Хм, это не 'отлично', а значит, есть куда расти! Рецепт простой: бахнуть крепкого кофе и бегом на работу - день сам наладится по пути! Держись, Сашенька, у тебя всё получится! Включаю Европа Плюс!"
        
        response = {
            'response': {
                'text': text,
                'end_session': True
            },
            'version': '1.0'
        }
        
        logger.info(f'Sending response: {response}')
        return jsonify(response)
    
    except Exception as e:
        logger.error(f'Error processing request: {e}')
        return jsonify({
            'response': {
                'text': 'Произошла ошибка. Попробуй ещё раз!',
                'end_session': True
            },
            'version': '1.0'
        }), 500

if __name__ == '__main__':
    port = 10000
    app.run(host='0.0.0.0', port=port, debug=False)
