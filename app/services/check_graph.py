import pickle
import networkx as nx


print("inside")
with open("user_graph.pkl", "rb") as f:
    G = pickle.load(f)


print("Total users (nodes):", G.number_of_nodes())
print("Total connections (edges):", G.number_of_edges())


print("\nUser IDs in graph:")
for node in list(G.nodes)[:10]:  # limit to first 10
    print("-", node)


print("\nSample connections:")
for u1, u2, data in list(G.edges(data=True))[:10]: 
    print(f"{u1} <--> {u2} | weight = {data['weight']:.2f}")


target_user = list(G.nodes)[0]  # just pick the first user for demo
print(f"\nTop neighbors of {target_user}:")
neighbors = sorted(G[target_user].items(), key=lambda x: x[1]['weight'], reverse=True)
for neighbor, attrs in neighbors[:5]:
    print(f"- {neighbor} (weight = {attrs['weight']:.2f})")