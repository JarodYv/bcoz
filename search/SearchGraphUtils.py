from data.IKnowledge import IKnowledge
from data.Knowledge import Knowledge
from graph.Graph import Graph
from graph.Node import Node
from graph.EdgeListGraph import EdgeListGraph
from search.MeekRules import MeekRules
from typing import List, Optional


class SearchGraphUtils:
    """
    Graph utilities for search algorithm. Lots of orientation method, for instance.
    """

    @classmethod
    def pc_orient_bk(cls, bk: IKnowledge, graph: Graph, nodes: List[Node]):
        """
        Orients according to background knowledge.
        :return:
        """
        for edge in bk.forbidden_edges_iterator():
            # match strings to variables in the graph.
            from_node = cls.translate(edge.get_from(), nodes)
            to_node = cls.translate(edge.get_to(), nodes)

            if not from_node or not to_node:
                continue

            if not graph.get_edge(from_node, to_node):
                continue

            # Orient to-->from
            graph.remove_connecting_edge(from_node, to_node)
            graph.add_directed_edge(to_node, from_node)

        for edge in bk.required_edges_iterator():
            from_node = cls.translate(edge.get_from(), nodes)
            to_node = cls.translate(edge.get_to(), nodes)

            if not from_node or not to_node:
                continue

            if not graph.get_edge(from_node, to_node):
                continue

            # Orient from-->to
            graph.remove_connecting_edge(from_node, to_node)
            graph.add_directed_edge(from_node, to_node)

    @classmethod
    def translate(cls, name: str, nodes: List[Node]) -> Optional[Node]:
        """ Return the string in node list which matches string in background knowledge.

        :param name:
        :param nodes:
        :return:
        """
        for node in nodes:
            if node.get_name() == name:
                return node
        return None

    @classmethod
    def pattern_for_dag(cls, dag: Graph, knowledge: IKnowledge = None) -> Graph:
        if not knowledge:
            knowledge = Knowledge()
        pattern = EdgeListGraph(dag)
        rules = MeekRules()
        rules.set_knowledge(knowledge)
        rules.set_revert_to_unshielded_colliders(True)
        rules.orient_implied(pattern)
        return pattern
