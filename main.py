import io
import tkinter as tk
from pytube import YouTube
from pytube import Search
from PIL import Image, ImageTk
import urllib.request
from tkinter import messagebox


class MainWindow:
    def __init__(self):

        # Windows Information
        self.__root = tk.Tk()
        self.__root.title('Youtube Downloader')
        self.__root.geometry('310x330')
        self.__root.resizable(width=False, height=False)

        # Title
        self.__title = tk.Label(self.__root, text='Youtube Downloader by QLAUSE', font='montserrat')
        self.__title.pack()

        # Create Frame For Search Entry
        self.__mainframe = tk.Frame(self.__root)
        self.__mainframe.pack(pady=20)

        # Search Entry + Search Button
        self.__link = tk.StringVar()

        self.__search = tk.Entry(self.__mainframe, textvariable=self.__link, width=30)
        self.__search.grid(row=0, columnspan=3, pady=5)

        self.__search_button = tk.Button(self.__mainframe, text='Search', command=self.search)
        self.__search_button.grid(row=0, column=3, columnspan=2)

        # Next Button
        self.__next_button = tk.Button(self.__mainframe, text='More >', command=self.more)
        self.__next_button.grid(row=1, column=3)

        # ListBox + scrollbar
        self.__scrollbar = tk.Scrollbar(self.__mainframe, orient='horizontal')

        self.__list_box = tk.Listbox(self.__mainframe, width=35, xscrollcommand=self, selectmode='single')
        self.__list_box.grid(row=1, columnspan=3, padx=10, pady=5)

        self.__scrollbar.config(command=self.__list_box.xview)
        self.__scrollbar.grid(row=2, columnspan=3, sticky='nsew')

        # Download Button
        self.__download_button = tk.Button(self.__mainframe, text='Download', command=self.download, width=10)
        self.__download_button.grid(row=3, column=2)

        # Option
        self.__quality = ['High-Quality', '720p', '480p', 'Audio-Only']
        self.__quality_selected = tk.StringVar()
        self.__quality_selected.set('720p')

        self.__options = tk.OptionMenu(self.__mainframe, self.__quality_selected, *self.__quality)
        self.__options.grid(row=3, column=1)

        self.__root.mainloop()

    # Search Func
    def search(self):
        global vid_name

        self.__list_box.delete(0, tk.END)
        inp_user = str(self.__link.get())

        if inp_user[0:5] == 'https':

            user_link = YouTube(inp_user)
            vid_name = Search(user_link.title)
            self.__list_box.insert(0, vid_name.results[0].title)

        else:
            vid_name = Search(inp_user)
            for i in range(0, 5):
                self.__list_box.insert(i, vid_name.results[i].title)

    # Download Func
    @staticmethod
    def complete(link, path):
        messagebox.showinfo("Completed", f"""Video has Downloaded\nFile Saved at {path}""")
        print(link)

    def download(self):

        if self.__quality_selected.get() == 'High-Quality':

            selected_vid = self.__list_box.curselection()[0]
            vid_name.results[selected_vid].register_on_complete_callback(self.complete)

            selected_vid = vid_name.results[selected_vid].streams.get_highest_resolution()
            selected_vid.download('DownloadedVideo')

        elif self.__quality_selected.get() == '720p' or self.__quality_selected.get() == '480p':

            selected_vid = self.__list_box.curselection()[0]
            vid_name.results[selected_vid].register_on_complete_callback(self.complete)

            selected_vid = vid_name.results[selected_vid].streams.filter(progressive=True,
                                                                         res=self.__quality_selected.get()).first()
            selected_vid.download('DownloadedVideo')

        elif self.__quality_selected.get() == 'Audio-Only':

            selected_vid = self.__list_box.curselection()[0]
            vid_name.results[selected_vid].register_on_complete_callback(self.complete)

            selected_vid = vid_name.results[selected_vid].streams.filter(only_audio=True).first()
            selected_vid.download('DownloadedVideo')

    # Next Button
    def more(self):

        if self.__quality_selected.get() == 'High-Quality':
            selected_vid = self.__list_box.curselection()[0]
            selected_vid = vid_name.results[selected_vid].streams.filter(adaptive=True).first()
            thumbnail = vid_name.results[self.__list_box.curselection()[0]].thumbnail_url

            VidInfo(selected_vid, thumbnail, vid_name.results[self.__list_box.curselection()[0]])

        elif self.__quality_selected.get() == '720p' or self.__quality_selected.get() == '480p':

            res = str(self.__quality_selected.get())

            selected_vid = self.__list_box.curselection()[0]
            selected_vid = vid_name.results[selected_vid].streams.filter(res=res).first()
            thumbnail = vid_name.results[self.__list_box.curselection()[0]].thumbnail_url

            VidInfo(selected_vid, thumbnail, vid_name.results[self.__list_box.curselection()[0]])

        elif self.__quality_selected.get() == 'Audio-Only':
            selected_vid = self.__list_box.curselection()[0]
            selected_vid = vid_name.results[selected_vid].streams.filter(only_audio=True).first()
            thumbnail = vid_name.results[self.__list_box.curselection()[0]].thumbnail_url

            VidInfo(selected_vid, thumbnail, vid_name.results[self.__list_box.curselection()[0]])

        else:
            messagebox.showinfo("Info", """Video/Audio Not Available. Try Another Video's type""")


class VidInfo:
    def __init__(self, link, link_thumbnail, links):
        self.__top_level = tk.Toplevel()
        self.__top_level.title(f"""Pre-view Video""")
        self.__top_level.resizable(width=False, height=False)
        # self.__top_level.geometry('700x520')

        # Title
        self.__label = tk.Label(self.__top_level, text=link.title)
        self.__label.pack()

        # Vid Info Filesize
        self.__filesize = tk.Label(self.__top_level, text=f"File Size : {link.filesize / 1000000} MB")
        self.__filesize.pack()

        # Vid Info Views
        self.__views = tk.Label(self.__top_level, text=f"Views Times : {links.views} times")
        self.__views.pack()

        # Vid Info Author
        self.__author = tk.Label(self.__top_level, text=f"Author : {links.author}")
        self.__author.pack()

        # Vid Info Length
        self.__Length = tk.Label(self.__top_level, text=f"Vid Length : {links.length / 60} Min")
        self.__author.pack()

        # Thumbnail
        self.__req = urllib.request.urlopen(link_thumbnail).read()

        self.__img = ImageTk.PhotoImage(Image.open(io.BytesIO(self.__req)))
        self.__thumbnail = tk.Label(self.__top_level, text='ardial', image=self.__img)
        self.__thumbnail.image = self.__img
        self.__thumbnail.pack(fill="both", expand="yes")


if __name__ == '__main__':
    hai = MainWindow()
