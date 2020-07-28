import networkx as nx
import json

errorfile = open("erroring.log", "w")

def work(G, str):
    character = {}
    tempdict = nx.degree_centrality(G)
    errorfile.write("degree " + str + "\n")
    errorfile.flush()
    for key in tempdict.keys():
        character[key] = {}
        character[key]["degree_centrality"] = tempdict[key]
    errorfile.write("done\n")
    errorfile.flush()
    print("here")
    json.dump(character, open(str + "_Parameter.json", "w"))
    # character = json.load(open("General Health\\" + str + "_Parameter.json", "r"))

    errorfile.write("betweenness " + str + "\n")
    errorfile.flush()
    tempdict = nx.betweenness_centrality(G)
    for key in tempdict.keys():
        character[key]["betweenness_centrality"] = tempdict[key]
    errorfile.write("done\n")
    errorfile.flush()
    json.dump(character, open(str + "_Parameter.json", "w"))

    errorfile.write("eigenvector " + str+ "\n")
    errorfile.flush()
    tempdict = nx.eigenvector_centrality(G)
    for key in tempdict.keys():
        character[key]["eigenvector_centrality"] = tempdict[key]
    errorfile.write("done\n")
    errorfile.flush()
    json.dump(character, open(str + "_Parameter.json", "w"))

    errorfile.write("closeness " + str + "\n")
    errorfile.flush()
    tempdict = nx.closeness_centrality(G)
    for key in tempdict.keys():
        character[key]["closeness_centrality"] = tempdict[key]
    errorfile.write("done\n")
    errorfile.flush()
    json.dump(character, open(str + "_Parameter.json", "w"))

    errorfile.write("load " + str + "\n")
    errorfile.flush()
    tempdict = nx.load_centrality(G)
    for key in tempdict.keys():
        character[key]["load_centrality"] = tempdict[key]
    errorfile.write("done\n")
    errorfile.flush()
    json.dump(character, open(str + "_Parameter.json", "w"))

    try:
        errorfile.write("harmonic " + str + "\n")
        errorfile.flush()
        tempdict = nx.harmonic_centrality(G)
        for key in tempdict.keys():
            character[key]["harmonic_centrality"] = tempdict[key]
        errorfile.write("done\n")
        errorfile.flush()
        json.dump(character, open(str + "_Parameter.json", "w"))
    except:
        errorfile.write("harmonic bad\n")

    # print("constraint " + str)
    # tempdict = nx.algorithms.structuralholes.constraint(G)
    # for key in tempdict.keys():
    #     character[key]["constraint"] = tempdict[key]
    # print("done")
    # json.dump(character, open(str + "_Parameter.json", "w"))
    #
    # print("effectivesize " + str)
    # tempdict = nx.algorithms.structuralholes.effective_size(G)
    # for key in tempdict.keys():
    #     character[key]["effective_size"] = tempdict[key]
    # print("done")
    # json.dump(character, open(str + "_Parameter.json", "w"))

    errorfile.write("pagerank " + str + "\n")
    errorfile.flush()
    tempdict = nx.pagerank(G)
    for key in tempdict.keys():
        character[key]["pagerank"] = tempdict[key]
    errorfile.write("done\n")
    errorfile.flush()
    json.dump(character, open(str + "_Parameter.json", "w"))


if __name__ == "__main__":
    # G = nx.read_gml("friend_net.gml")
    # work(G, "Friend")
    G = nx.read_gml("commenter_net.gml")
    work(G, "Commenter")
    G = nx.read_gml("node_net.gml")
    work(G, "Notes")
    # print(nx.degree_centrality(Gf))

