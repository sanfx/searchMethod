#!/usr/bin/env python
 
'''
Copyright (c) 2009 John Schember 
 
Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
 
import sys

from PyQt4.Qt import Qt, QObject, QApplication, QLineEdit, QCompleter, \
	QStringListModel, SIGNAL
 
TAGS = ['Nature', 'buildings', 'home', 'City', 'country', 'Berlin']
 
class CompleterLineEdit(QLineEdit):
 
	def __init__(self, *args):
		QLineEdit.__init__(self, *args)
 
		QObject.connect(self, SIGNAL('textChanged(QString)'), self.text_changed)
 
	def text_changed(self, text):
		all_text = unicode(text)
		text = all_text[:self.cursorPosition()]
		prefix = text.split(',')[-1].strip()
 
		text_tags = []
		for t in all_text.split(','):
			t1 = unicode(t).strip()
			if t1 != '':
				text_tags.append(t)
		text_tags = list(set(text_tags))
 
		self.emit(SIGNAL('text_changed(PyQt_PyObject, PyQt_PyObject)'),
			text_tags, prefix)
 
	def complete_text(self, text):
		cursor_pos = self.cursorPosition()
		before_text = unicode(self.text())[:cursor_pos]
		after_text = unicode(self.text())[cursor_pos:]
		prefix_len = len(before_text.split(',')[-1].strip())
		self.setText('%s%s, %s' % (before_text[:cursor_pos - prefix_len], text,
			after_text))
		self.setCursorPosition(cursor_pos - prefix_len + len(text) + 2)
 
 
class TagsCompleter(QCompleter):
 
	def __init__(self, parent, all_tags):
		QCompleter.__init__(self, all_tags, parent)
		self.all_tags = set(all_tags)
 
	def update(self, text_tags, completion_prefix):
		tags = list(self.all_tags.difference(text_tags))
		model = QStringListModel(tags, self)
		self.setModel(model)
 
		self.setCompletionPrefix(completion_prefix)
		if completion_prefix.strip() != '':
			self.complete()
 
 
def main():
	app = QApplication(sys.argv)
 
	editor = CompleterLineEdit()
 
	completer = TagsCompleter(editor, TAGS)
	completer.setCaseSensitivity(Qt.CaseInsensitive)
 
	QObject.connect(editor,
		SIGNAL('text_changed(PyQt_PyObject, PyQt_PyObject)'),
		completer.update)
	QObject.connect(completer, SIGNAL('activated(QString)'),
		editor.complete_text)
 
	completer.setWidget(editor)
 
	editor.show()
 
	return app.exec_()
 
if __name__ == '__main__':
	main()