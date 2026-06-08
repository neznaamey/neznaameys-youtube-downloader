🛠 Jak zprovoznit Nez's YouTube Downloader (Krok za krokem)

Aby ti aplikace šlapala jako hodinky a stahovala v 4K kvalitě, musíš dodržet tyto tři fáze:
Fáze 1: Příprava prostředí

    Python: Pokud ho ještě nemáš, stáhni a nainstaluj si ho z python.org. Při instalaci zaškrtni políčko "Add Python to PATH" – to je kriticky důležité!

    Stažení kódu: Stáhni si můj repozitář jako ZIP a rozbal si ho do libovolné složky.

    Instalace knihoven: - Otevři složku s projektem.

        Klikni do adresního řádku průzkumníka (tam nahoře, kde je cesta), napiš cmd a potvrď Enterem.

        Do černého okna, co se otevře, vlož: pip install -r requirements.txt a počkej, až se to nainstaluje.

Fáze 2: FFmpeg (Tvoje "vstupenka" do 4K)

yt-dlp potřebuje FFmpeg na to, aby spojil video a audio do jednoho kvalitního souboru.

    Stáhni si FFmpeg z ffmpeg.org.

    Rozbal ZIP soubor.

    Složku bin (ve které je soubor ffmpeg.exe) si přesuň přímo do C:\ tak, aby cesta vypadala přesně takto: C:\ffmpeg\bin.

    Hotovo. Moje aplikace je naprogramovaná tak, aby si ho přesně tady našla.

Fáze 3: Spuštění

    Najdi soubor YoutubeDownloader.pyw.

    Dvojklikni na něj.

    Žádné černé okno, žádné chyby – jen čisté, zelené GUI, kde vložíš link, vybereš kvalitu, složku a stahuješ.

Proč to takhle děláme?

    Proč .pyw? Protože nechceme, aby na tebe při každém kliknutí vyskakovalo černé "DOSové" okno.

    Proč C:\ffmpeg\bin? Aby ses nemusel hrabat v systémových proměnných Windows (což je pro většinu lidí noční můra). Takhle to máme pod kontrolou my.

    Proč requirements.txt? Protože je to profi standard. Každý, kdo někdy dělal v Pythonu, ví, že tohle je první věc, kterou má hledat.
