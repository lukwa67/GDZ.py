import tkinter as tk
from tkinter import ttk, messagebox
import threading
import re
import os     # Для работы с Рабочим столом и папкой AppData
import json   # Для сохранения темы оформления

# =====================================================================
#       ШАГ 1 ИЗ 4: СИСТЕМНЫЕ НАСТРОЙКИ И БАЗА РУССКИХ СЛОВ
# =====================================================================

# Путь для автоматического сохранения выбранной темы оформления в AppData
CONFIG_DIR = os.path.join(os.environ.get("APPDATA", ""), "SuperGDZ")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

RUSSIAN_WORDS = [
    "пошел", "школа", "санаторий", "солнце", "здравствуй", "очередь", 
    "корова", "молоко", "пирог", "пирожков", "всего", "привет", 
    "купил", "больше", "меньше", "ваня", "коля", "дети", "яблоко",
    "класс", "ученик", "учитель", "тетрадь", "учебник", "задача",
    "пример", "решение", "ответ", "сумма", "разность", "произведение",
    "деление", "умножение", "цифра", "число", "уравнение", "пропорция",
    "процент", "столбик", "скорость", "время", "расстояние", "путь",
    "километр", "метр", "час", "минута", "секунда", "машина", "поезд"
]
# =====================================================================
#       ЧАСТЬ 2 ИЗ 8: ИМЕНА И БАЗА АНГЛИЙСКИХ СЛОВ (SPOTLIGHT)
# =====================================================================

# Дописываем имена и персонажей к русскому словарю
RUSSIAN_WORDS.extend([
    "самолет", "пешеход", "велосипедист", "рубль", "копейка", "цена",
    "количество", "стоимость", "сдача", "было", "потратил", "осталось",
    "периметр", "площадь", "длина", "ширина", "высота", "прямоугольник",
    "квадрат", "треугольник", "сантиметр", "миллиметр", "килограмм", "грамм",
    "язык", "текст", "слово", "предложение", "буква", "звук", "гласный",
    "согласный", "ударение", "слог", "корень", "суффикс", "приставка",
    "окончание", "ошибка", "исправление", "правило", "диктант", "изложение",
    "сочинение", "домашняя", "работа", "классная", "задание", "урок",
    "петя", "маша", "миша", "саша", "лена", "дима", "оля", "игорь",
    "ларри", "лулу", "чаклс", "нэнни", "шайн", "гарри", "дядя", "теара", 
    "кэти", "джон", "билл", "сэлли", "пит", "эмма", "ли", "дэвид", 
    "джейн", "марк", "мэри", "дэн", "сьюзан", "пол", "анн"
])

ENGLISH_WORDS = {
    # Герои Spotlight 1-4
    "lulu": "Лулу (Lulu)", "larry": "Ларри (Larry)", "chuckles": "Чаклс (Chuckles)",
    "nanny": "Няня (Nanny)", "rose": "Роуз (Няня Роуз)", "shine": "Шайн (Няня Шайн)",
    "uncle": "дядя", "harry": "Гарри (Дядя Гарри — ветеринар из Австралии)",
    "aunt": "тётя", "pam": "Пэм (Тётя Пэм)", "cousin": "двоюродный брат / кузен", "robbie": "Робби (Кузен Робби)",
    "william": "Уильям", "tom": "Том", "simon": "Саймон", "dan": "Дэн", "bob": "Боб", "fifi": "Фифи",
    "punch": "Панч", "judy": "Джуди", "sam": "Сэм", "bella": "Белла", "arthur": "Артур", "rascal": "Раскал", "tricky": "Трики", "paco": "Пако", "rosy": "Рози",
    # Герои Spotlight 5-7
    "theara": "Теара", "kathy": "Кэти", "john": "Джон", "bill": "Билл", "sally": "Сэлли", "pete": "Пит", "emma": "Эмма", "lee": "Ли", "david": "Дэвид", "jane": "Джейн", "mark": "Марк", "mary": "Мэри", "dan": "Дэн", "susan": "Сьюзан", "paul": "Пол", "ann": "Анн",
    # Внешность, вещи, спорт
    "tall": "высокий", "short": "низкий", "slim": "стройный", "hair": "волосы", "fair hair": "светлые волосы", "dark hair": "тёмные волосы", "funny": "забавный", "kind": "добрый", "friendly": "дружелюбный", "shirt": "рубашка", "trousers": "брюки",
    "watch": "часы", "cds": "диски", "guitar": "гитара", "hairbrush": "расческа", "helmet": "шлем", "camera": "фотоаппарат", "keys": "ключи", "gloves": "перчатки", "mobile phone": "телефон", "roller blades": "ролики", "box": "коробка", "clock": "настенные часы",
    "in": "в", "on": "на", "under": "под", "next to": "рядом с", "behind": "позади", "in front of": "перед",
    "skiing": "лыжи", "sailing": "парусный спорт", "skating": "коньки", "violin": "скрипка", "surfing": "серфинг", "diving": "ныряние",
    # Профессии и здания
    "baker": "пекарь", "greengrocer": "продавец овощей", "mechanic": "механик", "postman": "почтальон", "waiter": "официант", "nurse": "медсестра", "vet": "ветеринар", "uniform": "форма", "injection": "укол", "curtain": "занавеска",
    "station": "станция", "garage": "гараж", "cafe": "кафе", "theatre": "театр", "baker's": "пекарня", "hospital": "больница", "greengrocer's": "овощной", "post office": "почта",
    "always": "всегда", "usually": "обычно", "sometimes": "иногда", "never": "никогда", "how often": "как часто", "wake up late": "поздно просыпаться",
    # Общие школьные слова
    "school": "школа", "computer": "компьютер", "english": "английский", "book": "книга", "task": "задача", "example": "пример", "solution": "решение", "answer": "ответ", "rule": "правило", "error": "ошибка", "correct": "правильно", "number": "число"
}
# =====================================================================
#       ЧАСТЬ 3 ИЗ 8: ОФЛАЙН-АЛГОРИТМ ЛЕВЕНШТЕЙНА С ТРИГГЕРОМ ЗАСТАВКИ
# =====================================================================

