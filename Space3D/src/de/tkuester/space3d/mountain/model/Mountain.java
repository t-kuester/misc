package de.tkuester.space3d.mountain.model;

import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.IntStream;
import java.util.stream.Stream;

import de.tkuester.space3d.Point3D;

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
	
	@Override
	public String toString() {
		return String.format("Mountain(%s)", sides);
	}

	/**
	 * Create regular mountain with given number of sides. This is a bit
	 * simplified, creating each side with one inverted line, thus creating
	 * some unnecessary objects, but making the creation much simpler.
	 *
	 * @param height	height of the mountain
	 * @param radius	radius of the mountain
	 * @param sides		number of sides/ridges
	 * @return			new mountain according to parameters
	 */
	public static Mountain createMountain(double height, double radius, int sides) {

		// create top point and list of base points
		Point3D top = new Point3D(0, 0, -height);
		List<Point3D> points = IntStream.range(0, sides)
				.mapToDouble(n -> n * 2 * Math.PI / sides)
				.mapToObj(a -> new Point3D(radius * Math.sin(a), radius * Math.cos(a), 0))
				.collect(Collectors.toList());

		// create the ridges
		List<Line> lines = IntStream.range(0, sides)
				.mapToObj(n -> new Line(top, points.get(n)))
				.collect(Collectors.toList());

		// create sides, including base lines and inverted ridge
		List<Triangle> triangles = IntStream.range(0, sides)
				.mapToObj(n -> new Triangle(
						lines.get(n),
						new Line(points.get(n), points.get((n + 1) % sides)),
						new Line.Inverse(lines.get((n + 1) % sides))
						)).collect(Collectors.toList());

		return new Mountain(triangles);
	}

}
