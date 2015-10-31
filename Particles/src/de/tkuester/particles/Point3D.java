package de.tkuester.particles;

public class Point3D {

	public static int count = 0;
	
	public double x, y, z;
	
	public Point3D(double x, double y, double z) {
		this.x = x;
		this.y = y;
		this.z = z;
		count++;
	}
	
//	public Point3D add(Point3D other) {
//		return new Point3D(this.x + other.x, this.y + other.y, this.z + other.z);
//	}
//	
//	public Point3D diff(Point3D other) {
//		return new Point3D(other.x - this.x, other.y - this.y, other.z - this.z);
//	}
//	
//	public Point3D mult(double factor) {
//		return new Point3D(this.x * factor, this.y * factor, this.z * factor);
//	}
//	
//	public Point3D div(double divisor) {
//		return new Point3D(this.x / divisor, this.y / divisor, this.z / divisor);
//	}
//
//	public double distance(Point3D other) {
//		return Math.sqrt(Math.pow(this.x - other.x, 2)
//				       + Math.pow(this.y - other.y, 2)
//				       + Math.pow(this.z - other.z, 2));
//	}
//	
//	public double absolute() {
//		return Math.sqrt(x*x + y*y + z*z);
//	}
//	
//	public Point3D norm() {
//		return this.div(this.absolute());
//	}
	
}
