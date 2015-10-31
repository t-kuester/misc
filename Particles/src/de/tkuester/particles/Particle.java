package de.tkuester.particles;

/**
 * Class encapsulating all the attributes of a single particle in the 
 * universe. Not much OOP here, all computations are done centrally in 
 * the universe class.
 *
 * @author tkuester
 */
public class Particle {

	/** current position of the particle, relative to center */
//	double posX = 0, posY = 0, posZ = 0;
	Point3D pos = new Point3D(0, 0, 0);
	
	/** current speed of particle, as movement per time step */
//	double speedX = 0, speedY = 0, speedZ = 0;
	Point3D speed = new Point3D(0, 0, 0);
	
	/** size of the particle, with mass ~= size^3 */
	double size = 0;
	
	double getMass() {
		return Math.pow(this.size, 3);
	}
	
}
