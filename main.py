from datetime import datetime, timedelta
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

def get_full_orthodox_calendar(year):
    # =========================================================================
    # 1. МАТЕМАТИЧЕСКИЙ РАСЧЕТ ПАСХИ (Алгоритм Гаусса)
    # =========================================================================
    a = year % 19
    b = year % 4
    c = year % 7
    d = (19 * a + 15) % 30
    e = (2 * b + 4 * c + 6 * d + 6) % 7
    
    days_st = 22 + d + e
    if days_st <= 31:
        day_old, month_old = days_st, 3
    else:
        day_old, month_old = days_st - 31, 4

    # Автоматический расчет разницы календарей для любого века (для XX-XXI вв. = 13)
    century = year // 100
    diff = century - century // 4 - 2
    
    day_new = day_old + diff
    month_new = month_old
    if month_new == 3 and day_new > 31:
        day_new -= 31
        month_new = 4
    elif month_new == 4 and day_new > 30:
        day_new -= 30
        month_new = 5

    # Главная точка отсчета — Светлое Христово Воскресение
    easter = datetime(year, month_new, day_new)

    # =========================================================================
    # 2. РАСЧЕТ ПЕРЕХОДЯЩИХ ПРАЗДНИКОВ И ПОСТОВ (Зависят от Пасхи)
    # =========================================================================
    maslenica_start = easter - timedelta(days=56)
    nachalo_posta = easter - timedelta(days=48)
    lazareva = easter - timedelta(days=8)
    verbnoe = easter - timedelta(days=7)
    chistiy_chetverg = easter - timedelta(days=3)
    strastnaya_pyatnica = easter - timedelta(days=2)
    voznesenie = easter + timedelta(days=39)
    troica = easter + timedelta(days=49)
    
    # Петров пост (начинается через неделю после Троицы, до 12 июля)
    petrov_start = troica + timedelta(days=8)
    petrov_end = datetime(year, 7, 12)
    if petrov_start >= petrov_end:
        petrov_info = "В этом году отсутствует (очень поздняя Пасха)"
    else:
        petrov_info = f"с {petrov_start.day}.06 по 11.07 (Длительность: {(petrov_end - petrov_start).days} дн.)"

    # Переходящие родительские субботы
    subbota_meat = nachalo_posta - timedelta(days=9)   # Вселенская мясопустная
    subbota_2 = nachalo_posta + timedelta(days=12)     # 2-я седмица поста
    subbota_3 = nachalo_posta + timedelta(days=19)     # 3-я седмица поста
    subbota_4 = nachalo_posta + timedelta(days=26)     # 4-я седмица поста
    radonica = easter + timedelta(days=9)              # Радоница
    subbota_troica = troica - timedelta(days=1)        # Троицкая вселенская

    # =========================================================================
    # 3. ФИКСИРОВАННЫЕ ПРАЗДНИКИ (Всегда в один и тот же день)
    # =========================================================================
    fixed_dates = {
        "Рождество Христово": datetime(year, 1, 7),
        "Обрезание Господне / Св. Василия Вел.": datetime(year, 1, 14),
        "Bогоявление (Крещение Господне)": datetime(year, 1, 19),
        "Сретение Господне": datetime(year, 2, 15),
        "Благовещение Пресвятой Богородицы": datetime(year, 4, 7),
        "Рождество Иоанна Предтечи": datetime(year, 7, 7),
        "Святых апостолов Петра и Павла": datetime(year, 7, 12),
        "Преображение Господне (Яблочный Спас)": datetime(year, 8, 19),
        "Успенский пост": "с 14 по 27 августа (14 дней)",
        "Успенский пост (конец)": datetime(year, 8, 28),
        "Усекновение главы Иоанна Предтечи": datetime(year, 9, 11),
        "Рождество Пресвятой Богородицы": datetime(year, 9, 21),
        "Воздвижение Креста Господня": datetime(year, 9, 27),
        "Покров Пресвятой Богородицы": datetime(year, 10, 14),
        "Введение во храм Пресвятой Богородицы": datetime(year, 12, 4),
        "Рождественский пост": "с 28 ноября по 6 января (40 дней)"
    }

    # =========================================================================
    # 4. БЕЗОПАСНОЕ ФОРМАТИРОВАНИЕ БЕЗ ИСПОЛЬЗОВАНИЯ СИСТЕМНОЙ ЛОКАЛИ
    # =========================================================================
    def format_date(dt):
        if isinstance(dt, str):  # Если это строка с информацией о посте
            return dt
        months = {1: "января", 2: "февраля", 3: "марта", 4: "апреля", 5: "мая", 
                  6: "июня", 7: "июля", 8: "августа", 9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"}
        days = {0: "Понедельник", 1: "Вторник", 2: "Среда", 3: "Четверг", 4: "Пятница", 5: "Суббота", 6: "Воскресенье"}
        return f"{dt.day} {months[dt.month]} ({days[dt.weekday()]})"

    # Собираем данные в хронологическом порядке по объектам datetime, чтобы избежать сбоев сортировки
    events_list = [
        ("Рождество Христово", fixed_dates["Рождество Христово"]),
        ("Обрезание Господне / Св. Василия Вел.", fixed_dates["Обрезание Господне / Св. Василия Вел."]),
        ("Богоявление (Крещение Господне)", fixed_dates["Bогоявление (Крещение Господне)"]),
        ("Масленица (начало)", maslenica_start),
        ("Сретение Господне", fixed_dates["Сретение Господне"]),
        ("НАЧАЛО ВЕЛИКОГО ПОСТА", nachalo_posta),
        ("Благовещение Пресвятой Богородицы", fixed_dates["Благовещение Пресвятой Богородицы"]),
        ("Лазарева суббота", lazareva),
        ("Вербное Воскресенье", verbnoe),
        ("Чистый Четверг", chistiy_chetverg),
        ("Страстная Пятница", strastnaya_pyatnica),
        ("ПАСХА ХРИСТОВА", easter),
        ("Вознесение Господне", voznesenie),
        ("День Святой Троицы", troica),
        ("ПЕТРОВ ПОСТ (Апостольский)", petrov_info),
        ("Рождество Иоанна Предтечи", fixed_dates["Рождество Иоанна Предтечи"]),
        ("Святых апостолов Петра и Павла", fixed_dates["Святых апостолов Петра и Павла"]),
        ("УСПЕНСКИЙ ПОСТ", fixed_dates["Успенский post"]),
        ("Преображение Господне", fixed_dates["Преображение Господне (Яблочный Спас)"]),
        ("Успение Пресвятой Богородицы", fixed_dates["Успенский пост (конец)"]),
        ("Усекновение главы Иоанна Предтечи", fixed_dates["Усекновение главы Иоанна Предтечи"]),
        ("Рождество Пресвятой Богородицы", fixed_dates["Рождество Пресвятой Богородицы"]),
        ("Воздвижение Креста Господня", fixed_dates["Воздвижение Креста Господня"]),
        ("Покров Пресвятой Богородицы", fixed_dates["Покров Пресвятой Богородицы"]),
        ("Введение во храм Богородицы", fixed_dates["Введение во храм Пресвятой Богородицы"]),
        ("РОЖДЕСТВЕНСКИЙ ПОСТ", fixed_dates["Рождественский пост"])
    ]

    # Сортируем список по дате (строки-описания постов ставим условно в конец или обрабатываем)
    events_list.sort(key=lambda x: x[1] if isinstance(x[1], datetime) else datetime(year, 1, 1))

    # Форматируем в текст
    result_text = f"=== КАЛЕНДАРЬ НА {year} ГОД ===\n\n"
    for name, date_val in events_list:
        result_text += f"• {name}:\n  {format_date(date_val)}\n\n"

    result_text += "=== РОДИТЕЛЬСКИЕ СУББОТЫ ===\n\n"
    result_text += f"• Вселенская мясопустная: {format_date(subbota_meat)}\n"
    result_text += f"• 2-я седмица поста: {format_date(subbota_2)}\n"
    result_text += f"• 3-я седмица поста: {format_date(subbota_3)}\n"
    result_text += f"• 4-я седмица поста: {format_date(subbota_4)}\n"
    result_text += f"• Радоница: {format_date(radonica)}\n"
    result_text += f"• Троицкая вселенская: {format_date(subbota_troica)}\n"

    return result_text

# =========================================================================
# 5. ГРАФИЧЕСКИЙ ИНТЕРФЕЙС KIVY ДЛЯ СБОРКИ НА ANDROID
# =========================================================================
class OrthodoxCalendarApp(App):
    def build(self):
        self.title = "Православный Календарь"
        
        # Главный контейнер
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Контейнер для ввода года
        input_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=100, spacing=10)
        
        self.year_input = TextInput(
            text=str(datetime.now().year),
            multiline=False,
            input_filter='int',
            font_size=32,
            halign='center',
            size_hint_x=0.6
        )
        
        calc_button = Button(
            text="Расчитать",
            font_size=24,
            size_hint_x=0.4,
            background_color=(0.2, 0.6, 0.8, 1)
        )
        calc_button.bind(on_press=self.calculate_calendar)
        
        input_layout.add_widget(self.year_input)
        input_layout.add_widget(calc_button)
        main_layout.add_widget(input_layout)
        
        # Область для вывода календаря с прокруткой
        scroll = ScrollView(size_hint=(1, 1))
        self.result_label = Label(
            text="Введите год выше и нажмите кнопку.",
            font_size=20,
            size_hint_y=None,
            halign='left',
            valign='top'
        )
        self.result_label.bind(texture_size=self.result_label.setter('size'))
        
        scroll.add_widget(self.result_label)
        main_layout.add_widget(scroll)
        
        return main_layout

    def calculate_calendar(self, instance):
        try:
            year = int(self.year_input.text)
            if 1 <= year <= 9999:
                calendar_data = get_full_orthodox_calendar(year)
                self.result_label.text = calendar_data
            else:
                self.result_label.text = "Ошибка: введите корректный год (1 - 9999)."
        except ValueError:
            self.result_label.text = "Пожалуйста, введите числовое значение года."

if __name__ == '__main__':
    OrthodoxCalendarApp().run()
