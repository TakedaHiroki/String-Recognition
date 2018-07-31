# MSERを利用した文字領域検出
MSERを利用して文字領域を検出し, テキストを出力する.

<img src="https://user-images.githubusercontent.com/39133269/43440406-1796e002-94d2-11e8-8996-ca4f4c944092.png" width=50%>
<img src="https://user-images.githubusercontent.com/39133269/43440408-1c668f06-94d2-11e8-964f-7dea9214cfae.png" width=50%>



## 実行環境
- MacOS 10.13.4

- Python 3.6.5

- OpenCV 3.4.1

- numpy 1.14.3

## コード詳細
- ### MSERでの処理
入力画像をグレースケール画像に変換してMSERで文字の候補を検出する. 
但し, OpenCV4.3.1ではdetectRegionsの引数が2つになっているので注意.

```python
imgname = image_name
img = cv2.imread(imgname)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
mser = cv2.MSER_create()
mser.setMinArea(100)
mser.setMaxArea(800)
coordinates = mser.detectRegions(gray, None)
```

- ### 文字の抽出

検出した文字の候補に対してアスペクト比と大きさの条件で文字以外を削減処理し, 残りを文字として登録する.

for coord in coordinates:
    bbox = cv2.boundingRect(coord)
    x,y,w,h = bbox
    aspect_ratio = w / h
    if w < 10 or h < 10 or w/h > 5:
        continue
    moji.append([x, y, h, w])

- ### 文字列検出

登録した文字を左から順にソートし, 上から順に先頭の文字 の中線を登録して中線上の文字を文字列として登録する.
```python
moji_sort = sorted(moji, key=lambda x: x[1])
    for i in range(len(moji_sort)):
        if high_line >= moji_sort[i][1]-10 and high_line <= (moji_sort[i][1] + moji_sort[i][3]+10):
            string[j].append(moji_sort[i])
        else:
            high_line = moji_sort[i][1]+moji_sort[i][3]/2
            string.append([])
            j = j + 1
            string[j].append(moji_sort[i])
```

- ### OCRによるテキスト出力

文字列が右上がりか, 左上がりかで(これは文字列そのものだけではなく撮影時に斜めになる場合などもある)処理を変えている.

```python
for i in range(len(string)):
        if len(string[i]) < 30:
            continue
        string_sort = sorted(string[i], key=lambda x: x[0])
        string_sort = np.array(string_sort)
        im = img[string_sort.min(axis=0)[1]-2:string_sort.min(axis=0)[1]+(string_sort.min(axis=0)[1]+string_sort.max(axis=0)[3]-string_sort.min(axis=0)[1]), string_sort.min(axis=0)[0]-2:string_sort.min(axis=0)[0]+(string_sort.max(axis=0)[0]-string_sort.min(axis=0)[0]+string_sort.max(axis=0)[2])]
        cv2.imwrite("result"+str(num)+".png", im)
        txt = tool.image_to_string(Image.open('result'+str(num)+'.png'), lang="eng", builder=pyocr.builders.TextBuilder(tesseract_layout=6))
        print(txt)
```

## 参考文献

[機械学習のデータセット画像枚数を増やす方法](https://qiita.com/bohemian916/items/9630661cd5292240f8c7)（LUTの使い方を参考）

