package de.tkuester.particles;

import java.util.ArrayList;

import javax.swing.JFrame;

/**
 * Class for running/testing the universe. This just creates a new universe 
 * and a component for displaying it, embeds it into a plain frame, and
 * advances the universe step by step in an infinite loop.
 * 
 * @author tkuester
 */
public class RunUniverse {

	public static void main(String[] args) throws Exception {
		
		Universe universe = new Universe();
		universe.initialize(200);
//		universe = new TestUniverse();
//		universe.randomInit(5);

		runUniverseFrame(universe, 600, 100);
	}
	
	/**
	 * Create a Frame for running and showing the Universe. The universe is
	 * advanced in regular intervals and the frame is updated accordingly.
	 * 
	 * TODO user proper Swing threading
	 * 
	 * @param universe		the Universe to simulate
	 * @param size			size of the frame (both width and height)
	 * @param sleep			sleep time between steps
	 */
	public static void runUniverseFrame(Universe universe, int size, int sleep) {

		// create frame with UniverseComponent
		JFrame frame = new JFrame("Universe");
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.getContentPane().add(new UniverseComponent(universe));
		frame.pack();
		frame.setSize(size, size);
		frame.setVisible(true);

		// update universe state and repaint frame
		while (true) {
			universe.update();
			frame.repaint();
			try {
				Thread.sleep(sleep);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
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
		public void initialize(int n) {
			this.particles = new ArrayList<Particle>(n*n*n);
			for (int i = 0; i < n; i++) {
				for (int j = 0; j < n; j++) {
					for (int k = 0; k < n; k++) {
						Particle p = new Particle();
						
						p.pos.x = (i - n/2.) * D;
						p.pos.y = (j - n/2.) * D;
						p.pos.z = (k - n/2.) * D;
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
