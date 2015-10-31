package de.tkuester.particles;

/**
 * Class for doing performance benchmarks.
 *
 * @author tkuester
 */
public class Benchmark {

	/*
	 * all runs are "warmed-up"
	 * 200 particles, 1000 iterations
	 * without Point class: ~1500ms+-300ms
	 * Point just as wrapper: about the same; 400 points created
	 * adding speed: still same, ~50k points created
	 * adding merge: still same, ~51k points created
	 * 
	 * 100 particles, 1000 iterations, no merging
	 * wrapper: 4000ms, 200 points
	 * pos-update: 4100ms, 100k points
	 * spd-update: 5300ms, 30M points
	 */
	public static void main(String[] args) {
		runBenchmark(100, 1000, false);
	}
	
	private static long runBenchmark(int particles, int iterations, boolean merging) {
		Universe universe = new Universe();
		universe.initialize(particles);
		universe.merging = merging;
		
		long startTime = System.currentTimeMillis();
		for (int i = 0; i < iterations; i++) {
			if (i % 100 == 0) {
				System.out.println("iter " + i);
			}
			universe.update();
		}
		long endTime = System.currentTimeMillis();
		System.out.println("time " + (endTime - startTime));
		System.out.println("points " + Point3D.count);
		System.out.println("particles " + universe.particles.size());
		return endTime;
	}
	
}
