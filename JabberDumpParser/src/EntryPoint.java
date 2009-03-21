import DumpParser.LineParser;
import DumpParser.FileException;
import DumpParser.LogBuilder;
import GUI.BaseForm;

public class EntryPoint {

	public static void main(String[] args) {
		switch (args.length) {
		case 0:
			new BaseForm();
			break;
		case 1:
			if ("--help".equalsIgnoreCase(args[0]) || "/?".equalsIgnoreCase(args[0])) {
				System.out.println("no parametrs for GUI, <fileName> for CLI");
			} else {
				try {
					LineParser parser = new LineParser(args[0]);
					parser.doParse();
					LogBuilder lBuilder = parser.getLogBuilder();
					lBuilder.saveAll();
				} catch (FileException e) {
					System.out.println(e.getMessage());
				}
			}
			break;
		default:
			System.out.println("no parametrs for GUI, <fileName> for CLI");
			break;
		}
	}

}
