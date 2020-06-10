import os
import xml.etree.ElementTree as ET
import sys


class InvalidFileException(Exception):
    pass


class ParsedGxlGraph:
    def __init__(self, path_to_gxl, color_by_feature=None) -> object:
        """
        This class contains all the information encoded in a single gxl file = one graph
        Parameters
        ----------
        path_to_gxl: str
            path to the gxl file
        """
        self.filepath = path_to_gxl
        self.filename = os.path.basename(self.filepath)
        # this is the node feature we want to color by later
        self.color_by_feature = color_by_feature
        # initiate the list (will be set by setup_graph())
        self.color_by_features = None
        # name of the gxl file (without the ending)
        self.file_id = self.filename[:-4]

        # parsing the gxl
        # sets up the following properties: node_features, node_feature_names, edges, edge_features, edge_feature_names,
        # node_position, graph_id, edge_ids_present and edgemode
        self.setup_graph()

    @property
    def filepath(self) -> str:
        return self._filepath

    @filepath.setter
    def filepath(self, path_to_gxl):
        if not os.path.isfile(path_to_gxl):
            print(f'File {path_to_gxl} does not exist.')
            sys.exit(-1)
        self._filepath = path_to_gxl

    @property
    def nb_of_nodes(self):
        return len(self.node_features)

    @property
    def nb_of_edges(self):
        return len(self.edge_features)

    def setup_graph(self):
        """
        Parses the gxl file and sets the following graph properties
        - graph info: graph_id, edge_ids_present and edgemode
        - node: node_features, node_feature_names, and node_position
        - edge: edges, edge_features and edge_feature_names

        """
        tree = ET.parse(self.filepath)
        root = tree.getroot()

        # verify that the file contains the expected attributes (node, edge, id, edgeids and edgemode)
        self.sanity_check(root)

        self.edges = self.get_edges(root)  # [[int, int]]
        self.node_feature_names, self.node_features = self.get_features(root, 'node')  # ([str], list)

        # Add the coordinates to their own variable
        if self.node_feature_names is None or 'x' not in self.node_feature_names and 'y' not in self.node_feature_names:
            print('Graph does not contain x or y coordinates as features. '
                  'Coordinates have to be specified in the gxl file as "x" and "y".')

        x_ind = self.node_feature_names.index('x')
        y_ind = self.node_feature_names.index('y')

        self.node_positions = [[node[x_ind], node[y_ind]] for node in self.node_features]
        if self.color_by_feature:
            self.color_by_features = [node[self.node_feature_names.index(self.color_by_feature)] for node in self.node_features]

    def get_features(self, root, mode):
        """
        get a list of the node features out of the element tree (gxl)

        Parameters
        ----------
        root: gxl element
        mode: str
            either 'edge' or 'node'

        Returns
        -------
        tuple ([str], [mixed values]])
            list of all node features for that tree
            ([feature name 1, feature name 2, ...],  [[feature 1 of node 1, feature 2 of node 1, ...], [feature 1 of node 2, ...], ...])
        """
        features_info = [[feature for feature in graph_element] for graph_element in root.iter(mode)]
        if len(features_info) > 0:
            feature_names = [i.attrib['name'] for i in features_info[0]]
        else:
            feature_names = []

        # check if we have features to generate
        if len(feature_names) > 0:
            features = [[self.decode_feature(value) for feature in graph_element for value in feature if feature.attrib['name'] in feature_names] for graph_element in root.iter(mode)]
        else:
            feature_names = None
            features = []

        return feature_names, features

    def sanity_check(self, root):
        """
        Check if files contain the expected content

        Parameters
        ----------
        root:

        Returns
        -------
        None
        """
        # check if node, edge, edgeid, edgemode, edgemode keyword exists
        if len([i.attrib for i in root.iter('graph')][0]) != 3:
            raise InvalidFileException

        if len([node for node in root.iter('node')]) == 0:
            print(f'File {os.path.basename(self.filepath)} is an empty graph!')
            raise InvalidFileException
        elif len([edge for edge in root.iter('edge')]) == 0:
            print(f'File {os.path.basename(self.filepath)} has no edges!')

    @staticmethod
    def get_edges(root) -> list:
        """
        Get the start and end points of every edge and store them in a list of lists (from the element tree, gxl)
        Parameters
        ----------
        root: gxl element

        Returns
        -------
        [[int, int]]
            list of indices of connected nodes
        """
        edge_list = []

        start_points = [int(edge.attrib["from"].replace('_', '')) for edge in root.iter('edge')]
        end_points = [int(edge.attrib["to"].replace('_', '')) for edge in root.iter('edge')]
        assert len(start_points) == len(end_points)

        # move enumeration start to 0 if necessary
        if len(start_points) > 0 and len(end_points) > 0:
            if min(min(start_points, end_points)) > 0:
                shift = min(min(start_points, end_points))
                start_points = [x - shift for x in start_points]
                end_points = [x - shift for x in end_points]

            edge_list = [[start_points[i], end_points[i]] for i in range(len(start_points))]

        return edge_list

    @staticmethod
    def decode_feature(f) -> str:
        data_types = {'string': str,
                      'float': float,
                      'int': int}

        # convert the feature value to the correct data type as specified in the gxl
        return data_types[f.tag](f.text.strip())