def lev_distance(s1, s2):
    if len(s1) < len(s2): return lev_distance(s2, s1)
    if len(s2) == 0: return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def find_closest_word(word, word_list, max_dist=2):
    word = word.lower().strip(",.?!()\"")
    if not word: return None
    if word in word_list: return word
    closest = None
    min_d = max_dist + 1
    for w in word_list:
        d = lev_distance(word, w)
        if d < min_d:
            min_d = d
            closest = w
    return closest if min_d <= max_dist else None

# СИСТЕМНЫЙ СИГНАЛ ДЛЯ ЗАКРЫТИЯ ЗАСТАВКИ ПРИ СБОРКЕ И ОФЛАЙН-ТЕСТАХ
try:
    import pyi_splash 
    if pyi_splash.is_alive():
        pyi_splash.close()
except Exception:
    pass
# =====================================================================
#       ЧАСТЬ 4 ИЗ 8: МАТЕМАТИЧЕСКИЕ АЛГОРИТМЫ И СУПЕР ИИ ЗАДАЧ
# =====================================================================

def compare_expressions(expr_text):
    parts = re.split(r'\s+и\s+|\s*vs\s*|\s*,\s*', expr_text.lower())
    if len(parts) != 2: return "❌ Ошибка: Введите два выражения через 'и'"
    try:
        val1 = eval(parts[0].strip())
        val2 = eval(parts[1].strip())
        sign = ">" if val1 > val2 else ("<" if val1 < val2 else "=")
        return f"📊 Сравнение выражений:\n Левая часть: {parts[0].strip()} = {val1}\n Правая часть: {parts[1].strip()} = {val2}\n\n✅ Итог: {val1} {sign} {val2}"
    except: return "❌ Ошибка: Проверьте правильность знаков выражений."

def get_division_column(dividend, divisor):
    if divisor == 0: return "❌ На ноль делить нельзя!"
    quotient = dividend // divisor
    remainder = dividend % divisor
    s_dividend, s_divisor, s_quotient = str(dividend), str(divisor), str(quotient)
    lines = [f" {dividend}  │ {divisor}"]
    current_idx, current_val_str, step = 0, "", 0
    while current_idx < len(s_dividend):
        current_val_str += s_dividend[current_idx]
        current_val = int(current_val_str)
        current_idx += 1
        if current_val >= divisor:
            mult = current_val // divisor
            sub_val = mult * divisor
            indent = " " * (current_idx - len(str(current_val)) + 1)
            if step == 0:
                space_fill = " " * (len(s_dividend) - len(str(sub_val)))
                lines.append(f"{indent}─{sub_val}{space_fill}  ├──" + "─" * max(len(s_divisor), len(s_quotient)))
                lines.append(f"{indent}{' ' * len(str(sub_val))}{space_fill}  │ {quotient}")
            else:
                lines.append(f"{indent} {current_val}\n{indent}─{sub_val}\n{indent} " + "─" * len(str(sub_val)))
            current_val = current_val - sub_val
            current_val_str = str(current_val) if current_val != 0 or current_idx < len(s_dividend) else ""
            step += 1
    final_indent = " " * (len(s_dividend) + 1)
    lines.append(f"{final_indent}0  (нацело)" if remainder == 0 else f"{final_indent}{remainder}  (остаток)")
    return "\n".join(lines)

