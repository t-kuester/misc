package de.tkuester.particles;

import java.awt.Graphics;

import javax.swing.JComponent;

@SuppressWarnings("serial")
public class UniverseComponent extends JComponent {
	
	final Universe universe;
	
	// TODO current camera position
	
	public UniverseComponent(Universe universe) {
		this.universe = universe;
		
		// TODO add mouse listener for perspective
	}
	
	@Override
	protected void paintComponent(Graphics g) {
		// TODO Auto-generated method stub
		super.paintComponent(g);
	}

}
