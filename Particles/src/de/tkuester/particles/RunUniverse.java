package de.tkuester.particles;

import javax.swing.JFrame;

import de.tkuester.particles.model.Particle;
import de.tkuester.particles.model.Universe;

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
//		addLattice(universe, 100, 5);
//		universe.merging = false;

		runUniverseFrame(universe, 600, 100, true);
	}
	
	/**
	 * Create a Frame for running and showing the Universe. The universe is
	 * advanced in regular intervals and the frame is updated accordingly.
	 * 
	 * @param universe		the Universe to simulate
	 * @param size			size of the frame (both width and height)
	 * @param sleep			sleep time between steps
	 * @param update		whether to update the universe (false for testing just the camera)
	 */
	public static void runUniverseFrame(Universe universe, int size, int sleep, boolean update) {

		// create frame with UniverseComponent
		JFrame frame = new JFrame("Universe");
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.getContentPane().add(new UniverseComponent(universe));
		frame.pack();
		frame.setSize(size, size);
		frame.setVisible(true);

		// update universe state and repaint frame
		while (update) {
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
	 * Create particles laid out in a regular lattice in the given universe.
	 * 
	 * @param universe		some universe (existing particles will be removed)
	 * @param spacing		spacing between particles
	 * @param side			number of particles in each dimension (total: side^3)
	 */
	public static void addLattice(Universe universe, int spacing, int side) {
		universe.particles.clear();
		for (int i = 0; i < side; i++) {
			for (int j = 0; j < side; j++) {
				for (int k = 0; k < side; k++) {
					Particle p = new Particle();
					
					p.pos.x = (i - side/2.) * spacing;
					p.pos.y = (j - side/2.) * spacing;
					p.pos.z = (k - side/2.) * spacing;
					p.size = 10;
					
					universe.particles.add(p);
				}
			}
		}
	}
}
