package de.tkuester.particles;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

/**
 * The "universe" containing the particles. It manages how the particles
 * move in each step, attracting each other via "gravity" and merging into 
 * larger bodies when being close enough to each other.
 *
 * @author tkuester
 */
public class Universe {

	/** list of particles currently present in the universe */
	List<Particle> particles;
	
	/** 'Gravitational constant'. Too low, and nothing happens; too 
	 * high and after a very short contraction the universe explodes. */
	double G = .10;
	
	int step = 0;
	
	/**
	 * Randomly initialize a number of particles in the universe.
	 * 
	 * @param number	number of particles to generate
	 */
	public void randomInit(int number) {
		Random random = new Random();
		double positions = 1000;
		double speeds = 10;
		double sizes = 50;
		
		this.particles = new ArrayList<Particle>(number);
		// create and add particles with random position, speed, and size
		for (int i = 0; i < number; i++) {
			Particle p = new Particle();
			
			p.posX = random.nextGaussian() * positions;
			p.posY = random.nextGaussian() * positions;
			p.posZ = random.nextGaussian() * positions;
			
			p.speedX = random.nextGaussian() * speeds;
			p.speedY = random.nextGaussian() * speeds;
			p.speedZ = random.nextGaussian() * speeds;
			
			p.size = Math.abs(random.nextGaussian() * sizes);
			
			this.particles.add(p);
		}
		this.step = 0;
	}
	
	/**
	 * Update speed and position of each particle in the universe after
	 * another "time step" (or indeterminate length). Particles are
	 * attracted to each other by gravity and will merge if close enough.
	 */
	public void update() {
		// the particles that were destroyed (absorbed) in this step
		Set<Particle> destroyed = new HashSet<>();
		// deferred tasks for merging particles
		Set<Runnable> merger = new HashSet<>();
		
		// for each combination of pairs of particles...
		for (int i = 0; i < this.particles.size(); i++) {
			for (int k = i + 1; k < this.particles.size(); k++) {
				Particle p1 = this.particles.get(i);
				Particle p2 = this.particles.get(k);
				
				// ... get some basic metrics ...
				double dX = p1.posX - p2.posX;
				double dY = p1.posY - p2.posY;
				double dZ = p1.posZ - p2.posZ;
				double d = Math.sqrt(dX * dX + dY * dY + dZ * dZ);
				double m1 = Math.pow(p1.size, 3);
				double m2 = Math.pow(p2.size, 3);
				double m = m1 + m2;
				
				// ... and see whether the particles touch each other
				if (d < p1.size + p2.size) {
					
					// if so, merge second into first, and destroy second
					Runnable merge = () -> {
						p1.posX = (p1.posX * m1 + p2.posX * m2) / m;
						p1.posY = (p1.posY * m1 + p2.posY * m2) / m;
						p1.posZ = (p1.posZ * m1 + p2.posZ * m2) / m;
						
						p1.speedX = (p1.speedX * m1 + p2.speedX * m2) / m;
						p1.speedY = (p1.speedY * m1 + p2.speedY * m2) / m;
						p1.speedZ = (p1.speedZ * m1 + p2.speedZ * m2) / m;
						
						p1.size = Math.pow(m, 1/3.);
					};
					merger.add(merge);
					destroyed.add(p2);
					
				} else {
					// otherwise, calculate gravitational force ...
					double force = (m1 * m2 * G) / (d * d);
					
					// ...and accelerate the particles towards each other
					double accel1 = force / m1;
					p1.speedX -= accel1 * dX / d;
					p1.speedY -= accel1 * dY / d;
					p1.speedZ -= accel1 * dZ / d;
					
					double accel2 = force / m2;
					p2.speedX += accel2 * dX / d;
					p2.speedY += accel2 * dY / d;
					p2.speedZ += accel2 * dZ / d;
				}
			}
		}

		// execute all the "merger" tasks
		merger.forEach(Runnable::run);
		
		// remove particles that were destroyed in this step
		this.particles.removeAll(destroyed);
		
		// update position of remaining particles
		this.particles.forEach(p -> {
			p.posX += p.speedX;
			p.posY += p.speedY;
			p.posZ += p.speedZ;
		});
		
		// finally, update step
		this.step++;
	}
	
}
