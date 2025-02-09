"""
[Title/Звание]
Student Monopoly/Студентски Монопол

[Description/Обрисовка]
Писна ли ви всеки път със семейството да играете една и съща прашасала и остаряла игра(единствената, която имате в шкафа),
а имменно класическото "Монополи"? "Отвъд Монополи" е решението на вашия екзистенциален проблем! Играта е насочена към това да разбие
скуката и обикновеното. Тя представлява multiplayer платформа на тематика "Студентски живот", в която могат да участват от двама до 
трима играчи(идеята за развитие е за повече играчи-повече връзки за поддържане). Всички участници стартират с различни специални
способностти, но еднаква сума пари. След което основната им цел е да станат най-богати накрая. Разликите от традиционната игра са,
че има възможност за ползване на някои хитринки, атакуване на другарче, допълнителни правила, персонализация на полета. 

[Functionalities/Надарености]
0. Картата е с размери 11x11. Полетата приемат своят конкретен тип на случаен принцип от базата данни, като единственото условие е 
да има 1 начало.

1. Видове полета, които ще бъдат част:
#Аналог на традиционните
- "Джобни от дома" - предоставя бонус средства; аналог на началната позиция
- "Имоти" - "Автобусна спирка"(аналог на гара), "Фитнес33"(обикновен имот), "Лападунди"(обикновен имот) и т.н.
- "Пробвай се" - тегли се карта на късмета
- "Жълта книжка" - аналог на "Затвор" в традиционната игра
- "Общежитие/Квартира" - не е поле, но е аналог на къща/хотел

#Нови
- "8 декември" - поле капан, която отнема значителна част от бюджета и прилага cool-down на играча за два хода
- "Изпит" - Задава въпрос, от който зависи дали изходът от хода ще е положителен/отрицателен
- "УНСС" - +1 диплома
- "Студентски стол" - ако имаш късмет ще се нахраниш добре и ще се увеличи живота ти, ако ли не - си се натровил и ще се намали живота ти
- "Exe" - замайва играчът, т.е. го кара играчът да изпълнява ходовете си наобратно докато не се върне до началото
- "Еразъм" - Телепортира играча на случайно място по игралното поле, като същевременно добавя бонус към бюджета му
- "Студентско радио" - Позволява ти да "разпространиш слух", който променя правилата на играта за всички за три хода
(например: всички полета дават двойни награди)

2. Всеки играч притежава следните атрибути:
#Традиционни
-бюджет
-ниво на недепресираност - живот

#Нови
-специални способностти
-ниво на пиянство - брой ходове, които да пропусне
-брой домашни и контролни - при получаване на ново, животът се преизчислява и намалява с известно количество
-дипломи - могат да бъдат използвани само за бонус ход еднократно
-"Mystery Shots"(могат да бъдат приложени на всеки от участниците и на случаен принцип, или да повлияят на нивото на пиянство или
на нивото на недепресираност)

Предоставените герои се различават по своите специалнни способности:
-"BookWorm" - може да предизвика опонент на борба със зарове(знания), като предизвиканият определя залога
-"GirlsMagnet" - почва с повече пари. На всяко завъртане губи част от тях и печели живот
-"NightLife" - притежава повече Mystery Shots
-"94TicketChecker" - има право да глоби играч общо до три пъти
-"Tutor" - (често е студент също) депресира всички други играчи студенти, като добави ново контролно(лимит от 3 общо)
-"Roommate" -  може да създаде "парти" на всяко поле, което променя неговите ефекти. 
Вместо стандартния ефект, всички играчи на това поле получават Mystery Shots

3. Заровете се генерират на случаен принцип. Те притежават и седма страна("no cofee"), която има стойност 0. При всяко хвърляне на чифт
от нея, ходът приключва моментално. При хвърлянето на чифт с друга стойност, играчът получава "Mystery Shot".

4. "Резерве" - опция, която се прилага на най-много едно поле едновременно. Полето е резервирано, докато не бъде преминато 
през него отново. Неговото действие става неактивно за другите играчи

5. В рамките на свой ход играчът може да приложи не повече от един Mystery shot, една диплома, използва веднъж специална способност. 
Ходът приключва с изиграване на стъпките от зара

5. Участник може да загуби, ако му свърши живота или банкрутира.

6. Създаване на персонализирани полета - всяко поле има вид от основните(имот, затвор, начало, карта шанс, гара), описание. След 
запазването му, то се добавя към базата данни.

###Бонус, ако се видя във време

7. Игра срещу бот - предлага се възможност на играча да избере противников бот, използващ различни стратегии.

8. Таймер - допълнителна опция, която се селектира в началото. Губят се пари при надвишаване на ограничението за даден ход. 

[Milestones/Възлови точки]
-Създаване на йерархията и геймлууп
-Добро структуриране на възможностти за ход
-Създаване на герои със способности, базата данни от полета
-Добавяне на визуална репрезентация
-Реализацията на генерирането на случаен принцип на полетата на картата
-Реализацията на заровете, имайки предвид допълнителните правила
-Добавяне на интеракции между играчите
-Реализиране на функционалността "Резерве"
-Реализиране на функционалност за създаване на персонализирани полета
-Реализиране на възможност за повече играчи
-Реализиране на бот противник чрез алгоритми
-Добавяне на таймер и различни моудове спрямо него
(Подредени са по значимост и нужда от реализация, като последните ще бъдат реализирани само ако имам време)

[Estimate in man-hours/Времеоценка в човекочасове]
- Разучаване на Pygame - 6 човекочасове.
- Изготвяне на йерархии, карта, полета - 20 чч.
- Изготвяне на различните герои - 30 чч.
- Имплементиране на визуална репрезентация - 6 чч.
- Изготвяне на основната логика по играта - 30 чч.
- Осъществяване на връзката между играчи - 15 чч.
- Реализиране на създаване на персонализирани полета - 10 чч.
- Тестове - 15 чч.
Общо - 134 човекочасове.

[Usage of technologies/Потребление на технологии]
- Pygame
- Вградени модули
- Socket, threading

------------------------------------------------------------------------------------------------------------------------
(Нямам реална представа дали това е много като обем или малко. Ще съм благодарна за мнение по въпроса и съответно кое да бъде променено)
"""