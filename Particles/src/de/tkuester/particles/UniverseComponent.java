package de.tkuester.particles;

import java.awt.Graphics;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.event.MouseWheelEvent;
import java.util.Locale;

import javax.swing.JComponent;

/**
 * Component for displaying a universe of particles. The particles are shown
 * in a more or less correct three dimensional perspective. The camera is
 * always pointed towards the center but can be moved around a sphere and
 * moved further in or outwards, using the mouse.
 * 
 * @author tkuester
 */
public class UniverseComponent extends JComponent {
	
	private static final long serialVersionUID = -3154952439452964085L;

	/** the universe to draw */
	final Universe universe;
	
	/** the camera's position */
	final Camera camera;
	
	/**
	 * Create new universe component.
	 * 
	 * @param universe	the universe
	 */
	public UniverseComponent(Universe universe) {
		this.universe = universe;
		this.camera = new Camera();
		
		// add mouse listener for camera control
		CameraControl cameraControl = new CameraControl();
		this.addMouseListener(cameraControl);
		this.addMouseMotionListener(cameraControl);
		this.addMouseWheelListener(cameraControl);
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
				
				// TODO take size and distance into account
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

	
	/**
	 * Class for encapsulating the current orientation of the camera.
	 * 
	 * @author tkuester
	 */
	private class Camera {
		double yaw = 0;
		double pitch = 0;
		double distance = 1000;
		
		@Override
		public String toString() {
			return String.format(Locale.UK, "Camera(%.2f, %.2f, %.2f)", yaw, pitch, distance); 
		}
	}
	
	/**
	 * Mouse adapter for controlling the camera.
	 *
	 * @author tkuester
	 */
	private class CameraControl extends MouseAdapter {

		private int x;
		private int y;
		
		@Override
		public void mousePressed(MouseEvent e) {
			this.x = e.getX();
			this.y = e.getY();
		}
		
		@Override
		public void mouseDragged(MouseEvent e) {
			int dx = e.getX() - x;
			int dy = e.getY() - y;
			x = e.getX();
			y = e.getY();
			
			Camera camera = UniverseComponent.this.camera;
			camera.yaw += dx;
			camera.pitch = Math.min(Math.max(camera.pitch + dy, -90), 90);
		}
		
		@Override
		public void mouseWheelMoved(MouseWheelEvent e) {
			double amount = 1 + (e.getWheelRotation() * .1);
			UniverseComponent.this.camera.distance *= amount;
		}
		
	}

}
