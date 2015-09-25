package de.tkuester.particles;

import java.util.ArrayList;

import javax.swing.JFrame;

/**
 * Class for running/testing the universe. This just creates a new universe 
 * and a component for displaying it, embeds it into a plain frame, and
 * advances the universe step by step in an infinite loop.
 * 
 * TODO user proper Swing threading for launching and running. 
 *
 * @author tkuester
 */
public class RunUniverse {

	public static void main(String[] args) throws Exception {
		
		Universe universe = new Universe();
//		universe = new TestUniverse();
		universe.randomInit();

		UniverseComponent component = new UniverseComponent(universe);
		
		JFrame frame = new JFrame("Universe");
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.getContentPane().add(component);
		frame.pack();
		frame.setSize(600, 600);
		frame.setVisible(true);

		while (true) {
			universe.update();
			frame.repaint();
			Thread.sleep(100);
		}
	}
	
	/**
	 * Test-"Universe", creating an evenly spaced lattice of NxNxN particles 
	 * for testing the drawing component and camera movement.
	 * 
	 * @author tkuester
	 */
	static class TestUniverse extends Universe {

		/** number of particles in each row, column, and layer */
		final static int N = 4;
		
		/** spacing between particles */
		final static double D = 100;
		
		@Override
		public void randomInit() {
			this.particles = new ArrayList<Particle>(N*N*N);
			for (int i = 0; i < N; i++) {
				for (int j = 0; j < N; j++) {
					for (int k = 0; k < N; k++) {
						Particle p = new Particle();
						
						p.posX = (i - N/2.) * D;
						p.posY = (j - N/2.) * D;
						p.posZ = (k - N/2.) * D;
						p.size = 10;
						
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
