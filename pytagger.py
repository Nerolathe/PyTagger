from gi.repository import GdkPixbuf, Gtk, Gio
from mutagen.flac import FLAC

class HeaderBarWindow(Gtk.Window):
	def __init__(self):
		# Create Window
		Gtk.Window.__init__(self, title="PyTagger")
		self.set_border_width(10)
		self.set_default_size(400, 200)

  		# Utilize HeaderBar
		hb = Gtk.HeaderBar()
		hb.set_show_close_button(True)
  		# should probably use a 20-char limit
		hb.props.title = "Veela.flac"
		self.set_titlebar(hb)

  		# Open File Button
		open_button = Gtk.Button()
		open_icon = Gio.ThemedIcon(name="document-open-symbolic")
		open_image = Gtk.Image.new_from_gicon(open_icon, Gtk.IconSize.BUTTON)
		open_button.add(open_image)
		hb.pack_start(open_button)

  		# Save File Button
		save_button = Gtk.Button()
		save_icon = Gio.ThemedIcon(name="document-save-symbolic")
		save_image = Gtk.Image.new_from_gicon(save_icon, Gtk.IconSize.BUTTON)
		save_button.add(save_image)
		hb.pack_start(save_button)

  		# Main grid
		grid = Gtk.Grid()
		self.add(grid)
		title = Gtk.Entry()
		title.set_text("Title")
		artist = Gtk.Entry()
		artist.set_text("Artist")
		album = Gtk.Entry()
		album.set_text("Album")
		year = Gtk.Entry()
		year.set_text("Year")
		rend = GdkPixbuf.Pixbuf.new_from_file_at_scale("test.png", 150, 150, True)
		pic = Gtk.Image.new_from_pixbuf(rend)
		pic.props.pixbuf = rend
		grid.attach(title, 1, 0, 1, 1)
		grid.attach(artist, 1, 1, 1, 1)
		grid.attach(album, 1, 2, 1, 1)
		grid.attach(year, 1, 3, 1, 1)
		grid.attach(pic, 0, 0, 1, 4)
		grid.set_row_spacing(6)
		grid.set_column_spacing(6)
		open_button.connect("clicked", self.on_save_clicked)

	def on_save_clicked(self, open_button):
		audio = FLAC("/home/nerolathe/Music/Veela/Veela - My Enemy.flac")
		print(audio["artist"][0])

win = HeaderBarWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
