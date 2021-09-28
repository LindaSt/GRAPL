from graph_plotter import graph_plotter
import fire
import glob
import os

def process_folder(gxl_folder, img_folder, output_path, separator='_', color_by_feature=None, scaling=1, transparency=125):
    gxl_files = {os.path.basename(f).split(separator)[0]: f for f in glob.glob(os.path.join(gxl_folder, '*.gxl'))}
    img_files = {os.path.basename(f).split(separator)[0]: f for f in glob.glob(os.path.join(img_folder, '*'))}

    # get the file ids that are present in both
    file_ids = [value for value in gxl_files.keys() if value in img_files.keys()]

    for file_id in file_ids:
        graph_plotter(gxl_files[file_id], img_files[file_id], output_path, color_by_feature=color_by_feature, scaling=scaling, transparency=transparency)


if __name__ == '__main__':
    fire.Fire(process_folder)