def solve_text_task(task_text):
    text = task_text.lower()
    numbers = [int(n) for n in re.findall(r'\d+', text)]
    if not numbers: return "❌ Ошибка: В тексте задачи не найдено численных данных."
    
    if "за" in text and ("рубл" in text or "коп" in text):
        try:
            if len(numbers) >= 3:
                k1, price_total1, k2 = numbers[0], numbers[1], numbers[2]
                name1 = "Катя" if "катя" in text else "Lulu" if "lulu" in text else "1-й объект"
                name2 = "Ваня" if "ваня" in text else "Chuckles" if "chuckles" in text else "2-й объект"
                
                one_price = price_total1 // k1
                price_total2 = k2 * one_price
                final_sum = price_total1 + price_total2
                
                out = "📝 КРАТКАЯ ЗАПИСЬ:\n┌──────────────────────────────────────────┐\n"
                out += f"  {name1} — {k1} шт. за {price_total1} руб.  ┐\n"
                out += f"                                   ├─ ? рублей (Всего)\n"
                out += f"  {name2} — {k2} шт. за ? руб.     ┘\n"
                out += "└──────────────────────────────────────────┘\n\n"
                out += "📊 РЕШЕНИЕ (в 3 действия):\n"
                out += f"1) {price_total1} : {k1} = {one_price} руб. — цена за 1 шт.\n"
                out += f"2) {k2} * {one_price} = {price_total2} руб. — заплатил {name2}.\n"
                out += f"3) {price_total1} + {price_total2} = {final_sum} руб. — стоимость всей покупки.\n\n"
                out += f"✅ ОТВЕТ: Вся покупка стоила {final_sum} рублей."
                return out
        except Exception:
            pass

    if "больше" in text or "меньше" in text:
        if len(numbers) >= 2:
            n1, n2 = numbers[0], numbers[1]
            name1 = "Lulu" if "lulu" in text else "Ваня" if "ваня" in text else "1-й объект"
            name2 = "Chuckles" if "chuckles" in text else "Коля" if "коля" in text else "2-й объект"
            
            if "в" in text and "больше" in text:
                res1 = n1 * n2
                out = "📝 КРАТКАЯ ЗАПИСЬ:\n┌──────────────────────────────────────────┐\n"
                out += f"  {name1} — {n1} шт.            ┐\n"
                out += f"                                ├─ ? шт. (Всего)\n"
                out += f"  {name2} — ?, в {n2} раз БОЛЬШЕ  ┘\n"
                out += "└──────────────────────────────────────────┘\n\n"
                out += f"📊 РЕШЕНИЕ:\n1) {n1} * {n2} = {res1} шт. (у {name2})\n2) {n1} + {res1} = {n1 + res1} шт.\n\n✅ ОТВЕТ: Всего {n1 + res1} шт."
                return out
            elif "на" in text and "больше" in text:
                res1 = n1 + n2
                out = "📝 КРАТКАЯ ЗАПИСЬ:\n┌──────────────────────────────────────────┐\n"
                out += f"  {name1} — {n1} шт.            ┐\n"
                out += f"                                ├─ ? шт. (Всего)\n"
                out += f"  {name2} — ?, на {n2} шт. БОЛЬШЕ  ┘\n"
                out += "└──────────────────────────────────────────┘\n\n"
                out += f"📊 РЕШЕНИЕ:\n1) {n1} + {n2} = {res1} шт. (у {name2})\n2) {n1} + {res1} = {n1 + res1} шт.\n\n✅ ОТВЕТ: Всего {n1 + res1} шт."
                return out
                
    return f"📝 КРАТКАЯ ЗАПИСЬ:\n┌──────────────────────────────┐\n  Дано числа: {', '.join(map(str, numbers))}\n└──────────────────────────────┘\n\n📊 РЕШЕНИЕ: {' + '.join(map(str, numbers))} = {sum(numbers)}"
# =====================================================================
#   ЧАСТЬ 5 ИЗ 8 (КУСОК 1 ИЗ 2): ИНИЦИАЛИЗАЦИЯ И КЭШИРОВАНИЕ ЗАСТАВКИ
# =====================================================================

class GDZApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 ИИ-ПОМОЩНИК ГДЗ v2.5 — [LUKWA STUDIOS]")
        
        # Скрываем главное окно на время показа игровой заставки
        self.root.withdraw()
        
        self.window_width = 760
        self.window_height = 680
        self.root.geometry(f"{self.window_width}x{self.window_height}")
        self.root.resizable(False, False)
        self.font_size = 10
        
        self.themes = {
            "🌌 Тёмный космос": {
                "main": "#1E222B", "card": "#282C34", "tab_sel": "#3E4451",
                "text_lbl": "#61AFEF", "text_ent": "#FFFFFF", "text_hint": "#ABB2BF", "text_out": "#FFFFFF",
                "btn_math": "#4CAF50", "btn_rus": "#FF9800", "btn_en": "#009688", "btn_extra": "#2196F3", "btn_fg": "#FFFFFF"
            },
            "🧛 Ночной вампир": {
                "main": "#1E1F29", "card": "#2D3139", "tab_sel": "#FF79C6",
                "text_lbl": "#FF79C6", "text_ent": "#F8F8F2", "text_hint": "#6272A4", "text_out": "#FFFFFF",
                "btn_math": "#50FA7B", "btn_rus": "#FFB86C", "btn_en": "#8BE9FD", "btn_extra": "#BD93F9", "btn_fg": "#1E1F29"
            },
            "🌱 Лесная прохлада": {
                "main": "#161B16", "card": "#222A22", "tab_sel": "#4E774E",
                "text_lbl": "#A3BE8C", "text_ent": "#E0E0E0", "text_hint": "#859985", "text_out": "#FFFFFF",
                "btn_math": "#A3BE8C", "btn_rus": "#D08770", "btn_en": "#88C0D0", "btn_extra": "#5E81AC", "btn_fg": "#161B16"
            },
            "☀️ Светлый день": {
                "main": "#F5F5F5", "card": "#FFFFFF", "tab_sel": "#E0E0E0",
                "text_lbl": "#1565C0", "text_ent": "#212121", "text_hint": "#757575", "text_out": "#212121",
                "btn_math": "#2E7D32", "btn_rus": "#EF6C00", "btn_en": "#00838F", "btn_extra": "#1565C0", "btn_fg": "#FFFFFF"
            }
        }
        
        self.all_labels, self.all_entries, self.all_frames, self.all_texts, self.all_hints = [], [], [], [], []
        self.current_theme = "🌌 Тёмный космос"
        
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if data.get("theme") in self.themes:
                        self.current_theme = data["theme"]
        except Exception:
            pass
        
        style = ttk.Style()
        style.theme_use('clam')
        self.style = style
        
        notebook = ttk.Notebook(root)
        self.notebook = notebook
        notebook.pack(expand=True, fill="both", padx=10, pady=10)
        
        self.tab_math = ttk.Frame(notebook)
        self.tab_rus = ttk.Frame(notebook)
        self.tab_en = ttk.Frame(notebook)
        
        notebook.add(self.tab_math, text="  📐 Математика  ")
        notebook.add(self.tab_rus, text="  ✍️ Русский язык  ")
        notebook.add(self.tab_en, text="  🌐 Английский  ")
        
        self.setup_math_ui()
        self.setup_rus_ui()
        self.setup_en_ui()
        self.update_fonts_and_sizes()
        self.apply_theme_colors()
        
        # ЗАПУСКАЕМ ИГРОВОЙ ПЛАВНЫЙ ПЕРЕХОД
        self.show_smooth_splash()

    def show_smooth_splash(self):
        """Создает игровое окно заставки LUKWA STUDIOS, которая плавно исчезает"""
        self.splash_win = tk.Toplevel()
        self.splash_win.overrideredirect(True) # Убираем рамки Windows
        self.splash_win.attributes("-topmost", True)
        
        sw, sh = 500, 500
        sx = (self.splash_win.winfo_screenwidth() - sw) // 2
    def show_smooth_splash(self):
        """Создает игровое окно заставки LUKWA STUDIOS, которая плавно исчезает"""
        self.splash_win = tk.Toplevel()
        self.splash_win.overrideredirect(True) # Убираем рамки Windows
        self.splash_win.attributes("-topmost", True)
        
        sw, sh = 500, 500
        sx = (self.splash_win.winfo_screenwidth() - sw) // 2
        sy = (self.splash_win.winfo_screenheight() - sh) // 2
        self.splash_win.geometry(f"{sw}x{sh}+{sx}+{sy}")
        
        # УМНЫЙ ПОИСК ТВОЕГО ЛОГОТИПА В НОВОМ СТАБИЛЬНОМ ФОРМАТЕ .PNG
        import sys
        if hasattr(sys, '_MEIPASS'):
            splash_img_path = os.path.join(sys._MEIPASS, "image (1).png")
        else:
            splash_img_path = "C:\\Users\\Luka\\Desktop\\image (1).png"
            
        if os.path.exists(splash_img_path):
            self.img = tk.PhotoImage(file=splash_img_path)
            lbl = tk.Label(self.splash_win, image=self.img, bg="#1E222B")
            lbl.pack()
        else:
            lbl = tk.Label(self.splash_win, text="LUKWA STUDIOS\nX\nGEMINI", font=("Consolas", 24, "bold"), fg="#61AFEF", bg="#1E222B")
            lbl.pack(expand=True, fill="both")
            
        self.splash_alpha = 1.0
        self.splash_win.attributes("-alpha", self.splash_alpha)
        
        # Ждем 1.5 секунды (как в играх) и запускаем плавное растворение
        self.splash_win.after(1500, self.fade_out_splash)

        """Эффект растворения заставки (Fade Out)"""
        if self.splash_alpha > 0.05:
            self.splash_alpha -= 0.05
            self.splash_win.attributes("-alpha", self.splash_alpha)
            self.splash_win.after(20, self.fade_out_splash) # Скорость затухания
        else:
            self.splash_win.destroy() # Полностью уничтожаем окно логотипа
            
            # Начинаем плавно проявлять основное тёмное окно программы
            self.root.deiconify()
            self.root.update()
            self.root.attributes("-alpha", 0.0)
            self.main_alpha = 0.0
            self.fade_in_main()

    def fade_in_main(self):
        """Эффект плавного появления главного окна (Fade In)"""
        if self.main_alpha < 1.0:
            self.main_alpha += 0.05
            self.root.attributes("-alpha", self.main_alpha)
            self.root.after(20, self.fade_in_main)

    def add_top_control_panel(self, parent_tab):
        frame = tk.Frame(parent_tab)
        frame.pack(anchor="ne", padx=15, pady=(5, 0))
        self.all_frames.append(frame)
        
        btn_minus = tk.Button(frame, text=" ➖ Меньше ", font=("Arial", 8, "bold"), bg="#E040FB", fg="white", relief="flat", command=self.decrease_scale)
        btn_minus.pack(side="left", padx=2)
        
        btn_plus = tk.Button(frame, text=" ➕ Больше ", font=("Arial", 8, "bold"), bg="#00E676", fg="black", relief="flat", command=self.increase_scale)
        btn_plus.pack(side="left", padx=2)
        
        lbl = tk.Label(frame, text="  🎨 Тема:", font=("Segoe UI", 9, "bold"))
        lbl.pack(side="left", padx=2)
        self.all_labels.append(lbl)
        
        cb = ttk.Combobox(frame, values=list(self.themes.keys()), state="readonly", width=16, font=("Segoe UI", 9))
        cb.set(self.current_theme)
        cb.pack(side="left", padx=2)
        cb.bind("<<ComboboxSelected>>", lambda e: self.on_theme_changed(e))

    def increase_scale(self):
        if self.font_size < 20:
            self.font_size += 1
            self.window_width += 30
            self.window_height += 20
            self.root.geometry(f"{self.window_width}x{self.window_height}")
            self.update_fonts_and_sizes()
            self.apply_theme_colors()

    def decrease_scale(self):
        if self.font_size > 8:
            self.font_size -= 1
            self.window_width -= 30
            self.window_height -= 20
            self.root.geometry(f"{self.window_width}x{self.window_height}")
            self.update_fonts_and_sizes()
            self.apply_theme_colors()

    def update_fonts_and_sizes(self):
        self.font_ui = ("Segoe UI", self.font_size, "bold")
        self.font_lbl = ("Segoe UI Semibold", self.font_size)
        self.font_hint = ("Segoe UI", self.font_size - 1, "italic")
        self.font_code = ("Consolas", self.font_size + 1)
        self.style.configure("TNotebook.Tab", font=("Segoe UI Emoji", self.font_size, "bold"), padding=(self.font_size + 2, self.font_size // 2))

    def on_theme_changed(self, event):
        self.current_theme = event.widget.get()
        self.apply_theme_colors()
        try:
            if not os.path.exists(CONFIG_DIR):
                os.makedirs(CONFIG_DIR)
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump({"theme": self.current_theme}, f, ensure_ascii=False, indent=4)
        except Exception:
            pass

    def apply_theme_colors(self):
        colors = self.themes[self.current_theme]
        self.root.configure(bg=colors["main"])
        self.style.configure("TNotebook", background=colors["main"])
        self.style.configure("TNotebook.Tab", background=colors["card"], foreground=colors["text_hint"])
        self.style.map("TNotebook.Tab", background=[("selected", colors["tab_sel"])], foreground=[("selected", colors["text_ent"])])
        self.style.configure("TFrame", background=colors["main"])
        for f in self.all_frames: f.configure(bg=colors["main"])
        for lbl in self.all_labels: lbl.configure(bg=colors["main"], fg=colors["text_lbl"], font=self.font_lbl)
        for hint in self.all_hints: hint.configure(bg=colors["main"], fg=colors["text_hint"], font=self.font_hint)
        for ent in self.all_entries: ent.configure(bg=colors["card"], fg=colors["text_ent"], insertbackground=colors["text_ent"], font=self.font_lbl)
        for txt in self.all_texts: txt.configure(bg=colors["card"], fg=colors["text_out"], font=self.font_code)
        btn_fg = colors["btn_fg"]
        self.btn_calc.configure(bg=colors["btn_math"], fg=btn_fg, font=self.font_ui)
        self.btn_comp.configure(bg=colors["btn_extra"], fg=btn_fg, font=self.font_ui)
        self.btn_div.configure(bg=colors["btn_en"], fg=btn_fg, font=self.font_ui)
        self.btn_task.configure(bg=colors["btn_rus"], fg=btn_fg, font=self.font_ui)
        self.btn_rus.configure(bg=colors["btn_rus"], fg=btn_fg, font=self.font_ui)
        self.btn_en_spell.configure(bg=colors["btn_en"], fg=btn_fg, font=self.font_ui)
        self.btn_en_ru.configure(bg=colors["btn_math"], fg=btn_fg, font=self.font_ui)
        self.btn_ru_en.configure(bg=colors["btn_extra"], fg=btn_fg, font=self.font_ui)
        if hasattr(self, "btn_export_math"): self.btn_export_math.configure(bg=colors["btn_extra"], fg=btn_fg, font=self.font_ui)
        if hasattr(self, "btn_export_rus"): self.btn_export_rus.configure(bg=colors["btn_extra"], fg=btn_fg, font=self.font_ui)
        if hasattr(self, "btn_export_en"): self.btn_export_en.configure(bg=colors["btn_extra"], fg=btn_fg, font=self.font_ui)

# =====================================================================
#       ЧАСТЬ 6 ИЗ 8: ИНТЕРФЕЙС ВКЛАДКИ МАТЕМАТИКА
# =====================================================================

    def setup_math_ui(self):
        self.add_top_control_panel(self.tab_math)
        
        # 1. Простой калькулятор выражений
        lbl_calc = tk.Label(self.tab_math, text="🧮 Калькулятор выражений:")
        lbl_calc.pack(anchor="w", padx=15, pady=(2, 2))
        self.all_labels.append(lbl_calc)
        
        frame_calc = tk.Frame(self.tab_math)
        frame_calc.pack(fill="x", padx=15)
        self.all_frames.append(frame_calc)
        
        self.ent_calc = tk.Entry(frame_calc, borderwidth=1, relief="flat")
        self.ent_calc.pack(side="left", expand=True, fill="x", padx=(0, 10), ipady=3)
        self.all_entries.append(self.ent_calc)
        
        self.btn_calc = tk.Button(frame_calc, text="⚡ Посчитать", relief="flat", command=self.calc_expression)
        self.btn_calc.pack(side="right", ipadx=10, ipady=2)

        # 2. Сравнение чисел и примеров
        lbl_comp = tk.Label(self.tab_math, text="⚖️ Сравнение чисел (через 'и', например: 5*5 и 20):")
        lbl_comp.pack(anchor="w", padx=15, pady=(8, 2))
        self.all_labels.append(lbl_comp)
        
        frame_comp = tk.Frame(self.tab_math)
        frame_comp.pack(fill="x", padx=15)
        self.all_frames.append(frame_comp)
        
        self.ent_comp = tk.Entry(frame_comp, borderwidth=1, relief="flat")
        self.ent_comp.pack(side="left", expand=True, fill="x", padx=(0, 10), ipady=3)
        self.all_entries.append(self.ent_comp)
        
        self.btn_comp = tk.Button(frame_comp, text="🔍 Сравнить", relief="flat", command=self.calc_comparison)
        self.btn_comp.pack(side="right", ipadx=13, ipady=2)

        # 3. Деление в столбик
        lbl_div = tk.Label(self.tab_math, text="✏️ Деление в столбик:")
        lbl_div.pack(anchor="w", padx=15, pady=(8, 2))
        self.all_labels.append(lbl_div)
        
        frame_div = tk.Frame(self.tab_math)
        frame_div.pack(fill="x", padx=15)
        self.all_frames.append(frame_div)
        
        lbl_d1 = tk.Label(frame_div, text="Что делим:")
        lbl_d1.pack(side="left")
        self.all_hints.append(lbl_d1)
        
        self.ent_div1 = tk.Entry(frame_div, width=8, borderwidth=1, relief="flat")
        self.ent_div1.pack(side="left", padx=5, ipady=3)
        self.all_entries.append(self.ent_div1)
        
        lbl_d2 = tk.Label(frame_div, text="На что:")
        lbl_d2.pack(side="left", padx=(10, 0))
        self.all_hints.append(lbl_d2)
        
        self.ent_div2 = tk.Entry(frame_div, width=8, borderwidth=1, relief="flat")
        self.ent_div2.pack(side="left", padx=5, ipady=3)
        self.all_entries.append(self.ent_div2)
        
        self.btn_div = tk.Button(frame_div, text="🔢 Разделить", relief="flat", command=self.calc_division)
        self.btn_div.pack(side="right", ipadx=12, ipady=2)

        # 4. Решение текстовых задач из учебника
        lbl_task = tk.Label(self.tab_math, text="📖 Решение задач из учебника (работает и с героями Spotlight):")
        lbl_task.pack(anchor="w", padx=15, pady=(8, 2))
        self.all_labels.append(lbl_task)
        
        frame_task = tk.Frame(self.tab_math)
        frame_task.pack(fill="x", padx=15)
        self.all_frames.append(frame_task)
        
        self.ent_task = tk.Entry(frame_task, borderwidth=1, relief="flat")
        self.ent_task.pack(side="left", expand=True, fill="x", padx=(0, 10), ipady=3)
        self.all_entries.append(self.ent_task)
        
        self.btn_task = tk.Button(frame_task, text="🚀 Решить задачу", relief="flat", command=self.calc_text_task)
        self.btn_task.pack(side="right", ipadx=3, ipady=2)
        
        # Общая верхняя доска результатов математики с кнопкой сохранения
        frame_res_top = tk.Frame(self.tab_math)
        frame_res_top.pack(fill="x", padx=15, pady=(10, 2))
        self.all_frames.append(frame_res_top)
        
        lbl_res = tk.Label(frame_res_top, text="📋 Результаты вычислений и Краткая запись (Дано):")
        lbl_res.pack(side="left")
        self.all_hints.append(lbl_res)
        
        self.btn_export_math = tk.Button(frame_res_top, text="💾 Сохранить решение", relief="flat", command=lambda: self.export_to_txt(self.txt_math_res, "Решение_Математика.txt"))
        self.btn_export_math.pack(side="right", ipadx=5)

        self.txt_math_res = tk.Text(self.tab_math, height=11, borderwidth=0, highlightthickness=0)
        self.txt_math_res.pack(fill="both", padx=15, pady=(0, 10))
        self.txt_math_res.config(state="disabled")
        self.all_texts.append(self.txt_math_res)
# =====================================================================
#       ЧАСТЬ 7 ИЗ 8: ИНТЕРФЕЙС ВКЛАДОК РУССКОГО И АНГЛИЙСКОГО ЯЗЫКОВ
# =====================================================================

    def setup_rus_ui(self):
        self.add_top_control_panel(self.tab_rus)
        lbl = tk.Label(self.tab_rus, text="🔍 Проверка русской орфографии:")
        lbl.pack(anchor="w", padx=15, pady=(2, 2))
        self.all_labels.append(lbl)
        
        self.ent_rus = tk.Entry(self.tab_rus, borderwidth=1, relief="flat")
        self.ent_rus.pack(fill="x", padx=15, pady=5, ipady=4)
        self.all_entries.append(self.ent_rus)
        
        self.btn_rus = tk.Button(self.tab_rus, text="✅ Проверить ошибки", relief="flat", command=self.check_rus_errors)
        self.btn_rus.pack(anchor="e", padx=15, pady=5, ipadx=10, ipady=3)
        
        frame_res_top = tk.Frame(self.tab_rus)
        frame_res_top.pack(fill="x", padx=15, pady=(8, 2))
        self.all_frames.append(frame_res_top)
        
        lbl_res = tk.Label(frame_res_top, text="📝 Отчёт об исправлениях:")
        lbl_res.pack(side="left")
        self.all_hints.append(lbl_res)
        
        self.btn_export_rus = tk.Button(frame_res_top, text="💾 Сохранить отчёт", relief="flat", command=lambda: self.export_to_txt(self.txt_rus_res, "Отчёт_Русский.txt"))
        self.btn_export_rus.pack(side="right", ipadx=5)
        
        self.txt_rus_res = tk.Text(self.tab_rus, height=15, borderwidth=0, highlightthickness=0)
        self.txt_rus_res.pack(fill="both", padx=15, pady=(0, 15))
        self.txt_rus_res.config(state="disabled")
        self.all_texts.append(self.txt_rus_res)

    def setup_en_ui(self):
        self.add_top_control_panel(self.tab_en)
        lbl = tk.Label(self.tab_en, text="🌐 Модуль Английского Языка (Встроены герои Spotlight!):")
        lbl.pack(anchor="w", padx=15, pady=(2, 2))
        self.all_labels.append(lbl)
        
        self.ent_en = tk.Entry(self.tab_en, borderwidth=1, relief="flat")
        self.ent_en.pack(fill="x", padx=15, pady=5, ipady=4)
        self.all_entries.append(self.ent_en)
        
        frame_btns = tk.Frame(self.tab_en)
        frame_btns.pack(fill="x", padx=15, pady=5)
        self.all_frames.append(frame_btns)
        
        self.btn_en_spell = tk.Button(frame_btns, text="🔎 Ошибки + Перевод", relief="flat", command=self.check_en_errors_and_translate)
        self.btn_en_spell.pack(side="left", expand=True, fill="x", padx=(0, 5), ipady=3)
        
        self.btn_en_ru = tk.Button(frame_btns, text="🔤 Умный EN ➔ RU", relief="flat", command=lambda: self.translate(1))
        self.btn_en_ru.pack(side="left", expand=True, fill="x", padx=2, ipady=3)
        
        self.btn_ru_en = tk.Button(frame_btns, text="🇷🇺 Чистый RU ➔ EN", relief="flat", command=lambda: self.translate(2))
        self.btn_ru_en.pack(side="left", expand=True, fill="x", padx=(5, 0), ipady=3)
        
        frame_res_top = tk.Frame(self.tab_en)
        frame_res_top.pack(fill="x", padx=15, pady=(8, 2))
        self.all_frames.append(frame_res_top)
        
        lbl_res = tk.Label(frame_res_top, text="📚 Результат работы переводчика:")
        lbl_res.pack(side="left")
        self.all_hints.append(lbl_res)
        
        self.btn_export_en = tk.Button(frame_res_top, text="💾 Сохранить перевод", relief="flat", command=lambda: self.export_to_txt(self.txt_en_res, "Перевод_Английский.txt"))
        self.btn_export_en.pack(side="right", ipadx=5)
        
        self.txt_en_res = tk.Text(self.tab_en, height=15, borderwidth=0, highlightthickness=0)
        self.txt_en_res.pack(fill="both", padx=15, pady=(0, 15))
        self.txt_en_res.config(state="disabled")
        self.all_texts.append(self.txt_en_res)
# =====================================================================
#       ЧАСТЬ 8 ИЗ 8: ОБРАБОТЧИКИ КНОПОК, ЭКСПОРТ И ЗАПУСК СИСТЕМЫ
# =====================================================================

    def export_to_txt(self, text_widget, filename):
        """Функция экспорта: сохраняет чистый текст на Рабочий стол пользователя"""
        content = text_widget.get("1.0", tk.END).strip()
        if not content or "⏳" in content or "Проверяю" in content:
            messagebox.showwarning("Внимание", "Окно результатов пустое! Нечего сохранять.")
            return
        try:
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            if not os.path.exists(desktop_path):
                desktop_path = os.path.join(os.path.expanduser("~"), "Рабочий стол")
            full_path = os.path.join(desktop_path, filename)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("Успешно", f"Файл сохранён на Рабочий стол!\nНазвание: {filename}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{str(e)}")

    def set_clean_text(self, text_widget, text):
        """Вывод текста с возможностью выделения и копирования (Ctrl+C)"""
        text_widget.config(state="normal")
        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, text)
        text_widget.bind("<Key>", lambda e: "break") 
        text_widget.config(state="normal", cursor="xterm")

    def calc_expression(self):
        expr = self.ent_calc.get()
        try:
            res = eval(expr)
            self.set_clean_text(self.txt_math_res, f"Пример: {expr}\nОтвет: {res}")
        except:
            self.set_clean_text(self.txt_math_res, "❌ Ошибка в знаках примера!")

    def calc_comparison(self):
        expr_text = self.ent_comp.get()
        res = compare_expressions(expr_text)
        self.set_clean_text(self.txt_math_res, res)

    def calc_text_task(self):
        task_text = self.ent_task.get()
        res = solve_text_task(task_text)
        self.set_clean_text(self.txt_math_res, res)

    def calc_division(self):
        try:
            d1 = int(self.ent_div1.get())
            d2 = int(self.ent_div2.get())
            res_table = get_division_column(d1, d2)
            self.set_clean_text(self.txt_math_res, res_table)
        except ValueError:
            self.set_clean_text(self.txt_math_res, "❌ Вводи только целые числа!")

    def check_rus_errors(self):
        text = self.ent_rus.get()
        if not text.strip():
            messagebox.showwarning("Внимание", "Поле ввода пустое!")
            return
        self.txt_rus_res.config(state="normal")
        self.txt_rus_res.delete("1.0", tk.END)
        self.txt_rus_res.insert(tk.END, "⏳ Проверяю текст...")
        
        def process():
            words = text.split()
            out_lines = ["📝 Локальный отчёт об ошибках (Автономно):\n"]
            found_errors = False
            for w in words:
                clean_w = w.strip(",.?!()\"").lower()
                if not clean_w or len(clean_w) <= 2 or clean_w.isdigit(): continue
                base_w = clean_w
                if clean_w.endswith("у") or clean_w.endswith("е") or clean_w.endswith("а"):
                    base_w = clean_w[:-1]
                closest = find_closest_word(base_w, RUSSIAN_WORDS, max_dist=2)
                if closest and not closest.startswith(base_w[:3]):
                    closest = find_closest_word(clean_w, RUSSIAN_WORDS, max_dist=2)
                if closest and closest != clean_w and closest != base_w and not clean_w.startswith(closest[:3]):
                    out_lines.append(f"• Ошибка в слове: '{w}'\n  👉 Правильно: \"{closest}\"\n")
                    found_errors = True
            if not found_errors:
                out_lines.append("✨ Ошибок не найдено! Всё написано верно.")
            self.set_clean_text(self.txt_rus_res, "\n".join(out_lines))
        threading.Thread(target=process, daemon=True).start()

    def check_en_errors_and_translate(self):
        text = self.ent_en.get()
        if not text.strip():
            messagebox.showwarning("Внимание", "Поле ввода пустое!")
            return
        self.txt_en_res.config(state="normal")
        self.txt_en_res.delete("1.0", tk.END)
        self.txt_en_res.insert(tk.END, "⏳ Проверяю текст...")
        
        def process():
            words = text.split()
            out_lines = ["📝 Локальный ИИ-разбор английского (Автономно):\n"]
            found_any = False
            for w in words:
                clean_w = w.strip(",.?!()\"").lower()
                if not clean_w or clean_w.isdigit(): continue
                closest = find_closest_word(clean_w, list(ENGLISH_WORDS.keys()), max_dist=2)
                if closest:
                    trans = ENGLISH_WORDS[closest]
                    if closest != clean_w:
                        out_lines.append(f"Ошибка в слове '{w}'\nПравильно: \"{closest}\"\nЕго перевод: \"{trans}\"\n")
                    else:
                        out_lines.append(f"Слово: '{w}' написано верно.\nЕго перевод: \"{trans}\"\n")
                    found_any = True
            if not found_any:
                out_lines.append("❌ Слово не найдено в локальной базе школьной программы.")
            self.set_clean_text(self.txt_en_res, "\n".join(out_lines))
        threading.Thread(target=process, daemon=True).start()

    def translate(self, direction):
        text = self.ent_en.get()
        if not text.strip():
            messagebox.showwarning("Внимание", "Поле ввода пустое!")
            return
        self.txt_en_res.config(state="normal")
        self.txt_en_res.delete("1.0", tk.END)
        self.txt_en_res.insert(tk.END, "⏳ Перевожу...")
        
        def process():
            clean_text = text.strip().lower()
            out_text = "📚 [Локальный переводчик фраз]\n\n"
            if direction == 1:
                if clean_text in ENGLISH_WORDS:
                    out_text += f"Полный перевод слова:\n{ENGLISH_WORDS[clean_text]}"
                else:
                    closest = find_closest_word(clean_text, list(ENGLISH_WORDS.keys()), max_dist=2)
                    if closest:
                        out_text += f"⚠️ Была опечатка! Исправлено на '{closest}'.\n\nПеревод: {ENGLISH_WORDS[closest]}"
                    else:
                        out_text += f"Перевод фразы:\n[Слово '{text}' не найдено в базе английского]"
            else:
                closest_rus = find_closest_word(clean_text, RUSSIAN_WORDS, max_dist=2)
                target_rus = closest_rus if closest_rus else clean_text
                found = False
                for eng, rus in ENGLISH_WORDS.items():
                    if target_rus == rus.lower() or (hasattr(rus, 'lower') and target_rus in rus.lower()):
                        if closest_rus and closest_rus != clean_text:
                            out_text += f"⚠️ Найдена ошибка в русском слове! Исправлено на: \"{closest_rus}\"\n\n"
                        out_text += f"Полный перевод на английский:\n{eng}"
                        found = True
                        break
                if not found:
                    if closest_rus and closest_rus != clean_text:
                        out_text += f"⚠️ Возможно, вы имели в виду \"{closest_rus}\", но для него нет перевода в базе."
                    else:
                        out_text += f"Перевод на английский:\n[Слово '{text}' не найдено в локальной базе русского]"
            self.set_clean_text(self.txt_en_res, out_text)
        threading.Thread(target=process, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = GDZApp(root)
    root.mainloop()
