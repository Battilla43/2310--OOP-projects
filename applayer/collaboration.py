from typing import List
from applayer.artist import Artist

class Collaboration(object):

    def __init__(self, art0: Artist, art1: Artist, role: List[str]):

         self.__artist0: Artist = art0
         self.__artist1: Artist = art1
         self.__roles: List[str] = role
    @property
    def artist0(self) -> Artist:
        return self.__artist0

    @property
    def artist1(self) -> Artist:
        return self.__artist1

    @property
    def roles(self) -> List[str]:
        return self.__roles
