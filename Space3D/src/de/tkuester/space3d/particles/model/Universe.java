package de.tkuester.space3d.particles.model;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

/**
 * The "universe" containing the particles. It manages how the particles
 * move in each step, attracting each other via "gravity" and merging into 
 * larger bodies when being close enough to each other.
 *
 * @author tkuester
 */
public class Universe {

	/** list of particles currently present in the universe */
	public final List<Particle> particles = new ArrayList<>();
	
	/** 'Gravitational constant'. Too low, and nothing happens; too 
	 * high and after a very short contraction the universe explodes. */
	public double G = .10;
	
	/** the current step in the simulation, just for tracking */
	public int step = 0;
	
	/** whether to merge very close particles */
	public boolean merging = true;
	
	/**
	 * Randomly initialize a number of particles in the universe.
	 * 
	 * @param number	number of particles to generate
	 */
	public synchronized void initialize(int number) {
		Random random = new Random(0); // fixed seed for reproducible results
		double positions = 1000;
		double speeds = 10;
		double sizes = 50;
		
		this.particles.clear();;
		// create and add particles with random position, speed, and size
		for (int i = 0; i < number; i++) {
			Particle p = new Particle();
			
			p.pos.x = random.nextGaussian() * positions;
			p.pos.y = random.nextGaussian() * positions;
			p.pos.z = random.nextGaussian() * positions;
			
			p.speed.x = random.nextGaussian() * speeds;
			p.speed.y = random.nextGaussian() * speeds;
			p.speed.z = random.nextGaussian() * speeds;
			
			p.size = Math.abs(random.nextGaussian() * sizes);
			
			this.particles.add(p);
		}
		this.step = 0;
	}
	
	/**
	 * Update speed and position of each particle in the universe after
	 * another "time step" (or indeterminate length). Particles are
	 * attracted to each other by gravity and will merge if close enough.
	 * 
	 * @param debug		print some debug information
	 */
	public synchronized void update(boolean debug) {
		// what particles have to be merged into what other particles
		Map<Particle, Particle> mergeInto = new HashMap<>();
		
		// for each combination of pairs of particles...
		for (int i = 0; i < this.particles.size(); i++) {
			for (int k = i + 1; k < this.particles.size(); k++) {
				Particle p1 = this.particles.get(i);
				Particle p2 = this.particles.get(k);
				
				// ... get some basic metrics ...
				double dX = p1.pos.x - p2.pos.x;
				double dY = p1.pos.y - p2.pos.y;
				double dZ = p1.pos.z - p2.pos.z;
				double d = Math.sqrt(dX * dX + dY * dY + dZ * dZ);
//				Point3D diff = p1.pos.sub(p2.pos);
//				double d = diff.absolute();
				
				// ... and see whether the particles touch each other
				if (merging && d < p1.size + p2.size) {
					/*
					 *  particles are merged sort-of union-find-like; if this particle 
					 *  intersects with many others, it does not really matter which 
					 *  one it is merged into, as long as it is merged before the one 
					 *  it is merged into is merged itself into some other particle
					 */
					mergeInto.put(p1, p2);
					
				} else {
					// otherwise, calculate gravitational force ...
					double m1 = p1.getMass();
					double m2 = p2.getMass();
					double force = (m1 * m2 * G) / (d * d);
					
//					Point3D norm = diff.norm();
					
					// ...and accelerate the particles towards each other
					double accel1 = -force / m1;
					p1.speed.x += accel1 * dX / d;
					p1.speed.y += accel1 * dY / d;
					p1.speed.z += accel1 * dZ / d;
//					p1.speed = p1.speed.add(norm.mult(accel1));
					
					double accel2 = force / m2;
					p2.speed.x += accel2 * dX / d;
					p2.speed.y += accel2 * dY / d;
					p2.speed.z += accel2 * dZ / d;
//					p2.speed = p2.speed.add(norm.mult(accel2));
				}
			}
		}

		if (merging) {
			// merge particles in the same order they were put into the map
			for (Particle p1 : particles) {
				if (mergeInto.containsKey(p1)) {
					Particle p2 = mergeInto.get(p1);
					double m1 = p1.getMass();
					double m2 = p2.getMass();
					double m = m1 + m2;
					
					p2.pos.x = (p1.pos.x * m1 + p2.pos.x * m2) / m;
					p2.pos.y = (p1.pos.y * m1 + p2.pos.y * m2) / m;
					p2.pos.z = (p1.pos.z * m1 + p2.pos.z * m2) / m;
	//				p2.pos = p1.pos.mult(m1).add(p2.pos.mult(m2)).div(m);
					
					p2.speed.x = (p1.speed.x * m1 + p2.speed.x * m2) / m;
					p2.speed.y = (p1.speed.y * m1 + p2.speed.y * m2) / m;
					p2.speed.z = (p1.speed.z * m1 + p2.speed.z * m2) / m;
	//				p2.speed = p1.speed.mult(m1).add(p2.speed.mult(m2)).div(m);
					
					p2.setMass(m);
				}
			}
			particles.removeAll(mergeInto.keySet());
		}
		
		// update position of remaining particles
		this.particles.forEach(p -> {
			p.pos.x += p.speed.x;
			p.pos.y += p.speed.y;
			p.pos.z += p.speed.z;
//			p.pos = p.pos.add(p.speed);
		});
		
		// finally, update step
		this.step++;
		
		if (debug) {
			double totalMass = particles.stream().mapToDouble(Particle::getMass).sum();
			double totalSpeed = particles.stream().mapToDouble(p -> p.speed.absolute()).sum();
			System.out.printf("Step %d, Particles: %d, Total Mass: %e, Total Speed: %e\n", 
					this.step, this.particles.size(), totalMass, totalSpeed);
		}
	}
	
}
