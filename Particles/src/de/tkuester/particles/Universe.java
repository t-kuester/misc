package de.tkuester.particles;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public class Universe {

	List<Particle> particles;
	
	final double G = 10.0;
	
	public void randomInit() {
		Random random = new Random();
		double positions = 1000;
		double speeds = 10;
		double sizes = 5;
		int number = 1000;
		
		this.particles = new ArrayList<Particle>(number);
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
	}
	
	public void update() {
		
		Set<Particle> destroyed = new HashSet<>();
		Set<Runnable> merger = new HashSet<>();
		
		for (int i = 0; i < this.particles.size(); i++) {
			for (int k = i + 1; k < this.particles.size(); k++) {
				Particle p1 = this.particles.get(i);
				Particle p2 = this.particles.get(k);
				
				double dX = p1.posX - p2.posX;
				double dY = p1.posY - p2.posY;
				double dZ = p1.posZ - p2.posZ;
				double d = Math.sqrt(dX * dX + dY * dY + dZ * dZ);
				double m1 = Math.pow(p1.size, 3);
				double m2 = Math.pow(p2.size, 3);
				double m = m1 + m2;
				
				if (d < p1.size + p2.size) {
					
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
					
				} else if (d > 0) {
					
					double force = (m1 * m2 * G) / (d * d);
					double accel1 = force / m1;
					double accel2 = force / m2;
					
					p1.speedX -= accel1 * dX / d;
					p1.speedY -= accel1 * dY / d;
					p1.speedZ -= accel1 * dZ / d;
					
					p2.speedX += accel2 * dX / d;
					p2.speedY += accel2 * dY / d;
					p2.speedZ += accel2 * dZ / d;
					
				}
			}
		}

		merger.forEach(Runnable::run);
		
		this.particles.removeAll(destroyed);
		this.particles.forEach(p -> {
			p.posX += p.speedX;
			p.posY += p.speedY;
			p.posZ += p.speedZ;
		});
	}
	
}
