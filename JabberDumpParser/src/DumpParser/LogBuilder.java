package DumpParser;

import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.LinkedList;

import org.apache.commons.io.FileUtils;

import DumpParser.Record.MesType;
import DumpParser.Record.RawType;

public class LogBuilder {

	public class Room {
		private String prev = null;
		private String log = "";

		// TODO Собрать сюда все jid и nick участников чата
		@SuppressWarnings("unused")
		private HashMap<String, String> jidNick = null;
		@SuppressWarnings( { "unused" })
		private LinkedList<HashMap<String, String>> userlist = null;

		void appendLog(String time, String nick, String record) {
			log += time + " <" + nick + "> " + record;
		}

		void appendRaw(String raw) {
			int index = raw.indexOf("<") + 1;
			if (raw.substring(index, raw.length()).equals(prev)) {
				return;
			}
			prev = raw.substring(index, raw.length());
			log += "\n" + raw;
		}

		/**
		 * Лог комнаты
		 * 
		 * @return - строка с логом
		 */
		public String getLog() {
			return log;
		}

		/**
		 * Сохраняет лог комнаты в файл
		 * 
		 * @param fileName
		 *            - имя файла
		 */
		public void saveToFile(String fileName) {
			File file = new File(fileName);
			try {
				FileUtils.writeStringToFile(file, log, "UTF-8");
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}

	/**
	 * Чат
	 * 
	 * @author anon
	 */
	public class Chat {
		private String log = "";

		void appendLog(String time, String nick, String record) {
			log += time + " <" + nick + "> " + record + "\n";
		}

		/**
		 * Возвращает лог чата
		 * 
		 * @return - строка с логом
		 */
		public String getLog() {
			return log;
		}

		/**
		 * Сохраняет чат в файл
		 * 
		 * @param fileName
		 *            - имя файла
		 */
		public void saveToFile(String fileName) {
			File file = new File(fileName);
			try {
				FileUtils.writeStringToFile(file, log, "UTF-8");
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}

	HashMap<String, Room> rooms = null;
	HashMap<String, String> passwords = null;
	HashMap<HashSet<String>, Chat> chats = null;

	LogBuilder() {
		rooms = new HashMap<String, Room>();
		passwords = new HashMap<String, String>();
		chats = new HashMap<HashSet<String>, Chat>();
	}

	void addRecord(Record record) {
		if (record == null) {
			return;
		}
		record.parseRaw();
		if (!isInteresting(record)) {
			return;
		}

		if (record.getRawType() == RawType.MESSAGE && record.getMesType() == MesType.CHAT) {

			HashSet<String> fromTo = new HashSet<String>();
			int index = record.getTo().indexOf("/");
			if (index != -1) {
				fromTo.add(record.getTo().substring(0, index));
			} else {
				fromTo.add(record.getTo());
			}
			index = record.getFrom().indexOf("/");
			if (index != -1) {
				fromTo.add(record.getFrom().substring(0, index));
			} else {
				fromTo.add(record.getFrom());
			}

			if (getRoomName(record.getTo()) == null && getRoomName(record.getFrom()) == null) {

				Chat chat = null;
				if (chats.containsKey(fromTo)) {
					chat = chats.get(fromTo);
					chat.appendLog(record.getDate(), record.getFrom(), record.getMessage());
				} else {
					chat = new Chat();
					chat.appendLog(record.getDate(), record.getFrom(), record.getMessage());
					chats.put(fromTo, chat);
				}
			} else {
				// TODO Здесь надо таким же образом собрать приваты комнат, но в моем логе их нет 
			}
			return;
		}

		// TODO Переделать этот метод, чтобы он соибрал не только пароли
		if (getRoomName(record.getTo()) != null && record.getPassword().length() > 0) {
			String room = "";
			int index = record.getTo().indexOf("/");
			if (index == -1) {
				room = record.getTo();
			} else {
				room = record.getTo().substring(0, index);
			}
			if (!passwords.containsKey(room)) {
				passwords.put(room, record.getPassword());
			}
			return;
		}

		String roomName = getRoomName(record.getFrom());
		if (roomName != null) {
			Room room = new Room();
			String sender = record.getFrom().substring(record.getFrom().indexOf("/") + 1, record.getFrom().length());

			if (record.getRawType() == RawType.MESSAGE) {
				room.appendLog(record.getDate(), sender, record.getMessage());
			} else if (record.getRawType() == RawType.PRESENCE) {
				room.appendLog(record.getDate(), sender, record.getStatus() + " " + record.getPassword() + " "
						+ record.getIp() + " " + record.getRole());
			}

			if (rooms.containsKey(roomName)) {
				Room tmp = rooms.get(roomName);
				tmp.appendRaw(room.getLog());
			} else {
				rooms.put(roomName, room);
			}
		}

	}

	private String getRoomName(String jid) {
		int index = jid.indexOf("@conference");
		int sep = jid.indexOf("/");
		if (index != -1 && sep == -1) {
			return jid;
		}
		if (index != -1 && sep != -1) {
			return jid.substring(0, sep);
		}
		return null;
	}

	private boolean isInteresting(Record record) {
		if (record.getRawType() == RawType.IQ || record.getRawType() == RawType.DB
				|| record.getRawType() == RawType.XDB || record.getRawType() == RawType.ROUTE) {
			return false;
		}
		return true;
	}

	/**
	 * Сохраняет на диск все логи
	 */
	public void saveAll() {

		Iterator<String> iterator = rooms.keySet().iterator();
		while (iterator.hasNext()) {
			String room = iterator.next();
			rooms.get(room).saveToFile(room);
		}

		iterator = passwords.keySet().iterator();
		String out = "";
		while (iterator.hasNext()) {
			String roomKey = iterator.next();
			out += roomKey + "\t" + passwords.get(roomKey) + "\n";
		}
		try {
			File file = new File("passwords");
			FileUtils.writeStringToFile(file, out, "UTF-8");
		} catch (IOException e) {
			e.printStackTrace();
		}

		Iterator<HashSet<String>> chatIter = chats.keySet().iterator();
		while (chatIter.hasNext()) {
			HashSet<String> fromTo = chatIter.next();
			try {
				File file = new File(fromTo.toString());
				FileUtils.writeStringToFile(file, chats.get(fromTo).getLog(), "UTF-8");
			} catch (IOException e) {
				e.printStackTrace();
			}

		}
	}

	/**
	 * @return - Хешмап <Имя комнаты, Команта>
	 */
	public HashMap<String, Room> getRooms() {
		return rooms;
	}

	/**
	 * @return - Хешмап <Имя комнаты, Пароль команты>
	 */
	public HashMap<String, String> getPasswords() {
		return passwords;
	}

	/**
	 * @return - Хешмап <Хешсет из двух строк с jid-ами пользователей, Чат>
	 */
	public HashMap<HashSet<String>, Chat> getChats() {
		return chats;
	}

}
