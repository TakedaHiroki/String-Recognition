# String-Recognition
# トラックバーを利用した画像処理
OpenCVのトラックバーから変数の値を受け取り画像処理を行う.

## 実行環境
- MacOS 10.13.4

- Python 3.6.5

- OpenCV 3.4.1

- numpy 1.14.3

## コード詳細
- ### color.py

RGB値の変化割合をトラックバーで受け取り色調を変化させる.


トラックバーの初期値は100%に設定しておく.
```python
cv2.setTrackbarPos('R', 'Color', 100)
cv2.setTrackbarPos('G', 'Color', 100)
cv2.setTrackbarPos('B', 'Color', 100)
```


初期状態でのRGB値を100%として, トラックバーからそれぞれの変化割合を受け取り, 相対値を出力する.
なおRGB値の変化割合は0%〜200%に設定してある（ある程度の明度調整も可能）.
また処理はfloatに変換してから行う.
```python
r = cv2.getTrackbarPos('R', 'Color') / 100
g = cv2.getTrackbarPos('G', 'Color') / 100
b = cv2.getTrackbarPos('B', 'Color') / 100
frame = frame / 255
frame[:,:,2] *= r
frame[:,:,1] *= g
frame[:,:,0] *= b
```

実際には以下のように動作する.

![color](https://user-images.githubusercontent.com/39133269/42129317-b662809e-7cfc-11e8-82ea-b64321192c19.gif)


- ### gamma.py

ガンマ値をトラックバーで受け取りガンマ変換する.


ルックアップテーブルを使い, それぞれの輝度値についてトラックバーから受け取ったガンマ値を適応させる.
```python
LUT = np.zeros(256, dtype=np.uint8)
for i in range(256):
LUT[i] = 255 * pow(i / 255., 1.0 / gamma)
```


ゼロによる除算を避けるためにトラックバーから受け取ったガンマ値がゼロの場合は0.01とする.
```python
if gamma == 0:
  gamma = 0.01
```

実際には以下のように動作する.

![gamma](https://user-images.githubusercontent.com/39133269/42129322-c019cd9a-7cfc-11e8-9490-03c1f86d80a6.gif)


- ### gausian.py

分散をトラックバーで受け取り画像にガウシアンフィルタを適応させる.


トラックバーから分散を受け取りフィルターで畳み込む.
今回は画素値が大きいのでフィルターサイズを25x25に設定している.
```python
frame = cv2.GaussianBlur(frame, (25, 25), variance)
```

実際には以下のように動作する. パラメータの変化が大きすぎて変化がわかりにくいためもう少し小さくすると良かったかもしれない.

![gausian](https://user-images.githubusercontent.com/39133269/42129326-d39dce16-7cfc-11e8-841b-45b3fbac06ff.gif)


またLinuxやWindowsでは実際にトラックバーの値が表示されるようだが, Macでは表示されないため以下のように画像中に書き込むようにしている.

```python
cv2.putText(frame, "variance:" + str(variance), (20, 40), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255,255,255),2)
```

## 参考文献

[機械学習のデータセット画像枚数を増やす方法](https://qiita.com/bohemian916/items/9630661cd5292240f8c7)（LUTの使い方を参考）

