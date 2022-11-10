- [X] requirements.txt

Setup
- [X] start functie --> kijkt hoeveel mensen mee doen en vertelt welke rollen meedoen. (als tijd over kan speler de pool aanpassen)
- [X] maakt channels aan voor elke rol. En een dead chat
- [X] maakt permissions aan voor elke rol. 
- [X] geeft iedereen "???" rollen. (toont aan dat onbekend is wat ze zijn).

SpelCyclus
- [X] begint met een compelling story --> legt uit dat weerwolven aanwezig zijn en eind met "het wordt nacht in wakkerdam".
- [X] roept op volgorde elke rol en wat ze willen doen. (zie vanaf r.)
- [X] "iedereen wordt wakker behalve @....".
- [X] speeches worden gegeven en burgemeester wordt gekozen. (enkel if not burgemeester_aanwezig:)
- [X] stem fase gebeurt. --> overleg en daarna stem.
- [X] "@.... is gekilled en was een ...."
- [X] "het wordt nacht in wakkerdam".
- [X] Nachtfase zonder de dode rollen.

Eindcyclus:
- [X] blijf checken of het aantal wolven die leven groter is dan burgers. (gelijk als de burgemeester weerwolf is)
- [X] blijf checken of alle weerwolven dood zijn.
- [X] blijf checken of alleen de 2 liefjes leven.
- [X] feliciteer alle spelers.
- [X] maak alle channels en rollen openbaar.
- [X] bedank spelers voor spelen en stop de code.

Burgers:
- [X] kan stemmen op mensen in de dag. In de nacht alleen wolvensnack.

Weerwolven:
- [X] alle weerwolven eten elke nacht 1 iemand op.

Ziener:
- [X] elke nacht wordt 1 iemands rol gerevealed. (de reveal verwijdert na een tijdje of blijft voor altijd)

Het Onschuldige Meisje:
- [X] ziet de berichtjes die de weerwolven heeft gestuurd in de nacht. geen namen van wie het zijn maar ze zou het kunnen afleiden.

De Jager:
- [X] als jager sterft laat m iemand meenemen plz

Cupido:
- [X] koppelt op nacht 1 2 mensen. Die twee mensen zijn verliefd. (nieuw channel). In code moeten deze gekoppeld worden. niet met rollen.
- [X] winconditie --> if Lover1.state == alive and Lover2.state == alive: game.win() ofz

De heks:
- [X] levensdrankje 1 usage. Healt iemand die sterft
- [X] doodsdrankje 1 usage. killt iemand.

Burgemeester:
- [X] heeft 2 stem. (dus bij ties wint de stemmen met de burgemeester)
- [X] als burgemeester sterft kiest hij nieuwe.
