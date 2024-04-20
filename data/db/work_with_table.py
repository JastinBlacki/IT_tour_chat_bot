from data.db.query import get_data
from PIL import Image, ImageDraw, ImageFont
from config import PATH_FOR_TABLES
import os


def data_for_table(user_id):
    data_list = get_data(user_id)
    Pv, r, n = data_list
    r = round(float(r) / 12, 3)
    n = round(float(n) * 12, 3)
    P = Pv * r * (1 + r) ** n / (1 + r) ** n - 2
    sum_p = Pv + P
    data = []
    for num in range(int(n)):
        sum_p -= sum_p * r / 100
        data.append([str(num), str(round(sum_p, 2)), str(round(r, 2)), str(round(Pv, 2)), str(round(P,2))])
    return data


def create_table(user_id):

    data = data_for_table(user_id)

    image_width = 750
    image_height = len(data) * 35
    image = Image.new('RGB', (image_width, image_height), color = (255, 255, 255))
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype('arial.ttf', 16)
    draw.text((10, 10), "№ платежа | Остаток задолженности | Начисленные проценты | Основной долг | Сумма платежа", fill=(0, 0, 0), font=font)

    font = ImageFont.truetype('arial.ttf', 16)
    y_position = 40
    for row in data:
        x_position = 10
        for item in row:
            draw.text((x_position, y_position), item, fill=(0, 0, 0), font=font)
            x_position += 150
        y_position += 30

    image.save(f'{PATH_FOR_TABLES}table{user_id}.png')


def delete_img(user_id):
    os.remove(f'{PATH_FOR_TABLES}table{user_id}.png')
