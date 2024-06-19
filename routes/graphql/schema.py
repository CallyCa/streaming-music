import graphene
from routes.graphql.queries.user_queries import UserQueries
from routes.graphql.queries.song_queries import SongQueries
from routes.graphql.queries.playlist_queries import PlaylistQueries
from routes.graphql.mutations.user_mutations import UserMutations
from routes.graphql.mutations.song_mutations import SongMutations
from routes.graphql.mutations.playlist_mutations import PlaylistMutations
from routes.graphql.mutations.auth_mutations import AuthMutations

class Query(UserQueries, SongQueries, PlaylistQueries, graphene.ObjectType):
    pass

class Mutation(UserMutations, SongMutations, PlaylistMutations, AuthMutations, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
