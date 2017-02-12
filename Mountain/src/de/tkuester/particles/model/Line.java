package de.tkuester.particles.model;

/**
 * Class representing a Line, making up one of the sides of a Triangle.
 *
 * @author tkuester
 */
public class Line {

	public final Point3D source, target;
	
	public Line left, right;
	
	public Line(Point3D source, Point3D target) {
		this.source = source;
		this.target = target;
	}

	public void split() {
		if (left == null && right == null) {
			Point3D midpoint = source.add(target).div(2);
			
			// TODO randomization
//			double length = source.distance(target);
//			p = complex(random.gauss(midpoint.real, length * FACTOR),
//            random.gauss(midpoint.imag, length * FACTOR))
			
			this.left = new Line(source, midpoint);
			this.right = new Line(midpoint, target);
		}
	}
	
}
