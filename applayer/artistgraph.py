from applayer.graphbase import GraphBase
from applayer.artistlist import ArtistList
from applayer.collaboration import Collaboration
from datalayer.artistnotfound import ArtistNotFound
from datalayer.mongobridge import MongoBridge
from applayer.artist import Artist
from typing import List


class ArtistGraph(GraphBase):

    def __init__(self, artist_list: ArtistList, depth: int) -> None:
        super().__init__()
        self.__artists: List[Artist] = artist_list.artist_objects.copy()
        self.__collaborations: List[Collaboration] = []
        mongodb = MongoBridge("mongodb://localhost:27017/", "BristolData", "Artists")
        visit: List[Artist]
        collab_dep: int = 0

        while collab_dep <= depth:
            for artsy in self.__artists:
                self.add_artist(artsy)

                collab_dep = artsy.level + 1
                if collab_dep <= depth:
                    if artsy.collaborators is not None:
                        for temp in artsy.collaborators:
                            try:
                                mongo = mongodb.get_artist_by_id(temp['collaboratorID'])
                                artist_collab = Artist(mongo)
                                artist_collab.level = collab_dep
                            except ArtistNotFound:
                                artist_collab = Artist(temp["collaboratorID"], temp["collaboratorName"], " ", collab_dep)

                            self.add_artist(artist_collab)
                            self.__artists.append(artist_collab)

                            Collaborator = Collaboration(artsy, artist_collab, temp['roles'])
                            self.add_collaboration(Collaborator)

    def add_collaboration(self, collab: Collaboration) -> None:
        if super().has_edge(collab.artist0, collab.artist1):
            super().incr_edge(collab.artist0, collab.artist1)
        else:
            super().add_edge(collab.artist0, collab.artist1)

    def add_artist(self, artist: Artist) -> None:
        if not super().has_node(artist):
            super().add_node(artist)

    @property
    def artists(self):
        return self.__artists

    @property
    def collaborations(self):
        return self.__collaborations

