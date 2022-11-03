import json
from xml.etree.ElementTree import Element, SubElement, tostring
import xml.etree.ElementTree
from xml.dom import minidom


class Book():
  
    title: str
    author: str

    def __init__(self,title: str, author: str ):

        if type(title) != str:
            raise TypeError("title must be str")

        if type(author) != str:
            raise TypeError("author must be str")

        self.title = title
        self.author = author
        self.rating = None
        self.reviews = dict()


class Person():
      def __init__(self, name: str, last_name: str, user_ID: int):

        if type(name) != str:
            raise TypeError("name must be str")

        if type(last_name) != str:
            raise TypeError("last_name must str")
          
        if type(user_ID) != int:
            raise TypeError("user_ID must be int")
  
        self.name = name
        self.last_name = last_name
        self.user_ID = user_ID


class Library():
  def __init__(self, library_json_file):
    
    with open(library_json_file) as jsonfile:
      lib = json.load(jsonfile)
      
    lib['Library']['Books'] = [Book(book['title'], book['author']) for book in lib['Library']['Books']] 
    lib['Library']['Readers'] = [Person(person['name'], person['last_name'], int(person['user_ID'])) for person in lib['Library']['Readers']]
    
    self.library_db = lib  # База данных, которая подгружается из файла

  def add_book(self, title, author):
    with open('Library.json') as jsonfile:
        lib = json.load(jsonfile)
      
    if all([book.title != title and book.author != author for book in self.library_db['Library']['Books']]) and \
    all([book['title'] != title and book['author'] != author for book in lib['Library']['Books']]): 
      self.library_db['Library']['Books'].append(Book(title, author))
        
      lib['Library']['Books'].append(Book(title, author).__dict__)

      with open('Library.json', 'w') as jsonfile:
        json.dump(lib, jsonfile, ensure_ascii=False, indent=4)

      et = xml.etree.ElementTree.parse('Library.xml') 
      root = et.getroot() 
      for Books in root.findall('Books'): 
        book = SubElement(Books, 'book_class_object')
        SubElement(book, 'title').text = title
        SubElement(book, 'author').text = author
        
        
        str_root = ''.join([s.strip() for s in tostring(root).decode("utf-8").split('\n')]) 
        xmlstr = minidom.parseString(str_root).toprettyxml() # делаем строку из xml и разделяем пробелами

        with open('Library.xml', 'w') as f:
          f.write(xmlstr)
        
      print('Book added to the Library')
      return 1
    else:
      print('This book already exists, try again')
      return 0

  def add_person(self, name, last_name, user_ID):
    with open('Library.json') as jsonfile:
        lib = json.load(jsonfile)
    
    try:
      int(user_ID)
    except ValueError:
      print('User_ID should be number')
      return 0
      
    if all([person.user_ID != int(user_ID) for person in self.library_db['Library']['Readers']]) and \
    all([person['user_ID'] != int(user_ID) for person in lib['Library']['Readers']]):
      self.library_db['Library']['Readers'].append(Person(name, last_name, int(user_ID)))

      lib['Library']['Readers'].append(Person(name, last_name, int(user_ID)).__dict__)

      with open('Library.json', 'w') as jsonfile:
        json.dump(lib, jsonfile, ensure_ascii=False, indent=4)

      et = xml.etree.ElementTree.parse('Library.xml')
      root = et.getroot()
      for Readers in root.findall('Readers'):
        person = SubElement(Readers, 'person_class_object')
        SubElement(person, 'name').text = name
        SubElement(person, 'last_name').text = last_name
        SubElement(person, 'user_ID').text = str(user_ID)
        
        str_root = ''.join([s.strip() for s in tostring(root).decode("utf-8").split('\n')])
        xmlstr = minidom.parseString(str_root).toprettyxml()

        with open('Library.xml', 'w') as f:
          f.write(xmlstr)
        
      print('Person added to the Library')
      return 1
    else:
      print('This person already exists, try again')
      return 0

  def del_book(self, title):
    with open('Library.json') as jsonfile:
        lib = json.load(jsonfile)

    lib['Library']['Books'] = [book for book in lib['Library']['Books'] if book['title'] != title] 
    self.library_db['Library']['Books'] = [book for book in self.library_db['Library']['Books'] if book.title != title] 

    with open('Library.json', 'w') as jsonfile:
        json.dump(lib, jsonfile, ensure_ascii=False, indent=4)

    et = xml.etree.ElementTree.parse('Library.xml')
    root = et.getroot()
    for parent in root.findall('Books'):
      for book in root.findall('Books/book_class_object'):
        if [child.text == title for child in list(book)][0] == True:
          parent.remove(book)

    str_root = ''.join([s.strip() for s in tostring(root).decode("utf-8").split('\n')])
    xmlstr = minidom.parseString(str_root).toprettyxml()

    with open('Library.xml', 'w') as f:
      f.write(xmlstr)
          
    print('Book has been deleted')

  def del_person(self, user_ID):
    try:
      int(user_ID)
    except ValueError:
      print('User_ID should be number')
      return 0
    
    with open('Library.json') as jsonfile:
        lib = json.load(jsonfile)

    lib['Library']['Readers'] = [person for person in lib['Library']['Readers'] if person['user_ID'] != int(user_ID)]
    self.library_db['Library']['Readers'] = [person for person in self.library_db['Library']['Readers'] if person.user_ID != int(user_ID)]

    with open('Library.json', 'w') as jsonfile:
        json.dump(lib, jsonfile, ensure_ascii=False, indent=4)

    et = xml.etree.ElementTree.parse('Library.xml')
    root = et.getroot()
    for parent in root.findall('Readers'):
      for person in root.findall('Readers/person_class_object'):
        if [child.text == str(user_ID) for child in list(person)][2] == True:
          parent.remove(person)

    str_root = ''.join([s.strip() for s in tostring(root).decode("utf-8").split('\n')])
    xmlstr = minidom.parseString(str_root).toprettyxml()

    with open('Library.xml', 'w') as f:
      f.write(xmlstr)
          
    print('Person has been deleted')

  def find_person(self, user_ID) -> bool:
    try:
      int(user_ID)
    except ValueError:
      print('User_ID should be number')
      return 0
      
    return any([person.user_ID == int(user_ID) for person in self.library_db['Library']['Readers']])

  def find_book(self, title) -> bool:
    return any([book.title == title for book in self.library_db['Library']['Books']])

  def rate_book(self, title, user_ID, rating):
    try:
      int(user_ID)
    except ValueError:
      print('User_ID should be number')
      return 0
      
    try:
      full_name = [person.name + ' ' + person.last_name for person in self.library_db['Library']['Readers'] if person.user_ID == int(user_ID)][0] #проверка наличия человека в файле, далее используется для оценки книг определенным человеком
    except IndexError:
      print('There is no such reader in the Library')
      return 0
      
    for book in self.library_db['Library']['Books']:
      if book.title == title:
        book.reviews[full_name] = int(rating)
        book.rating = sum(book.reviews.values())/len(book.reviews.values()) #считаем средний рейтинг книги 
        print(title + " - " + 'book rated')
        return 1
    print('There is no such book in the Library')
    return 0

  def get_book_rating(self, title):
    for book in self.library_db['Library']['Books']:
      if book.title == title:
        if book.rating is None:
          print("Nobody haven't rated this book yet")
        else:
          print(f"Rating: {book.rating}")
        return 1
    print('There is no such book in the Library')
    return 0
      
