# -*- coding: utf-8 -*-
# 2015.03.06 K. Kuwata
# GetValue.py
"""
    画像から値を取得する
"""

__author__ = 'ken'

from osgeo import ogr
import csv, os
import pandas as pd
import numpy as np
import timeit
from lib.GdalHandle import GImage

#パスを取得する
tiffpath = os.getcwd() + "/tiff/"

aoipath = os.getcwd() + "/AOI/"

poipath = os.getcwd() + "/POI/"


#ポイントのシェープファイルを読み込み、緯度経度をリストで取得
shapeData = ogr.Open(aoipath + "deeplearning.shp")
layer = shapeData.GetLayer()
points = []
for index in xrange(layer.GetFeatureCount()):
    feature = layer.GetFeature(index)
    geometry = feature.GetGeometryRef()
    points.append((geometry.GetX(), geometry.GetY()))


#値を取得したい画像のパスをリストで取得（複数枚）
images = [tiffpath + "2t.%s.Standard.Clip.tif" % 
    (year) for year in xrange(2010, 2013)]

#画像から値を取得し、ポイント毎にcsvファイルを作成
n = 0
for point in points:
  lat = point[1]
  lon = point[0]
  out_csv = poipath + "poi%02d.csv" % (n)
  listData = []
  for i in images:
    #画像名の拡張なしを取得
    y = ".".join(os.path.split(i)[1].split(".")[1:3])
    #自作の画像ライブラリ
    #まず、インスタンスを作る
    image = GImage(i)
    #緯度経度のピクセル値を取得
    #緯度経度が画像外だとエラー
    value = image.GetValue(lat, lon)
    #画像名、ピクセル値をリストでまとめ、連結させる
    listData.append([y, '%0.5f' % (value)])
  #取得した値リストをpandasデータフレームに変換
  data = pd.DataFrame(listData)
  #pandasのcsv出力でファイル作成
  data.to_csv(out_csv, sep=',', index=False, header=False)
  n += 1
  print "Got value at %0.5f, %0.5f" % (lon, lat)

