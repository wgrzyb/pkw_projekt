# pkw projekt
[![en](https://img.shields.io/badge/lang-en-blue.svg)](https://github.com/wgrzyb/pkw_projekt/blob/master/README.en.md)

Projekt został zrealizowany w ramach zajęć laboratoryjnych „Podstawy kryptologii współczesnej” na Wojskowej Akademii Technicznej.

Projekt dotyczy rozwiązania problemu trwałego nośnika z wykorzystaniem łańcucha bloków Algorand oraz technologii InterPlanetary File System (IPFS).
Aby zademonstrować rozwiązanie, zaimplementowano aplikację internetową w języku Python z wykorzystaniem frameworka Flask.

## Szczegóły aplikacji

Aplikacja umożliwia przesyłanie plików i publikowanie wiadomości (pastebin) zaszyfrowanych hasłem.
Przesłane pliki są umieszczane i przechowywane w IPFS.
Aby zachować informację, że plik został wysłany do IPFS, uzyskany identyfikator CID pliku jest dodawany do sieci testowej łańcucha bloków Algorand.
Aplikacja umożliwia również pobieranie wgranych plików i opublikowanych wiadomości.

## Przygotowanie środowiska

  1. Zklonuj repozytorium:

  ```
  git clone git@github.com:wgrzyb/pkw_projekt.git
  ```

  2. Przejdź do folderu repozytorium i zainstaluj wymagane biblioteki (z pliku `requirements.txt`):
  
  ```
  cd .\pkw_projekt
  pip install -r .\requirements.txt
  ```
  
  3. Uruchom Go-IPFS na dockerze:
  
  ```
  docker run -d --name ipfs-node -p 8080:8080 -p 4001:4001 -p 5001:5001 ipfs/go-ipfs:latest
  ```
  
  4. Uruchom [aplikację flask](https://github.com/wgrzyb/pkw_projekt/blob/master/flask_app/main.py) z katalogu repozytorium.
  
  5. Otwórz [aplikację web](http://127.0.0.1:5000/).