# Code adapted from https://developpaper.com/simple-implementation-of-region-growing-in-python/

import numpy as np
import pydicom
import matplotlib.pyplot as plt

class Point(object):
  def __init__(self,x,y):
    self.x = x
    self.y = y

  def getX(self):
    return self.x
  def getY(self):
    return self.y

def getGrayDiff(img,currentPoint,tmpPoint):
  return abs(int(img[currentPoint.x,currentPoint.y]) - int(img[tmpPoint.x,tmpPoint.y]))

def selectConnects(p):
  if p != 0:
    connects = [Point(-1, -1), Point(0, -1), Point(1, -1), Point(1, 0), Point(1, 1), \
      Point(0, 1), Point(-1, 1), Point(-1, 0)]
  else:
    connects = [ Point(0, -1), Point(1, 0),Point(0, 1), Point(-1, 0)]
  return connects

def regionGrow(img,seeds,thresh,p = 1):
  height = img.shape[0]
  width = img.shape[1]
  seedMark = np.zeros([height, width])
  seedList = []
  for seed in seeds:
    seedList.append(seed)
  label = 1
  connects = selectConnects(p)
  while(len(seedList)>0):
    # print('Aktuelle Länge der Seeds: {}'.format(len(seedList)))
    currentPoint = seedList.pop(0)

    seedMark[currentPoint.x,currentPoint.y] = label
    for i in range(8):
      tmpX = currentPoint.x + connects[i].x
      tmpY = currentPoint.y + connects[i].y
      if tmpX < 0 or tmpY < 0 or tmpX >= height or tmpY >= width:
        continue
      grayDiff = getGrayDiff(img,currentPoint,Point(tmpX,tmpY))
      if grayDiff < thresh and seedMark[tmpX,tmpY] == 0:
        seedMark[tmpX,tmpY] = label
        seedList.append(Point(tmpX,tmpY))
  return seedMark