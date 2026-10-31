# Sturmhilfe: Arbeitsregeln

## Artefakte bei jeder Änderung mit aktualisieren
Die App liegt in `index.html` und zusätzlich als drei veröffentlichte Claude-Artefakte. Bei jeder inhaltlichen Änderung an der App gehören diese mit aktualisiert (nicht nur das Repo):

1. **Live** („Sturmhilfe“): https://claude.ai/artifact/BK9juka3x6QWJ6d9vBQa9C, die echte App mit Notion, Konto-Speicher und Nutzer.
2. **Demo** („Sturmhilfe Demo“): https://claude.ai/artifact/MrDH5sW6kko1S7Ckprn9cx, gleiche App, aber nur im Arbeitsspeicher (`MEM`), ohne `claude.use`, mit DEMO-Banner und fest eingetragenen Lügen in `DB.lies`. Neue Lügen dort ebenfalls in die Liste aufnehmen.
3. **Wireframe** („Sturmhilfe Ablauf“, `wireframe.html`): https://claude.ai/artifact/MzYLzTBh1xeSq29yG9z5gG, wenn sich Screens, Reihenfolge oder Texte des Ablaufs ändern. Die Seite lädt gespeicherte Abläufe aus der Artefakt-Datenbank (`flow/main`); nur `defaults()` zu ändern reicht nicht, auch das gespeicherte Dokument muss angepasst werden (mit `ArtifactData`, `if_version` beachten).

Vorgehen: Artefakt mit `Artifact read` lesen, die gleichen Änderungen auf die gespeicherte Datei anwenden (Live und Demo unterscheiden sich von `index.html` nur im Wrapper, bei Demo zusätzlich in den Stellen mit `MEM`, `if (false)` und der Lügenliste), Syntax mit `node --check` prüfen und unter derselben URL veröffentlichen.

## GitHub Pages
Die GitHub Page (`https://lightcatcher-77.github.io/sturmhilfe/`) muss aktuell nicht aktualisiert werden. Kein Merge nach `main`, kein Pull Request und kein Hinweis darauf nötig, nur wenn ausdrücklich verlangt. Maßgeblich sind zurzeit die Artefakte; `index.html` im Repo wird trotzdem mitgepflegt.

## Lügen und Wahrheiten
- Lügen kommen aus der Notion-Datenbank „Gedanken-Statistik“ (Spalte `Gedanke`), die Wahrheit steht in der Spalte `Wahrheit`.
- Fallback sind die Texte in `LIE_TRUTHS` in `index.html`. Neue Lüge: in Notion anlegen, `LIE_TRUTHS` ergänzen und im Demo-Artefakt in `DB.lies` aufnehmen.
- Abschlussbildschirme: `S.end` (ausgehalten) und `S.fallend` (Rückfall) zeigen die gewählten Lügen mit Wahrheit.
- Neue Lügen: Im Live-Artefakt erzeugt Claude (Fähigkeit `sample`) automatisch eine Wahrheit. `sample` muss bei jedem Publish in `capabilities` mit angegeben werden, zusammen mit `db`, `user` und `mcp` (Notion), sonst wird es entfernt. Die Wahrheit ist bearbeitbar und wird mit der Lüge in Notion ergänzt (Spalte `Wahrheit`). Im Demo-Artefakt gibt es das nicht.
