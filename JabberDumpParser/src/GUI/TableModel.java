package GUI;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;

import javax.swing.table.AbstractTableModel;

import DumpParser.LogBuilder;
import DumpParser.LogBuilder.Chat;
import DumpParser.LogBuilder.Room;
import GUI.BaseForm.LogType;

@SuppressWarnings("serial")
public class TableModel extends AbstractTableModel {

	private ArrayList<String> items;

	private HashMap<String, Room> rooms;
	private HashMap<String, String> passwords;
	private HashMap<HashSet<String>, Chat> chats;
	private LogType logType;

	public TableModel(LogType logType, LogBuilder logBuilder) {
		this.logType = logType;
		items = new ArrayList<String>();

		if (logBuilder == null) {
			return;
		}

		if (logType == LogType.Rooms) {
			rooms = logBuilder.getRooms();
			Iterator<String> iterator = rooms.keySet().iterator();
			while (iterator.hasNext()) {
				items.add(iterator.next());
			}
		}
		if (logType == LogType.Chats) {
			chats = logBuilder.getChats();
			Iterator<HashSet<String>> chatIter = chats.keySet().iterator();
			while (chatIter.hasNext()) {
				String[] nicks = (String[]) chatIter.next().toArray();
				items.add(nicks[0] + " - " + nicks[1]);
			}
		}
		if (logType == LogType.Privates) {
			// TODO Сперва доделать дампинг приватов
		}
		if (logType == LogType.Passwords) {
			passwords = logBuilder.getPasswords();
			Iterator<String> iterator = passwords.keySet().iterator();
			while (iterator.hasNext()) {
				items.add(iterator.next());
			}
		}
	}

	public int getColumnCount() {
		return 1;
	}

	public int getRowCount() {
		return items.size();
	}

	public Object getValueAt(int rowIndex, int columnIndex) {
		return items.get(rowIndex);
	}

	public String getLogByKey(String key) {
		if (logType == LogType.Rooms) {
			return rooms.get(key).getLog();
		}
		if (logType == LogType.Passwords) {
			return passwords.get(key);
		}
		if (logType == LogType.Chats) {
			HashSet<String> fromTo = new HashSet<String>();
			fromTo.add(key.substring(0, key.indexOf(" -")));
			fromTo.add(key.substring(key.indexOf("- "), key.length()));
			return chats.get(fromTo).getLog();
		}
		if (logType == LogType.Privates) {
			// TODO Сперва доделать дампинг приватов
		}

		return null;
	}
}
