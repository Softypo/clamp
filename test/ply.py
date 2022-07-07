
import pyvista as pv
from dash_vtk.utils import to_mesh_state, to_volume_state

reader = pv.get_reader("data\liner_hanger_final.ply")
mesh = reader.read()

# filename = examples.download_lobster(load=False)
# filename.split("/")[-1]  # omit the path
# 'lobster.ply'
# reader = pv.get_reader(filename)
# mesh = reader.read()
# mesh.plot()
mesh_state = to_mesh_state(mesh)
mesh.plot()


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
