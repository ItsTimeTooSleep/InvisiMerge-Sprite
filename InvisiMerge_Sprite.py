import tkinter as tk
from tkinter import filedialog, messagebox, StringVar
from tkinter import ttk  # 导入ttk模块
import os
import sys  # 导入sys模块

class FileMergerApp:
    def __init__(self, master):
        self.master = master
        master.title("隐合精灵")

        # 设置图标
        if getattr(sys, 'frozen', False):  # 如果是打包后的exe文件
            icon_path = os.path.join(os.path.dirname(sys.executable), '图标.ico')
        else:  # 如果是.py文件
            icon_path = os.path.join(os.getcwd(), '图标.ico')
        
        try:
            master.iconbitmap(icon_path)  # 设置窗口图标
            master.wm_iconbitmap(icon_path)  # 设置任务栏图标
        except Exception as e:
            print(f"设置图标时出错: {e}")

        self.file1_path = StringVar()
        self.file2_path = StringVar()
        self.output_file_name = StringVar()
        self.output_directory = StringVar(value=os.getcwd())  # 默认保存位置为当前工作目录

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.master, text="文件1:（建议选择图片）").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        tk.Entry(self.master, textvariable=self.file1_path, width=50).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(self.master, text="选择文件", command=self.select_file1).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.master, text="文件2:（建议选择zip文件）").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        tk.Entry(self.master, textvariable=self.file2_path, width=50).grid(row=3, column=0, padx=5, pady=5)
        tk.Button(self.master, text="选择文件", command=self.select_file2).grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self.master, text="输出文件名:").grid(row=4, column=0, sticky='w', padx=5, pady=5)
        tk.Entry(self.master, textvariable=self.output_file_name, width=50).grid(row=5, column=0, padx=5, pady=5)

        tk.Label(self.master, text="保存位置:").grid(row=6, column=0, sticky='w', padx=5, pady=5)
        tk.Entry(self.master, textvariable=self.output_directory, width=50).grid(row=7, column=0, padx=5, pady=5)
        tk.Button(self.master, text="浏览", command=self.select_directory).grid(row=7, column=1, padx=5, pady=5)

        tk.Button(self.master, text="合并文件", command=self.merge_files).grid(row=8, column=0, columnspan=2, pady=10)
        
        self.progress = ttk.Progressbar(self.master, orient='horizontal', length=400, mode='determinate')
        self.progress.grid(row=9, column=0, columnspan=2, padx=5, pady=5)
        self.progress_label = tk.Label(self.master, text="")
        self.progress_label.grid(row=10, column=0, columnspan=2)

    def select_file1(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file1_path.set(file_path)
            # 设置输出文件名为文件1的名称
            output_name = os.path.splitext(file_path)[0] + os.path.splitext(file_path)[1]
            self.output_file_name.set(output_name)

    def select_file2(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file2_path.set(file_path)

    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_directory.set(directory)

    def merge_files(self):
        file1 = self.file1_path.get()
        file2 = self.file2_path.get()
        output_file_name = self.output_file_name.get()
        output_directory = self.output_directory.get()

        if not file1 or not file2 or not output_file_name:
            messagebox.showerror("错误", "请确保选择了两个文件并指定输出文件名。")
            return

        # 如果没有指定保存位置，则使用当前工作目录
        output_file = os.path.join(output_directory, output_file_name)

        try:
            total_size = os.path.getsize(file1) + os.path.getsize(file2)
            self.progress['maximum'] = total_size
            self.progress['value'] = 0

            with open(output_file, 'wb') as outfile:
                for fname in (file1, file2):
                    with open(fname, 'rb') as infile:
                        while True:
                            chunk = infile.read(1024)  # 每次读取1024字节
                            if not chunk:
                                break
                            outfile.write(chunk)
                            self.progress['value'] += len(chunk)  # 更新进度条
                            self.progress_label.config(text="合并中... 当前进度: {} bytes".format(self.progress['value']))
                            self.master.update_idletasks()  # 更新界面

            self.progress_label.config(text="合并成功！输出文件大小: {} bytes".format(os.path.getsize(output_file)))
        except Exception as e:
            messagebox.showerror("错误", f"合并文件时出错: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileMergerApp(root)
    root.mainloop()