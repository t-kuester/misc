package de.tkuester.space3d.mountain.model;

import java.util.Random;

/**
 * Class representing a Line, making up one of the sides of a Triangle.
 *
 * @author tkuester
 */
public class Line {

	private static final Random RANDOM = new Random();

	public static double FACTOR = 0.07;


	public final Point3D source, target;
	
	public Line left, right;
	
	public Line(Point3D source, Point3D target) {
		this.source = source;
		this.target = target;
	}

	public void split() {
		if (left == null && right == null) {
			Point3D midpoint = source.add(target).div(2);
			
			// randomization
			double magnitude = FACTOR * source.distance(target);
			midpoint = new Point3D(
					midpoint.x + RANDOM.nextGaussian() * magnitude,
					midpoint.y + RANDOM.nextGaussian() * magnitude,
					midpoint.z + RANDOM.nextGaussian() * magnitude);
			
			this.left = new Line(source, midpoint);
			this.right = new Line(midpoint, target);
		}
	}

	@Override
	public String toString() {
		return String.format("Line(%s, %s)", source, target);
	}

	
	/**
	 * Inverse of a line; reference to original Line and segments,
	 * but with order reversed. Needed for odd-sided mountains.
	 *
	 * @author tkuester
	 */
	public static class Inverse extends Line {

		private final Line line;

		public Inverse(Line line) {
			super(line.target, line.source);
			this.line = line;
		}

		@Override
		public void split() {
			if (this.left == null && this.right == null) {
				this.line.split();
				this.left = new Inverse(line.right);
				this.right = new Inverse(line.left);
			}
		}
	}
}
