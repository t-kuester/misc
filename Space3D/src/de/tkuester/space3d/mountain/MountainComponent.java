package de.tkuester.space3d.mountain;

import java.awt.Color;
import java.awt.Graphics;
import java.awt.Point;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import de.tkuester.space3d.CameraComponent;
import de.tkuester.space3d.Point3D;
import de.tkuester.space3d.mountain.model.Line;
import de.tkuester.space3d.mountain.model.Mountain;
import de.tkuester.space3d.mountain.model.Triangle;

/**
 * Component for displaying a fractal mountain.
 * 
 * @author tkuester
 */
public class MountainComponent extends CameraComponent {
	
	private static final long serialVersionUID = 3684311418667499852L;

	// OPTIONS FOR DRAWING

	/** whether to draw lines or point cloud */
	public static boolean drawLines = true;
	
	
	// MEMBER VARIABLES / CURRENT STATE
	
	/** the mountain to draw */
	private final Mountain mountain;
	
	
	/**
	 * Create new mountain component.
	 * 
	 * @param mountain	the mountain
	 */
	public MountainComponent(Mountain mountain) {
		super();
		this.mountain = mountain;
		
		this.addMouseListener(new MouseControl());
	}

	@Override
	protected void drawModel(Graphics g, double yaw, double pitch) {
		final int W = this.getWidth();
		final int H = this.getHeight();

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
	
	/**
	 * Expand another level by clicking right mouse button
	 *
	 * @author tkuester
	 */
	private class MouseControl extends MouseAdapter {
		
		@Override
		public void mouseClicked(MouseEvent e) {
			if (e.getButton() == 3) {
				MountainComponent.this.mountain.expandAll();
				MountainComponent.this.repaint();				
			}
		}
		
	}

}
