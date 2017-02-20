package de.tkuester.space3d.particles.model;

import de.tkuester.space3d.Point3D;

/**
 * Class encapsulating all the attributes of a single particle in the 
 * universe. Not much OOP here, all computations are done centrally in 
 * the universe class.
 *
 * @author tkuester
 */
public class Particle {

	/** current position of the particle, relative to center */
	public Point3D pos = new Point3D(0, 0, 0);
	
	/** current speed of particle, as movement per time step */
	public Point3D speed = new Point3D(0, 0, 0);
	
	/** size of the particle */
	public double size = 0;
	
	/** density of the particle */
	public double density = 1;
	
	/**
	 * @return	the mass, being size^3
	 */
	public double getMass() {
		return Math.pow(this.size, 3) * this.density;
	}
	
	/**
	 * @param mass	mass of the particle, determining its size
	 */
	public void setMass(double mass) {
		this.size = Math.pow(mass / this.density, 1/3.);
	}
	
}
