package DumpParser;

import java.io.CharArrayReader;
import java.io.IOException;
import java.io.Reader;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.xml.sax.SAXException;

public class Record {

	private static final String XML_PROLOG = "<?xml version='1.0' encoding='UTF-8'?>";
	private static long count = 0;
	private static long error = 0;

	enum LineType {
		ROUTE, NORM, WRONG, NONE
	};

	enum RawType {
		MESSAGE, PRESENCE, IQ, DB, XDB, ROUTE
	};

	enum MesType {
		CHAT, GROUPCHAT
	};

	private LineType lineType;
	private RawType rawType;
	private MesType mesType;

	private String date = "";
	private String from = "";
	private String to = "";
	private String message = "";
	private String raw = "";
	private String password = "";
	private String ip = "";
	private String status = "";
	private String role = "";

	Record() {
		lineType = LineType.NONE;
		count++;
	}

	void parseRaw() {
		if (lineType.equals(LineType.WRONG)) {
			return;
		}
		DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
		factory.setIgnoringElementContentWhitespace(true);
		factory.setValidating(false);
		try {
			// TODO Метод работает слишком медленно! Возможно стоит попробовать regexp-ы
			raw = XML_PROLOG.concat(raw);

			DocumentBuilder builder = factory.newDocumentBuilder();
			Reader reader = new CharArrayReader(raw.toCharArray());
			Document doc = builder.parse(new org.xml.sax.InputSource(reader));
			Element el = doc.getDocumentElement();

			class Presence {
				private Element el;

				Presence(Element el) {
					this.el = el;
				}

				void parsePresence() {
					try {
						if (!el.getAttribute("to").equals("")) {
							to = el.getAttribute("to");
						}
						if (!el.getAttribute("from").equals("")) {
							from = el.getAttribute("from");
						}

						Element tmp = (Element) el.getElementsByTagName("password").item(0);
						if (tmp != null) {
							password = tmp.getTextContent();
						}

						tmp = (Element) el.getElementsByTagName("item").item(0); // права
						if (tmp != null) {
							role = tmp.getAttribute("affiliation");
							role = role + "/" + tmp.getAttribute("role");
						}

						tmp = (Element) el.getElementsByTagName("show").item(0); // изменение статуса
						if (tmp != null) {
							status = tmp.getTextContent();
						}

						tmp = (Element) el.getElementsByTagName("title").item(0); // заголовок статуса
						if (tmp != null) {
							status = status + " " + tmp.getTextContent();
						}

						tmp = (Element) el.getElementsByTagName("status").item(0); // содержание статуса
						if (tmp != null) {
							status = status + "(" + tmp.getTextContent() + ")";
						}

					} catch (Exception e) {
						System.out.println(date + " [" + lineType + "] " + raw);
						e.printStackTrace();
					}
				}
			}

			class Message {
				private Element el;

				Message(Element el) {
					this.el = el;
				}

				void parseMessage() {
					try {
						if (!el.getAttribute("to").equals("")) {
							to = el.getAttribute("to");
						}
						if (!el.getAttribute("from").equals("")) {
							from = el.getAttribute("from");
						}

						if ("chat".equals(el.getAttribute("type"))) {
							mesType = MesType.CHAT;
						} else if ("groupchat".equals(el.getAttribute("type"))) {
							mesType = MesType.GROUPCHAT;
						}

						Element tmp = (Element) el.getElementsByTagName("body").item(0);
						if (tmp != null) {
							message = tmp.getTextContent();
						}

					} catch (Exception e) {
						System.out.println(date + " [" + lineType + "] " + raw);
						e.printStackTrace();
					}
				}
			}

			if (el.getNodeName().equalsIgnoreCase("xdb")) {
				rawType = RawType.XDB;
				return;
			} else if (el.getNodeName().equalsIgnoreCase("route")) {
				rawType = RawType.ROUTE;
				to = el.getAttribute("to");
				from = el.getAttribute("from");
				ip = el.getAttribute("ip");
			} else if (el.getNodeName().equalsIgnoreCase("presence")) {
				rawType = RawType.PRESENCE;
				new Presence(el).parsePresence();
			} else if (el.getNodeName().equalsIgnoreCase("iq")) {
				rawType = RawType.IQ;
				// TODO В IQ бывает vCard неплохо бы их разбирать вплоть до <PHOTO><TYPE>image/png</TYPE><BINVAL>
			} else if (el.getNodeName().equalsIgnoreCase("db:verify")) {
				rawType = RawType.DB;
			} else if (el.getNodeName().equalsIgnoreCase("message")) {
				rawType = RawType.MESSAGE;
				new Message(el).parseMessage();
			}
		} catch (ParserConfigurationException e) {
			e.printStackTrace();
		} catch (SAXException e) {
			if (raw.length() > 1000) {
				System.out.println(date + " [" + lineType + "] " + raw.substring(0, 500) + " ... "
						+ raw.substring(raw.length() - 500, raw.length()));
			} else {
				System.out.println(date + " [" + lineType + "] " + raw);
			}
			lineType = LineType.WRONG;
			error++;
			return;
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	void setType(LineType type) {
		this.lineType = type;
	}

	void setDate(String date) {
		this.date = date;
	}

	void setRaw(String raw) {
		this.raw = raw;
	}

	void appendRaw(String append) {
		raw += append;
	}

	LineType getLineType() {
		return lineType;
	}

	RawType getRawType() {
		return rawType;
	}

	MesType getMesType() {
		return mesType;
	}

	String getDate() {
		return date;
	}

	String getFrom() {
		return from;
	}

	String getTo() {
		return to;
	}

	String getMessage() {
		return message;
	}

	static long getCount() {
		return count;
	}

	static long getErrorCount() {
		return error;
	}

	static void cleanCount() {
		count = 0;
	}

	static void cleanErrorCount() {
		error = 0;
	}

	String getPassword() {
		return password;
	}

	String getIp() {
		return ip;
	}

	String getRole() {
		return role;
	}

	String getStatus() {
		return status;
	}

}
