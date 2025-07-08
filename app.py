#GRAFICOS CON EL EXCEL 
# GRAFICOS CON EL EXCEL 
import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# Cargar los datos de Excel
Dataf = pd.read_excel('datos_estudiantes_limpio.xlsx')
print(Dataf)
#inicializar la app
app = dash.Dash(__name__)
#Definir el servidor en render
server = app.server
app.tittle='Esistica notas'

# Inicialización de la app
Estanotas = dash.Dash(__name__, title='Estadística de Notas')

# Crear layout
Estanotas.layout = html.Div([
    html.H1("Tablero de notas de estudiantes", style={
        'textAlign': "center",
        'color': "blue",
        'padding': "20px",
        'fontFamily': "Arial",
        'backgroundColor': "white"
    }),
    # Aquí puedes seguir añadiendo más componentes como dropdowns, gráficos, etc.


# Crear la barra para la selección de materias 
    html.Label("Seleccionar una materia: ", style={"margin": "10px"}),

    dcc.Dropdown(
        id="filtro_materia",
        options=[{"label": carrera, "value": carrera} for carrera in sorted(Dataf["Carrera"].unique())],
        value=Dataf["Carrera"].unique()[0],
        style={"width": "100%", "margin": "auto"}
        ),

     html.Br(),

# Crear los Tabs
       dcc.Tabs([
           dcc.Tab(label='Gráfico de promedios', children=[
           dcc.Graph(id='histograma')
           ]),
           dcc.Tab(label="Edad vs Promedio", children=[
           dcc.Graph(id='dispersion')
          ]),
         dcc.Tab(label="Desempeño", children=[
          dcc.Graph(id='pie')
         ]),
         dcc.Tab(label="Promedio de notas x carrera", children=[
           dcc.Graph(id='barra')
         ]),
         ], style={"fontWeight": "bold", "color": "#2c3e50"}),
])
# Callback
@Estanotas.callback(
    Output("histograma", "figure"),
    Output("dispersion", "figure"),
    Output("pie", "figure"),
    Output("barra", "figure"),
    Input("filtro_materia", "value")
)
def actualizar(filtro_materia):
    filtro = Dataf[Dataf["Carrera"] == filtro_materia]

    # Histograma
    histo = px.histogram(
        filtro, 
        x="Promedio", 
        nbins=10,
        title=f"Distribución de promedios - {filtro_materia}",
        color_discrete_sequence=["#3498db"]
    ).update_layout(
        template="plotly_white", 
        yaxis_title="Cantidad de estudiantes"
    )

    # Dispersión
    disper = px.scatter(
        filtro, 
        x="Edad", 
        y="Promedio", 
        color="Desempeño", 
        title=f"Edad vs Promedio - {filtro_materia}",
        color_discrete_sequence=px.colors.qualitative.Set2
    ).update_layout(template="presentation")

    # Pie
    pi = px.pie(
        filtro, 
        names="Desempeño", 
        values="Promedio",
        title=f"Desempeño - {filtro_materia}",
        color_discrete_sequence=px.colors.qualitative.Pastel
    ).update_layout(template="plotly_dark")

    # Barras
    promedios = filtro.groupby("Carrera")["Promedio"].mean().reset_index()
    barr = px.bar(
        promedios, 
        x="Carrera", 
        y="Promedio", 
        title="Promedio de notas por carrera",
        color="Carrera",
        color_discrete_sequence=px.colors.qualitative.Prism
    ).update_layout(template="ggplot2")

    return histo, disper, pi, barr

# Ejecutar la aplicación
if __name__ == '__main__':
    Estanotas.run(debug=True)