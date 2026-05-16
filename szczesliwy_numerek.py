import random  # Importujemy moduł do losowania liczb
import os      # Importujemy moduł do sprawdzania plików na dysku

# --- KONFIGURACJA ---
# Lista przedmiotów, dla których będą losowane numery
LISTA_PRZEDMIOTOW = ["Polski", "Matma", "Fizyka", "Chemia", "Angielski"]
LICZBA_UCZNIOW = 30  # Zakres numerów w dzienniku (od 1 do 30)
HISTORIA_DLUGOSC = 10  # Maksymalna liczba pamiętanych losowań w historii
NAZWA_PLIKU = "historia.txt"  # Nazwa pliku, w którym zapiszemy dane

# 1. FUNKCJA DO POBIERANIA HISTORII Z PLIKU - dla pojedynczego przedmiotu
def pobierz_historie(szukany_prefix):
    wynik = []  # Tworzymy pustą listę na numery z historii
    if os.path.exists(NAZWA_PLIKU):  # Sprawdzamy, czy plik z historią w ogóle istnieje
        plik = open(NAZWA_PLIKU, "r", encoding="utf-8")  # Otwieramy plik do odczytu ("r")
        for linia in plik:  # Przeglądamy plik linia po linii
            if linia.startswith(szukany_prefix + ":"):  # Szukamy linii zaczynającej się od np. "Fizyka+:"
                czesci = linia.strip().split(":")  # Dzielimy linię na nazwę i numery (rozdzielone dwukropkiem)
                if len(czesci) > 1:  # Jeśli po dwukropku są jakieś dane
                    teksty = czesci[1].split(",")  # Rozbijamy ciąg numerów na pojedyncze teksty po przecinku
                    for t in teksty:  # Przechodzimy przez każdy kawałek tekstu
                        if t != "":  # Jeśli tekst nie jest pusty
                            wynik.append(int(t))  # Zamieniamy tekst na liczbę i dodajemy do listy 'wynik'
        plik.close()  # Zamykamy plik po przeczytaniu
    return wynik  # Zwracamy listę znalezionych numerów (lub pustą, jeśli nic nie było)

# --- START PROGRAMU ---
print("=== SZKOLNY LOSOWNIK ===")
# Prosimy użytkownika o wybór trybu pracy
wybor = input("Wybierz: 1 - Szybko (bez historii), 2 - Sprawiedliwie (z historią): ")

dzis_plus = []  # Lista, w której zapiszemy dzisiejszych szczęściarzy [przedmiot, numer]
dzis_minus = [] # Lista, w której zapiszemy dzisiejszych pechowców [przedmiot, numer]

# Pętla wykonująca losowanie dla każdego przedmiotu z listy
for przedmiot in LISTA_PRZEDMIOTOW:
    h_plus = []  # Pusta lista na historię 'h' szczęśliwych '+' dla tego przedmiotu
    h_minus = [] # Pusta lista na historię 'h' pechowych '-' dla tego przedmiotu
    
    if wybor == "2":  # Jeśli wybrano tryb sprawiedliwy, ładujemy historię z pliku
        h_plus = pobierz_historie(przedmiot + "+")
        h_minus = pobierz_historie(przedmiot + "-")

    # Losowanie SZCZĘŚLIWEGO numerka
    szczesliwy = random.randint(1, LICZBA_UCZNIOW)  # Losujemy pierwszy raz - liczba całkowita z zakresu
    while szczesliwy in h_plus:  # Dopóki wylosowany numer jest w historii...
        szczesliwy = random.randint(1, LICZBA_UCZNIOW)  # ...losujemy ponownie - liczba całkowita z zakresu

    # Losowanie PECHOWEGO numerka
    pechowy = random.randint(1, LICZBA_UCZNIOW)  # Losujemy pierwszy raz
    # Losujemy ponownie, jeśli pechowy jest taki sam jak szczęśliwy LUB jest w historii pecha
    while pechowy == szczesliwy or pechowy in h_minus:
        pechowy = random.randint(1, LICZBA_UCZNIOW)

    # Wyświetlamy wynik losowania dla danego przedmiotu
    print(f"{przedmiot}: Szczęśliwy {szczesliwy}, Pechowy {pechowy}")
    
    # Dodajemy dzisiejsze wyniki do tymczasowych list (przygotowanie do zapisu)
    dzis_plus.append([przedmiot, szczesliwy])
    dzis_minus.append([przedmiot, pechowy])

# --- ZAPIS DO PLIKU (tylko jeśli wybrano tryb 2) ---
if wybor == "2":
    nowe_linie = []  # Pusta zmienna - tu zbierzemy wszystkie linie, które trafią do pliku
    
    for przedmiot in LISTA_PRZEDMIOTOW:  # Przechodzimy przez listę przedmiotów, by przygotować ich historię
        # AKTUALIZACJA SZCZĘŚLIWYCH (+)
        h_p = pobierz_historie(przedmiot + "+")  # Pobieramy to, co już było w pliku
        for d in dzis_plus:  # Szukamy, jaki numer dzisiaj wylosowaliśmy dla tego przedmiotu
            if d[0] == przedmiot: # Jeśli wyszukano 'właściwy' przedmiot
                h_p.append(d[1])  # Dodajemy dzisiejszy numer do listy historycznej
        if len(h_p) > HISTORIA_DLUGOSC: h_p.pop(0)  # Jeśli historia jest za długa, usuwamy najstarszy numer
        
        tekst_p = ",".join(map(str, h_p))  # Zamieniamy listę liczb na tekst oddzielony przecinkami
        nowe_linie.append(przedmiot + "+:" + tekst_p + "\n")  # Tworzymy gotową linię i dodajemy znak nowej linii

        # AKTUALIZACJA PECHOWYCH (-)
        h_m = pobierz_historie(przedmiot + "-")  # Robimy to samo dla pechowych numerków
        for d in dzis_minus:
            if d[0] == przedmiot:
                h_m.append(d[1])
        if len(h_m) > HISTORIA_DLUGOSC: h_m.pop(0)
        
        tekst_m = ",".join(map(str, h_m))
        nowe_linie.append(przedmiot + "-:" + tekst_m + "\n")

    # FINALNY ZAPIS NA DYSK
    plik = open(NAZWA_PLIKU, "w", encoding="utf-8")  # Otwieramy plik w trybie "w" (nadpisanie/wyczyszczenie)
    plik.writelines(nowe_linie)  # Zapisujemy wszystkie przygotowane linie za jednym razem
    plik.close()  # Zamykamy plik, aby system go zapisał
    print("\nHistoria została zaktualizowana i zapisana w pliku!")
