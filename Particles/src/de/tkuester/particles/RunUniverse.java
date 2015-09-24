package de.tkuester.particles;

import java.util.ArrayList;
import java.util.Random;

import javax.swing.JFrame;

import de.tkuester.particles.UniverseComponent.Camera;

public class RunUniverse {

	public static void main(String[] args) throws Exception {
		
		Universe universe = new TestUniverse();
		universe.randomInit();

		UniverseComponent component = new UniverseComponent(universe);
		
		JFrame frame = new JFrame("Universe");
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.getContentPane().add(component);
		frame.pack();
		frame.setSize(800, 600);
		frame.setVisible(true);

		Random random = new Random();

		component.camera.yaw      = 0;//random.nextInt(360);
		component.camera.pitch    = 0;//random.nextInt(180) - 90;
		component.camera.distance = 0;//Math.abs(random.nextGaussian() * 100);
		
		int d = +1;
		while (true) {
			
			// testing
			component.camera.yaw   += 1;
//			component.camera.pitch += d;
//			component.camera.distance += 1;//random.nextGaussian();
			if (Math.abs(component.camera.pitch) > 90) {
				d *= -1;
			}
			System.out.println(component.camera);
			
			universe.update();
			frame.repaint();
			Thread.sleep(100);
		}
		
	}
	
	static class TestUniverse extends Universe {
		
		@Override
		public void randomInit() {
			
			int N = 5;
			double D = 100;
			
			// create an evenly spaced lattice of NxNxN particles
			// for testing the component and camera movement
			
			this.particles = new ArrayList<Particle>(N*N*N);
			for (int i = 0; i < N; i++) {
				for (int j = 0; j < N; j++) {
					for (int k = 0; k < N; k++) {
						Particle p = new Particle();
						
						p.posX = (i - N/2) * D;
						p.posY = (j - N/2) * D;
						p.posZ = (k - N/2) * D;
						
						this.particles.add(p);
					}
				}
			}
		}
		
		@Override
		public void update() {
			// do nothing
		}
	}
	
}
