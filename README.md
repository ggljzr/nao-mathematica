#Rozpoznávání příkladů z tabule

##Úvod, cíl práce

Cílem práce bylo vytvořit program, pomocí kterého bude robot číst příklady napsané na tabuli a hlásit výsledky. Robot by tedy měl pořídit fotografii tabule, na ní rozpoznat jednotlivé příklady a ty postupně spočítat.

Práci je tedy možno rozdělit do třech částí:
* Zpracování fotografie -- rozpoznání tabule a příkladů na ní
* Zpracování příkladů -- převod příkladů (obrázků) do vhodného textového formátu
* Výpočet příkladů -- v tomto případě s využitím API pro jazyk Mathematica 


##Zpracování fotografie tabule

V této části bude využita především knihovna pro zpracování obrazu OpenCV (verze 2.4.13). Knihovna kromě C++ podporuje i rozhraní pro Javu, Python a další jazyky. Já jsem se kvůli snadnému prototypování rozhodl pro implementaci programu použít Python (verze 2.7). Funkce z této knihovny v textu začínají **//cv2.//**.

### Rozpoznání tabule a transformace perspektivy

Nejdřív je potřeba vymezit plochu, na které se budou hledat příklady. Musí se tedy nalézt krajní body tabule a podle těchto bodů transformovat perspektivu tak, aby každý roh tabule odpovídal krajnímu bodu obrázku. Při použití obrázků s rozlišením 640x480 budou tedy krajní body tabule na souřadnicích (0,0), (640,0), (480,0), (640,480).

#### Hledání krajních bodů

#### Transformace perspektivy
