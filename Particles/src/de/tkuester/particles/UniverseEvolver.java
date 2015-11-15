package de.tkuester.particles;

import java.util.Random;

import de.tkuester.particles.model.Particle;
import de.tkuester.particles.model.Universe;

/**
 * This class can be used for "evolving" a universe that remains relatively 
 * stable for some time. Starting with some random universe, it is repeatedly
 * copied, mutated, and simulated, and the best one is kept for the next 
 * iteration until a given number of turns have passed or the quality somewhat
 * converges, using a simple form of evolutionary algorithm.
 *
 * @author tkuester
 */
public class UniverseEvolver {

	/** random number generator for random mutations */
	private static Random random = new Random();
	
	public static void main(String[] args) throws Exception {
		// create universe using universe evolver
		UniverseEvolver evolver = new UniverseEvolver();
		Universe universe = evolver.evolveUniverse(2, 100, 100_000);
		
		// run the resulting universe
		RunUniverse.runUniverseFrame(universe, 600, 10, 10, true);
	}
	
	/**
	 * Gradually evolve a universe with a given number of particles until the
	 * universe remains stable as long as possible. After creating a random
	 * initial universe, repeatedly create copies of that universe, mutate
	 * those copies, and determine their quality, i.e. a simple (1+1)-ES 
	 * 
	 * @param particles			number of particles in the universe
	 * @param maxGenerations	max number of generations
	 * @param maxTurns			max number of turns for the universe to remain stable
	 * @return					evolved universe
	 */
	public Universe evolveUniverse(int particles, int maxGenerations, int maxTurns) {
		Universe universe = new Universe();
		universe.initialize(particles);
		int best = testRun(universe);
		
		for (int gen = 0; gen < maxGenerations; gen++) {
			System.out.println("Generation: " + gen + ",\t Turns: " + best);
			Universe offspring = copy(universe);
			mutate(offspring);
			int turns = testRun(offspring);
			
			if (turns > best) {
				universe = offspring;
				best = turns;
			}
			
			if (turns > maxTurns) {
				break;
			}
		}
		return universe;
	}
	
	/**
	 * Slightly change position, speed, size, etc. of the particles in the 
	 * universe. This will change the universe and its particles in-place, 
	 * so this should be done with a copy of the parent universe. 
	 * 
	 * @param universe		universe to mutate
	 */
	public void mutate(Universe universe) {
		if (random.nextBoolean()) {
			// XXX is this a good idea? might end up just setting it to 0.0
			universe.G += random.nextGaussian();
		}
		for (Particle p : universe.particles) {
			if (random.nextBoolean()) {
				if (random.nextBoolean()) {
					p.pos.x += random.nextGaussian();
					p.pos.y += random.nextGaussian();
					p.pos.z += random.nextGaussian();
				}
				if (random.nextBoolean()) {
					p.speed.x += random.nextGaussian();
					p.speed.y += random.nextGaussian();
					p.speed.z += random.nextGaussian();
				}
				if (random.nextBoolean()) {
					p.size += random.nextGaussian();
				}
			}
		}
	}
	
	/**
	 * Evaluate the evolved universe. The evaluation is based on the  number of 
	 * steps until the orbits deteriorate. Currently, this is determined by the 
	 * distance between particles becoming twice or half the distance of that 
	 * pair in the beginning of the simulation.
	 *   
	 * @param universe		universe under evaluation
	 * @return				number of steps until orbits deteriorate
	 */
	public int testRun(Universe universe) {
		/*
		 * for two particles, just see that the distance between them stays relatively constant,
		 * but what for 3 or more particles? see that for each particle the distance to at least
		 * one other remains constant? 
		 */
		
		// always run a copy
		universe = copy(universe);
		
		Particle p = universe.particles.get(0);
		Particle q = universe.particles.get(1);
		
		double distance = p.pos.distance(q.pos);
		
		while (true) {
			universe.update(false);
			double newDistance = p.pos.distance(q.pos);
			
			if (newDistance < distance / 2 || newDistance > distance * 2) {
				break;
			}
			if (universe.step > 100000) {
				break;
			}
		}
		return universe.step;
	}
	
	/**
	 * Create a deep-copy of the universe and all its particles.
	 * 
	 * @param original		given universe
	 * @return				deep-copy of that universe
	 */
	public Universe copy(Universe original) {
		Universe copy = new Universe();
		copy.G = original.G;
		
		for (Particle p : original.particles) {
			Particle q = new Particle();
			
			q.pos.x = p.pos.x;
			q.pos.y = p.pos.y;
			q.pos.z = p.pos.z;
			
			q.speed.x = p.speed.x;
			q.speed.y = p.speed.y;
			q.speed.z = p.speed.z;
			
			q.size = p.size;
			
			copy.particles.add(q);
		}
		return copy;
	}
	
}
