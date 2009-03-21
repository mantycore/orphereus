package GUI;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Container;
import java.awt.Dimension;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.io.File;
import java.net.URL;

import javax.swing.AbstractAction;
import javax.swing.BorderFactory;
import javax.swing.ImageIcon;
import javax.swing.JComboBox;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JProgressBar;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import javax.swing.JToolBar;

import DumpParser.FileException;
import DumpParser.LineParser;
import DumpParser.LogBuilder;

@SuppressWarnings("serial")
public class BaseForm extends JFrame {

	private JTextField statusBar;
	private LogBuilder logBuilder;
	private File file;
	private JComboBox logTypeSelector;
	private JTable itemsTabel;
	private JTextArea log;
	private LineParser parser = null;
	private SwingWorker parse;
	private JProgressBar progressBar; 

	enum LogType {
		Rooms, Chats, Privates, Passwords;

		String getDescription() {
			if (this == LogType.Rooms) {
				return "Конференции";
			}
			if (this == LogType.Chats) {
				return "Чаты";
			}
			if (this == LogType.Privates) {
				return "Приватные чаты в комнатах";
			}
			if (this == LogType.Passwords) {
				return "Пароли от комнат";
			}
			return null;
		}
	}

	private JToolBar createToolBar() {
		final JToolBar toolbar = new JToolBar();
		toolbar.setFloatable(false);

		logTypeSelector = new JComboBox();
		logTypeSelector.addItem(LogType.Rooms);
		logTypeSelector.addItem(LogType.Chats);
		//		logTypeSelector.addItem(LogType.Privates);
		logTypeSelector.addItem(LogType.Passwords);
		logTypeSelector.setSelectedItem(null);
		logTypeSelector.setEnabled(false);

		logTypeSelector.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				LogType logType = (LogType) logTypeSelector.getSelectedItem();
				itemsTabel.setModel(new TableModel(logType, logBuilder));
				itemsTabel.getColumnModel().getColumn(0).setHeaderValue(logType.getDescription());
				itemsTabel.getColumnModel().getColumn(0).setMinWidth(295);
				statusBar.setText(logType.getDescription());
			}
		});

		toolbar.add(new Open());
		toolbar.add(new DoParse());
		toolbar.add(logTypeSelector);

		return toolbar;
	}

	class Open extends AbstractAction {

		public Open() {
			ImageIcon icon = null;
			URL iconURL = ClassLoader.getSystemResource("icons32/open.png");
			if (iconURL != null) {
				icon = new ImageIcon(iconURL);
			}
			putValue(AbstractAction.SMALL_ICON, icon);
			putValue(AbstractAction.SHORT_DESCRIPTION, "Открыть файл");
			putValue(AbstractAction.NAME, "Открыть");
		}

		public void actionPerformed(ActionEvent arg0) {
			logTypeSelector.setEnabled(false);

			JFileChooser fc = new JFileChooser();
			fc.setDialogTitle("Открыть файл с дампом");

			if (fc.showOpenDialog(BaseForm.this) == JFileChooser.APPROVE_OPTION) {
				file = fc.getSelectedFile();
				itemsTabel.setModel(new TableModel(null, logBuilder));
				itemsTabel.getColumnModel().getColumn(0).setHeaderValue(null);
				log.setText("");
				statusBar.setText("Файл готов к парсингу");
			} else {
				statusBar.setText("Файл не был загружен");
			}
		}
	}

	class DoParse extends AbstractAction {

		public DoParse() {
			ImageIcon icon = null;
			URL iconURL = ClassLoader.getSystemResource("icons32/parse.png");
			if (iconURL != null) {
				icon = new ImageIcon(iconURL);
			}
			putValue(AbstractAction.SMALL_ICON, icon);
			putValue(AbstractAction.SHORT_DESCRIPTION, "Начать парсинг");
			putValue(AbstractAction.NAME, "Парсить");

		}

		public void actionPerformed(ActionEvent arg0) {

			if (file == null) {
				statusBar.setText("Файл не выбран");
				return;
			}

			logTypeSelector.setEnabled(false);

			try {
				parser = new LineParser(file);
			} catch (FileException e) {
				statusBar.setText("Ошибка парсинга файла <" + file + "> " + e.getMessage());
				return;
			}

			parse = new SwingWorker() {
				public Object construct() {
					parser.doParse();
					return null;
				}

				public void finished() {
					statusBar.setText("Парсинг завершен, выбирете тип лога в верхнем меню");
					logBuilder = parser.getLogBuilder();
					logTypeSelector.setEnabled(true);
				}
			};
			parse.start();

//			pbar = new ProgressMonitor(BaseForm.this, "Прогресс", "Ждите...", 1, parser.getLineCount());
//			pbar.setMillisToPopup(10);
//			Timer timer = new Timer(100, this);
//			timer.start();

//			SwingUtilities.invokeLater(new Parsing());

			//			progressBar = new JProgressBar(1, parser.getLineCount());
			//			progressBar.setValue(parser.getCurLine());
		}
	}

	public BaseForm() {
		log = new JTextArea();
		log.setLineWrap(true);
		log.setWrapStyleWord(true);

		statusBar = new JTextField();
		statusBar.setEditable(false);
		statusBar.setBorder(BorderFactory.createLineBorder(Color.LIGHT_GRAY));

		itemsTabel = new JTable();
		itemsTabel.setAutoResizeMode(JTable.AUTO_RESIZE_OFF);
		itemsTabel.setFocusable(false);
		itemsTabel.setModel(new TableModel(null, logBuilder));
		itemsTabel.getColumnModel().getColumn(0).setHeaderValue(null);

		itemsTabel.addMouseListener(new MouseAdapter() {
			public void mouseClicked(MouseEvent e) {
				String key = (String) itemsTabel
						.getValueAt(itemsTabel.getSelectedRow(), itemsTabel.getSelectedColumn());
				log.setText(((TableModel) itemsTabel.getModel()).getLogByKey(key));
			}
		});

		JScrollPane tblPane = new JScrollPane(itemsTabel);
		tblPane.setBorder(BorderFactory.createLineBorder(Color.LIGHT_GRAY));
		tblPane.setPreferredSize(new Dimension(300, 300));

		JScrollPane logPane = new JScrollPane(log);
		logPane.setBorder(BorderFactory.createLineBorder(Color.LIGHT_GRAY));

		JPanel panel = new JPanel(new BorderLayout(), true);
		panel.add(createToolBar(), BorderLayout.NORTH);
		panel.add(tblPane, BorderLayout.WEST);
		panel.add(logPane, BorderLayout.CENTER);
		
//		progressBar = new JProgressBar(1, 100);
//		panel.add(progressBar, BorderLayout.SOUTH);
		panel.add(statusBar, BorderLayout.SOUTH);

		Container content = getContentPane();
		content.add(panel);

		setTitle("Logs viewer");
		setPreferredSize(new Dimension(800, 600));
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		pack();
		setVisible(true);
	}
}
