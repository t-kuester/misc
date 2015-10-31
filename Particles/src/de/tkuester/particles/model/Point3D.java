package de.tkuester.particles.model;

import java.util.Locale;

/**
 * Wrapper class for coordinates of a 3D point.
 * 
 * Also provides some helper functions for adding points etc.,
 * but using those means creating thousands and millions of new
 * points each time when calculating a new state.
 *
 * @author tkuester
 */
public class Point3D {

	/** total number of points created; for debugging */
	public static int count = 0;
	
	/** X, Y and Z coordinates of the point */
	public double x, y, z;
	
	/**
	 * Create new 3D point
	 * 
	 * @param x		X coordinate
	 * @param y		Y coordinate
	 * @param z		Z coordinate
	 */
	public Point3D(double x, double y, double z) {
		this.x = x;
		this.y = y;
		this.z = z;
		count++;
	}
	
	@Override
	public String toString() {
		return String.format(Locale.ENGLISH, "(%.2f, %.2f, %.2f)", this.x, this.y, this.z);
	}
	
	/*
	 * HELPER METHODS
	 */
	
	public Point3D add(Point3D other) {
		return new Point3D(this.x + other.x, this.y + other.y, this.z + other.z);
	}
	
	public Point3D diff(Point3D other) {
		return new Point3D(other.x - this.x, other.y - this.y, other.z - this.z);
	}
	
	public Point3D mult(double factor) {
		return new Point3D(this.x * factor, this.y * factor, this.z * factor);
	}
	
	public Point3D div(double divisor) {
		return new Point3D(this.x / divisor, this.y / divisor, this.z / divisor);
	}

	public double distance(Point3D other) {
		return Math.sqrt(Math.pow(this.x - other.x, 2)
				       + Math.pow(this.y - other.y, 2)
				       + Math.pow(this.z - other.z, 2));
	}
	
	public double absolute() {
		return Math.sqrt(x*x + y*y + z*z);
	}
	
	public Point3D norm() {
		return this.div(this.absolute());
	}
	
}
