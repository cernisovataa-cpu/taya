import math
import matplotlib.pyplot as plt


def calculate_coverage():

    print("РОЗРАХУНОК ЗОНИ ПОКРИТТЯ БАЗОВОЇ СТАНЦІЇ (Модель Окумура-Хата)")


    bs_params = {}

    try:
        print("\nВведення вихідних даних ")

        # 1. Введення та перевірка частоти
        f_val = float(input("Введіть робочу частоту f (від 150 до 1500 МГц): "))
        if f_val < 150 or f_val > 1500:
            print("    ПОПЕРЕДЖЕННЯ: Нормальний діапазон частот для цієї моделі варіюється від 150 до 1500 МГц.")
            print(
                "   Пояснення: При введенні занадто низьких або високих частот формули можуть дати теоретичний, а не практичний результат. Розрахунок продовжується...\n")
        bs_params['f'] = f_val

        # 2. Введення та перевірка потужності
        ptx_val = float(input("Введіть потужність передавача БС Ptx (від 20 до 50 дБм): "))
        if ptx_val < 20 or ptx_val > 50:
            print("    ПОПЕРЕДЖЕННЯ: Нормальний діапазон потужності БС варіюється від 20 до 50 дБм.")
            print(
                "   Пояснення: Введене значення є нетиповим для стандартних макростільників. Розрахунок продовжується...\n")
        bs_params['ptx'] = ptx_val

        # 3. Введення висоти вишки
        hb_val = float(input("Введіть висоту антени БС hb (від 10 до 100 м): "))
        if hb_val < 10 or hb_val > 100:
            print("    ПОПЕРЕДЖЕННЯ: Нормальна висота вишки варіюється від 10 до 100 метрів.")
            print(
                "   Пояснення: Занадто низька або висока антена сильно вплине на радіус покриття. Розрахунок продовжується...\n")
        bs_params['hb'] = hb_val

        # 4. Введення висоти абонента
        bs_params['hm'] = float(input("Введіть висоту антени абонента hm (від 1 до 2 м): "))

        # 5. Введення та перевірка чутливості
        psens_val = float(input("Введіть чутливість приймача телефона Psens (від -70 до -120 дБм): "))
        if psens_val > -70 or psens_val < -120:
            print("   ПОПЕРЕДЖЕННЯ: Нормальний діапазон чутливості телефонів варіюється від -70 до -120 дБм.")
            print(
                "   Пояснення: Якщо значення плюсове або ближче до нуля, сигнал зникне миттєво. Якщо менше -120, радіус буде нереалістично великим. Розрахунок продовжується...\n")
        bs_params['psens'] = psens_val

        gtx = 15  # Підсилення антени БС (дБ)
        grx = 0  # Підсилення антени мобільного (дБ)

        print("\n Оберіть тип місцевості")
        print("1 - Місто (мале або середнє)")
        print("2 - Передмістя")
        print("3 - Сільська місцевість / Відкритий простір")
        terrain_type = int(input("Ваш вибір (1, 2 або 3): "))

        if terrain_type not in [1, 2, 3]:
            print("   Увага: невідомий тип місцевості. Автоматично обрано Місто (1).")
            terrain_type = 1

    except ValueError:
        print("\n ПОМИЛКА ВВОДУ: Ви ввели літери або символи замість чисел!")
        print("Програма зупинена. Запустіть її знову.")
        return

    # Ініціалізація списків для графіка
    distances = []
    signal_levels = []

    d = 0.1  # Початкова відстань у кілометрах
    step = 0.1  # Крок

    f = bs_params['f']
    hb = bs_params['hb']
    hm = bs_params['hm']
    ptx = bs_params['ptx']
    psens = bs_params['psens']

    # Коригуючий коефіцієнт антени мобільної станції
    ahm = (1.1 * math.log10(f) - 0.7) * hm - (1.56 * math.log10(f) - 0.8)

    print("\nВиконується розрахунок...")

    # Цикл розрахунку втрат на різних відстанях
    while True:
        # Базова формула втрат Хата
        lpath = 69.55 + 26.16 * math.log10(f) - 13.82 * math.log10(hb) - ahm + (
                    44.9 - 6.55 * math.log10(hb)) * math.log10(d)

        # Коригування залежно від місцевості
        if terrain_type == 1:
            l_total = lpath
        elif terrain_type == 2:
            l_total = lpath - 2 * (math.log10(f / 28)) ** 2 - 5.4
        elif terrain_type == 3:
            l_total = lpath - 4.78 * (math.log10(f)) ** 2 + 18.33 * math.log10(f) - 40.94

            # Розрахунок потужності прийнятого сигналу
        prx = ptx + gtx - l_total + grx

        distances.append(d)
        signal_levels.append(prx)

        # Якщо сигнал слабший за чутливість — зупиняємо розрахунок
        if prx < psens:
            break

            # Запобіжник від нескінченного розрахунку (захист системи)
        if d > 150:
            print("\n ДОСЯГНУТО АПАРАТНИЙ ЛІМІТ: Відстань перевищила 150 км.")
            print("Примусова зупинка розрахунків для запобігання зависанню комп'ютера.")
            break

        d += step

    max_distance = round(d - step, 2)


    print(f"РЕЗУЛЬТАТ: Максимальний радіус зони покриття = {max_distance} км")

    # Збереження результатів у файл
    report_filename = "coverage_report.txt"
    try:
        with open(report_filename, "w", encoding="utf-8") as file:
            file.write("=== ЗВІТ ПРО РОЗРАХУНОК ЗОНИ ПОКРИТТЯ БАЗОВОЇ СТАНЦІЇ ===\n")
            file.write(f"Частота: {f} МГц\n")
            file.write(f"Потужність БС: {ptx} дБм\n")
            file.write(f"Висота БС: {hb} м\n")
            file.write(f"Висота абонента: {hm} м\n")
            file.write(f"Чутливість приймача: {psens} дБм\n")

            terrain_name = {1: "Місто", 2: "Передмістя", 3: "Село"}.get(terrain_type)
            file.write(f"Тип місцевості: {terrain_name}\n")
            file.write("-" * 50 + "\n")
            file.write(f"Радіус впевненого покриття: {max_distance} км\n")

        print(f"Звіт успішно збережено у файл: {report_filename}")
    except Exception as e:
        print("Помилка при збереженні файлу.")

    # Побудова графіка
    print("\nГенерую графік... (Закрийте вікно з графіком для завершення програми)")

    plt.figure(figsize=(10, 6))
    plt.plot(distances, signal_levels, label="Рівень сигналу (Prx)", color='blue', linewidth=2)
    plt.axhline(y=psens, color='red', linestyle='--', label=f"Межа чутливості ({psens} дБм)")

    plt.title(f"Затухання сигналу базової станції (Частота: {f} МГц, Радіус: {max_distance} км)")
    plt.xlabel("Відстань від базової станції (км)")
    plt.ylabel("Потужність прийнятого сигналу (дБм)")
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    calculate_coverage()