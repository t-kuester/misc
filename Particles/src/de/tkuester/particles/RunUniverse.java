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
		universe.randomInit(200);
//		universe = new TestUniverse();
//		universe.randomInit(5);

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

		/** spacing between particles */
		final static double D = 100;
		
		@Override
		public void randomInit(int n) {
			this.particles = new ArrayList<Particle>(n*n*n);
			for (int i = 0; i < n; i++) {
				for (int j = 0; j < n; j++) {
					for (int k = 0; k < n; k++) {
						Particle p = new Particle();
						
						p.posX = (i - n/2.) * D;
						p.posY = (j - n/2.) * D;
						p.posZ = (k - n/2.) * D;
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
