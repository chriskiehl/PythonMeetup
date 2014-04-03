'''
Created on Mar 29, 2014

@author: Chris
'''

from pathlib import Path 
import os
import time

class Direction:
  left  = (-1, 0)
  right = (1,  0)
  down  = (0,  1)
  up    = (0, -1)
  
class Cave: 
  def __init__(self, layout):
    self.layout = layout
    
    if not self.layout[1][0] == 0:
      raise Exception("Inlet not in expected location. "
                      "Layout likely parsed incorrectly")
    
  def is_empty(self, pos):
    return self.layout[pos[1]][pos[0]] == 0
    
  def mark(self, water):
    y, x = water.pos
    self.layout[x][y] = 5
    
class WaterUnit:
  def __init__(self, pos):
    self.char = '~'
    self.pos = pos
    self.x = self.pos[0] 
    self.y = self.pos[1]
    
  def move(self, direction):
    self.pos = tuple(sum(x) for x in zip(self.pos, direction))
    self.x = self.pos[1]
    self.y = self.pos[0]
    
def can_move(water, cave_layout, direction):
  new_pos = tuple(sum(x) for x in zip(water.pos, direction))
  return cave_layout.is_empty(new_pos)
  
def load(filename):
  with open(filename) as f: 
    for line in f.readlines():
      yield line
    
def col_values(i, layout):
  col = [row[i] for row in layout if row[i] != 1]
  try:
    # checking for 'hanging' water. Invert the column,
    # if a water tile isn't first in the list, we've got 
    # some danglin' water 
    if [x for x in reversed(col)].index(5) > 0:
      return '~'
    else:
      return sum([1 for x in col if x == 5]) 
  except:
    return 0 # no water 

def calc_totals(cave_layout):
  return [col_values(i, cave_layout)
          for i in range(len(cave_layout[0]))]
  
def to_output_format(val):
  output_chars = [' ', '#',None,None,None,'~']
  return output_chars[val]

if __name__ == '__main__':
#   cave_data = load('testdata\\simple_cave.txt')
  cave_data = load('testdata\\complex_cave.txt')

  
  total_water = next(cave_data)
  
  next(cave_data)
  cave = Cave([[1 if x == '#' else 0 for x in line[:-1]]
               for line in cave_data])

  water_unit = WaterUnit((0,1))
  cave.mark(water_unit)
  
  for water in range(int(total_water) - 1): 
    if can_move(water_unit, cave, Direction.down):
      water_unit.move(Direction.down)
      cave.mark(water_unit)
    elif can_move(water_unit, cave, Direction.right):
      water_unit.move(Direction.right)
      cave.mark(water_unit)
    else:
      water_unit.move(Direction.up)
      while can_move(water_unit, cave, Direction.left):
        water_unit.move(Direction.left)
      cave.mark(water_unit)
    if water % 7 == 0:
      os.system('cls')
      for i in cave.layout: print(''.join([to_output_format(x) for x in i]))
      time.sleep(.05)
  
  os.system('cls')
  for i in cave.layout: print(''.join([to_output_format(x) for x in i]))
  time.sleep(.05)
  
  print(calc_totals(cave.layout))
    
    
    
  
  
  
  
  
  
  