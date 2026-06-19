from predict_tab1 import predict_velocity

result = predict_velocity(

    calibre="40mm",

    projectile_type="Type A",

    projectile_dimension=40,

    dai=2,

    projectile_mass=120,

    total_mass_with_sabbot=150,

    petal_burst_pressure=12,

    powder_mass=50,

    shape="Conical",

    s_type="Standard",

    breadth=10,

    height=20,

    material="Steel",

    c_drag=0.4,

    surface_area=150,

    volume=100,

    sa_vol=1.5,

    density=7.8,

    moment_of_inerta=45,

    cd=0.4,

    sabo_length=30

)

print(result)