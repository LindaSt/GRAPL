from util.gxl_graph import ParsedGxlGraph
import fire
import cv2
import os


class GraphDrawer:
    def __init__(self, graph, img, node_style=None, edge_style=None) -> object:
        self.graph = graph
        self.img = img

        self.id = graph.file_id

        self.node_style = node_style
        self.edge_style = edge_style

    @property
    def node_style(self):
        return self._node_config

    @node_style.setter
    def node_style(self, node_config):
        default = {'color': (0, 0, 255), 'radius': 3, 'thickness': -1}  # red
        if node_config is None:
            node_config = default
        elif len(node_config) != default:
            for k, v in default.items():
                if k not in node_config:
                    node_config[k] = v

        self._node_config = node_config

    @property
    def edge_style(self):
        return self._edge_config

    @edge_style.setter
    def edge_style(self, edge_config):
        default = {'color': (0, 255, 0), 'thickness': 2, 'lineType': cv2.LINE_AA}  #
        if edge_config is None:
            edge_config = default
        elif len(edge_config) != default:
            for k, v in default.items():
                if k not in edge_config:
                    edge_config[k] = v

        self._edge_config = edge_config

    def get_image(self):
        img = self.img
        points = {i: tuple([int(x_y[0]), int(x_y[1])]) for i, x_y in enumerate(self.graph.node_positions)}
        # draw the points
        for index, point in points.items():
            img = cv2.circle(img, point, radius=self.node_style['radius'], color=self.node_style['color'],
                             thickness=self.node_style['thickness'])

        # draw the edges
        for edge in self.graph.edges:
            pt1, pt2 = (points[edge[0]], points[edge[1]])
            img = cv2.line(img, pt1, pt2, color=self.edge_style['color'], thickness=self.edge_style['thickness'],
                           lineType=self.edge_style['lineType'])

        return img

    def save(self, output_path):
        cv2.imwrite(os.path.join(output_path, self.id + ".png"), self.get_image())


def graph_plotter(gxl_filepath, img_filepath, output_path):
    graph = ParsedGxlGraph(gxl_filepath)
    img = cv2.imread(img_filepath)

    graph_img = GraphDrawer(graph, img)
    graph_img.save(output_path)

if __name__ == '__main__':
    fire.Fire(graph_plotter)

