import fire
import cv2
import os

from util.drawing_config import edgeless_graphs as draw_style
from util.gxl_graph import ParsedGxlGraph
from util.draw_graph import GraphDrawer


def graph_plotter(gxl_filepath, img_filepath, output_path, color_by_feature=None, scaling=1, transparency=125):
    """
    This function draws a graph on an image and saves it.

    :param gxl_filepath: path to the gxl file with the graph
    :param img_filepath: path to the corresponding image file
    :param output_path: folder where the overlayed imaged is saved to
    :param color_by_feature: name of the feature the nodes should be colored by
    :param scaling: x,y coordinates will be scaled accordingly (in case they are not in pixel)
    :param transparency: transparency of the image
    """
    if not os.path.isdir(output_path):
        os.makedirs(output_path, exist_ok=True)

    graph = ParsedGxlGraph(gxl_filepath, color_by_feature=color_by_feature)
    img = cv2.imread(img_filepath)

    # graph_img = GraphDrawer(graph, img, scaling=scaling, color_by_feature=color_by_feature)
    graph_img = GraphDrawer(graph, img, scaling=scaling, color_by_feature=color_by_feature,
                            node_style=draw_style['node_style'], edge_style=draw_style['edge_style'],
                            transparency=transparency)
    graph_img.save(output_path)


if __name__ == '__main__':
    fire.Fire(graph_plotter)

