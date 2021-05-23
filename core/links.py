# Links and Link functions

links = []


def add_links():
   links = []
   # supplements
   with open('src/links/supplements.txt', 'r') as f:
      for line in f:
         links.append(line.strip())
   return links
