from kivy.uix.label import Label
from kivy.clock import Clock
 
class Sits(Label):
   def __init__(self, total, **kwargs):
       self.current = 0
       self.total = total
       my_text = "Осталось приседаний: " + str(self.total)
       super().__init__(text=my_text, **kwargs)
 
   def next(self, *args):
       self.current += 1
       remain = max(0, self.total - self.current)
       my_text = "Осталось приседаний: " + str(remain)
       self.text=my_text