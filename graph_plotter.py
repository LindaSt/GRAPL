import fire
import cv2
from util.drawing_config import bts_graphs as draw_style

from util.gxl_graph import ParsedGxlGraph
from util.draw_graph import GraphDrawer


def graph_plotter(gxl_filepath, img_filepath, output_path, color_by_feature=None, scaling=1, transparency=125):
    graph = ParsedGxlGraph(gxl_filepath, color_by_feature=color_by_feature)
    img = cv2.imread(img_filepath)

    # graph_img = GraphDrawer(graph, img, scaling=scaling, color_by_feature=color_by_feature)
    graph_img = GraphDrawer(graph, img, scaling=scaling, color_by_feature=color_by_feature,
                            node_style=draw_style['node_style'], edge_style=draw_style['edge_style'],
                            transparency=transparency)
    graph_img.save(output_path)


if __name__ == '__main__':
    fire.Fire(graph_plotter)

