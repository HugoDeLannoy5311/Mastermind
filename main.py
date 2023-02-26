import random
global code
global aantal_getallen_in_code
global al_gestelde_vragen
global teller
import itertools
aantal_getallen_in_code = 6
al_gestelde_vragen = []
teller = 0


def creeer_code():
    """"
    Creeert een random geheime code
    """
    geheime_code = []
    for i in range(4):
        geheime_code.append(random.randint(1,aantal_getallen_in_code))
    return geheime_code

code = creeer_code()
#print("                                              ",code)

def gok():
    """
    input: 4 getallen
    output:
    Met deze functie word de invoer van de gebruiker gecontroleerd dat deze aan de voorwaardes voldoet en in een list gezet om een antwoord te kunnen krijgen
    """
    vraag = input("voer 4 getallen in als gok: ")
    vraag_list = []
    if len(vraag) != 4:
        print("verkeerde invoer")
        gok()
    else:
        for i in range(len(vraag)):
            vraag_list.append(int(vraag[i]))
        return vraag_list

def zwart_wit_vraag(code, vraag):
    """"
    input: de geheime code en de vraag die de gebruiker heeft gesteld
    output: een tuple van (aantal zwarte pinnen, aantal witte pinnen)
    Met deze functie word de invoer van de gebruiker gecontroleerd en feedback gegeven over de code
    """
    aantal_zwart = 0
    aantal_wit = 0
    vraag_copy = list(vraag)
    code_copy = list(code)

    for i in range(len(code)):
        if code[i] == vraag[i]:
            aantal_zwart = aantal_zwart + 1
            vraag_copy.remove(vraag[i])
            code_copy.remove(vraag[i])

    for i in range(len(vraag_copy)):
        if vraag_copy[i] in code_copy:
            aantal_wit = aantal_wit + 1
            code_copy.remove(vraag_copy[i])

    return (aantal_zwart, aantal_wit)


def simple_strategy(code, mogelijke_codes, teller):
    """
    input: de geheime code, alle mogelijke codes en de teller van hoeveel vragen al zijn gesteld
    output: de gegokte geheime code
    Met deze functie word de simple strategy uitgevoerd: neemt steeds het element 0 in de lijst met mogelijke codes en recuceerd
    deze op basis van de feedback. Er blijven alleen codes over die nog mogelijk zijn op basis van de feedback.
    Dit word herhaald totdat er maar 1 code over blijft en dus de geheime code moet zijn
    """
    teller = teller + 1
    while teller <= 8:
        print("                                              ", mogelijke_codes[0])
        antwoord = zwart_wit_vraag(code, mogelijke_codes[0])
        print("zwart:", antwoord[0], "wit:", antwoord[1], "                                               ",
              antwoord[0], antwoord[1])
        overgebleven_zoekruimte = []

        for i in range(len(mogelijke_codes)):
            antwoord2 = zwart_wit_vraag(mogelijke_codes[0], mogelijke_codes[i])
            if antwoord == antwoord2:
                overgebleven_zoekruimte.append(mogelijke_codes[i])


        if len(overgebleven_zoekruimte) > 1:
            return simple_strategy(code, overgebleven_zoekruimte, teller)
        else:
            return overgebleven_zoekruimte[0]

    return "te veel gokken"

def getelde_antwoorden_per_vraag(mogelijke_vragen, mogelijke_codes):
    """"
    input: alle (nog) mogelijke antwoorden en vragen
    output: een dict van de aantallen van antwoorden per mogelijke code die getest is per mogelijke vraag
    Met deze functie kunnen we een dict ophalen om later de laagste hoogste te kunnen bepalen
    """
    getelde_antwoorden = {}

    for mogelijke_vraag in mogelijke_vragen:
        getelde_antwoorden[mogelijke_vraag] = {}

    for mogelijke_vraag in mogelijke_vragen:
        for mogelijke_code in mogelijke_codes:
            antwoord = zwart_wit_vraag(mogelijke_code, mogelijke_vraag)

            try:
                getelde_antwoorden[mogelijke_vraag][antwoord] += 1
            except KeyError:
                getelde_antwoorden[mogelijke_vraag][antwoord] = 1
            except Exception as e:
                print(e)
    return getelde_antwoorden

