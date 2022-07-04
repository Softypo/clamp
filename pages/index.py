from dash import html
import dash
import dash_vtk
import pyvista as pv
from pyvista import examples
from dash_vtk.utils import to_mesh_state, to_volume_state
import vtk

dash.register_page(__name__, path="/", title="DV Dashboard")


reader = pv.get_reader("C:\.repos\clamp\data\liner_hanger_final.ply")
mesh = reader.read()

# filename = examples.download_lobster(load=False)
# filename.split("/")[-1]  # omit the path
# 'lobster.ply'
# reader = pv.get_reader(filename)
# mesh = reader.read()
# mesh.plot()
mesh_state = to_mesh_state(mesh)


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


layout = html.Div(
    style={"width": "100%", "height": "calc(100vh - 3rem)"},
    children=dash_vtk.View([
        dash_vtk.GeometryRepresentation([
            # dash_vtk.Algorithm(
            #     vtkClass="vtkConeSource",
            #     state={"resolution": 64, "capping": False},
            # )
            # dash_vtk.Reader(
            #     vtkClass="vtkPLYReader",
            #     url="C:\\Users\\Softypo\\Downloads\\dv_tool_15200ft_final.ply",
            #     renderOnUpdate=True,
            # ),
            # dash_vtk.PolyData(
            #     polys=mesh_state,
            # ),
            dash_vtk.Mesh(state=mesh_state),
        ],
            actor={"material": {"ambient": 0.5, "diffuse": 0.5,
                                "specular": 0.5}},
        ),
    ],
        cameraPosition=[1, 1, 2],
        background=[0.152, 0.168, 0.188]
    ),
)
