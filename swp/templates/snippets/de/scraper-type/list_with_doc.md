**List with Documents** deckt typische Publikationslisten wie sie häufig bei wissenschaftlichen Instituten zu finden sind. Gescraped wird hier eine einzelne Seite auf welcher ein Liste von PDF Dokumenten verlinkt sind.

Haupt-Element des Scrapers ist der *List Resolver*. Hier sind drei Elemente zu konfigurieren:

* Der **Listenselektor** selektiert das Element welches die Liste der Dokumente enthält.
* Der **Einzelselektor** selektiert ein einzelnes Element der Liste innerhalb des Listenselektors. Alle Selektoren der Kind-Resolver arbeiten auf diesem Element.
* Der **Paginierungsselektor** selektiert ein Element (Button oder Link) auf der Startseite über welches die nächste Seite der Liste abgerufen werden kann. Diese Angabe ist optional. Bleibt der Selektor leer wird nur eine Seite abgerufen. Für gewöhnlich haben Publikationslisten keine Paginierung.
* Die **Maximale Seitenanzahl** bestimmt wieviele Seiten über die Paginierung abgerufen werden sollen. Der Wert sollte mit der Veröffentlichungsfrequenz der gescrapten Seite und dem eingestellten Abrufintervall so gewählt werden, dass neue Beiträge auf jeden Fall erfasst werden, aber nicht zu viele unnötige Seiten abgerufen werden.

Wichtigstes Element des *List Resolvers* ist der **Document Resolver**. Dessen Selektor findet das Element welches den Download des PDF Dokuments anstößt.

Alle im PDF vorhandenen Daten werden automatisch extrahiert. Zusätzlich können über weitere Kind-Resolver des *List Resolvers** weitere Daten extrahiert werden.
