import logging
import sys
import os
import math

os.makedirs("logs", exist_ok=True)

log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(
    level=logging.DEBUG,
    format=log_format,
    datefmt=date_format,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/file_txt.log", encoding="utf-8")
    ]
)

logging.info("Логгер успешно сконфигурирован")
logging.info("Приложение запущено")

def calculate_triangle(str_a, str_b, str_c):
    logging.info(f"Получены входные данные: A={str_a}, B={str_b}, C={str_c}")
    
    try:
        a = float(str_a)
        b = float(str_b)
        c = float(str_c)
    except ValueError as ex:
        logging.error("Ошибка: переданы нечисловые (невалидные) данные.")
        logging.exception("Детали ошибки конвертации:")
        return "", [(-2, -2), (-2, -2), (-2, -2)]

    epsilon = 1e-9

    if a <= 0 or b <= 0 or c <= 0 or not (a + b > c + epsilon and a + c > b + epsilon and b + c > a + epsilon):
        logging.warning(f"Некорректные размеры сторон для треугольника: A={a}, B={b}, C={c}")
        return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

    if abs(a - b) < epsilon and abs(b - c) < epsilon:
        t_type = "равносторонний"
    elif abs(a - b) < epsilon or abs(b - c) < epsilon or abs(a - c) < epsilon:
        t_type = "равнобедренный"
    else:
        t_type = "разносторонний"
    
    logging.info(f"Определен тип треугольника: {t_type}")

    try:
        max_side = max(a, b, c)
        scale = 70.0 / max_side if max_side > 0 else 1.0
        sa = a * scale
        sb = b * scale
        sc = c * scale

        x1, y1 = 10, 80
        x2 = int(x1 + sa)
        y2 = 80

        cos_val = (sb**2 + sc**2 - sa**2) / (2 * sb * sc) if (sb * sc) > 0 else 0
        cos_val = max(-1.0, min(1.0, cos_val))
        sin_val = math.sqrt(1.0 - cos_val**2)

        x3 = int(x1 + sb * cos_val)
        y3 = int(y1 - sb * sin_val)

        coords = [
            (max(0, min(100, x1)), max(0, min(100, y1))),
            (max(0, min(100, x2)), max(0, min(100, y2))),
            (max(0, min(100, x3)), max(0, min(100, y3)))
        ]
        logging.info(f"Рассчитаны координаты вершин: {coords}")
    except Exception as ex:
        logging.error("Ошибка при расчете координат.")
        logging.exception(ex)
        coords = [(-1, -1), (-1, -1), (-1, -1)]

    return t_type, coords

if __name__ == "__main__":

    while True:
        user_input = input("\nВведите стороны a, b, c через пробел (или 'q' для выхода): ").strip()
        
        if user_input.lower() == 'q':
            print("Выход из программы. Логи сохранены в logs/file_txt.log.")
            logging.info("Приложение остановлено пользователем.")
            break
            
        parts = user_input.split()
        if len(parts) != 3:
            print("Ошибка: нужно ввести ровно три значения")
            continue
            
        t_type, coords = calculate_triangle(parts[0], parts[1], parts[2])
        
        if t_type == "":
            print("Ошибка: введены нечисловые значения")
        elif t_type == "не треугольник":
            print("Треугольник с такими сторонами не существует.")
        else:
            print(f"Тип треугольника: {t_type}")
            print(f"Координаты вершин: {coords}")