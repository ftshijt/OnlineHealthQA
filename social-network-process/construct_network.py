import json
import traceback
import os
import networkx as nx

if __name__ == "__main__":
    Gf = nx.Graph()
    Gc = nx.DiGraph()
    Gn = nx.DiGraph()
    for root, dirs, files in os.walk("C:\\Users\\嘉彤\\Desktop\\project\\online health\\url_list\\General Health\\PEOPLE"):
        for file in files:
            target = open(os.path.join(root, file), "r")
            people = json.load(target)
            node = file[:-4]
            print(node)
            Gf.add_node(node)
            Gc.add_node(node)
            Gn.add_node(node)
            try:
                for notes_leaver in people['note_leavers']:
                    if Gn.has_edge(notes_leaver, node):
                        Gn[notes_leaver][node]['weight'] += 1
                    else:
                        Gn.add_edge(notes_leaver, node, weight = 1)

                for commenter in people['commenters']:
                    if Gc.has_edge(commenter, node):
                        Gc[commenter][node]['weight'] += 1
                    else:
                        Gc.add_edge(commenter, node, weight = 1)

                for friend in people['friends']:
                    if Gf.has_edge(node, friend):
                        continue
                    else:
                        Gf.add_edge(node, friend, weight = 1)
            except:
                traceback.print_exc()

    nx.write_gml(Gf, "friend_net.gml")
    nx.write_gml(Gc, "node_net.gml")
    nx.write_gml(Gn, "commenter_net.gml")

