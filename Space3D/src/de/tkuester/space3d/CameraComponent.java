package de.tkuester.space3d;

import java.awt.Color;
import java.awt.Graphics;
import java.awt.Point;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.event.MouseWheelEvent;
import java.util.Locale;

import javax.swing.JComponent;

/**
 * Component for displaying a three-dimensional space, for drawing Points
 * and connecting lines in a more or less current perspective. The camera
 * is always pointed towards the center but can be moved around a sphere
 * and moved further in or outwards, using the mouse.
 * 
 * @author tkuester
 */
public abstract class CameraComponent extends JComponent {
	
	private static final long serialVersionUID = 3151904194557857942L;

	// OPTIONS FOR DRAWING

	/** whether to draw orthogonal lines on XY plane and in Z direction */
	public static boolean drawOrthogonals = false;
	
	/** whether to draw X/Y/Z axes */
	public static boolean drawCoordinateAxes = false;
	
	/** whether to draw lines or point cloud */
	public static boolean drawLines = true;
	
	
	// MEMBER VARIABLES / CURRENT STATE
	
	/** the camera's position */
	protected final Camera camera;
	
	/**
	 * Create new camera component.
	 */
	public CameraComponent() {
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
		
		if (drawCoordinateAxes) {
			double extend = 10_000;
			Point3D[] endpoints = {new Point3D(extend, 0, 0), new Point3D(-extend, 0, 0),
					               new Point3D(0, extend, 0), new Point3D(0, -extend, 0),
					               new Point3D(0, 0, extend), new Point3D(0, 0, -extend)};
			g.setColor(Color.WHITE);
			for (Point3D point : endpoints) {
				Point p = projection(normalize(point, yaw, pitch, camera.distance), W, H);
				g.drawLine(W/2, H/2, p.x, p.y);
			}
		}
		
		// draw the actual model
		drawModel(g, yaw, pitch);
		
		// show camera position
		g.setColor(Color.WHITE);
		g.drawString(this.camera.toString(), 10, 10);
	}
	
	/**
	 * Abstract method for drawing the actual model
	 */
	protected abstract void drawModel(Graphics g, double yaw, double pitch);

	/*
	 * SOME HELPER FUNCTIONS
	 */
	
	protected Point3D normalize(Point3D p, double yaw, double pitch, double distance) {
		// determine horizontal angle and position
		double dxy = distance(p.x, p.y);
		double a = angle(p.x, p.y, dxy);
		double x2 = Math.cos(a - yaw) * dxy;
		double y2 = Math.sin(a - yaw) * dxy;

		// determine vertical angle and position
		double dxz = distance(x2, p.z);
		double b = angle(x2, p.z, dxz);
		double x3 = Math.cos(b - pitch) * dxz;
		double z2 = Math.sin(b - pitch) * dxz;
		
		// if particle is in front of camera
		double x4 = camera.distance - x3;

		return new Point3D(x4, y2, z2);
	}
	
	protected Point projection(Point3D p, int width, int height) {
		int side = Math.max(width, height);
		int horz = (int) ( width/2 + (p.y / p.x) * side/2); 
		int vert = (int) (height/2 + (p.z / p.x) * side/2);
		return new Point(horz, vert);
	}

	protected double distance(double x, double y) {
		return Math.sqrt(x*x + y*y);
	}
	
	protected double angle(double x, double y, double d) {
		return d == 0 ? 0 : Math.acos(x / d) * (y > 0 ? +1 : -1); 
	}
	
	/**
	 * Class for encapsulating the current orientation of the camera.
	 * All angles are in degrees.
	 * 
	 * @author tkuester
	 */
	protected class Camera {
		public double yaw = 0;
		public double pitch = 0;
		public double distance = 10000;
		
		@Override
		public String toString() {
			return String.format(Locale.ENGLISH, 
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
		}
		
		@Override
		public void mouseDragged(MouseEvent e) {
			int dx = e.getX() - x;
			int dy = e.getY() - y;
			x = e.getX();
			y = e.getY();
			
			CameraComponent.this.camera.yaw -= dx;
			CameraComponent.this.camera.pitch -= dy;
			CameraComponent.this.repaint();
		}
		
		@Override
		public void mouseWheelMoved(MouseWheelEvent e) {
			double amount = 1 + (e.getWheelRotation() * .1);
			CameraComponent.this.camera.distance *= amount;
			CameraComponent.this.repaint();
		}
	}

}
