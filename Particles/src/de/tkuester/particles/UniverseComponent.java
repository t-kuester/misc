package de.tkuester.particles;

import java.awt.Graphics;
import java.util.Locale;

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
			
			// determine horizontal angle and position
			double dxy = distance(p.posX, p.posY);
			double a = angle(p.posX, p.posY, dxy);
			double x2 = Math.cos(a - yaw) * dxy;
			double y2 = Math.sin(a - yaw) * dxy;

			// determine vertical angle and position
			double dxz = distance(x2, p.posZ);
			double b = angle(x2, p.posZ, dxz);
			double x3 = Math.cos(b - pitch) * dxz;
			double z2 = Math.sin(b - pitch) * dxz;
			
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
	
	double distance(double x, double y) {
		return Math.sqrt(x*x + y*y);
	}
	
	double angle(double x, double y, double d) {
		return d == 0 ? 0 : Math.acos(x / d) * (y > 0 ? +1 : -1); 
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
