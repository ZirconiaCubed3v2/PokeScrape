import requests
from bs4 import BeautifulSoup

# In the final 'entry' of data (a dict), we need the following information:
#     name (str)
#     dex number (int)
#     first dex entry listed (str)
#     gen (int)
#     type(s) (list<str>; one item if single-type and two items if dual-type)
#     species (str)
#     height (float)
#     weight (float)
#     base stats (dict; keys: ["hp", "atk", "def", "spa", "spd", "spd", "tot"])
#     evolutions (dict; {(int)order: [(str)name, (int)dexnum, (str)method]} for each evolution)

# defining the final dict to contain all the data
finalData = {"name": '',
             "dex": 0,
             "entry": '',
             "gen": 0,
             "types": [],
             "species": '',
             "height": 0,
             "weight": 0,
             "base_stats": {"hp": 0, "atk": 0, "def": 0, "spa": 0, "sde": 0, "spd": 0, "tot": 0},
             "evos": {}}

# grab the url of the page
URL = "https://pokemondb.net/pokedex/flabebe"
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
tempSoup = BeautifulSoup(''.join(str(child) for child in soup.findAll("td")[1]), "html.parser")
for tag in tempSoup.findAll("a", class_="type-icon"):
  finalData["types"].append(tag.text.lower())

# species isn't too hard either, it's just the third <td> tag on the page
finalData["species"] = str(soup.findAll("td")[2].text).lower()

# height and weight are going to be kept in metric measurements just to keep things simple
finalData["height"] = float(soup.findAll("td")[3].text.split(" ", 1)[0][:-2])
finalData["weight"] = float(soup.findAll("td")[4].text.split(" ", 1)[0][:-3])

# base stats are in a table, not too hard to extract, just a lot of code repeating, but constructing a loop would take longer than just writing the code multiple times
entries = BeautifulSoup(''.join(str(child) for child in soup.find("div", class_="grid-col span-md-12 span-lg-8")), "html.parser").findAll("tr")    # get all the table entries into a list
for entry in entries:
  tempSoup = BeautifulSoup(str(entry), "html.parser")
  val = tempSoup.findAll("td", class_="cell-num")[0].text
  match ((tempSoup.findAll("th")[0].text).lower()):    # before this project, i was completely unaware that python had switch-case structures now
    case "hp":
      finalData["base_stats"]["hp"] = val
    case "attack":
      finalData["base_stats"]["atk"] = val
    case "defense":
      finalData["base_stats"]["def"] = val
    case "sp. atk":
      finalData["base_stats"]["spa"] = val
    case "sp. def":
      finalData["base_stats"]["sde"] = val
    case "speed":
      finalData["base_stats"]["spd"] = val
    case "total":
      finalData["base_stats"]["tot"] = val

# evolutions are to be fairly hard, because they're kinda buried under other tags and stuff, and the levels are in seperate card divs
evos = {}
cards = soup.findAll("div", class_="infocard")
arrows = soup.findAll("span", class_="infocard infocard-arrow")
counter = 1
for card in cards[1:]:
  tempSoup = BeautifulSoup(''.join(str(child) for child in card), "html.parser")
  evos[counter] = {"name": str(tempSoup.find("a", class_="ent-name").text.lower()),
               "num": int(tempSoup.find("small").text.lower()[1:]),
               "mtd": ''
              }
  mtd = BeautifulSoup(''.join(str(child) for child in arrows[cards.index(card)-1]), "html.parser").find("small").text.lower().split(" ", 1)[1][:-1]
  try:
    int(mtd)
    evos[counter]["mtd"] = "lvl" + str(mtd)
  except Exception:
    evos[counter]["mtd"] = str(mtd).replace(" ", "")
  counter += 1
finalData["evos"] = evos

print(finalData)