#функция записи пользователя в файл:
def create_library():
  lib_dict = {'Library': {'Books' : [], 'Readers': []}}
  root = Element('Library')
  books = SubElement(root, 'Books') 
  readers = SubElement(root, 'Readers')
  
  print('Enter books title and author.\nTo finish entering type STOP.')
  print('-'*55)
  
  while True:
    title = input('Enter book title: ')
    if title == 'STOP': break
    author = input('Enter book author: ')
    if author == 'STOP': break
    print('-'*55)

    if all([book['title'] != title and book['author'] != author for book in lib_dict['Library']['Books']]):
      book = SubElement(books, 'book_class_object')
      lib_dict['Library']['Books'].append(Book(title, author).__dict__) 
      SubElement(book, 'title').text = title
      SubElement(book, 'author').text = author
    else:
      print('This book is already in library')
      print('-'*55)

  print('-'*55)

  print("Enter person's name, last name and user id.\nTo finish entering type STOP.")
  print('-'*55)
  
  while True:
    name = input('Enter person name: ')
    if name == 'STOP': break
    last_name = input('Enter person last name: ')
    if last_name == 'STOP': break
    user_ID = input('Enter person user_ID: ')
    if user_ID == 'STOP': break
    print('-'*55)

    if all([person['user_ID'] != int(user_ID) for person in lib_dict['Library']['Readers']]):
      person = SubElement(readers, 'person_class_object')
      lib_dict['Library']['Readers'].append(Person(name, last_name, int(user_ID)).__dict__)
      
      SubElement(person, 'name').text = name
      SubElement(person, 'last_name').text = last_name
      SubElement(person, 'user_ID').text = user_ID
    else:
      print('User with this ID already exists')
      print('-'*55)

  xmlstr = minidom.parseString(tostring(root)).toprettyxml(indent="   ")#делаем строку из xml и разделяем пробелами

  with open('Library.xml', 'w') as f:
    f.write(xmlstr)

  with open('Library.json', 'w') as jsonfile:
    json.dump(lib_dict, jsonfile, ensure_ascii=False, indent=4)


Action = Library('Library.json')



print("Доступные функции: ",
      "1 - rate_book" , 
      "2 - get_book_rating" ,
      "3 - find_person", 
      "4 - find_book",
      "5 - add_book",
      "6 - add_person",
      "7 - del_book",
      "8 - del_person",
      "9 - exit", sep="\n")

print('-'*55)

while True:
  n = input()
  if n == "1":
    title = input("Enter title: ")
    user_ID = input("Enter user_ID: ")
    rating = input("Enter rating: ")
    Action.rate_book(title, user_ID, rating)
  elif n == "2":
    title = input('Enter title: ')
    Action.get_book_rating(title)
  elif n == "3":
    user_ID = input('Enter user_ID: ')
    print(Action.find_person(user_ID))
  elif n == "4":
    title = input('Enter title: ')
    print(Action.find_book(title))
  elif n == '5':
    title = input('Enter title: ')
    author = input('Enter author: ')
    Action.add_book(title, author)
  elif n == '6':
    name = input('Enter name: ')
    last_name = input('Enter last name: ')
    user_ID = input('Enter user ID: ')
    Action.add_person(name, last_name, user_ID)
  elif n == '7':
    title = input('Enter title: ')
    Action.del_book(title)
  elif n == '8':
    user_ID = input('Enter user ID: ')
    Action.del_person(user_ID)
  elif n == "9":
    break
  else:
    print('-'*55)
    print("Введите число от 1 до 9:")
  print('-'*55)