import requests
from bs4 import BeautifulSoup

# In the final 'entry' of data (a dict), we need the following information:
#     name (str)
#     dex number (int)
#     first dex entry listed (str)
#     gen (int)
#     type(s) (list of strings with one item if single-type and two items if dual-type)
#     species (str)
#     height (int)
#     weight (int)
#     base stats (list; [HP, Attack, Defense, Sp. Atk, Sp. Def, Speed, Total])
#     evolutions (dict; {(int)level: (str)name} for each evolution)

# defining the final dict to contain all the data
finalData = {"name": '', "dex": 0, "entry": '', "gen": 0, "types": [], "species": '', "height": 0, "weight": 0, "base_stats": [0, 0, 0, 0, 0, 0, 0], "evos": {}}

# grab the url of the page
URL = "https://pokemondb.net/pokedex/bulbasaur"
page = requests.get(URL)

# set up the parser
soup = BeautifulSoup(page.content, "html.parser")

# separate out the header and footer (yes i know i could have done them in the same line but i wanted some semblance of readability)
soup = BeautifulSoup(''.join(str(child) for child in soup.find(class_="main-content grid-container").children), "html.parser")

# easiest first, grab the name, dex number, dex entry, and gen
finalData["name"] = str(soup.find("h1").text).lower()   # lowercase just so we don't have to worry about uppercase stuff later
finalData["dex"] = int(soup.find("td").text)
finalData["gen"] = int(''.join(i for i in soup.find("abbr").text if i.isdigit()))
finalData["entry"] = str(soup.findAll("td", class_="cell-med-text")[0].text)

# now to get the types, which are <a> tags of class "type-icon type-{type}" with the text of the type, but thankfully they're in a fixed spot wrapped in a <td> tag
types = []
tempSoup = BeautifulSoup(''.join(str(child) for child in soup.findAll("td")[1]), "html.parser")
for tag in tempSoup.findAll("a", class_="type-icon"):
  types.append(tag.text.lower())

# species isn't too hard either, it's just the third <td> tag on the page
finalData["species"] = str(soup.findAll("td")[2].text).lower()
