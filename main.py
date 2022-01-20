from kivy.app import App
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from instructions import *
from ruffier import *
from seconds import Seconds
from runner import Runner
from sits import Sits

age = 7
name = ""
p1, p2, p3 = 0, 0, 0
bg = (1, .48, .1, 1)
btn_color = (0, 0, 0, 1)
Window.clearcolor = bg
text_size = Window.width - dp(20), None


def check_int(str_num):
    try:
        return int(str_num)
    except ValueError:
        return False


class InstrScr(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        instr = Label(text=txt_instruction, text_size=text_size)

        self.lbl1 = Label(text='Введите [b]имя[/b]:', halign='center', markup=True)
        self.in_name = TextInput(multiline=False)
        self.lbl2 = Label(text='Введите [b]возраст[/b]:', halign='center', markup=True)
        self.in_age = TextInput(text=str(age), multiline=False)

        self.btn = Button(text='Начать', size_hint=(1, 0.1), pos_hint={'center_x': 0.5})
        self.btn.background_color = btn_color
        self.btn.on_press = self.next

        line1 = BoxLayout(size_hint=(0.9, None), height='30sp')
        line2 = BoxLayout(size_hint=(0.9, None), height='30sp')
        line1.add_widget(self.lbl1)
        line1.add_widget(self.in_name)
        line2.add_widget(self.lbl2)
        line2.add_widget(self.in_age)

        outer = BoxLayout(orientation='vertical', padding=8, spacing=8)
        outer.add_widget(instr)
        outer.add_widget(line1)
        outer.add_widget(line2)
        outer.add_widget(self.btn)
        self.add_widget(outer)

    def next(self):
        global name, age
        name = self.in_name.text

        age = check_int(self.in_age.text)
        if not name:
            self.lbl1.text = "Неверный ввод!\nВведите [b]имя[/b]:"
        elif not age or age <= 7:
            self.lbl1.text = "Введите [b]имя[/b]:"
            self.lbl2.text = "Неверный ввод!\nВведите [b]возраст[/b]:"
        else:
            self.manager.current = 'pulse1'


class PulseScr(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        instr = Label(text=txt_test1, text_size=text_size)
        self.next_screen = False

        line = BoxLayout(size_hint=(0.8, None), height='30sp')
        self.lbl_result = Label(text='[b]Результат[/b]:', halign='center', markup=True)
        self.in_result = TextInput(text='0', multiline=False, halign='right')
        line.add_widget(self.lbl_result)
        line.add_widget(self.in_result)

        self.lbl_sec = Seconds(1)
        self.lbl_sec.bind(done=self.sec_finished)

        self.btn = Button(text='Начать', size_hint=(0.3, 0.2), pos_hint={'center_x': 0.5})
        self.btn.background_color = btn_color
        self.btn.on_press = self.next

        outer = BoxLayout(orientation='vertical', padding=8, spacing=8)
        outer.add_widget(instr)
        outer.add_widget(self.lbl_sec)
        outer.add_widget(line)
        outer.add_widget(self.btn)
        self.add_widget(outer)

    def sec_finished(self, *args):
        self.in_result.set_disabled(False)
        self.btn.set_disabled(False)
        self.btn.text = 'Продолжить'
        self.next_screen = True

    def next(self):
        if not self.next_screen:
            self.btn.set_disabled(True)
            self.lbl_sec.start()
        else:
            global p1
            p1 = check_int(self.in_result.text)
            if p1 <= 0 or not p1:
                self.lbl_result.text = "Неверный ввод!\n[b]Результат[/b]:"
            else:
                self.manager.current = 'sits'


class CheckSits(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.next_screen = False

        instr = Label(text=txt_test2, text_size=(Window.width - dp(200), Window.height - dp(15)), pos_hint={'center_y': .85})
        self.lbl_sits = Sits(3)
        self.run = Runner(total=3, steptime=1.5, size_hint=(.4, 1))
        self.run.bind(finished=self.run_finished)

        line = BoxLayout()
        line.add_widget(instr)
        line.add_widget(self.run)

        self.btn = Button(text='Начать', size_hint=(.3, .2), pos_hint={'center_x': .5})
        self.btn.background_color = btn_color
        self.btn.on_press = self.next

        outer = BoxLayout(orientation='vertical', padding=8, spacing=8)
        outer.add_widget(line)
        outer.add_widget(self.lbl_sits)
        outer.add_widget(self.btn)

        self.add_widget(outer)

    def run_finished(self, instance, value):
        self.btn.set_disabled(False)
        self.btn.text = 'Продолжить'
        self.next_screen = True

    def next(self):
        if not self.next_screen:
            self.btn.set_disabled(True)
            self.run.start()
            self.run.bind(value=self.lbl_sits.next)
        else:
            self.manager.current = 'pulse2'


class PulseScr2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        instr = Label(text=txt_test3, text_size=text_size)
        self.next_screen = False
        self.stage = 1

        line1 = BoxLayout(size_hint=(0.8, None), height='30sp')
        self.lbl_result1 = Label(text='[b]Результат[/b]:', halign='center', markup=True)
        self.in_result1 = TextInput(text='0', multiline=False)
        line1.add_widget(self.lbl_result1)
        line1.add_widget(self.in_result1)

        line2 = BoxLayout(size_hint=(0.8, None), height='30sp')
        self.lbl_result2 = Label(text='[b]Результат[/b]\nпосле отдыха:', halign='center', markup=True)
        self.in_result2 = TextInput(text='0', multiline=False)
        line2.add_widget(self.lbl_result2)
        line2.add_widget(self.in_result2)

        self.lbl_sec = Seconds(3)
        self.lbl_sec.bind(done=self.sec_finished)

        self.btn = Button(text='Начать', size_hint=(0.3, 0.2), pos_hint={'center_x': 0.5})
        self.btn.background_color = btn_color
        self.btn.on_press = self.next

        outer = BoxLayout(orientation='vertical', padding=8, spacing=8)
        outer.add_widget(instr)
        outer.add_widget(self.lbl_sec)
        outer.add_widget(line1)
        outer.add_widget(line2)
        outer.add_widget(self.btn)
        self.add_widget(outer)

    def sec_finished(self, *args):
        if self.lbl_sec.done:
            if self.stage == 1:
                self.lbl_sec.restart(6)
                self.stage = 2
            elif self.stage == 2:
                self.lbl_sec.restart(3)
                self.stage = 3
            elif self.stage == 3:
                self.btn.text = "Завершить"
                self.btn.set_disabled(False)
                self.next_screen = True
                self.stage = 0

    def next(self):
        if not self.next_screen:
            self.btn.set_disabled(True)
            self.lbl_sec.start()
        else:
            global p2, p3
            p2 = check_int(self.in_result1.text)
            p3 = check_int(self.in_result2.text)
            if p2 <= 0 or not p2:
                self.lbl_result1.text = "Неверный ввод!\n[b]Результат[/b]:"
            elif p3 <= 0 or not p3:
                self.lbl_result1.text = "Введите [b]результат[/b]:"
                self.lbl_result2.text = "Неверный ввод!\n[b]Результат[/b]\nпосле отдыха:"
            else:
                self.manager.current = 'result'


class Result(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.outer = BoxLayout(orientation='vertical', padding=8, spacing=8)
        self.instr = Label(text='')
        self.outer.add_widget(self.instr)
        self.add_widget(self.outer)
        self.on_enter = self.before

    def before(self):
        global name
        self.instr.text = name + '\n' + test(p1, p2, p3, age)


class HeartCheck(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(InstrScr(name='instr'))
        sm.add_widget(PulseScr(name='pulse1'))
        sm.add_widget(PulseScr2(name='pulse2'))
        sm.add_widget(CheckSits(name='sits'))
        sm.add_widget(Result(name='result'))
        return sm


app = HeartCheck()
app.run()
