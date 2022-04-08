# GRAPL
GRAPL is an easy to use tool for drawing graphs onto images.

It uses the following command line parameters with `graph_plotter.py`. To process a whole folder, you can use `process_folder.py` with the same command line arguments, except `--gxl-filepath`
needs to be changed to `--gxl-folder` and `--img-filepath` to `--img-folder`. The files need to have matching names
before the specified identifier.

- `--gxl-filepath`: Path to the gxl file (graphs need to have at least the x and y coordinates as node features).
- `--img-filepath`: Path to the image, that the graphs should be drawn on
- `--output-path`: Path to where the visualisation should be saved (the output name will be {input-img-name}-vis.png).
- `--scaling`: Optional. Factor by which the x and y coordinates should be multiplied. (e.g. ` --scaling 4.118660172440437` when working with images from the BTS project)
- `--color-by-feature`: Optional. Name of the node feature, by which the nodes should be colored.
- `--transparency`: Optional. Value of the alpha channel for the image (0-255). Default is 125.

Only for `process_folder.py`:
- `--separator`: Default `_`. Anything before that is used to match the files. (E.g. 123_hotspot.png with 123_graph.gxl)

There are default color, thickness, and point/line types implemented, but configurations can be manually
specified too. Just add your profile to the `drawing_config.py`, and change the `import`
as well as the parameters passed to `GraphDrawer()` in `graph_plotter.py`.

You can set up the conda environment by running `conda env create -f environment.yml` in this directory.