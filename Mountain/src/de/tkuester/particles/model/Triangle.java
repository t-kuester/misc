package de.tkuester.particles.model;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Stream;

/**
 * Class representing a fractal triangle, being one side of the mountain.
 *
 * @author tkuester
 */
public class Triangle {

	public final Line ab, bc, ca;
	
	public List<Triangle> children;
	
	public Triangle(Line ab, Line bc, Line ca) {
		this.ab = ab;
		this.bc = bc;
		this.ca = ca;
	}

	public void expand() {
		if (children != null) {
			children.forEach(Triangle::expand);
		} else {
			Stream.of(ab, bc, ca).forEach(Line::split);
			Line a = new Line(ab.left.target, ca.right.source);
			Line b = new Line(bc.left.target, ab.right.source);
			Line c = new Line(ca.left.target, bc.right.source);
			
			children = Arrays.asList(
					new Triangle(a, ca.right, ab.left),
					new Triangle(b, ab.right, bc.left),
					new Triangle(c, bc.right, ca.left),
					new Triangle(c, b, a));
		}
	}

	public Stream<Triangle> getLeafs() {
		if (children == null) {
			return Stream.of(this);
		} else {
			return children.stream().flatMap(Triangle::getLeafs);
		}
	}
	
	@Override
	public String toString() {
		return String.format("Triangle(%s, %s, %s)", ab, bc, ca);
	}

}
