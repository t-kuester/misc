package de.tkuester.particles.model;

import java.util.List;
import java.util.stream.Stream;

/**
 * Class representing the multi-sided mountain.
 *
 * @author tkuester
 */
public class Mountain {

	public final List<Triangle> sides;
	
	public Mountain(List<Triangle> sides) {
		this.sides = sides;
	}
	
	public Stream<Triangle> getAllTriangles() {
		return sides.stream().flatMap(Triangle::getLeafs);
	}
	
	public void expandAll() {
		sides.forEach(Triangle::expand);
	}
	
}
