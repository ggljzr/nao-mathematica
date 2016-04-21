#MI-IVS - rozpoznavani textu
parsovani matematickejch vyrazu z vobrazku
ve finale urceny pro robota https://www.aldebaran.com/en/cool-robots/nao

##rozpoznat tabuli
vyrovnat obraz aby byl kolmo (proste rovne) -- perspective transformation
detekce tabule - mozna funkce pro detekci rohu
taky funkce pro prevod kontur na polygony

pak jednotlivy tahy pak prevyst kontury na polygony

este me napadlo ze kdyby mel ten robot nak cidlo vzdalenosti
tak by se ten vobrazek pak moh nak voriznout podle toho jak je daleko vod steny

##sehat
https://github.com/falvaro/seshat pro rozpoznavani matematickejch vyrazu
zatim sem zkousel udelat z tech kontur .scgink soubor a ten dat tomu
seshatu, ten z nej spravne vyrenderuje vobrazek, ale ofc v nem nic nepozna
(alternativa - Tesseract - mozna zminit v ty zaverecny zprave)

##ziskani tahu z obrazku
https://stackoverflow.com/questions/23506105/extracting-text-opencv
pro ziskani strokes je asi potreba neco jako
https://en.wikipedia.org/wiki/Topological_skeleton, coz neni v opencv
distance transformation
clusterizace
stackoverflow -> finding continuous areas of bits in 2d bit array

este by to teda chtelo udelat nakou tu transformaci tim morpholgy operatorem
(dilatace a tak), protoze u toho vobrazku pod uhlem je pak treba ta sedmicka 
takova potrhana coz by asi chtelo zacelit, i kdyz ten seshat by to mozna vydrzel

jinak co se tyce tech vobrazku tak to numpy.nonzero vypada dobre, akorat by to chtelo
rozrezat ten text region este na jednotlivy znaky zase pomoci kontur a bounding boxes
aby byly ty jednotlivy strokes jakoby voddeleny 

^^to asi nebude potreba

a pak delat ten kazdej znak zvlast s tim, ze by se udaly ty cerny body pomoci
toho nonzero a pak by se udal nakej clustering (naky knn nebo takovy nesmysly)
co by dal ty sousedni body dohromady

hledani souvisle oblasti:
nejdriv teda asi musime najit souvislou voblast ktera bude tvorit jeden tah
takze vzit prvni bilej bod a pak projit vsechny sousedni body a hledat sousedy

ale stejne by to pak chtelo ty jednotlivy body shluknout do vetsich aby treba nebylo vic bodu tahu
na jednim radku, to pak dela v tim seshatu celkem bordel

este se taky podivat jesli by se nedalo nak pouzit to hierarchalClustering z opencv,
najit nakej tutorial


