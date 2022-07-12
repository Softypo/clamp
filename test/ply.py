from dash import html
import dash
import dash_vtk
import pyvista as pv
#from pyvista import examples
from dash_vtk.utils import to_mesh_state, to_volume_state
from numpy import amin, amax
#import vtk
from vtk.util.numpy_support import vtk_to_numpy


reader = pv.get_reader("data\liner_hanger_final.ply")
mesh = reader.read()

# filename = examples.download_lobster(load=False)
# filename.split("/")[-1]  # omit the path
# 'lobster.ply'
# reader = pv.get_reader(filename)
# mesh = reader.read()
# mesh.plot()
mesh_state = to_mesh_state(mesh)
mesh.plot(rgb=True)


def vtk_ply(filepath):
    reader = pv.get_reader(filepath)
    mesh = reader.read()
    # mesh_state = to_mesh_state(mesh)
    # points = mesh_state['mesh']['points']
    # polys = mesh_state['mesh']['polys']
    polydata = mesh.extract_geometry()
    points = polydata.points.ravel()
    polys = vtk_to_numpy(polydata.GetPolys().GetData())
    #texture = [rgba[0] for rgba in polydata['RGB']]
    texture = polydata['RGB']
    min_texture = amin(texture)
    max_texture = amax(texture)
    return [points, polys, texture, [min_texture, max_texture]]


points, polys, texture, color_range = vtk_ply("data\liner_hanger_final.ply")

mesh.plot(color=True)

# reader = vtk.vtkPLYReader()
# reader.SetFileName("C:\\Users\\Softypo\\Downloads\\dv_tool_15200ft_final.ply")

# polyDataMapper = vtk.vtkPolyDataMapper()
# polyDataMapper.SetInputConnection(reader.GetOutputPort())
# polyDataMapper.ScalarVisibilityOn()
# polyDataMapper.Update()

# actor = vtk.vtkActor()
# actor.SetMapper(polyDataMapper)
# actor.GetProperty().SetOpacity(1.0)
# actor.Modified()
