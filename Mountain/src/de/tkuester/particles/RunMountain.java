package de.tkuester.particles;

import javax.swing.JFrame;
import javax.swing.SwingUtilities;

import de.tkuester.particles.model.Mountain;

/**
 * Class for running/testing the mountain. This just creates a new mountain 
 * and a component for displaying it, embeds it into a plain frame.
 * 
 * @author tkuester
 */
public class RunMountain {

	public static void main(String[] args) throws Exception {
		Mountain mountain = Mountain.createMountain(1000, 1000, 5);
		runMountainFrame(mountain, 600);
	}
	
	/**
	 * Create a Frame for running and showing the Universe. The universe is
	 * advanced in regular intervals and the frame is updated accordingly.
	 * 
	 * @param mountain		the mountain to show
	 * @param size			size of the frame (both width and height)
	 */
	public static void runMountainFrame(Mountain mountain, int size) {
		SwingUtilities.invokeLater(() -> {
			// create frame with UniverseComponent
			JFrame frame = new JFrame("Mountain");
			frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
			frame.getContentPane().add(new MountainComponent(mountain));
			frame.pack();
			frame.setSize(size, size);
			frame.setVisible(true);
		});
	}
	
}
