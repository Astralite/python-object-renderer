import pygame as pg
from colorsys import *
from time import sleep
from matrix_functions import *

default_vertices = np.array([(0, 0, 0, 1), (0, 1, 0, 1), (1, 1, 0, 1), (1, 0, 0, 1),
                                (0, 0, 1, 1), (0, 1, 1, 1), (1, 1, 1, 1), (1, 0, 1, 1)])

default_faces = np.array([(0, 1, 2, 3), (4, 5, 6, 7), (0, 4, 5, 1), (2, 3, 7, 6), (1, 2, 6, 5), (0, 3, 7, 4)])

def int_to_rgb_tuple(i):
  return tuple([round(h * 255) for h in hsv_to_rgb(i/360,1,1)])

class Object3D:
  def __init__(self, render, vertices=default_vertices, faces=default_faces):
    self.render = render
    self.vertices = vertices
    self.faces = faces

    # Flags for customizing object behavior
    self.movement_flag = True
    self.draw_faces_flag = False
    self.draw_solid_faces_flag = False
    self.rainbow_faces_flag = False
    self.draw_vertices_flag = True
    self.pulsing_vertices_flag = False
    self.rainbow_vertices_flag = True
    
    if self.rainbow_faces_flag:
      # Rainbow colored faces
      self.n_faces = len(self.faces)
      self.colors = [int_to_rgb_tuple(round(i * 360 / self.n_faces)) for i in range(self.n_faces)]
      self.color_faces = [(color, face) for color, face in zip(self.colors, self.faces)]
    else:
      # Regular colored faces
      self.color_faces = [('#81EB81', face) for face in self.faces]
    
    self.font = pg.font.SysFont('Arial', 30, bold=True)
    self.label = ''

    self.movement_speed = 0.01
    
  def draw(self):
    self.screen_projection()
    self.movement()
    
  def movement(self):
    if self.movement_flag:
      self.rotate_y(pg.time.get_ticks() % self.movement_speed)
      
  # Todo: why does rotation speed pulsate when set to max?
  def control(self):
    increment = 0.0025
    key = pg.key.get_pressed()
    if key[pg.K_z]:
      self.movement_speed += 0 if self.movement_speed > 0.04 else increment
      self.movement_speed = round(self.movement_speed, 4) + 0.0000001 # quick hack to avoid division by zero
    if key[pg.K_x]:
      self.movement_speed -= 0 if self.movement_speed < -0.04 else increment
      self.movement_speed = round(self.movement_speed, 4) + 0.0000001 # quick hack to avoid division by zero

  def screen_projection(self):
    vertices = self.vertices @ self.render.camera.camera_matrix()
    vertices = vertices @ self.render.projection.projection_matrix
    vertices /= vertices[:, -1].reshape(-1, 1)
    vertices[(vertices > 2) | (vertices < -2)] = 0
    vertices = vertices @ self.render.projection.to_screen_matrix
    vertices = vertices[:, :2]
    
    if self.draw_faces_flag:
      for index, color_face in enumerate(self.color_faces):
        color, face = color_face
        polygon = vertices[face]
        if not np.any((polygon == self.render.H_WIDTH) | (polygon == self.render.H_HEIGHT)):
          pg.draw.polygon(self.render.screen, color, polygon, 1)
          if self.draw_solid_faces_flag:
            pg.draw.polygon(self.render.screen, pg.Color('black'), polygon, 0)
          if self.label:
            text = self.font.render(self.label[index], True, pg.Color('white'))
            self.render.screen.blit(text, polygon[-1])
    
    if self.draw_vertices_flag:
      size = 1
      if self.pulsing_vertices_flag:
        size = round(abs((pg.time.get_ticks() / 100 % 16) - 8))
      for vertex in vertices:
        if not np.any((vertex == self.render.H_WIDTH) | (vertex == self.render.H_HEIGHT)):
          color = pg.Color('white')
          if self.rainbow_vertices_flag:
            color = int_to_rgb_tuple(abs(int(vertex[0] * 360) / self.render.WIDTH))
          pg.draw.circle(self.render.screen, color, vertex, size)
  
  def translate(self, pos):
    self.vertices = self.vertices @ translate(pos)
    
  def scale(self, s):
    self.vertices = self.vertices @ scale(s)
  
  def rotate_x(self, angle):
    self.vertices = self.vertices @ rotate_x(angle)
  
  def rotate_y(self, angle):
    self.vertices = self.vertices @ rotate_y(angle)
    
  def rotate_z(self, angle):
    self.vertices = self.vertices @ rotate_z(angle)

class Axes(Object3D):
  def __init__(self, render):
    super().__init__(render)
    self.vertices = np.array([(0, 0, 0, 1), (1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)])
    self.faces = np.array([(0, 1), (0, 2), (0, 3)])
    self.colors = [pg.Color('red'), pg.Color('green'), pg.Color('blue')]
    self.color_faces = [(color, face) for color, face in zip(self.colors, self.faces)]
    self.draw_vertices = False
    self.label = 'XYZ'