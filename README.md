# BDO_bot_fish
👀🎣 Бот на компьютерном зрении для рыбалки в Black desert online


## Установка и настройка бота


### Клорирование
В консоли IDE/CMD/Powershild по желаему пути использовать команду `git clone https://github.com/LilViewer/BDO_bot_fish.git`
###### или просто скачать файлы из репозитория


### Установка всех зависемостей 

- Если нет python, то установите, [3.11+](https://www.python.org/downloads/)
- Установить драйвер [interception](https://github.com/oblitum/Interception/releases/tag/v1.0.1), нужен для имитации кликов, для установки скачайте и разархивируйте zip, в CMD(от имени Адменистратора) открыть папку `command line installer` и выволните - `install-interception.exe /install` и перезапустите ПК
     - Из папки `library/x64` перенести файл `interception.dll` в папку бота
- Перенести из репозитория [AutoHotpy](https://github.com/dc740/AutoHotPy/tree/master), в папку бота, файлы:
     [AutoHotPy.py](https://github.com/dc740/AutoHotPy/blob/1f751d1aa0c7c264e5b29a9e13a4dea3cab11407/AutoHotPy.py,AutoHotPy.py),
     [InterceptionWrapper.py](https://github.com/dc740/AutoHotPy/blob/1f751d1aa0c7c264e5b29a9e13a4dea3cab11407/InterceptionWrapper.py,InterceptionWrapper.py)

-  Скачайте [Tesseract-ocr](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.1.20230401.exe) в папку с ботом или в желаемое место с указанием пути до `tesseract.exe`
     ```Python
     40# pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe'
     ```
- Установить библиотеки
  ```
  pip install numpy
  pip install mss
  pip install Pillow
  pip install opencv-python
  pip install pytesseract
  pip install threaded
  ```

### Настройка BDO

- Видео > окно

  ![Видео > окно](https://sun9-74.userapi.com/impg/RbwTGfEj83-_BlXP0IONiHrKgFji2WTwmADOfA/zhCthiA2GQM.jpg?size=532x295&quality=96&sign=9c9d103e188f332443527dd4c84c1412&type=album, "Видео > окно")

- Настройки > отображение

  ![Настройки > отображение](https://sun9-14.userapi.com/impg/MZfz7Iz2rJg6KB_4q5nQbqtuSAiKSApx_SS1nQ/H9-Yq-ERks4.jpg?size=527x335&quality=96&sign=4bfb89716aa6f7c57085d86a29e5af4f&type=album, " Настройки > отображение")

- Хот-кей поиска НИП

  Установите <kbd>Alt</kbd>+<kbd>V</kbd>, в противном случае другое сочетание
  ###### в строчке 321, файла start.py поменять ```autohotpy.V.press()``` на желаемое

  ![Поиск НИП](https://sun9-69.userapi.com/impg/PS_GB9L2Xbc0Z-9fJqzsM0wgFSKiTRS1kJQFQA/6lnBcbvRBkw.jpg?size=451x232&quality=96&sign=8c6ba67511a692af7c0607e3084a634b&type=album, 'Поиск НИП')

  - Добавление 3 точек в избраном

    В поиске НИП(<kbd>Alt</kbd>+<kbd>V</kbd>) в разделе избраное добавить 3 точки: торговец, ремонт, рыбалка
  
    ![Избраное](https://sun9-79.userapi.com/impg/QY1Eh03pDWibWuuVOjSY2U6H5_vLCfQ--Wll-w/oFILX9-48qA.jpg?size=325x184&quality=96&sign=5a41cc4c1afdb55e09ce5bb5fb6683dd&type=album, 'Избраное')


### Настройка Бота

1. Запуск скрипта, по стандарту на F4, можно менять по желанию
    ```Python
    498# auto.registerForKeyDown(auto.F4, enableDisableSuperCombo)
    ```

2. Выбор монитора на котором будет работать скрипт, если больше одного смотрите порядок в системе Windows
    ```Python
    13# monitor=0
    ```

3. Вкл/выкл проверки на прочность удочки/инветоря и бег на прожажу/починку, для отключение прописать `False`
    ```Python
    43# Nips = True
    ```

4. Изменение функции ToRun(autohotpy), если вы рыбачите в Велии, от торговца, к конюшне и обратно на рыбвлку, то вам будет достаточно и имеющиесего кода, в противном случае, редактируйте под свои задачи



    4.1. Функция SearchNip определяет на какую точку побежать, если написать 1, то он поставит точку соответственно вашему второму пункту избраного
    ```Python
    362-406# SearchNip(autohotpy, 0)
    ```
    
    4.2. leftButton эмуляция ЛКМ, sleep(*) - задержка до следуюшей строчки кода 
    ```Python
    407# sleep(.2)
    408# leftButton(autohotpy)
    409# sleep(1)
    ```

    4.3. autohotpy.*.press() - функция для эмитации клавиатуры, заместо * ставьте желаемую клавишу, для цифр 1,2,3 и т.д указывайте N1,N2,N3
    ```Python
    368# autohotpy.R.press()
    369# sleep(1)
    370# autohotpy.N1.press()
    ```

    4.4. autohotpy.moveMouseToPosition(*, *) сдвиг мышки до отпределеных коорденат
    ```Python
    392# autohotpy.N2.press()
    393# autohotpy.moveMouseToPosition(728, 801)  # Починка всего
    394# leftButton(autohotpy)
    ```
    

5. Количество занятых слотов когда бежать на продажу
   ```Python
   46# inventary = 35
   ```
  
### Проблема Бота

Если при появление мини-игры(скриншот ниже), сразу появляется текст BAD или ползунок просто бегает, то добавьте число побольше в `sleep(*)` 

![Мини-игра](https://sun9-45.userapi.com/impg/Sv3Gqg7KheQRC8EtAh3Tu6mCaf5pt7Ap2BZDKA/Ku5EK5AHMkg.jpg?size=320x76&quality=96&sign=1a1a398fcbc343733dd7a3d1991eaa59&type=album, 'Мини-игра')
  
```Python
134# sleep(1.5)
135# miniGameThree(autohotpy)
```

### Запуск Бота

Запустите CMD, укажите путь к папке, допустип - `C:\Users\demac\PycharmProjects\test`, дальше вызывать скрипт - `python start.py` и прожимаем дважды <kbd>F4</kbd>

![CMD](https://sun9-70.userapi.com/impg/VDbT6jhE-dGTC9T8T-7TEf_HFCe7-8PbAzkYtA/MLhrSKDnYVQ.jpg?size=429x119&quality=96&sign=b21545ab8cf588731e2f7427220f801d&type=album, 'CMD')
