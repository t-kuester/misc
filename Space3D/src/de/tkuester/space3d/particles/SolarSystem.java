package de.tkuester.space3d.particles;

import java.util.Arrays;

import de.tkuester.space3d.particles.model.Particle;
import de.tkuester.space3d.particles.model.Point3D;
import de.tkuester.space3d.particles.model.Universe;

/**
 * Solar system simulation. The goal of this class is to simulate the
 * mayor bodies in the solar system, both as a test for the physics in
 * this simulation, and because awesome.
 * 
 * The numbers are taken from Wikipedia, but its not working correctly
 * yet, probably a problem with making all the units fit with each other.
 *
 * @author tkuester
 */
public class SolarSystem {

	public static void main(String[] args) {

		// sun: 1.98855×10^30 kg, 1.408 g/cm³
		Particle sun = createSatellite(1.98855e30, 1.408, 0, 0, 0, null);
		
		// earth: 149598023 km; 29.78 km/s; 5.97237×10^24 kg, 5.514 g/cm³
		Particle earth = createSatellite(5.97237e24, 5.514, 149598023., 29.78, 0, sun);
//		Particle earth = createSatellite(5.97237e24, 5.514, 0, 0, 0, null);
		
		// moon: 384399 km; 1.022 km/s; 27.321582 d; 7.3477×10^22 kg, 3.3464 g/cm³
		Particle moon = createSatellite(7.3477e22, 3.3464, 384399., 1.022, 0, earth);
		
		// create Universe with G = 6.674×10^-11 N⋅m^2/kg^2
		Universe universe = new Universe();
		universe.G = 6.674e-11 * Math.pow(1000, -2); // km^2 instead of m^2
		universe.particles.addAll(Arrays.asList(sun, earth, moon));
		RunUniverse.runUniverseFrame(universe, 600, 10, 10, true);
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
		Point3D posRel = new Point3D(0, radius, 0);
		Point3D spdRel = new Point3D(speed, 0, 0);
		
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
