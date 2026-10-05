import webbrowser
from datetime import datetime, timedelta
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp, sp


def get_full_orthodox_calendar(year):
    # 1. МАТЕМАТИЧЕСКИЙ РАСЧЕТ ПАСХИ (Алгоритм Гаусса)
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

    easter = datetime(year, month_new, day_new)

    # 2. РАСЧЕТ ПЕРЕХОДЯЩИХ ПРАЗДНИКОВ И ПОСТОВ
    maslenica_start = easter - timedelta(days=56)
    nachalo_posta = easter - timedelta(days=48)
    lazareva = easter - timedelta(days=8)
    verbnoe = easter - timedelta(days=7)
    chistiy_chetverg = easter - timedelta(days=3)
    strastnaya_pyatnica = easter - timedelta(days=2)
    voznesenie = easter + timedelta(days=39)
    troica = easter + timedelta(days=49)

    petrov_start = troica + timedelta(days=8)
    petrov_end = datetime(year, 7, 12)
    if petrov_start >= petrov_end:
        petrov_info = "В этом году отсутствует (очень поздняя Пасха)"
    else:
        days_cnt = (petrov_end - petrov_start).days
        petrov_info = f"с {petrov_start.day}.06 по 11.07 ({days_cnt} дн.)"

    subbota_meat = nachalo_posta - timedelta(days=9)
    subbota_2 = nachalo_posta + timedelta(days=12)
    subbota_3 = nachalo_posta + timedelta(days=19)
    subbota_4 = nachalo_posta + timedelta(days=26)
    radonica = easter + timedelta(days=9)
    subbota_troica = troica - timedelta(days=1)

    # 3. ФИКСИРОВАННЫЕ ДАТЫ
    fixed_dates = {
        "Рождество Христово":
            datetime(year, 1, 7),
        "Обрезание Господне / Св. Василия Вел.":
            datetime(year, 1, 14),
        "Богоявление (Крещение Господне)":
            datetime(year, 1, 19),
        "Сретение Господне":
            datetime(year, 2, 15),
        "Благовещение Пресвятой Богородицы":
            datetime(year, 4, 7),
        "Рождество Иоанна Предтечи":
            datetime(year, 7, 7),
        "Святых апостолов Петра и Павла":
            datetime(year, 7, 12),
        "Преображение Господне":
            datetime(year, 8, 19),
        "Успенский пост (начало)":
            "с 14 по 27 августа (14 дней)",
        "Уснение Пресвятой Богородицы":
            datetime(year, 8, 28),
        "Усекновение главы Иоанна Предтечи":
            datetime(year, 9, 11),
        "Рождество Пресвятой Богородицы":
            datetime(year, 9, 21),
        "Воздвижение Креста Господня":
            datetime(year, 9, 27),
        "Покров Пресвятой Богородицы":
            datetime(year, 10, 14),
        "Введение во храм Пресвятой Богородицы":
            datetime(year, 12, 4),
        "Рождественский пост":
            "с 28 ноября по 6 января (40 дней)"
    }

    # 4. БЕЗОПАСНОЕ ФОРМАТИРОВАНИЕ ДАТЫ
    def format_date(dt):
        if isinstance(dt, str):
            return dt
        months = {
            1: "января", 2: "февраля", 3: "марта", 4: "апреля",
            5: "мая", 6: "июня", 7: "июля", 8: "августа",
            9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
        }
        days = {
            0: "Понедельник", 1: "Вторник", 2: "Среда",
            3: "Четверг", 4: "Пятница", 5: "Суббота", 6: "Воскресенье"
        }
        return f"{dt.day} {months[dt.month]} ({days[dt.weekday()]})"

    # Базовый URL для сокращения длины строк кода
    base_url = "https://azbyka.ru"

    events_list = [
        (f"[color=ff6b6b]• [ref={base_url}]Рождество Христово[/ref][/color]",
         fixed_dates["Рождество Христово"]),
        (f"[color=ff6b6b]• [ref={base_url}]Обрезание Господне[/ref][/color]",
         fixed_dates["Обрезание Господне / Св. Василия Вел."]),
        (f"[color=ff6b6b]• [ref={base_url}]Богоявление (Крещение)[/ref][/color]",
         fixed_dates["Богоявление (Крещение Господне)"]),
        (f"[color=4dabf7]• [ref={base_url}]Масленица (начало)[/ref][/color]",
         maslenica_start),
        (f"[color=ff6b6b]• [ref={base_url}]Сретение Господне[/ref][/color]",
         fixed_dates["Сретение Господне"]),
        (f"[color=51cf66]• [ref={base_url}]НАЧАЛО ВЕЛИКОГО ПОСТА[/ref][/color]",
         nachalo_posta),
        (f"[color=ff6b6b]• [ref={base_url}]Благовещение Богородицы[/ref][/color]",
         fixed_dates["Благовещение Пресвятой Богородицы"]),
        (f"[color=4dabf7]• [ref={base_url}]Лазарева суббота[/ref][/color]",
         lazareva),
        (f"[color=4dabf7]• [ref={base_url}]Вербное Воскресенье[/ref][/color]",
         verbnoe),
        (f"[color=4dabf7]• [ref={base_url}]Чистый Четверг[/ref][/color]",
         chistiy_chetverg),
        (f"[color=4dabf7]• [ref={base_url}]Страстная Пятница[/ref][/color]",
         strastnaya_pyatnica),
        (f"[color=ffd700][b]•• [ref={base_url}]ПАСХА ХРИСТОВА[/ref] ••[/b][/color]",
         easter),
        (f"[color=4dabf7]• [ref={base_url}]Вознесение Господне[/ref][/color]",
         voznesenie),
        (f"[color=4dabf7]• [ref={base_url}]День Святой Троицы[/ref][/color]",
         troica),
        (f"[color=51cf66]• [ref={base_url}]ПЕТРОВ ПОСТ[/ref][/color]",
         petrov_info),
        (f"[color=ff6b6b]• [ref={base_url}]Рождество Иоанна Предтечи[/ref][/color]",
         fixed_dates["Рождество Иоанна Предтечи"]),
        (f"[color=ff6b6b]• [ref={base_url}]Святых апостолов Петра и Павла[/ref][/color]",
         fixed_dates["Святых апостолов Петра и Павла"]),
        (f"[color=51cf66]• [ref={base_url}]УСПЕНСКИЙ ПОСТ[/ref][/color]",
         fixed_dates["Успенский пост (начало)"]),
        (f"[color=ff6b6b]• [ref={base_url}]Преображение Господне[/ref][/color]",
         fixed_dates["Преображение Господне"]),
        (f"[color=ff6b6b]• [ref={base_url}]Уснение Пресвятой Богородицы[/ref][/color]",
         fixed_dates["Уснение Пресвятой Богородицы"]),
        (f"[color=ff6b6b]• [ref={base_url}]Усекновение главы Иоанна Предтечи[/ref][/color]",
         fixed_dates["Усекновение главы Иоанна Предтечи"]),
        (f"[color=ff6b6b]• [ref={base_url}]Рождество Богородицы[/ref][/color]",
         fixed_dates["Рождество Пресвятой Богородицы"]),
        (f"[color=ff6b6b]• [ref={base_url}]Воздвижение Креста Господня[/ref][/color]",
         fixed_dates["Воздвижение Креста Господня"]),
        (f"[color=ff6b6b]• [ref={base_url}]Покров Пресвятой Богородицы[/ref][/color]",
         fixed_dates["Покров Пресвятой Богородицы"]),
        (f"[color=ff6b6b]• [ref={base_url}]Введение во храм Богородицы[/ref][/color]",
         fixed_dates["Введение во храм Пресвятой Богородицы"]),
        (f"[color=51cf66]• [ref={base_url}]РОЖДЕСТВЕНСКИЙ ПОСТ[/ref][/color]",
         fixed_dates["Рождественский пост"])
    ]

    result_text = f"[size={int(sp(26))}][b]КАЛЕНДАРЬ НА {year} ГОД[/b][/size]"
    msg = "(нажмите на название для описания)"
    result_text += f"[size={int(sp(14))}][color=aaaaaa]{msg}[/color][/size]"

    for name, date_val in events_list:
        result_text += f"{name}[color=ffffff]{format_date(date_val)}[/color]"
        result_text += f"[size={int(sp(24))}][b]РОДИТЕЛЬСКИЕ СУББОТЫ[/b][/size]"
        result_text += f"[color=b197fc]• [ref={base_url}]Вселенская мясопустная:[/ref][/color]{format_date(subbota_meat)}"
        result_text += f"[color=b197fc]• [ref={base_url}]2-я седмица поста:[/ref][/color]{format_date(subbota_2)}"
        result_text += f"[color=b197fc]• [ref={base_url}]3-я седмица поста:[/ref][/color]{format_date(subbota_3)}"
        result_text += f"[color=b197fc]• [ref={base_url}]4-я седмица поста:[/ref][/color]{format_date(subbota_4)}"
        result_text += f"[color=b197fc]• [ref={base_url}]Радоница:[/ref][/color]{format_date(radonica)}"
        result_text += f"[color=b197fc]• [ref={base_url}]Троицкая вселенская:[/ref][/color]{format_date(subbota_troica)}"

    return result_text


