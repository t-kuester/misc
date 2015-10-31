package de.tkuester.particles;

/**
 * Class for doing performance benchmarks.
 *
 * @author tkuester
 */
public class Benchmark {

	public static void main(String[] args) {
		
		Universe universe = new Universe();
		universe.initialize(200);
		
		long startTime = System.currentTimeMillis();
		for (int i = 0; i < 1000; i++) {
			if (i % 100 == 0) {
				System.out.println("iter " + i);
			}
			universe.update();
		}
		long endTime = System.currentTimeMillis();
		System.out.println("time " + (endTime - startTime));

		System.out.println("points " + Point3D.count);
		
		/*
		 * all runs are "warmed-up"
		 * 200 particles, 1000 iterations
		 * without Point class: ~1500ms+-300ms
		 * Point just as wrapper: about the same
		 */
	}
	
}