def worst_case(getelde_antwoorden):
    """"
    input: een dict van de aantallen van antwoorden per mogelijke code die getest is per mogelijke vraag, def getelde_antwoorden_per_vraag
    output: de tuple van de best worst case, met dus de laagste hoogste waarde van alle antwoorden op alle mogelijke vragen
    Met deze functie word de volgende gok bepaald van de functie worst case strategy
    """
    best_worst_case_value = 99999
    best_worst_case = ""
    for key in getelde_antwoorden:
        hoogste_waarde_bij_een_vraag = max(getelde_antwoorden[key].values())
        antwoord_met_hoogste_waarde = key
        if hoogste_waarde_bij_een_vraag < best_worst_case_value:
            best_worst_case_value = hoogste_waarde_bij_een_vraag
            best_worst_case = antwoord_met_hoogste_waarde

    return best_worst_case

def worst_case_strategy(code, mogelijke_codes, teller, mogelijke_vragen):
    """"
    input: de geheime code, alle (nog) mogelijke codes, de teller van hoeveel gokken zijn gedaan, alle (nog) mogelijke vragen
    output: de gegokte geheime code
    Met deze functie word de geheime code geraden doormiddel van het uitvoeren van de worst case strategy
    """
    teller = teller + 1
    while teller <= 8:
        getelde_antwoorden2 = getelde_antwoorden_per_vraag(mogelijke_codes, mogelijke_vragen)
        beste_worse_case = worst_case(getelde_antwoorden2)
        print("                                              ", beste_worse_case)
        antwoord = zwart_wit_vraag(code, beste_worse_case)
        print("zwart:", antwoord[0], "wit:", antwoord[1], "                                               ",
              antwoord[0], antwoord[1])
        overgebleven_zoekruimte = []


        for i in range(len(mogelijke_codes)):
            antwoord2 = zwart_wit_vraag(beste_worse_case, mogelijke_codes[i])
            if antwoord == antwoord2:
                overgebleven_zoekruimte.append(mogelijke_codes[i])

        if len(overgebleven_zoekruimte) > 1:
            return worst_case_strategy(code, overgebleven_zoekruimte, teller, mogelijke_codes)
        else:
            return overgebleven_zoekruimte[0]

    return "te veel gokken"

def heuristiek():
    """
    output: een random gok, die nog niet is gemaakt
    Met deze functie word Masterminde gespeeld zoals ik het speel. IK HAAT MASTERMIND.
    Ik heb geen geduld en vind er niets aan om de pinnen te onthouden en op basis van wat ik al heb gevraagd
    dingen te combineren, dus gooi ik een paar random pinnen bij elkaar en hoop op (4,0)
    Het gaat mij niet om het spel, maar om het gezelschap en ik zie het meer als een tijdsverdrijf en heb er
    daarom ook geen probleem mee om er 99/100 keer mee te verliezen
    """
    vraag = []
    for i in range(4):
        vraag.append(random.randint(1, aantal_getallen_in_code))
    if vraag in al_gestelde_vragen:
        random_vraag_generator()
    else:
        al_gestelde_vragen.append(vraag)
    return vraag


def game():
    print("kies een game mode\n1: zelf spelen\n2: AI de simple strategy laten spelen\n3: AI de worst case strategy laten spelen\n4: Heuristiek")
    keuze = int(input("Keuze: "))
    teller = 0
    if keuze == 1:
        while teller < 8:
            teller = teller + 1
            vraag = gok()
            print("                                              ", vraag)
            antwoord = zwart_wit_vraag(code, vraag)
            print("zwart:", antwoord[0], "wit:", antwoord[1], "                                               ",antwoord[0], antwoord[1])
            if antwoord == [4, 0]:
                return print("Je hebt gewonnen, in {} gokken".format(teller))

        return print("je hebt verloren, te veel gokken")
    if keuze == 2:
        KLEUREN = [1, 2, 3, 4, 5, 6]
        LENGTE = 4
        alle_mogelijke_codes = [k for k in itertools.product(KLEUREN, repeat=LENGTE)]
        print("De geheime code is: ", simple_strategy(code, alle_mogelijke_codes, teller))

    if keuze == 3:
        KLEUREN = [1, 2, 3, 4, 5, 6]
        LENGTE = 4
        mogelijke_vragen = [k for k in itertools.product(KLEUREN, repeat=LENGTE)]
        mogelijke_codes = mogelijke_vragen[::]
        print("De geheime code is: ", worst_case_strategy(code, mogelijke_vragen, teller, mogelijke_codes))

    if keuze == 4:
        while teller < 8:
            teller = teller + 1
            vraag = heuristiek()
            print("                                              ", vraag)
            antwoord = zwart_wit_vraag(code, vraag)
            print("zwart:", antwoord[0], "wit:", antwoord[1], "                                               ",antwoord[0], antwoord[1])
            if antwoord == [4, 0]:
                return print("Je hebt gewonnen, in {} gokken".format(teller))

        return print("je hebt verloren, te veel gokken")
    else:
        print("verkeerde invoer")
        return game()

game()


