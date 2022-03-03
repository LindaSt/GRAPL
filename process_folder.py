from graph_plotter import graph_plotter
import fire
import glob
import os
from util.gxl_graph import InvalidFileException
from multiprocessing import Process
import numpy as np
import re


def process_chunk(self, chunk):
    for c in chunk:
        output_folder_path, wsi_path, coord_path = tuple(c)
        self.process_file(output_folder_path, wsi_path, coord_path)


class ProcessFolder:
    def __init__(self, gxl_folder, img_folder, output_path, separator='', color_by_feature=None, scaling=1,
                       transparency=125, n_threads: int = 6, no_multi_thread: bool = False):
        """
        This function draws a graph on an image and saves it for a whole folder.

        :param gxl_folder: folder with the gxl files
        :param img_folder: folder with the corresponding images (they need to have the same file name as the gxl before the 'separator')
        :param output_path: folder where the output is saved to
        :param separator: separator until which the gxl and img files are identical (needed to match the files)
        :param color_by_feature: name of the feature to color the nodes by
        :param scaling: x,y coordinates will be scaled accordingly (in case they are not in pixel)
        :param transparency: transparency of the image
        :param n_threads: number of threads for multi-run (optional, default is 6)
        :param no_multi_thread: set to True if program should not run in multi-processing mode (optional, default is False)
        """
        self.output_path = output_path
        self.color_by_feature = color_by_feature
        self.scaling = scaling
        self.transparency = transparency
        self.n_threads = n_threads
        self.no_multi_thread = no_multi_thread

        regex = repr(f'(.*)_({separator})')[1:-1]

        self.gxl_files = {os.path.basename(re.search(regex, f).group(1)): f for f in glob.glob(os.path.join(gxl_folder, '*.gxl'))}
        self.img_files = {os.path.basename(re.search(regex, f).group(1)): f for f in glob.glob(os.path.join(img_folder, '*'))}

        # get the file ids that are present in both
        self.file_ids = [value for value in self.gxl_files.keys() if value in self.img_files.keys()]

    def main(self):
        if self.no_multi_thread:
            for file_id in self.file_ids:
                self.process_files(file_id)
        else:
            # process the files with coordinates
            chunks = np.array_split(self.file_ids, self.n_threads)
            prcs = []
            for c in chunks:
                p = Process(target=self.process_chunk, args=(c,))
                p.start()
                prcs.append(p)
            [pr.join() for pr in prcs]

    def process_chunk(self, chunk):
        for file_id in chunk:
            self.process_files(file_id)

    def process_files(self, file_id):
        try:
            graph_plotter(self.gxl_files[file_id], self.img_files[file_id], self.output_path,
                          color_by_feature=self.color_by_feature,
                          scaling=self.scaling, transparency=self.transparency)
        except InvalidFileException:
            print(
                f'Something went wrong with files {self.gxl_files[file_id]}/{self.img_files[file_id]}, skipping...')
            return


if __name__ == '__main__':
    fire.Fire(ProcessFolder).main()

