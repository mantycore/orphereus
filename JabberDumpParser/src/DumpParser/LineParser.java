package DumpParser;

import java.io.File;
import java.io.IOException;

import org.apache.commons.io.FileSystemUtils;
import org.apache.commons.io.FileUtils;
import org.apache.commons.io.LineIterator;

import DumpParser.Record.LineType;

public class LineParser {
	private File file = null;
	private LogBuilder logBuilder = null;
	private int debugCounterLine = 0;
	private int currentLine = 0;

	/**
	 * @return - Содержит все возможные логи
	 */
	public LogBuilder getLogBuilder() {
		return logBuilder;
	}

	/**
	 * @param filename
	 *            - путь к файлу дампа
	 * @throws FileException
	 *             - всевозможные файловые ошибки
	 */
	public LineParser(String filename) throws FileException {
		file = preLoad(new File(filename));
	}

	/**
	 * @param file
	 *            - объект файл дампа
	 * @throws FileException
	 *             - всевозможные файловые ошибки
	 */
	public LineParser(File file) throws FileException {
		this.file = preLoad(file);
	}

	/**
	 * Обрабатывает все строки файла дампа
	 */
	public void doParse() {
		logBuilder = new LogBuilder();
		// TODO должно быть 0
		parse(5000);
	}

	/**
	 * Возвращает число строчек в файле
	 * 
	 * @return - число строк
	 */
	public int getLineCount() {
		if (debugCounterLine > 0) {
			return debugCounterLine;
		}
		LineIterator iterator = null;
		int count = 0;
		try {
			iterator = FileUtils.lineIterator(file, "UTF-8");
			while (iterator.hasNext()) {
				iterator.nextLine();
				count++;
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
		return count;
	}

	/**
	 * Возвращает текущую строку файла
	 * 
	 * @return - номер текущей обрабатыаемой линии
	 */
	public int getCurLine() {
		return currentLine;
	}

	private File preLoad(File file) throws FileException {
		if (!file.isFile()) {
			file = null;
			throw new FileException("is not a file");
		}
		if (!file.canRead()) {
			file = null;
			throw new FileException("can't read this file");
		}

		long freeSpaceByte = 0;
		try {
			freeSpaceByte = FileSystemUtils.freeSpaceKb(file.getAbsolutePath()) * 1024;
		} catch (IOException e) {
			e.printStackTrace();
		}

		long fileSizeByte = file.length();
		if (freeSpaceByte < fileSizeByte * 1.5) {
			file = null;
			throw new FileException("no free space on disk");
		}
		return file;
	}

	@SuppressWarnings("static-access")
	private void parse(int count) {
		debugCounterLine = count;
		LineIterator iterator = null;
		Record currentRecord = null;
		try {
			iterator = FileUtils.lineIterator(file, "UTF-8");

			if (iterator.hasNext()) {
				iterator.nextLine();
			}
			int i = 0;
			while (iterator.hasNext() && (count == 0 ? ++i > 0 : i++ < count)) {
				currentLine = i;
				String line = iterator.nextLine();
				
				if (line.length() == 0) {
					continue;
				}

				if (currentRecord == null && line.charAt(0) != '[') {
					continue;
				}

				if (line.charAt(0) != '[') {
					currentRecord.appendRaw(line);
					continue;
				}

				int first = 0;
				int next = line.indexOf("]") + 1;

				int len = "[16.02.2009 10:16:54.991749]".length();
				if (line.substring(first, next).length() > len || line.substring(first, next).length() < len - 5) {
					currentRecord.appendRaw(line.substring(next, line.length()));
					continue;
				}

				if (currentRecord != null) {
					logBuilder.addRecord(currentRecord);
				}

				currentRecord = new Record();
				try {
					currentRecord.setDate(line.substring(first, next).substring(0, 20) + "]");

					first = line.indexOf("[", first + 1);
					next = line.indexOf("]", next) + 1;
					String type = line.substring(first, next);

					if (type.contains("NORM")) {
						currentRecord.setType(LineType.NORM);
					} else if (type.contains("ROUTE")) {
						currentRecord.setType(LineType.ROUTE);
					} else {
						currentRecord.setType(LineType.WRONG);
						System.out.println(line);
					}

					currentRecord.setRaw(line.substring(next, line.length()));

				} catch (StringIndexOutOfBoundsException e) {
					System.out.println("line " + i + " " + line);
					e.printStackTrace();
					return;
				}

			}
			logBuilder.addRecord(currentRecord);

			System.out.println("file parsed:\t\t" + file.getAbsolutePath());
			System.out.println("lines parsed:\t\t" + i);
			System.out.println("records created:\t" + currentRecord.getCount());
			System.out.print(currentRecord.getErrorCount() > 0 ? "error objects: " + currentRecord.getErrorCount()
					+ "\n" : "");
			System.out.println();
			currentRecord.cleanCount();
			currentRecord.cleanErrorCount();

		} catch (IOException e) {
			e.printStackTrace();
		} finally {
			LineIterator.closeQuietly(iterator);
		}
	}
}
