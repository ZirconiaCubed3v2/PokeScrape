class PokemonNotFoundError(Exception):
  "Raised when the requested pokemon was not found"
  def __init__(self, pokemon, message="Pokemon '%s' was not found"):
    self.message = message
    self.pokemon = pokemon
    super().__init__(self.message % str(self.pokemon))
