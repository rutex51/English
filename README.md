# Wczoraj, dziś, jutro

Aplikacja dla 8-latka do nauki angielskiego: najpierw *to be* (am, is, are, was, were, will be), potem czasy proste.
Krótkie misje, oś czasu, ćwiczenia z literkami, powtórki w odstępach, kruszce, kuźnia trofeów, medale, 50 stworków i 20 filmików.

## Jak uruchomić
Strona działa przez GitHub Pages: **Settings → Pages → Deploy from a branch → `main` / `(root)`**.
Adres: `https://rutex51.github.io/English/`

Na telefonie dziecka otwórz adres i wybierz „Dodaj do ekranu głównego”. Aplikacja otworzy się na pełnym ekranie.

## Gdzie jest postęp
W przeglądarce urządzenia (localStorage). Kopię zapasową zapisuje i wczytuje panel „Dla rodzica” (chroniony PIN-em).

## Offline i aktualizacje
Po pierwszym otwarciu z internetem aplikacja zapisuje się w telefonie i działa też bez internetu (plik `sw.js`).
Gdy w repozytorium pojawi się nowa wersja, aplikacja pokaże przycisk „Nowa wersja – dotknij, aby odświeżyć”
(nie w trakcie misji – dopiero po jej zakończeniu). Postęp zostaje.

## Jak wprowadzić zmianę
1. Edytuj `src/app.html` (cała aplikacja).
2. Dopisz na początku listy `CHANGES` w `src/app.html` linijkę z datą i opisem zmiany. Numer wersji (1.x) liczy się sam z liczby wpisów.
3. Uruchom `python3 tools/build.py` – zbuduje `index.html`, `sw.js` i `version.json` z nowym numerem i kodem wersji.
4. Zatwierdź i wyślij wszystkie zmienione pliki.

## Wersja aplikacji
Panel „Dla rodzica” → karta „Wersja aplikacji”: numer i data wersji uruchomionej na tym urządzeniu, lista zmian
i sprawdzenie, czy na serwerze jest nowsza wersja (`version.json`). Jeśli jest, przycisk „Zaktualizuj teraz” ją wczytuje.

## Pliki
- `src/app.html` – źródło aplikacji
- `index.html` – zbudowana strona (z `tools/build.py`)
- `sw.js` – praca offline i wykrywanie nowej wersji (generowany)
- `version.json` – numer, data i kod najnowszej wersji, sprawdzany z panelu rodzica (generowany)
- `manifest.webmanifest`, `icon-*.png`, `apple-touch-icon.png` – ikona i ustawienia dla „Dodaj do ekranu głównego”
