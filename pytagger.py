from gi.repository import GdkPixbuf, Gtk, Gio, GLib
from mutagen.flac import FLAC

class HeaderBarWindow(Gtk.Window):
    # Audio file
	audio = None

    # GTK+ Objects
    # TODO: Implement dialogue & logic for album cover button
	button_cover = Gtk.Button().new()
	entry_title = Gtk.Entry()
	entry_artist = Gtk.Entry()
	entry_album = Gtk.Entry()
	entry_year = Gtk.Entry()
	header = Gtk.HeaderBar()

 	# Load file
	def load(self, filename):
		# TODO: Verify input
		self.audio = FLAC(filename)
		# TODO: Search for cover art in list, if proper not found use first
		pi = self.audio.pictures[0]

		# Header title as filename
		self.header.props.title = filename[filename.rfind("/") + 1:]

		# Song Album Cover
		pic_loader = GdkPixbuf.PixbufLoader().new_with_mime_type(pi.mime)
		pic_loader.write(pi.data)
		pic_loader.close()
		pic = pic_loader.get_pixbuf()
		pic = pic.scale_simple(150, 150, GdkPixbuf.InterpType.BILINEAR)
		cover = Gtk.Image.new_from_pixbuf(pic)
		self.button_cover.set_image(cover)

		# Load metadata
		# TODO: Place checks for empty, if empty emplace what should be there
		# TODO: Manage synonymous tag names
		self.entry_title.set_text(self.audio["TITLE"][0])
		self.entry_artist.set_text(self.audio["ARTIST"][0])
		self.entry_album.set_text(self.audio["ALBUM"][0])
		self.entry_year.set_text(self.audio["DATE"][0])

	def save(self):
		# Write info from GTK.Entry to audio object
		self.audio["TITLE"] = self.entry_title.get_text()
		self.audio["ARTIST"] = self.entry_artist.get_text()
		self.audio["ALBUM"] = self.entry_album.get_text()
		self.audio["DATE"] = self.entry_year.get_text()

		# TODO: Implement cover art

		# Save audio object tags to file
		self.audio.save()

	def __init__(self):
		self.load("/home/nerolathe/Music/she/Axiom/Axiom.flac")

		# Create Window
		Gtk.Window.__init__(self, title="PyTagger")
		self.set_border_width(10)
		self.set_default_size(400, 200)

  		## Utilize HeaderBar ##
		self.header.set_show_close_button(True)
		self.header.props.title = "Please open a file"
		self.set_titlebar(self.header)

  		# Open File Button
		open_button = Gtk.Button()
		open_icon = Gio.ThemedIcon(name="document-open-symbolic")
		open_image = Gtk.Image.new_from_gicon(open_icon, Gtk.IconSize.BUTTON)
		open_button.add(open_image)
		self.header.pack_start(open_button)

  		# Save File Button
  		# TODO: Implement save
		save_button = Gtk.Button()
		save_icon = Gio.ThemedIcon(name="document-save-symbolic")
		save_image = Gtk.Image.new_from_gicon(save_icon, Gtk.IconSize.BUTTON)
		save_button.add(save_image)
		self.header.pack_start(save_button)

  		## Main Grid ##
		grid = Gtk.Grid()
		self.add(grid)

		# Song Title
		self.entry_title.set_text("Title")

		# Song Artist
		self.entry_artist.set_text("Artist")

  		# Song Album Name
		self.entry_album.set_text("Album")

		# Song Publication Year
		self.entry_year.set_text("Year")

  		# Align each element
		grid.attach(self.entry_title, 1, 0, 1, 1)
		grid.attach(self.entry_artist, 1, 1, 1, 1)
		grid.attach(self.entry_album, 1, 2, 1, 1)
		grid.attach(self.entry_year, 1, 3, 1, 1)
		grid.attach(self.button_cover, 0, 0, 1, 4)

		# Ensure spacing is pretty
		grid.set_row_spacing(6)
		grid.set_column_spacing(6)

		# Connect button and callback functions
		open_button.connect("clicked", self.on_open_clicked)
		save_button.connect("clicked", self.on_save_clicked)


	def on_open_clicked(self, open_button):
		filter_flac = Gtk.FileFilter()
		filter_flac.set_name("FLAC")
		filter_flac.add_mime_type("audio/flac")

		dialogue = Gtk.FileChooserDialog("Please select a .flac file", self, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
		dialogue.add_filter(filter_flac)
		dialogue.run()
		self.load(dialogue.get_filename())
		dialogue.destroy()

	def on_save_clicked(self, open_button):
		self.save()


win = HeaderBarWindow()
# Don't want a bunch of whitespace
win.set_resizable(False)
# Just using a random icon
win.set_icon_name("text-editor-symbolic")
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
