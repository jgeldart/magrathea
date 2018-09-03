from quantity_field import ureg

# Set up some celestial units

ureg.define('solar_mass = 1988500000000000000000000000000 * kg = M☉')
ureg.define('solar_luminosity = 382800000000000000000000000 * watt = L☉')
ureg.define('solar_radius = 695700 * km = R☉')
ureg.define('solar_surface_temperature = 5772 * K = T☉')
ureg.define('solar_lifetime = 10000000000*year')

ureg.define('earth_mass = 5972370000000000000000000 * kilogram = M⊕')
ureg.define('earth_radius = 6371 * km = R⊕')
ureg.define('earth_density = 5.514 * g/cm**3 = ρ⊕')
ureg.define('earth_gravity = 9.807 * m/s**2 = g⊕')
ureg.define('earth_escape_velocity = 11.186*km/s')
ureg.define('earth_insolation = 1366*watt/m**2 = Q⊕')

ureg.define('jovian_mass = 317.8 * earth_mass = M♃')
ureg.define('jovian_radius = 69911 * km = R♃')
ureg.define('jovian_density = 1326 * kg/m**3 = ρ♃')
ureg.define('jovian_gravity = 24.79 * m/s**2 = g♃')
