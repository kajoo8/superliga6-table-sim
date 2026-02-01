from bs4 import BeautifulSoup

with open("Terminarz_ Wszystkie zespoły _ Zima 2026 - 1. Liga Biznes.html", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

matches = []
current_round = None

for el in soup.find_all(["h4", "tr"]):
    # wykrywanie kolejki
    if el.name == "h4" and "Kolejka" in el.text:
        current_round = int(el.text.replace("Kolejka", "").strip())

    # mecze
    if el.name == "tr" and el.get("class") and "sectiontableentry" in el["class"][0]:
        teams = el.find_all("td", class_="resultsrow_teamname")
        if len(teams) == 2 and current_round >= 4:
            team1 = teams[0].get_text(strip=True)
            team2 = teams[1].get_text(strip=True)
            matches.append((team1, team2))

print(matches)
