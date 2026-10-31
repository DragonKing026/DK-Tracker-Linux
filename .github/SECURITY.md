# Polityka bezpieczeństwa

## Wspierane wersje

Poprawki bezpieczeństwa wychodzą tylko w **najnowszym wydaniu** DK Tracker. Starsze wersje nie dostają łatek —
zaktualizuj przez Flatpaka (`flatpak update`) albo z [wydań](https://github.com/DragonKing026/DK-Tracker-Linux/releases).

## Zgłaszanie podatności

Nie zgłaszaj podatności w publicznym issue. Użyj prywatnego zgłoszenia GitHuba: zakładka **Security** →
**Report a vulnerability** w
[repozytorium](https://github.com/DragonKing026/DK-Tracker-Linux/security/advisories/new). Zgłoszenie widzi tylko
autor; e-maila nie podajemy. Opisz, co i jak da się wykorzystać, w której wersji, oraz — jeśli to możliwe — jak to
odtworzyć. Odpowiem i wydam poprawkę najszybciej, jak się da.

## Co jest w zakresie

- wyciek albo niebezpieczne przechowywanie **tokenu API Kimai** (w logach, plikach konfiguracyjnych, komunikatach,
  zrzutach, poza magazynem sekretów systemu);
- wysyłanie danych gdziekolwiek poza adres Kimai podany przez użytkownika;
- obejście sprawdzania certyfikatu serwera albo wysyłanie tokenu na niewłaściwy adres;
- podatności w paczce Flatpak, repozytorium Flatpak (podpis GPG) i workflowach CI tego repozytorium.

Poza zakresem: błędy samego Kimai (zgłoś je [projektowi Kimai](https://github.com/kimai/kimai/security)), problemy
wymagające już przejętego konta użytkownika w systemie.
