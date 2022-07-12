from dash import html
import dash
import dash_vtk
import pyvista as pv
#from pyvista import examples
from dash_vtk.utils import to_mesh_state, to_volume_state
from numpy import amin, amax
#import vtk
from vtk.util.numpy_support import vtk_to_numpy

dash.register_page(__name__, path="/", title="DV Dashboard")


# reader = pv.get_reader("data\liner_hanger_final.ply")
# mesh = reader.read()

# filename = examples.download_lobster(load=False)
# filename.split("/")[-1]  # omit the path
# 'lobster.ply'
# reader = pv.get_reader(filename)
# mesh = reader.read()
# mesh.plot()
# mesh_state = to_mesh_state(mesh)


# reader = vtk.vtkPLYReader()
# reader.SetFileName("data\liner_hanger_final.ply")
# reader.Update()

# polyDataMapper = vtk.vtkPolyDataMapper()
# polyDataMapper.SetInputConnection(reader.GetOutputPort())
# polyDataMapper.ScalarVisibilityOn()
# polyDataMapper.Update()

# actor = vtk.vtkActor()
# actor.SetMapper(polyDataMapper)
# actor.GetProperty().SetOpacity(1.0)
# actor.Modified()

# mesh.plot()

def vtk_ply(filepath):
    reader = pv.get_reader(filepath)
    mesh = reader.read()
    # mesh_state = to_mesh_state(mesh)
    # points = mesh_state['mesh']['points']
    # polys = mesh_state['mesh']['polys']
    polydata = mesh.extract_geometry()
    points = polydata.points.ravel()
    polys = vtk_to_numpy(polydata.GetPolys().GetData())
    texture = [rgba[0] for rgba in polydata['RGBA']]
    #texture = polydata['RGBA']
    min_texture = amin(texture)
    max_texture = amax(texture)
    return [points, polys, texture, [min_texture, max_texture]]


points, polys, texture, color_range = vtk_ply("data\liner_hanger_final.ply")


layout = html.Div(
    style={"width": "100%", "height": "calc(100vh - 3rem)"},
    children=dash_vtk.View(
        id="vtk-view",
        pickingModes=["hover"],
        children=[
            dash_vtk.GeometryRepresentation(
                id="vtk-representation",
                children=[
                    dash_vtk.PolyData(
                        id="vtk-polydata",
                        points=points,
                        polys=polys,
                        children=[
                            dash_vtk.PointData(
                                [
                                    dash_vtk.DataArray(
                                        id="vtk-array",
                                        registration="setScalars",
                                        numberOfComponents=1,
                                        name='onPoints',
                                        values=texture,
                                    )
                                ]
                            )
                        ],
                    )
                ],
                colorMapPreset="Yellow 15",
                colorDataRange=color_range,
                property={"edgeVisibility": False},
                showCubeAxes=False,
                cubeAxesStyle={"axisLabels": ["", "", "Depth"]},
            ),
            # dash_vtk.GeometryRepresentation(
            #     id="pick-rep",
            #     actor={"visibility": False},
            #     children=[
            #         dash_vtk.Algorithm(
            #             id="pick-sphere",
            #             vtkClass="vtkSphereSource",
            #             state={"radius": 100},
            #         )
            #     ],
            # ),
        ],
        cameraPosition=[1, 1, 1],
        background=[0, 0, 0, 0],
    )
)
