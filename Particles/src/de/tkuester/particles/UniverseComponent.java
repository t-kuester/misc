package de.tkuester.particles;

import java.awt.Graphics;
import java.util.Locale;
import java.util.Random;

import javax.swing.JComponent;

@SuppressWarnings("serial")
public class UniverseComponent extends JComponent {
	
	final Universe universe;
	
	final Camera camera;
	
	public UniverseComponent(Universe universe) {
		this.universe = universe;
		this.camera = new Camera();
		
		// TODO add mouse listener for perspective
	}
	
	@Override
	protected void paintComponent(Graphics g) {
		super.paintComponent(g);
		
		final int W = this.getWidth();
		final int H = this.getHeight();

		double yaw   = Math.toRadians(camera.yaw);
		double pitch = Math.toRadians(camera.pitch);
		
		for (Particle p : this.universe.particles) {

			double x = p.posX;
			double y = p.posY;
			double z = p.posZ;
			double d = Math.sqrt(x*x + y*y + z*z);
			
			// determine horizontal angle and position
			double a = Math.acos(x / Math.sqrt(x*x + y*y)) - yaw;;
			double x2 = Math.cos(a) * d;
			double y2 = Math.sin(a) * d;

			// determine vertical angle and position
			double b = Math.acos(x2 / Math.sqrt(x2*x2 + z*z)) - pitch;
			double x3 = Math.cos(b) * d;
			double z2 = Math.sin(b) * d;
			
			// distance to camera and positions on screen
			double x4 = camera.distance - x3;
			if (x4 > 0) {
				int horizontal = (int) ((1 + y2 / x4) * W/2); 
				int vertical   = (int) ((1 + z2 / x4) * H/2);
				int s = 2;
				g.drawOval(horizontal - s, vertical - s, 2*s, 2*s);
			}

			// maybe show speed as some kind of arrow?
		}
	}
	
	class Camera {
		double yaw = 0;
		double pitch = 0;
		double distance = 1;
		
		@Override
		public String toString() {
			return String.format(Locale.UK, "Camera(%.2f, %.2f, %.2f)", yaw, pitch, distance); 
		}
	}

}
