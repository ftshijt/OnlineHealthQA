import json
import traceback
import networkx as nx

def get_knowledge():
    pass

def main():
    G = nx.Graph()
    file = open("cold-flu\\cold-flu-detail.txt", "r", encoding="utf-8")
    index = {}
    j = 0
    #file_out = open("edge.csv", "w", encoding = "utf-8")

    while 1:
        j = j + 1
        print("okok%d" % j)
        line = file.readline()
        if not line:
            break
        result = json.loads(line)
        # try:
        #     line.strip('\n')
        #     result = json.loads(line)
        #     if result['asker'] not in index.keys():
        #         pass
        #     index[result['asker']] = 0
        # except:
        #     traceback.print_exc()
        if result['answers'] == []:
            G.add_node(result['asker'])
            continue

        for answer in result['answers']:
            try:
                print(result['asker'])
                if G.has_edge(result['asker'], answer):
                    G[result['asker']][answer]['weight'] += 1
                else:
                    G.add_edge(result['asker'], answer, weight=1)
            except:
                traceback.print_exc()

    nx.write_gml(G, "graph_cold-flu.gml")

if __name__=="__main__":
    main()