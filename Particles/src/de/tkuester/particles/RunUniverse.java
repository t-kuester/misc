package de.tkuester.particles;

import javax.swing.JFrame;

public class RunUniverse {

	public static void main(String[] args) throws Exception {
		
		Universe universe = new Universe();
		universe.randomInit();

		UniverseComponent component = new UniverseComponent(universe);
		
		JFrame frame = new JFrame("Universe");
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.getContentPane().add(component);
		frame.pack();
		frame.setVisible(true);

		while (true) {
			universe.update();
			frame.repaint();
			Thread.sleep(100);
		}
		
	}
	
}
