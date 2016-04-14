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
