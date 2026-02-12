import rebound

def simulate():
    solar = rebound.Simulation()
    solar.integrator = "whfast"
    solar.G = 6.67443e-11
    solar.dt = 0.1
    solar.ri_whfast.corrector = 17
    solar.ri_whfast.safe_mode = 0

    sun = rebound.Particle()
    sun.mass = 1.9891e30
    sun.position = [0, 0, 0]
    sun.velocity = [0, 0, 0]
    sun.radius = 6.957e+8
    solar.particles = [sun]


