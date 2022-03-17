view = pdk.ViewState(
    **{"latitude": 48.3794, "longitude": 31.1656, "zoom": 5, "pitch": 45}
)

polygon_layer = pdk.Layer(
    "GeoJsonLayer",
    data=gdf_plot.__geo_interface__,
    opacity=0.8,
    stroked=False,
    filled=True,
    extruded=True,
    wireframe=True,
    get_elevation="properties.count",
    elevation_scale=300,
    get_fill_color="properties.color",
    get_line_color=[0, 0, 0],
    auto_highlight=True,
    pickable=True,
)

pdk.Deck(
    [polygon_layer],
    initial_view_state=view,
    map_style=pdk.map_styles.LIGHT,
)
