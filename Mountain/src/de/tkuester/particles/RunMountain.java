package de.tkuester.particles;

import java.util.Arrays;
import java.util.List;

import javax.swing.JFrame;
import javax.swing.SwingUtilities;

import de.tkuester.particles.model.Line;
import de.tkuester.particles.model.Mountain;
import de.tkuester.particles.model.Point3D;
import de.tkuester.particles.model.Triangle;

/**
 * Class for running/testing the mountain. This just creates a new mountain 
 * and a component for displaying it, embeds it into a plain frame.
 * 
 * @author tkuester
 */
public class RunMountain {

	public static void main(String[] args) throws Exception {

		double s = 100;
		Point3D t = new Point3D( 0,  0, -s);
		Point3D a = new Point3D( s,  0,  0);
		Point3D b = new Point3D( 0,  s,  0);
		Point3D c = new Point3D(-s,  0,  0);
		Point3D d = new Point3D( 0, -s,  0);

		Line edgeA = new Line(t, a);
		Line edgeB = new Line(b, t);
		Line edgeC = new Line(t, c);
		Line edgeD = new Line(d, t);
		Line baseAB = new Line(a, b);
		Line baseCB = new Line(c, b);
		Line baseCD = new Line(c, d);
		Line baseAD = new Line(a, d);
		
		List<Triangle> sides = Arrays.asList(
				new Triangle(baseAB, edgeB, edgeA),
				new Triangle(baseCB, edgeC, edgeB),
				new Triangle(baseCD, edgeC, edgeD),
				new Triangle(baseAD, edgeA, edgeD));
				
		Mountain mountain = new Mountain(sides);

		runMountainFrame(mountain, 600);
	}
	
	/**
	 * Create a Frame for running and showing the Universe. The universe is
	 * advanced in regular intervals and the frame is updated accordingly.
	 * 
	 * @param mountain		the mountain to show
	 * @param size			size of the frame (both width and height)
	 */
	public static void runMountainFrame(Mountain mountain, int size) {
		SwingUtilities.invokeLater(() -> {
			// create frame with UniverseComponent
			JFrame frame = new JFrame("Mountain");
			frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
			frame.getContentPane().add(new MountainComponent(mountain));
			frame.pack();
			frame.setSize(size, size);
			frame.setVisible(true);
		});
	}
	
}
