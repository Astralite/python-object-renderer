from object_3d import *
from camera import *
from projection import *
import pygame as pg

class SoftwareRenderer(object):
  def __init__(self):
    pg.init()
    self.RES = self.WIDTH, self.HEIGHT = 1600, 900
    self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
    self.FPS = 60
    self.screen = pg.display.set_mode(self.RES)
    self.clock = pg.time.Clock()
    self.create_objects()
    
  def create_objects(self):
    self.camera = Camera(self, [0, 180, -780])
    self.projection = Projection(self)

    self.object = self.get_obect_from_file('models/cat.obj')
    
    # self.axes = Axes(self)
    # self.axes.translate([0.7, 0.9, 0.7])
    
    # self.world_axes = Axes(self)
    # self.world_axes.movement_flag = False
    # self.world_axes.scale(2.5)
    # self.world_axes.translate([0, 0, 0])
    
  def get_obect_from_file(self, filename):
    vertices, faces = [], []
    with open(filename) as file:
      for line in file:
        if line.startswith('v '):
          vertices.append([float(i) for i in line.split()[1:]] + [1])
        elif line.startswith('f '):
          faces_ = line.split()[1:]
          faces.append([int(face_.split('/')[0]) - 1 for face_ in faces_])
    return Object3D(self, vertices, faces)
    
  def draw(self):
    self.screen.fill('#161816')
    # self.world_axes.draw()
    self.object.draw()
    # self.axes.draw()
    
  def run(self):
    while True:
      self.draw()
      self.camera.control()
      self.object.control()
      [exit() for e in pg.event.get() if e.type == pg.QUIT]
      pg.display.set_caption('FPS: {}'.format(self.clock.get_fps()))
      pg.display.flip()
      self.clock.tick(self.FPS)
        
if __name__ == '__main__':
  app = SoftwareRenderer()
  app.run()