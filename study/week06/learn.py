class Речник(dict):
  име = 'речник'
  def __getitem__(self, name):
    return "Не знам, брат. Ти си знаеш!"
  def __setitem__(self, indx, val):
    super().__setitem__(indx, val)

речник = Речник()
речник['име'] = 'стойност'
print(речник.__dict__) # ?
print(речник['име']) # ?