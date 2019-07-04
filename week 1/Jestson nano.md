# Jestson nano 
# 安裝教學

<!-- .slide: data-transition="zoom" -->

---

<!-- .slide: data-transition="fade-in convex-out" -->

## 目錄

---

<!-- .slide: data-transition="fade-in convex-out" -->

### 設備安裝
### 臉部辯識
### 影像識別

---

<!-- .slide: data-transition="fade-in convex-in" -->


## Part 1 設備安裝

----

### step 1 接上螢幕、鍵盤與滑鼠

![](https://i.imgur.com/QHWAsMb.jpg =300x400)


----


### step 2 接上相機

散熱片靠左，插銷拔起，拿起picamera ，藍色朝自己之後插入，插銷按入

----

![](https://i.imgur.com/XrWfzct.jpg =400x200)

----


### step 3 接上電源

![](https://i.imgur.com/ouaaCsW.jpg =300x400)


---

<!-- .slide: data-transition="fade-in convex-out" -->

## Part 2 臉部辯識

----

### step 1 打開終端機


![](https://i.imgur.com/PP4PiK8.jpg =400x500)



----

### step 2

```cmake=
cd head/part1
```

----

### step 3


```cmake=
python3 new.py
```

----

### step 4
```cmake=
face_recognition ./known/ ./unknown/1.jpg
```

----

### step 5
```cmake=
face_detection  ./known/
```


----


### step 6
```cmake=
python3 face.py
```


----

### step 7
```cmake=
python3 face_landmarks.py 
```

----

### step 8
```cmake=
python3 face_encodings.py 
```

----

### step 9


```cmake=
python3 new.py
```
> test picam ok

----

### step 10

```cmake=
python3 photo.py 
```
>(take photo)

---

<!-- .slide: data-transition="fade-in convex-out" -->

## Part3 影像識別

----

### step 1
```cmake=
cd head/part1
```

----

### step 2
```cmake=
python3 new.py
```
>test picam ok


----

### step 3
```cmake=
python3 photo.py 
```

----

### step 4
```cmake=
cd
```

----

### step 5

```cmake=
cd head/part2/face_classification/src
```

----

### step 6

```cmake=
python3 video_emotion_gender_demo.py
```
>emotion 

