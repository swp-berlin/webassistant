**List with Links and Documents** ist ähnlich zu **List with Links**. Auch hier zeigt eine Hauptseite eine (optional paginierte) Liste von Teasern für einzelne Beiträge. Jeder der Teaser linkt auf eine eigene Seite auf der eigentliche Beitrag im Detail zu finden ist. Zusätzlich enthält aber jeder Beitrag ein PDF Dokument.

Haupt-Element des Scrapers ist der *List Resolver*. Hier sind drei Elemente zu konfigurieren:

* Der **Listenselektor** selektiert das Element welches die Liste der Teaser enthält.
* Der **Einzelselektor** selektiert einen einzelnen Teaser innerhalb des Listenselektors. Alle Selektoren der Kind-Resolver arbeiten auf diesem Element.
* Der **Paginierungsselektor** selektiert ein Element (Button oder Link) auf der Startseite über welches die nächste Seite der Liste abgerufen werden kann. Diese Angabe ist optional. Bleibt der Selektor leer wird nur eine Seite abgerufen
* Die **Maximale Seitenanzahl** bestimmt wieviele Seiten über die Paginierung abgerufen werden sollen. Der Wert sollte mit der Veröffentlichungsfrequenz der gescrapten Seite und dem eingestellten Abrufintervall so gewählt werden, dass neue Beiträge auf jeden Fall erfasst werden, aber nicht zu viele unnötige Seiten abgerufen werden.

Das wichtigste Kind des *List Resolvers* ist der **Link Resolver**. Der hier eingestellte Selektor selektiert den Link innerhalb es Teasers. Der Scraper folgt diesem Link. Alle Kind-Elemente des List Resolvers werden auf diese Folgeseite angewandt.

Ein Kind des *Link Resolvers* ist der **Document Resolver**. Dessen Selektor findet das Element welches den Download des PDF Dokuments anstößt. Alle im PDF vorhandenen Daten werden automatisch extrahiert.

Für gewöhnlich werden die meisten benötigten Felder auf dieser Folgeseite als Kind des *Link Resolvers* extrahiert. Es ist aber auch möglich weitere Felder direkt aus der Liste als Kind des *List Resolvers* zu extrahieren. 
