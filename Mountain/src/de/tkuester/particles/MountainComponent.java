package de.tkuester.particles;

import java.awt.Color;
import java.awt.Graphics;
import java.awt.Point;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.event.MouseWheelEvent;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Locale;
import java.util.Set;

import javax.swing.JComponent;

import de.tkuester.particles.model.Line;
import de.tkuester.particles.model.Mountain;
import de.tkuester.particles.model.Point3D;
import de.tkuester.particles.model.Triangle;

/**
 * Component for displaying a fractal mountain. The points are shown
 * in a more or less correct three dimensional perspective. The camera is
 * always pointed towards the center but can be moved around a sphere and
 * moved further in or outwards, using the mouse.
 * 
 * @author tkuester
 */
public class MountainComponent extends JComponent {
	
	private static final long serialVersionUID = 3684311418667499852L;

	// OPTIONS FOR DRAWING

	/** whether to draw orthogonal lines on XY plane and in Z direction */
	public static boolean drawOrthogonals = false;
	
	/** whether to draw X/Y/Z axes */
	public static boolean drawCoordinateAxes = false;
	
	/** whether to draw lines or point cloud */
	public static boolean drawLines = true;
	
	
	// MEMBER VARIABLES / CURRENT STATE
	
	/** the mountain to draw */
	private final Mountain mountain;
	
	/** the camera's position */
	private final Camera camera;
	
	/**
	 * Create new mountain component.
	 * 
	 * @param mountain	the mountain
	 */
	public MountainComponent(Mountain mountain) {
		this.mountain = mountain;
		this.camera = new Camera();
		
		// add mouse listener for camera control
		CameraControl cameraControl = new CameraControl();
		this.addMouseListener(cameraControl);
		this.addMouseMotionListener(cameraControl);
		this.addMouseWheelListener(cameraControl);
		
		KeyboardControl keyboardControl = new KeyboardControl();
		this.addKeyListener(keyboardControl);
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
		
		synchronized (this.mountain) {
			
			Set<Object> drawn = new HashSet<>();
			
			Iterable<Triangle> triangles = this.mountain.getAllTriangles()::iterator;
			for (Triangle triangle : triangles) {
				for (Line line : Arrays.asList(triangle.ab, triangle.bc, triangle.ca)){
					if (! drawn.add(line)) continue;

					if (drawLines) {
						Point3D normSrc = normalize(line.source, yaw, pitch, camera.distance);
						Point3D normTgt = normalize(line.target, yaw, pitch, camera.distance);
						
						// if particle is in front of camera
						if (normSrc.x > 0 && normTgt.x > 0) {
							// determine position on screen
							Point pSrc = projection(normSrc, W, H);
							Point pTgt = projection(normTgt, W, H);
							g.setColor(Color.WHITE);
							g.drawLine(pSrc.x, pSrc.y, pTgt.x, pTgt.y);
						}
						continue;
					}
					
					List<Point3D> points = Arrays.asList(line.source, line.target);
					for (Point3D point : points) {
						if (! drawn.add(point)) continue;
						
						// normalize points' position w.r.t. camera
						Point3D norm = normalize(point, yaw, pitch, camera.distance);
						
						// if particle is in front of camera
						if (norm.x > 0) {
							// determine position on screen
							Point p = projection(norm, W, H);
							
							// draw lines from (0,0,0) to (x,y,0) and further to (x,y,z)
							if (drawOrthogonals) {
								Point3D posXY = new Point3D(point.x, point.y, 0);
								Point p2 = projection(normalize(posXY, yaw, pitch, camera.distance), W, H);
								
								g.setColor(Color.DARK_GRAY);
								g.drawLine(W/2, H/2, p2.x, p2.y);
								g.drawLine(p2.x, p2.y, p.x, p.y);
							}
							
							// finally, determine apparent size and draw particle itself
							if (0 <= p.x && p.x < W && 0 <= p.y && p.y < H) {
								double distance = norm.absolute();
								int s = Math.max((int) (1000. / distance), 1);
								
								// use color to indicate distance; further away -> dimmer
								float f = (float) Math.max(Math.min(camera.distance / distance, 1.0), 0.0);
								g.setColor(new Color(f, f, f));
								g.fillOval(p.x - s, p.y - s, 2*s, 2*s);
							}
						}
					}
				}
			}
		}
		// show camera position
		g.setColor(Color.WHITE);
		g.drawString(this.camera.toString(), 10, 10);
	}

	/*
	 * SOME HELPER FUNCTIONS
	 */
	
	private Point3D normalize(Point3D p, double yaw, double pitch, double distance) {
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
	
	private Point projection(Point3D p, int width, int height) {
		int side = Math.max(width, height);
		int horz = (int) ( width/2 + (p.y / p.x) * side/2); 
		int vert = (int) (height/2 + (p.z / p.x) * side/2);
		return new Point(horz, vert);
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
			if (e.getButton() == 3) {
				MountainComponent.this.mountain.expandAll();
				System.out.println(mountain.getAllTriangles().count());
				MountainComponent.this.repaint();
			} else {
				this.x = e.getX();
				this.y = e.getY();	
			}
		}
		
		@Override
		public void mouseDragged(MouseEvent e) {
			int dx = e.getX() - x;
			int dy = e.getY() - y;
			x = e.getX();
			y = e.getY();
			
			MountainComponent.this.camera.yaw -= dx;
			MountainComponent.this.camera.pitch -= dy;
			MountainComponent.this.repaint();
		}
		
		@Override
		public void mouseWheelMoved(MouseWheelEvent e) {
			double amount = 1 + (e.getWheelRotation() * .1);
			MountainComponent.this.camera.distance *= amount;
			MountainComponent.this.repaint();
		}
	}
	
	private class KeyboardControl extends KeyAdapter {
		
		@Override
		public void keyTyped(KeyEvent e) {
			// TODO fixme why is this not triggered?
			System.out.println(e);
			MountainComponent.this.mountain.expandAll();
			MountainComponent.this.repaint();
		}
		
	}
	

}
