from api import get_friends
from igraph import Graph, plot
import igraph


def get_network(users_ids, as_edgelist=True):
    list_name = []

    def id_fr(n):
        list_fr1 = get_friends(n, 'id')
        list_id1 = []
        for friend1 in list_fr1:
            list_id1.append(int(friend1['id']))
        return list_id1

    list_fr = get_friends(users_ids, 'id')
    list_id = []
    print(list_fr)
    for friend in list_fr:
        k = friend['first_name'] + ' ' + friend['last_name']
        list_name.append(k)
        list_id.append(int(friend['id']))
    edges = []
    for i in list_id:
        try:
            list_fr_fr = id_fr(i)
            print(i, list_fr_fr)
            if set(list_id) & set(list_fr_fr):
                u = set(list_id) & set(list_fr_fr)
                for j in u:
                    l = []
                    l.append(list_id.index(i))
                    l.append(list_id.index(j))
                    edges.append((tuple(l)))
        except:
            pass
    graph = [edges] + [list_name]
    return graph


def plot_graph(graph):
    list_name = graph[1]
    edges = graph[0]
    vertices = [i for i in list_name]
    g = Graph(vertex_attrs={"label": vertices},
              edges=edges, directed=False)
    N = len(vertices)
    visual_style = {
        "vertex_size": 20,
        "bbox": (2000, 2000),
        "margin": 100,
        "vertex_label_dist": 1.6,
        "edge_color": "gray",
        "autocurve": True,
        "layout": g.layout_fruchterman_reingold(
            maxiter=100000,
            area=N ** 2,
            repulserad=N ** 2)
    }
    g.simplify(multiple=True, loops=True)
    clusters = g.community_multilevel()
    pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    g.vs['color'] = pal.get_many(clusters.membership)
    plot(g, **visual_style)
