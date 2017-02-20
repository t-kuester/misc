package de.tkuester.space3d.particles;

import java.awt.Color;
import java.awt.Graphics;
import java.awt.Point;
import java.util.LinkedList;
import java.util.Map;
import java.util.stream.Collectors;

import de.tkuester.space3d.CameraComponent;
import de.tkuester.space3d.Point3D;
import de.tkuester.space3d.particles.model.Particle;
import de.tkuester.space3d.particles.model.Universe;

/**
 * Component for displaying a universe of particles.
 * 
 * @author tkuester
 */
public class UniverseComponent extends CameraComponent {
	
	private static final long serialVersionUID = -3154952439452964085L;

	// OPTIONS FOR DRAWING
	
	/** whether to draw orthogonal lines on XY plane and in Z direction */
	public static boolean drawOrthogonals = false;
	
	/** length of speed arrows as multiple of speed; 0 -> no vectors */
	public static int speedVectorLength = 0;
	
	/** length of particle trail to draw; 0 -> no trail */
	public static int trailLength = 3;
	
	/** how many steps to skip between trail segments; makes trails longer but more rugged */
	public static int trailSkip = 3; 
	
	// MEMBER VARIABLES / CURRENT STATE
	
	/** the universe to draw */
	private final Universe universe;
	
	/** holds some past positions of particles, for drawing trails */
	private final Map<Particle, LinkedList<Point3D>> particleTrails;
	
	/**
	 * Create new universe component.
	 * 
	 * @param universe	the universe
	 */
	public UniverseComponent(Universe universe) {
		super();
		this.universe = universe;
		this.particleTrails = this.universe.particles.stream()
				.collect(Collectors.toMap(p -> p, p -> new LinkedList<>()));
	}
	
	@Override
	protected synchronized void drawModel(Graphics g, double yaw, double pitch) {
		final int W = this.getWidth();
		final int H = this.getHeight();
		
		for (Particle particle : this.universe.particles) {
			
			// normalize particle's position w.r.t. camera
			Point3D norm = normalize(particle.pos, yaw, pitch, camera.distance);
			
			// if particle is in front of camera
			if (norm.x > 0) {
				// determine position on screen
				Point p = projection(norm, W, H);
				
				// draw lines from (0,0,0) to (x,y,0) and further to (x,y,z)
				if (drawOrthogonals) {
					Point3D posXY = new Point3D(particle.pos.x, particle.pos.y, 0);
					Point p2 = projection(normalize(posXY, yaw, pitch, camera.distance), W, H);

					g.setColor(Color.DARK_GRAY);
					g.drawLine(W/2, H/2, p2.x, p2.y);
					g.drawLine(p2.x, p2.y, p.x, p.y);
				}
				
				if (speedVectorLength > 0) {
					Point3D speed = particle.pos.add(particle.speed.mult(speedVectorLength));
					Point p2 = projection(normalize(speed, yaw, pitch, camera.distance), W, H);
					
					g.setColor(Color.YELLOW);
					g.drawLine(p.x, p.y, p2.x, p2.y);
				}
				
				if (trailLength > 0) {
					// store copy in list (only needed if pos is mutated)
					LinkedList<Point3D> trail = particleTrails.get(particle);
					if (trail.size() > trailLength) {
						trail.pop();
					}
					if (universe.step % trailSkip == 0) {
						trail.add(new Point3D(particle.pos.x, particle.pos.y, particle.pos.z));
					}
					// draw trails behind particles
					g.setColor(Color.BLUE);
					Point last = null;
					for (Point3D current : trail) {
						Point cur = projection(normalize(current, yaw, pitch, camera.distance), W, H);
						if (last != null) {
							g.drawLine(last.x, last.y, cur.x, cur.y);
						}
						last = cur;
					}
				}
				
				// finally, determine apparent size and draw particle itself
				if (0 <= p.x && p.x < W && 0 <= p.y && p.y < H) {
					double distance = norm.absolute();
					int s = Math.max((int) (particle.size / (distance / 100)), 1);
					
					// use color to indicate distance; further away -> dimmer
					float f = (float) Math.max(Math.min(camera.distance / distance, 1.0), 0.0);
					g.setColor(new Color(f, f, f));
					g.fillOval(p.x - s, p.y - s, 2*s, 2*s);
				}
			}
		}
	}

}
