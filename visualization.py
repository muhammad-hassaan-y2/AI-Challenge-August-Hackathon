
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def fmt(value, decimals=2):
    return f"{value:.{decimals}f}"


def create_motion_html(result):
    mass = result["mass"]
    force = result["applied_force"]
    friction = result["friction"]
    velocity = result["final_velocity"]

    return f"""
    <div style="
        padding: 20px;
        border-radius: 16px;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        margin-bottom: 15px;
    ">

        <h3 style="margin-top:0;">Interactive Motion Visualization</h3>

        <div style="
            position: relative;
            height: 150px;
            background: #e2e8f0;
            border-radius: 12px;
            overflow: hidden;
        ">

            <div style="
                position:absolute;
                left:40%;
                top:55px;
                width:90px;
                height:55px;
                background:#2563eb;
                border-radius:10px;
                display:flex;
                align-items:center;
                justify-content:center;
                color:white;
                font-weight:bold;
            ">
                {mass:.1f} kg
            </div>

            <div style="
                position:absolute;
                left:15%;
                top:20px;
                font-weight:bold;
            ">
                → Applied Force: {force:.1f} N
            </div>

            <div style="
                position:absolute;
                left:15%;
                bottom:15px;
                font-weight:bold;
            ">
                ← Friction: {friction:.2f} N
            </div>

        </div>

        <div style="
            display:flex;
            gap:20px;
            margin-top:15px;
            flex-wrap:wrap;
        ">

            <div>
                <b>Acceleration</b><br>
                {result["acceleration"]:.2f} m/s²
            </div>

            <div>
                <b>Final Velocity</b><br>
                {velocity:.2f} m/s
            </div>

            <div>
                <b>Distance</b><br>
                {result["distance"]:.2f} m
            </div>

        </div>

    </div>
    """


def create_graph(result):

    time = result["time"]
    position = result["position"]
    velocity = result["velocity"]

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(
            x=time,
            y=position,
            name="Position",
            mode="lines"
        ),
        secondary_y=False
    )

    fig.add_trace(
        go.Scatter(
            x=time,
            y=velocity,
            name="Velocity",
            mode="lines"
        ),
        secondary_y=True
    )

    fig.update_layout(
        title="Motion Over Time",
        height=400,
        margin=dict(l=40, r=40, t=60, b=40)
    )

    fig.update_xaxes(title_text="Time (s)")
    fig.update_yaxes(title_text="Position (m)", secondary_y=False)
    fig.update_yaxes(title_text="Velocity (m/s)", secondary_y=True)

    return fig


def create_dashboard(result):

    return f"""
### Physics Dashboard

| Quantity | Value |
|---|---:|
| Applied Force | **{result["applied_force"]:.2f} N** |
| Friction Force | **{result["friction"]:.2f} N** |
| Net Force | **{result["net_force"]:.2f} N** |
| Mass | **{result["mass"]:.2f} kg** |
| Acceleration | **{result["acceleration"]:.2f} m/s²** |
| Initial Velocity | **{result["initial_velocity"]:.2f} m/s** |
| Final Velocity | **{result["final_velocity"]:.2f} m/s** |
| Distance Travelled | **{result["distance"]:.2f} m** |

**Equations**

- Friction: `F₍friction₎ = μmg`
- Net Force: `F₍net₎ = F₍applied₎ - F₍friction₎`
- Acceleration: `a = F₍net₎ / m`
- Velocity: `v = u + at`
- Position: `x = ut + ½at²`
"""
