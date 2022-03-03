from graph_plotter import graph_plotter
import fire
import glob
import os
from util.gxl_graph import InvalidFileException


def process_folder(gxl_folder, img_folder, output_path, separator='', color_by_feature=None, scaling=1, transparency=125):
    """
    This function draws a graph on an image and saves it for a whole folder.

    :param gxl_folder: folder with the gxl files
    :param img_folder: folder with the corresponding images (they need to have the same file name as the gxl before the 'separator')
    :param output_path: folder where the output is saved to
    :param separator: separator until which the gxl and img files are identical (needed to match the files)
    :param color_by_feature: name of the feature to color the nodes by
    :param scaling: x,y coordinates will be scaled accordingly (in case they are not in pixel)
    :param transparency: transparency of the image
    """
    gxl_files = {os.path.basename(f).split(separator)[0]: f for f in glob.glob(os.path.join(gxl_folder, '*.gxl'))}
    img_files = {os.path.basename(f).split(separator)[0]: f for f in glob.glob(os.path.join(img_folder, '*'))}

    # get the file ids that are present in both
    file_ids = [value for value in gxl_files.keys() if value in img_files.keys()]

    for file_id in file_ids:
        try:
            graph_plotter(gxl_files[file_id], img_files[file_id], output_path, color_by_feature=color_by_feature,
                          scaling=scaling, transparency=transparency)
        except InvalidFileException:
            print(f'Something went wrong with files {gxl_files[file_id]}/{img_files[file_id]}, skipping...')
            continue


if __name__ == '__main__':
    fire.Fire(process_folder)

