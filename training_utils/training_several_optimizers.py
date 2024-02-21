from ultralytics import YOLO
from telegram import Bot
import requests
import json
import asyncio
import os


async def get_id(bot_token):
    """
    Obtención del id del chat con el bot.
    :param bot_token:
    :return:
    """
    url_id = "https://api.telegram.org/bot" + bot_token + "/getUpdates"
    response = requests.get(url_id)
    decode_result = response.content.decode("utf-8")
    dict_result = json.loads(decode_result)
    return dict_result["result"][0]["message"]["chat"]["id"]


async def main():
    """
    Este script permite el entrenamiento con varios optimizadores de manera automatica, en el se debe configurar
     el token de un bot de telegram al cual se le enviaran los resultados cuando cada entrenamiento comienze y finalice.

    Nota: Tener en cuenta que este script funcionara en el entorno de entrenamiento y se debe instalar la librería
            python-telegram-bot
    :return:
    """
    bot_token = os.environ.get("BOT_TOKEN") # definir variable de entorno con "export BOT_TOKEN="<API KEY>"
    bot = Bot(token=bot_token)
    chat_id = await get_id(bot_token)

    # Load a model
    model = YOLO('/shared_directory/yolov8s.pt')  # load a pretrained model (recommended for training)

    optimizers = ["SGD", "Adam", "AdamW", "NAdam", "RAdam", "RMSProp"]
    batch = [16, 32, 40]

    for optimizer in optimizers:
        await bot.send_message(chat_id=chat_id,
                               text=f"Entrenamiento con {optimizer} iniciado...\nTiempo estimado: 16hs")
        try:
            results = model.train(data='/shared_directory/yolov8/data.yaml', epochs=200, imgsz=640, batch=batch[1],
                                  patience=30, workers=0, device=0, optimizer=optimizer)
            messaje = f"Entrenamiento con {optimizer} finalizado...\n" + f"batch_size: {batch[1]}\n" + "Métricas de presicion:\n" + json.dumps(
                results.results_dict)
            await bot.send_message(chat_id=chat_id, text=messaje)
        except:
            messaje = "Ha ocurrido un error en el entrenamiento"
            await bot.send_message(chat_id=chat_id, text=messaje)


if __name__ == "__main__":
    asyncio.run(main())
