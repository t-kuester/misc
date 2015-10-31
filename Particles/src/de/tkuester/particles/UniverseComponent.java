package de.tkuester.particles;

import java.awt.Color;
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

	/*
	 * TODO 
	 * show coordinate axes (optional)
	 * show XYZ lines for each particle (optional)
	 * show particle speed as vector (optional)
	 */
	
	/** the universe to draw */
	private final Universe universe;
	
	/** the camera's position */
	private final Camera camera;
	
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
		g.setColor(Color.BLACK);
		g.fillRect(0, 0, W, H);

		double yaw   = Math.toRadians(camera.yaw);
		double pitch = Math.toRadians(camera.pitch);
		
		for (Particle p : this.universe.particles) {
			
			// determine horizontal angle and position
			double dxy = distance(p.pos.x, p.pos.y);
			double a = angle(p.pos.x, p.pos.y, dxy);
			double x2 = Math.cos(a - yaw) * dxy;
			double y2 = Math.sin(a - yaw) * dxy;

			// determine vertical angle and position
			double dxz = distance(x2, p.pos.z);
			double b = angle(x2, p.pos.z, dxz);
			double x3 = Math.cos(b - pitch) * dxz;
			double z2 = Math.sin(b - pitch) * dxz;
			
			// if particle is in front of camera
			double x4 = camera.distance - x3;
			if (x4 > 0) {
				// determine position on screen
				int horz = (int) ((1 + y2 / x4) * W/2); 
				int vert   = (int) ((1 + z2 / x4) * H/2);
				
				if (0 <= horz && horz < W && 0 <= vert && vert < H) {
					// determine apparent size and draw particle
					double distance = Math.sqrt(x4*x4 + y2*y2 + z2*z2);
					int s = Math.max((int) (p.size / (distance / 100)), 1);
					
					// use color to indicate either size or distance
					float f = (float) Math.max(Math.min(camera.distance / distance, 1.0), 0.0);
					Color c = new Color(f, f, f);
					g.setColor(c);
					
					g.fillOval(horz - s, vert - s, 2*s, 2*s);
				}
			}
		}
		// show camera position
		g.setColor(Color.WHITE);
		g.drawString(this.camera.toString(), 10, 10);
		
	}
	
	private double distance(double x, double y) {
		return Math.sqrt(x*x + y*y);
	}
	
	private double angle(double x, double y, double d) {
		return d == 0 ? 0 : Math.acos(x / d) * (y > 0 ? +1 : -1); 
	}

	
	/**
	 * Class for encapsulating the current orientation of the camera.
	 * All angles are in degrees.
	 * 
	 * @author tkuester
	 */
	private class Camera {
		double yaw = 0;
		double pitch = 0;
		double distance = 10000;
		
		@Override
		public String toString() {
			return String.format(Locale.UK, 
					"Camera: Yaw %.2f°, Pitch %.2f°, Distance %.2f", 
					yaw, pitch, distance); 
		}
	}
	
	/**
	 * Mouse adapter for controlling the camera.
	 *
	 * @author tkuester
	 */
	private class CameraControl extends MouseAdapter {

		/** the last camera position */
		private int x, y;
		
		@Override
		public void mousePressed(MouseEvent e) {
			this.x = e.getX();
			this.y = e.getY();
//			UniverseComponent.this.repaint();
		}
		
		@Override
		public void mouseDragged(MouseEvent e) {
			int dx = e.getX() - x;
			int dy = e.getY() - y;
			x = e.getX();
			y = e.getY();
			
			UniverseComponent.this.camera.yaw += dx;
			UniverseComponent.this.camera.pitch += dy;
			UniverseComponent.this.repaint();
		}
		
		@Override
		public void mouseWheelMoved(MouseWheelEvent e) {
			double amount = 1 + (e.getWheelRotation() * .1);
			UniverseComponent.this.camera.distance *= amount;
			UniverseComponent.this.repaint();
		}
	}

}