class OrthodoxCalendarApp(App):
    def build(self):
        self.title = "Православный Календарь"

        root_scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False)

        self.container = BoxLayout(
            orientation='vertical', padding=dp(20), spacing=dp(20), size_hint_y=None
        )
        self.container.bind(minimum_height=self.container.setter('height'))

        input_layout = BoxLayout(
            orientation='horizontal', size_hint_y=None, height=dp(70), spacing=dp(10)
        )

        btn_minus = Button(
            text="< -1 год",
            font_size=sp(18),
            size_hint_x=0.3,
            background_color=(0.2, 0.25, 0.3, 1),
            background_normal=''
        )
        btn_minus.bind(on_press=self.decrement_year)

        self.year_input = TextInput(
            text=str(datetime.now().year),
            multiline=False,
            input_filter='int',
            font_size=sp(26),
            halign='center',
            size_hint_x=0.4,
            padding=[0, dp(15), 0, 0]
        )
        self.year_input.bind(on_text_validate=self.calculate_calendar)

        btn_plus = Button(
            text="+1 год >",
            font_size=sp(18),
            size_hint_x=0.3,
            background_color=(0.2, 0.25, 0.3, 1),
            background_normal=''
        )
        btn_plus.bind(on_press=self.increment_year)

        input_layout.add_widget(btn_minus)
        input_layout.add_widget(self.year_input)
        input_layout.add_widget(btn_plus)
        self.container.add_widget(input_layout)

        self.result_label = Label(
            text="",
            font_size=sp(21),
            size_hint_y=None,
            halign='left',
            valign='top',
            markup=True,
            color=(1, 1, 1, 1)
        )
        self.result_label.bind(texture_size=self.result_label.setter('size'))
        self.result_label.bind(
            width=lambda instance, value: setattr(instance, 'text_size', (value, None))
        )
        self.result_label.bind(on_ref_press=self.open_holiday_link)

        self.container.add_widget(self.result_label)
        root_scroll.add_widget(self.container)

        self.calculate_calendar(None)

        return root_scroll

    def open_holiday_link(self, instance, value):
        try:
            webbrowser.open(value)
        except Exception:
            pass

    def decrement_year(self, instance):
        try:
            current_year = int(self.year_input.text)
            if current_year > 1:
                self.year_input.text = str(current_year - 1)
                self.calculate_calendar(None)
        except ValueError:
            pass

    def increment_year(self, instance):
        try:
            current_year = int(self.year_input.text)
            if current_year < 9999:
                self.year_input.text = str(current_year + 1)
                self.calculate_calendar(None)
        except ValueError:
            pass

    def calculate_calendar(self, instance):
        try:
            year = int(self.year_input.text)
            if 1 <= year <= 9999:
                calendar_data = get_full_orthodox_calendar(year)
                self.result_label.text = calendar_data
            else:
                err_msg = "[color=ff6b6b]Ошибка: введите год от 1 до 9999.[/color]"
                self.result_label.text = err_msg
        except Exception as e:
            err_text = f"[color=ff6b6b]Произошла ошибка при расчете:\n{str(e)}[/color]"
            self.result_label.text = err_text


if __name__ == '__main__':
    OrthodoxCalendarApp().run()
