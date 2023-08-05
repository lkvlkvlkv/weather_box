# digi+專題製作 - 氣象資訊盒

## 成品

### 照片

![](https://hackmd.io/_uploads/HkvIOnooh.png)

### 影片

[![影片連結](https://hackmd.io/_uploads/ryRAn6sjn.png)](https://www.youtube.com/watch?v=-JyeQE8a8uw)

## 相關連結

[報告簡報](https://docs.google.com/presentation/d/1mwt2YJJlF4_ikca8jIYy_ar2ijWcfhbtfx34N6Sk3Dk/edit#slide=id.p)

[weather_box - Github](https://github.com/lkvlkvlkv/weather_box)

[weather_box - HackMD](https://hackmd.io/@LKV/weather_box)

## Reference

[第一次就上手 玩轉樹梅派PicoW - 研蘋果](https://www.chainhao.com.tw/raspberry-pi-pico-w/)

## 起源

digi+計畫希望我們在兩天的課程中產出一個小專題，老師有指定題目氣象資訊盒，希望我們爬取網路資料，適當顯示氣象資訊。

## 零件

這次專題的零件有以下幾個：

1. LCD 螢幕
2. LED 燈條
3. 舵機 ( 指針 )
4. 五種顏色的 LED 燈泡
5. 光敏電阻 ( 亮度感測 )
6. 兩個按鈕

## 資訊

能爬取到的資訊有：

1. Wx 天氣種類
2. PoP 降雨機率
3. MinT 最低溫度
4. MaxT 最高溫度
5. CI 舒適程度

大概講一下每個的格式長怎樣

### 天氣種類

#### 資料格式

[氣象局API資料說明文件](https://opendata.cwb.gov.tw/opendatadoc/MFC/ForecastElement.pdf)

天氣種類的定義有點混亂，在顯示上相對不容易，大概列出幾個：

| 中文描述 | 英文描述 | 分類代碼 |
| -------- | -------- | -------- |
| 晴天 | CLEAR | 1 |
| 晴時多雲 | MOSTLY CLEAR | 2 |
| 多雲時晴 | PARTLY CLEAR | 3 |
| 多雲 | PARTLY CLOUDY | 4 |
| 多雲時陰 | MOSTLY CLOUDY | 5 |
| 陰時多雲 | MOSTLY CLOUDY | 6 |
| 陰天 | CLOUDY | 7 |
| 多雲陣雨 | PARTLY CLOUDY WITH SHOWERS | 8 |
| 多雲短暫雨 | PARTLY CLOUDY WITH OCCASIONAL RAIN | 8 |
| 多雲短暫陣雨 | PARTLY CLOUDY WITH OCCASIONAL SHOWERS | 8 |
| 午後短暫陣雨 | OCCASIONAL AFTERNOON SHOWERS | 8 |
| 短暫陣雨 | OCCASIONAL SHOWERS | 8 |
| 多雲時晴短暫陣雨 | PARTLY CLEAR WITH OCCASIONAL SHOWERS | 8 |
| 多雲時晴短暫雨 | PARTLY CLEAR WITH OCCASIONAL RAIN | 8 |
| 晴時多雲短暫陣雨 | MOSTLY CLEAR WITH OCCASIONAL SHOWERS | 8 |

#### 資料顯示

我選擇用指針做顯示，指向規則如下：

1. 當字串中包含"晴陰雨雷"其中一字時分別指向0,60,120,180度
2. 如果包含其中兩種氣象就指向平均值
3. 如果超過三個就取數字比較大的前兩個指中間值，ex. 晴時多雲短暫陣雨 會取陰和雨出來/2，就沒有雨

![](https://hackmd.io/_uploads/B1gp62sin.png)


### 降雨機率

#### 資料格式

給予一個百分比，ex. 30%

#### 資料顯示

我選擇使用LED燈條顯示，將100%分成8等分，若12.5%以下會亮一個燈，25%以下會亮兩個燈，依此類推

![](https://hackmd.io/_uploads/B1s5A2soh.png)


### 舒適程度

#### 資料格式

[氣象局API資料說明文件](https://opendata.cwb.gov.tw/opendatadoc/MFC/ForecastElement.pdf)

氣象局的文件沒寫舒適程度有什麼種類，也有點不知道怎麼顯示出來(頂多LCD吧)，沒把握能handle所有資料，所以就沒有顯示這個資訊，大概列出幾個我有看過的種類：

| 舒適程度 |
| -------- |
| 舒適      |
| 舒適至悶熱 |
| 舒適至易中暑 |
| 悶熱 |


### 溫度

#### 資料格式

數字，ex 30

#### 資料顯示

我選擇LCD來顯示，直接顯示字串MaxT, MinT和幾度c

![](https://hackmd.io/_uploads/B1GHuhjin.png)

## 特別巧思

因為零件差不多，所以我一直在思考要怎麼呈現才不會跟其他人過於相似。因為零件相同，外觀上不會相差太多，又因為要顯示天氣資訊，所以LCD、可以旋轉180度的舵機、燈條肯定會被使用到，原本有想過要用光敏電阻調整燈條的亮度，但怕這樣工作量過於巨大時間來不及。

最後我選擇了在LCD和LED燈條的顯示上動一點手腳。

### LCD 螢幕 => 跑馬燈

因為LCD螢幕只能顯示16\*2個字元，空間不太夠完整顯示太多東西，所以做了類似跑馬燈的效果。
具體來說每次顯示字串前16個字，並且每次顯示完後將第一個字元丟到最後面就完成了。

``` python=
while True:
    lcd.putstr(info[:16])
    lcd.putstr(copyRight[:16])
    # Circulate the information and copy right
    info = info[1:] + info[0]
    copyRight = copyRight[1:] + copyRight[0]
    sleep(0.3)
```

### LCD 螢幕 => 自訂字元

因為°C的°不在標準ASCII 128內，所以LCD螢幕的函式庫是沒辦法顯示這個字元的，但函式庫有開放自訂字元的函式給我們自己畫，每個字元有5\*7的空間，我們可以將自訂字元定義為特殊字元存在LCD的內建記憶體中，並透過chr(2)來取得特殊字元。

``` python=
# 定義°為自訂字元2號
lcd.custom_char(2, [
    0b00100,
    0b01010,
    0b00100,
    0b00000,
    0b00000,
    0b00000,
    0b00000,
    0b00000
])

# 透過chr(2)取得特殊字元
info = f"MinT: {self.minT}" + chr(2) + f"C MaxT: {self.maxT}" + chr(2) + f"C PoP: {self.pop}% "
lcd.putstr(info)
```

#### 特殊字元作畫

我使用了這個網站先畫出自己想要的自訂字元，他可以讓使用者用圖形化介面作畫，並且轉成bit array。
https://maxpromer.github.io/LCD-Character-Creator/

![](https://hackmd.io/_uploads/r1JeQ6jjh.png)

### LCD 螢幕 => 酷炫版權文字

我看別人會在自己用心做的作品中加入版權聲明，剛好LCD的第二行是空出來的，就利用跑馬燈顯示了這個字串作為版權聲明。
```
"© 2023 Copyright lkvlkvlkv. All rights reserved. "
```

©是一個特殊字元需要自訂，我用上面的網站怎麼畫都畫不像，我慢慢認知到5\*7是不夠顯示的，最後我利用兩個字元的空間，拼出這個字元來。

#### 使用了兩個字元的寬度顯示

![](https://hackmd.io/_uploads/HkKE4aioh.png)

#### bit array
``` python=
# 左半部
lcd.custom_char(0, [
    0b00111,
    0b01000,
    0b10001,
    0b10010,
    0b10010,
    0b10001,
    0b01000,
    0b00111
])
# 右半部
lcd.custom_char(1, [
    0b11100,
    0b00010,
    0b11001,
    0b00001,
    0b00001,
    0b11001,
    0b00010,
    0b11100
])
```

### LED 燈條 => 酷炫霓虹燈特效

覺得這個燈條上的LED可以變色不拿來利用有點可惜，就設計了一套亮燈邏輯：

1. 紅橙黃綠藍靛紫白 左shift
2. 紅橙黃綠藍靛紫白 全部顯示一樣顏色
3. 紅橙黃綠藍靛紫白 右shift
4. 白紫靛藍綠黃橙紅 全部顯示一樣顏色

``` python=
led_arr = [
    (255, 0, 0),   # red
    (255, 165, 0), # orange
    (255, 150, 0), # yellow
    (0, 255, 0),   # green
    (0, 0, 255),   # blue
    (75, 0, 130),  # indigo
    (138, 43, 226),# violet
    (255, 255, 255)# white
]

# 左shift
for i in range(16):
    colors = (led_arr[i%8:] + led_arr[:i%8])[:numpix]

    for index, color in enumerate(colors):
        neo.set_pixel(index, color)
        neo.show()
    sleep(0.3)
# 正序顯示同個顏色
for i in range(8):
    colors = (led_arr[i],) * numpix

    for index, color in enumerate(colors):
        neo.set_pixel(index, color)
        neo.show()
    sleep(0.3)
# 右shift
for i in range(16):
    colors = (led_arr[i%8:] + led_arr[:i%8])
    colors.reverse()
    colors = colors[:numpix]

    for index, color in enumerate(colors):
        neo.set_pixel(index, color)
        neo.show()
    sleep(0.3)
# 反序顯示同個顏色
for i in range(8):
    colors = (led_arr[7 - i],) * numpix

    for index, color in enumerate(colors):
        neo.set_pixel(index, color)
        neo.show()
    sleep(0.3)
```






