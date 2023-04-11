from tkinter import Tk, Canvas

point = [(250,250),
         (650,200),
         (750,550),
         (200,500)]

class App(Tk):
   def __init__(self):
      Tk.__init__(self)
      self.geometry('1000x800')
      self.title('AntyAliasing - Visualization Tool')

class AntyAliasingTool:
   def __init__(self, container, coord=[], diameter=20):
      self.canvas = Canvas(app) ; self.canvas.pack(fill='both', expand=True)
      self.create_points(coord, diameter)
      self.create_lines()

   def create_points(self, coord, diameter):
      self.points_object = []
      for c in coord:
         point = Point(self.canvas, c[0], c[1], diameter)
         self.canvas.tag_bind(point.id_, '<B1-Motion>', point.move_point)
         self.canvas.tag_bind(point.id_, '<Button-1>', point.cursor_position)
         self.canvas.tag_bind(point.id_, '<B1-Motion>', self.update_lines, add='+')
         self.points_object.append(point)

   def create_lines(self):
      self.lines = Line(self.canvas, self.get_position())

   def get_position(self):
      self.position_object = []
      for point in self.points_object + self.points_object[:1]:
         self.position_object.append(point.get_position())
      return self.position_object

   def update_lines(self, e):
      self.lines.delete_lines()
      self.create_lines()

class Line:
   def __init__(self, canvas, point, aa=True):
      self.canvas = canvas
      self.antialiasing = aa
      self.create_lines(point)

   def create_lines(self, point, size=1, color='black'):
      if self.antialiasing:
         self.aaline = self.canvas.create_line(point, width=1.5, fill='gray')
      self.lines = self.canvas.create_line(point, width=size, fill=color)

   def delete_lines(self):
      self.canvas.delete(self.lines)
      if self.antialiasing:
         self.canvas.delete(self.aaline)

class Point:
   def __init__(self, canvas, x, y, d):
      self.canvas = canvas
      self.x = x ; self.y = y ; self.d = d
      self.id_ = canvas.create_oval(x,y, x+d,y+d, fill='red', outline='green')

   def cursor_position(self, ev):
      self.cx = ev.x-self.x
      self.cy = ev.y-self.y
      
   def move_point(self, ev):
      x = ev.x-self.cx
      y = ev.y-self.cy
      self.x = x ; self.y = y
      self.canvas.coords(self.id_, x,y, x+self.d, y+self.d)

   def get_position(self):
      center = self.d/2
      return self.x+center, self.y+center


app = App()
AntyAliasingTool(app, point)
app.mainloop()
