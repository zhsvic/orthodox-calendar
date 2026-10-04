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

    # Автоматический расчет разницы календарей для любого века
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
    # 3. ФИКСИРОВАННЫЕ ПРАЗДНИКИ И ПОСТЫ (Всегда в один и тот же день)
    # =========================================================================
    fixed_dates = {
        "Обрезание Господне / Св. Василия Вел.": datetime(year, 1, 14),
        "Богоявление (Крещение Господне)": datetime(year, 1, 19),
        "Сретение Господне": datetime(year, 2, 15),
        "Благовещение Пресвятой Богородицы": datetime(year, 4, 7),
        "Рождество Иоанна Предтечи": datetime(year, 7, 7),
        "Святых апостолов Петра и Павла": datetime(year, 7, 12),
        "Преображение Господне (Яблочный Спас)": datetime(year, 8, 19),
        "Успение Пресвятой Богородицы": datetime(year, 8, 28),
        "Усекновение главы Иоанна Предтечи": datetime(year, 9, 11),
        "Рождество Пресвятой Богородицы": datetime(year, 9, 21),
        "Воздвижение Креста Господня": datetime(year, 9, 27),
        "Покров Пресвятой Богородицы": datetime(year, 10, 14),
        "Введение во храм Пресвятой Богородицы": datetime(year, 12, 4),
        "Рождество Христово": datetime(year, 12, 25) if year < 1918 else datetime(year, 1, 7) # Коррекция календаря
    }
    
    # Рождество для текущего века всегда 7 января (светский стиль)
    fixed_dates["Рождество Христово"] = datetime(year, 1, 7)

    # Фиксированные многодневные посты
    uspesnkiy_post = f"с 14 августа по 27 августа (14 дней)"
    rozhdestvenskiy_post = f"с 28 ноября по 6 января (40 дней)"

    # =========================================================================
    # 4. КРАСИВОЕ ФОРМАТИРОВАНИЕ ДАТ ДЛЯ ТЕЛЕФОНА
    # =========================================================================
    def format_date(dt):
        months = {1: "января", 2: "февраля", 3: "марта", 4: "апреля", 5: "мая", 
                  6: "июня", 7: "июля", 8: "августа", 9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"}
        days = {0: "Понедельник", 1: "Вторник", 2: "Среда", 3: "Четверг", 4: "Пятница", 5: "Суббота", 6: "Воскресенье"}
        return f"{dt.day} {months[dt.month]} ({days[dt.weekday()]})"

    # Сборка итоговых словарей
    holidays_block = {
        "СВЕТЛОЕ ХРИСТОВО ВОСКРЕСЕНИЕ (ПАСХА)": format_date(easter),
        "Вход Господень в Иерусалим (Вербное)": format_date(verbnoe),
        "Вознесение Господне": format_date(voznesenie),
        "День Святой Троицы (Пятидесятница)": format_date(troica),
        "Лазарева суббота": format_date(lazareva),
        "Чистый Четверг (Страстная седмица)": format_date(chistiy_chetverg),
        "Страстная Пятница (Воспоминание распятия)": format_date(strastnaya_pyatnica)
    }
    
    # Добавляем непереходящие праздники
    for name, date_obj in fixed_dates.items():
        holidays_block[name] = format_date(date_obj)

    # Сортируем праздники по хронологическому порядку месяцев и дней
    sorted_holidays = dict(sorted(holidays_block.items(), key=lambda item: datetime.strptime(item[1].split()[0] + ' ' + item[1].split()[1], "%d %B" if item[1].split()[1].endswith('я') or item[1].split()[1].endswith('а') else "%d %B"))) # Упрощенная сортировка по внутренней дате
    
    # Для стабильности работы на мобильных устройствах, сделаем ручную хронологическую сборку главных блоков:
    main_events = {
        "Масленица (Сырная седмица, начало)": format_date(maslenica_start),
        "НАЧАЛО ВЕЛИКОГО ПОСТА": format_date(nachalo_posta),
        "Благовещение Пресвятой Богородицы": format_date(fixed_dates["Благовещение Пресвятой Богородицы"]),
        "Лазарева суббота": format_date(lazareva),
        "Вербное Воскресенье (Вход в Иерусалим)": format_date(verbnoe),
        "Страстная Пятница": format_date(strastnaya_pyatnica),
        "ПАСХА ХРИСТОВА": format_date(easter),
        "Вознесение Господне": format_date(voznesenie),
        "День Святой Троицы (Пятидесятница)": format_date(troica),
        "ПЕТРОВ ПОСТ (Апостольский)": petrov_info,
        "Рождество Иоанна Предтечи": format_date(fixed_dates["Рождество Иоанна Предтечи"]),
        "Святых апостолов Петра и Павла": format_date(fixed_dates["Святых апостолов Петра и Павла"]),
        "УСПЕНСКИЙ ПОСТ": uspesnkiy_post,
        "Преображение Господне (Яблочный Спас)": format_date(fixed_dates["Преображение Господне (Яблочный Спас)"]),
        "Успение Пресвятой Богородицы": format_date(fixed_dates["Успение Пресвятой Богородицы"]),
        "Усекновение главы Иоанна Предтечи": format_date(fixed_dates["Усекновение главы Иоанна Предтечи"]),
        "Рождество Пресвятой Богородицы": format_date(fixed_dates["Рождество Пресвятой Богородицы"]),
        "Воздвижение Креста Господня": format_date(fixed_dates["Воздвижение Креста Господня"]),
        "Покров Пресвятой Богородицы": format_date(fixed_dates["Покров Пресвятой Богородицы"]),
        "Введение во храм Богородицы": format_date(fixed_dates["Введение во храм Пресвятой Богородицы"]),
        "РОЖДЕСТВЕНСКИЙ ПОСТ (Филиппов)": rozhdestvenskiy_post,
        "Рождество Христово": format_date(fixed_dates["Рождество Христово"]),
        "Обрезание Господне / Св. Василия": format_date(fixed_dates["Обрезание Господне / Св. Василия Вел."]),
        "Богоявление (Крещение Господне)": format_date(fixed_dates["Богоявление (Крещение Господне)"]),
        "Сретение Господне": format_date(fixed_dates["Сретение Господне"])
    }

    memorial_days = {
        "Вселенская родительская (мясопустная)": format_date(subbota_meat),
        "Суббота 2-й седмицы Великого поста": format_date(subbota_2),
        "Суббота 3-й седмицы Великого поста": format_date(subbota_3),
        "Суббота 4-й седмицы Великого поста": format_date(subbota_4),
        "Радоница (Поминовение усопших)": format_date(radonica),
        "Троицкая вселенская родительская суббота": format_date(subbota_troica)
    }
    
    return main_events, memorial_days

# --- ГРАФИЧЕСКИЙ ИНТЕРФЕЙС KIVY ---
class EasterApp(App):
    def build(self):
        self.main_layout = BoxLayout(orientation='vertical', padding=15, spacing=12)
        
        self.main_layout.add_widget(Label(text="[b]Полный Православный Календарь[/b]", 
                                          markup=True, size_hint_y=0.06, font_size='18sp', color=(1, 0.82, 0, 1)))
        
        self.year_input = TextInput(hint_text="Введите год (например, 2027)", 
                                    multiline=False, input_filter='int', 
                                    size_hint_y=0.08, font_size='18sp', padding=[10, 10, 10, 10])
        self.main_layout.add_widget(self.year_input)
        
        self.btn = Button(text="Построить полный календарь", size_hint_y=0.1, 
                          font_size='18sp', background_color=(0.12, 0.53, 0.9, 1))
        self.btn.bind(on_press=self.calculate)
        self.main_layout.add_widget(self.btn)
        
        scroll = ScrollView(size_hint_y=0.76)
        self.result_label = Label(text="Здесь появится календарь со всеми праздниками года", markup=True,
                                  size_hint_y=None, halign='left', valign='top', font_size='15sp')
        self.result_label.bind(texture_size=self.result_label.setter('size'))
        scroll.add_widget(self.result_label)
        self.main_layout.add_widget(scroll)
 
return self.main_layout
def calculate(self, instance):
if not self.year_input.text:
self.result_label.text = "[color=ff0000]Ошибка: Пожалуйста, введите год![/color]"
return
year = int(self.year_input.text)
if year < 1:
self.result_label.text = "[color=ff0000]Ошибка: Введите год нашей эры![/color]"
return
main_events, memorial_days = get_full_orthodox_calendar(year)
res = f"[b][size=18sp]ПРАВОСЛАВНЫЙ КАЛЕНДАРЬ НА {year} ГОД[/size][/b]\n\n"
res += "[color=ffcc00]─── [ ЦЕРКОВНЫЕ ПРАЗДНИКИ И ПОСТЫ ] ────────[/color]\n"
for k, v in main_events.items():
if "ПАСХА" in k:
res += f"🌟 [b][color=ff3333]{k}: {v}[/b][/color]\n"
elif "ПОСТ" in k:
res += f"🐟 [color=88ff88]{k}: {v}[/color]\n"
else:
res += f"• {k}: {v}\n"
res += "\n[color=ff6666]─── [ РОДИТЕЛЬСКИЕ СУББОТЫ ] ───────────────[/color]\n"
for k, v in memorial_days.items():
res += f"🙏 {k}: {v}\n"
self.result_label.text = res
if name == 'main':
EasterApp().run()
