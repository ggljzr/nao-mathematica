#MI-IVS - rozpoznavani textu
parsovani matematickejch vyrazu z vobrazku
ve finale urceny pro robota https://www.aldebaran.com/en/cool-robots/nao

##rozpoznat tabuli
sudoku example http://opencvpython.blogspot.com/2012/06/sudoku-solver-part-2.html

vyrovnat obraz aby byl kolmo (proste rovne) -- perspective transformation
detekce tabule - mozna funkce pro detekci rohu
taky funkce pro prevod kontur na polygony

pak jednotlivy tahy pak prevyst kontury na polygony

este me napadlo ze kdyby mel ten robot nak cidlo vzdalenosti
tak by se ten vobrazek pak moh nak voriznout podle toho jak je daleko vod steny

to rozpoznavani uz vicemene funguje
TODO: u vobrazku tabule2.png to este bere kus spodni hrany jako text region tak
na to se mozna podivat. Ale to by slo vyfiltrovat i pozdejc (moc malo tahu ve vobrazku
nebo tak neco)

##sehat
https://github.com/falvaro/seshat pro rozpoznavani matematickejch vyrazu
zatim sem zkousel udelat z tech kontur .scgink soubor a ten dat tomu
seshatu, ten z nej spravne vyrenderuje vobrazek, ale ofc v nem nic nepozna
(alternativa - Tesseract OCR - mozna zminit v ty zaverecny zprave)

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
vono je teda blby ze tohle zase zaceli ty diry co tam maj bejt, treba v sestce
nebo vosmicce

jinak co se tyce tech vobrazku tak to numpy.nonzero vypada dobre, akorat by to chtelo
rozrezat ten text region este na jednotlivy znaky zase pomoci kontur a bounding boxes
aby byly ty jednotlivy strokes jakoby voddeleny 

^^to asi nebude potreba

a pak delat ten kazdej znak zvlast s tim, ze by se udaly ty cerny body pomoci
toho nonzero a pak by se udal nakej clustering (naky knn nebo takovy nesmysly)
co by dal ty sousedni body dohromady

hledani souvisle oblasti:
nejdriv teda asi musime najit souvislou voblast ktera bude tvorit jeden tah
takze vzit prvni bilej bod a pak projit vsechny vostatni body a hledat sousedy
u prvniho bodu zalozit prvni cluster, pridat do nej vsechny body co sou souvisly
s tim bodem, pak vzit prvni bod co neni a zalozit dalsi cluster atd...
ve finale ten jeden cluster bude predstavovat ten jeden znak nebo jakoby tu jednu spojitou
plochu

ale stejne by to pak chtelo ty jednotlivy body shluknout do vetsich aby treba nebylo vic bodu tahu
na jednim radku, to pak dela v tim seshatu celkem bordel

este se taky podivat jesli by se nedalo nak pouzit to hierarchalClustering z opencv,
najit nakej tutorial


nebo>
0. zalozim novej cluster do kteryho budu davat ty serazeny body
1. vemu cluster
2. vemu prvni bod v nem a pro kazdej bod pocinaje tim prvim delam:
3. vemu bod A
4. najdu jemu nejblizsi bod B ve vsech vostatnich bodech
5. Bod A pridam do novyho cluster
6. B = A
7. goto 3

jakoby aby se seradili ty body do ty posloupnosti podle toho tahu


mozna by taky bylo dobry pouzit nakej thinning algoritmus na ty vobrazky, aby vsechny cary mely
sirku 1 (guo-hall algoritmus, zhang-suen algoritmus)
https://web.archive.org/web/20160314104646/http://opencv-code.com/quick-tips/implementation-of-guo-hall-thinning-algorithm/
https://web.archive.org/web/20160322113207/http://opencv-code.com/quick-tips/implementation-of-thinning-algorithm-in-opencv/

