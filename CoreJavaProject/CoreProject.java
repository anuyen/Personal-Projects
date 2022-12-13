package CoreProject;
import java.util.*;

class Batch {
	String batchTime; // am or pm
	
	public Batch(String batchTime) {
		this.batchTime = batchTime;
	}
	
	public void getInfo() {
		System.out.println("Participant belongs to the " + this.batchTime + " bactch");
	}
}

class Participant {
	String name;
	int age;
	
	public Participant(String name, int age) {
		this.name = name;
		this.age = age;
	}
	
	public Batch getTime(String ans) {
		if (ans.equals("am")) {
			return new Batch("am");
		} else if (ans.equals("pm")) {
			return new Batch("pm");
		} else {
			System.out.println("Please enter am or pm");
			return null;
		}
	}
	
	public Batch getTime(int ans) {
		if (ans >= 0 && ans <= 12) {
			return new Batch("am");
		} else if (ans > 12 && ans < 24) {
			return new Batch("pm");
		} else {
			System.out.println("Please enter a range between 0 to 24");
			return null;
		}
	}
	
	public void getInfo() {
		System.out.print("Participant name is " + this.name + "\n");
	}
	
}

public class CoreProject {

	public static void main(String[] args) {
		Scanner sc = new Scanner(System.in);
		System.out.println("Enter participant name: ");
		String pName = sc.next();
		
		System.out.println("Enter participant age: ");
		int pAge = sc.nextInt();
		
		Participant p = new Participant(pName,pAge);
		
		System.out.println("Would you like to run? (am, pm or a specific time between 0-24) ");
		String ans = sc.next();
		
		p.getInfo();
		if (ans.equals("am")) {
			Batch b = p.getTime(ans);
			b.getInfo();
		} else if (ans.equals("pm")) {
			Batch b = p.getTime(ans);
			b.getInfo();
		} else {
			int intAns = Integer.parseInt(ans);
			Batch b = p.getTime(intAns);
			b.getInfo();
		}
		
	}

}


















