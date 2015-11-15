package de.tkuester.particles;

import java.util.Arrays;

import de.tkuester.particles.model.Particle;
import de.tkuester.particles.model.Point3D;
import de.tkuester.particles.model.Universe;

public class SolarSystem {

	public static void main(String[] args) {

		// sun: 1.98855×10^30 kg, 1.408 g/cm³
		Particle sun = createSatellite(1.98855e30, 1.408, 0, 0, 0, null);
		
		// earth: 149598023 km; 29.78 km/s; 5.97237×10^24 kg, 5.514 g/cm³
		Particle earth = createSatellite(5.97237e24, 5.514, 149598023., 29.78, 0, sun);
		
		// moon: 384399 km; 1.022 km/s; 27.321582 d; 7.3477×10^22 kg, 3.3464 g/cm³
		Particle moon = createSatellite(7.3477e22, 3.3464, 384399., 1.022, 0, earth);
		
		// create Universe with G = 6.674×10^-11 N⋅m2/kg2
		Universe universe = new Universe();
		universe.G = 6.674e-11;
		universe.particles.addAll(Arrays.asList(sun, earth, moon));
		RunUniverse.runUniverseFrame(universe, 600, 100, true);
	}
	
	/**
	 * Create new particle orbiting a center at a given radius and speed, 
	 * starting at some angle and having a given mass. All movement happens 
	 * in a plane. Angle is in degrees; if a negative number is given, the 
	 * angle is random.
	 * 
	 * @param mass		mass of the particle, in kg
	 * @param density	density of the particle, in g/cm^3
	 * @param radius	radius of the orbit, in km
	 * @param speed		orbital speed, in km/s
	 * @param angle		starting angle, from 0 to 360, or -1 for random
	 * @param centre	particle being the center of the orbit
	 * @return			the new particle/satellite
	 */
	protected static Particle createSatellite(double mass, double density, double radius, double speed, double angle, Particle centre) {
		Particle satellite = new Particle();
		
		// TODO use angle
		Point3D posRel = new Point3D(radius, 0, 0);
		Point3D spdRel = new Point3D(0, speed, 0);
		
		if (centre != null) {
			posRel = centre.pos.add(posRel);
			spdRel = centre.speed.add(spdRel);
		}
		
		satellite.pos = posRel;
		satellite.speed = spdRel;
		satellite.density = density * Math.pow(100_000, 3) / 1000;
		satellite.setMass(mass);
		
		return satellite;
	}
	
}
