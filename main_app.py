from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from instructions import *
from ruffier import *
from kivy.animation import Animation
from seconds import Seconds
from kivy.properties import BooleanProperty
from runner import Runner
from sits import Sits

age = 7
name = ""
p1, p2, p3 = 0, 0, 0
bg = (1, .48, .1, 1)
btn_color = (0, 0, 0, 1)
Window.clearcolor = bg

def check_int(str_num):
    try:
        return int(str_num)
    except ValueError:
        return False

class InstrScr(Screen):
  def __init__(self, **kwargs):
      super().__init__(**kwargs)

      instr = Label(text=txt_instruction)

      self.lbl1 = Label(text='Введите [b]имя[/b]:', halign='right', markup=True)
      self.in_name = TextInput(multiline=False)
      self.lbl2 = Label(text='Введите [b]возраст[/b]:', halign='right', markup=True)
      self.in_age = TextInput(text=str(age), multiline=False)

      self.btn = Button(text='Начать', size_hint=(0.3, 0.2), pos_hint={'center_x': 0.5})
      self.btn.background_color = btn_color
      self.btn.on_press = self.next

      line1 = BoxLayout(size_hint=(0.8, None), height='30sp')
      line2 = BoxLayout(size_hint=(0.8, None), height='30sp')
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
        global name
        name = self.in_name.text

        age = check_int(self.in_age.text)
        if age == False or age <= 7:
            self.lbl2.text = "Некорректный ввод!\nВведите [b]возраст[/b]:"
        else:
            self.manager.current = 'pulse1'

class PulseScr(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        instr = Label(text=txt_test1)
        self.next_screen = False

        line = BoxLayout(size_hint=(0.8, None), height='30sp')
        self.lbl_result = Label(text='Введите [b]результат[/b]:', halign='right', markup=True)
        self.in_result = TextInput(text='0', multiline=False)
        line.add_widget(self.lbl_result)
        line.add_widget(self.in_result)

        self.lbl_sec = Seconds(15)
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
            if p1 <= 0 or p1 == False:
                self.lbl_result.text = "Некорректный ввод!\nВведите [b]результат[/b]:"
            else:
                self.manager.current = 'sits'

class CheckSits(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.next_screen = False

        instr = Label(text=txt_sits, size_hint=(0.5, 1))
        self.lbl_sits = Sits(30)
        self.run = Runner(total=30, steptime=1.5, size_hint=(0.4, 1))
        self.run.bind(finished=self.run_finished)

        line = BoxLayout()
        vlay = BoxLayout(orientation='vertical', size_hint=(0.3, 1))
        vlay.add_widget(self.lbl_sits)
        line.add_widget(instr)
        line.add_widget(vlay)
        line.add_widget(self.run)

        self.btn = Button(text='Начать', size_hint=(0.3, 0.2), pos_hint={'center_x': 0.5})
        self.btn.background_color = btn_color
        self.btn.on_press = self.next

        outer = BoxLayout(orientation='vertical', padding=8, spacing=8)
        outer.add_widget(line)
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

        instr = Label(text=txt_test3)
        self.next_screen = False
        self.stage = 1

        line1 = BoxLayout(size_hint=(0.8, None), height='30sp')
        self.lbl_result1 = Label(text='[b]Результат[/b]:', halign='right', markup=True)
        self.in_result1 = TextInput(text='0', multiline=False)
        line1.add_widget(self.lbl_result1)
        line1.add_widget(self.in_result1)

        line2 = BoxLayout(size_hint=(0.8, None), height='30sp')
        self.lbl_result2 = Label(text='[b]Результат[/b] после отдыха:', halign='right', markup=True)
        self.in_result2 = TextInput(text='0', multiline=False)
        line2.add_widget(self.lbl_result2)
        line2.add_widget(self.in_result2)
      
        self.lbl_sec = Seconds(15)
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
                self.lbl_sec.restart(30)
                self.stage = 2
            elif self.stage == 2:
                self.lbl_sec.restart(15)
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
            if p2 <= 0 or p2 == False:
                self.lbl_result1.text = "Некорректный ввод!\nВведите [b]результат[/b]:"
            elif p3 <= 0 or p3 == False:
                self.lbl_result2.text = "Некорректный ввод!\nВведите [b]результат[/b]:"
            else:
                self.manager.current = 'result'

class Result(Screen):
  def __init__(self, **kwargs):
      super().__init__(**kwargs)

      self.outer = BoxLayout(orientation='vertical', padding=8, spacing=8)
      self.instr = Label(text = '')
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
