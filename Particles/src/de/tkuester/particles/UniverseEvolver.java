package de.tkuester.particles;

import java.util.ArrayList;
import java.util.Random;

import javax.swing.JFrame;

public class UniverseEvolver {

	private static Random random = new Random();
	
	public static void main(String[] args) throws Exception {
		
		UniverseEvolver evolver = new UniverseEvolver();
		
		Universe universe = evolver.evolveUniverse(2);
		
		// TODO move this to a method to eliminate code duplication
		
		UniverseComponent component = new UniverseComponent(universe);
		
		JFrame frame = new JFrame("Universe");
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.getContentPane().add(component);
		frame.pack();
		frame.setSize(600, 600);
		frame.setVisible(true);

		while (true) {
			universe.update();
			if (universe.step % 100 == 0) {
				System.out.println(universe.step);
			}
			frame.repaint();
			Thread.sleep(10);
		}
	}
	
	public Universe evolveUniverse(int n) {

		Universe universe = new Universe();
		universe.randomInit(n);
		
		int best = testRun(universe);
		
		for (int gen = 0; gen < 100; gen++) {
			System.out.println("Generation: " + gen + ",\t Turns: " + best);
			Universe offspring = copy(universe);
			mutate(offspring);
			int turns = testRun(offspring);
			
			if (turns > best) {
				universe = offspring;
				best = turns;
			}
			
			if (turns > 100_000) {
				break;
			}
		}
		return universe;
	}
	
	
	public void mutate(Universe universe) {
		// slightly change position, speed, or size of the particles in this universe
		
		if (random.nextBoolean()) {
			universe.G += random.nextGaussian();
		}
		for (Particle p : universe.particles) {
			if (random.nextBoolean()) {
				if (random.nextBoolean()) {
					p.posX += random.nextGaussian();
					p.posY += random.nextGaussian();
					p.posZ += random.nextGaussian();
				}
				if (random.nextBoolean()) {
					p.speedX += random.nextGaussian();
					p.speedY += random.nextGaussian();
					p.speedZ += random.nextGaussian();
				}
				if (random.nextBoolean()) {
					p.size += random.nextGaussian();
				}
			}
		}
	}
	
	public int testRun(Universe universe) {
		// TODO test run the universe and return the number of steps until the orbits deteriorate
		/*
		 * for two particles, just see that the distance between them stays relatively constant,
		 * but what for 3 or more particles? see that for each particle the distance to at least
		 * one other remains contant? 
		 */
		
		// always run a copy
		universe = copy(universe);
		
		Particle p = universe.particles.get(0);
		Particle q = universe.particles.get(1);
		
		double distance = distance(p, q);
		
		while (true) {
			universe.update();
			double newDistance = distance(p, q);
			
			if (newDistance < distance / 2 || newDistance > distance * 2) {
				break;
			}
			if (universe.step > 100000) {
				break;
			}
		}
		return universe.step;
	}
	
	/*
	 * TODO move this to some appropriate helper class
	 */
	public double distance(Particle p, Particle q) {
		return Math.sqrt(Math.pow(p.posX - q.posX, 2)
				       + Math.pow(p.posY - q.posY, 2)
				       + Math.pow(p.posZ - q.posZ, 2));
	}
	
	public Universe copy(Universe original) {
		Universe copy = new Universe();
		copy.G = original.G;
		
		copy.particles = new ArrayList<Particle>();
		for (Particle p : original.particles) {
			Particle q = new Particle();
			
			q.posX = p.posX;
			q.posY = p.posY;
			q.posZ = p.posZ;
			
			q.speedX = p.speedX;
			q.speedY = p.speedY;
			q.speedZ = p.speedZ;
			
			q.size = p.size;
			
			copy.particles.add(q);
		}
		return copy;
	}
	
}
