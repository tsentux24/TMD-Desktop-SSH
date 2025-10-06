from tkinter import *
from tkinter import messagebox, ttk, scrolledtext
import os
import socket
import paramiko
import subprocess
import threading
import tempfile

# Variabel global untuk mode
dark_mode = False
ssh_client = None

root = Tk()
###-----------------------------------------------------------------------------------------
root.title("TMD Desktop - Modern SSH Client")
app_width=500
app_height=550
screen_width=root.winfo_screenwidth()
screen_height=root.winfo_screenheight()
x =(screen_width / 2) - (app_width / 2)
y =(screen_height / 2) - (app_height /2)
root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
root.resizable(False, False)
root.configure(bg='#3C467B')

# Warna tema light
LIGHT_THEME = {
    'bg_main': '#3C467B',
    'bg_frame': '#50589C',
    'bg_header': '#636CCB',
    'accent': '#6E8CFB',
    'text_primary': '#FFFFFF',
    'text_secondary': '#E0E0E0',
    'input_bg': '#FFFFFF',
    'input_fg': '#000000',
    'input_placeholder': '#888888'
}

# Warna tema dark
DARK_THEME = {
    'bg_main': '#1A1A2E',
    'bg_frame': '#16213E',
    'bg_header': '#0F3460',
    'accent': '#6E8CFB',
    'text_primary': '#FFFFFF',
    'text_secondary': '#B0B0B0',
    'input_bg': '#2D3047',
    'input_fg': '#FFFFFF',
    'input_placeholder': '#888888'
}

current_theme = LIGHT_THEME

def toggle_dark_mode():
    global dark_mode, current_theme
    dark_mode = not dark_mode
    
    if dark_mode:
        current_theme = DARK_THEME
        btn_mode.config(text='☀️ Light Mode', bg='#FFD700', fg='#000000')
    else:
        current_theme = LIGHT_THEME
        btn_mode.config(text='🌙 Dark Mode', bg=current_theme['accent'], fg=current_theme['text_primary'])
    
    apply_theme()

def apply_theme():
    root.configure(bg=current_theme['bg_main'])
    main_frame.configure(bg=current_theme['bg_frame'])
    header_frame.configure(bg=current_theme['bg_header'])
    form_frame.configure(bg=current_theme['bg_frame'])
    footer_frame.configure(bg=current_theme['bg_frame'])
    
    # Update labels
    title_label.configure(bg=current_theme['bg_header'], fg=current_theme['text_primary'])
    subtitle_label.configure(bg=current_theme['bg_header'], fg=current_theme['text_secondary'])
    lbl.configure(bg=current_theme['bg_frame'], fg=current_theme['text_primary'])
    lbl_username.configure(bg=current_theme['bg_frame'], fg=current_theme['text_primary'])
    lbl_password.configure(bg=current_theme['bg_frame'], fg=current_theme['text_primary'])
    footer_label.configure(bg=current_theme['bg_frame'], fg=current_theme['text_secondary'])
    
    # Update input fields
    for entry in [txt_ip, txt_username, txt_password]:
        entry.configure(bg=current_theme['input_bg'], fg=current_theme['input_fg'])
        if entry.get() in ['Enter IP Address', 'Enter Username', 'Enter Password']:
            entry.configure(fg=current_theme['input_placeholder'])
    
    # Update button
    btnopen.configure(bg=current_theme['accent'], fg=current_theme['text_primary'])

###------------------------------------------------------------------------------------------------
# Frame utama untuk konten
main_frame = Frame(root, bg=current_theme['bg_frame'], bd=0, highlightthickness=0, 
                  relief='ridge', highlightbackground=current_theme['accent'])
main_frame.place(x=50, y=80, width=400, height=420)

# Header dengan gradient effect
header_frame = Frame(main_frame, bg=current_theme['bg_header'], height=80, bd=0, highlightthickness=0)
header_frame.pack(fill=X)
header_frame.pack_propagate(False)

title_label = Label(header_frame, text="SSH Connection", font=("Microsoft YaHei UI Light", 20, "bold"), 
                   bg=current_theme['bg_header'], fg=current_theme['text_primary'])
title_label.pack(expand=True, pady=(10, 0))

subtitle_label = Label(header_frame, text="Secure Remote Access", font=("Microsoft YaHei UI Light", 10), 
                      bg=current_theme['bg_header'], fg=current_theme['text_secondary'])
subtitle_label.pack(expand=True, pady=(0, 10))

# Container untuk form
form_frame = Frame(main_frame, bg=current_theme['bg_frame'], bd=0, highlightthickness=0)
form_frame.pack(fill=BOTH, expand=True, padx=30, pady=25)

###------------------------------------------------------------------------------------------------
# Fungsi untuk efek hover pada input fields
def on_enter_field(e):
    e.widget.config(bg=current_theme['accent'], fg=current_theme['text_primary'])
    e.widget.config(highlightbackground=current_theme['accent'], highlightthickness=1)

def on_leave_field(e):
    e.widget.config(bg=current_theme['input_bg'], fg=current_theme['input_fg'])
    e.widget.config(highlightbackground=current_theme['bg_frame'], highlightthickness=1)
    if e.widget.get() in ['Enter IP Address', 'Enter Username', 'Enter Password']:
        e.widget.config(fg=current_theme['input_placeholder'])

# Fungsi untuk efek hover pada button
def on_enter_button(e):
    e.widget.config(bg='#8BA3FB', fg=current_theme['text_primary'])

def on_leave_button(e):
    e.widget.config(bg=current_theme['accent'], fg=current_theme['text_primary'])

###------------------------------------------------------------------------------------------------
lbl = Label(form_frame, text="IP Address : ", font=("Microsoft YaHei UI Light", 11, "bold"), 
            bg=current_theme['bg_frame'], fg=current_theme['text_primary'])
lbl.grid(row=0, column=0, sticky='w', pady=(0, 15))

lbl_username = Label(form_frame, text="Username :", font=("Microsoft YaHei UI Light", 11, "bold"), 
                    bg=current_theme['bg_frame'], fg=current_theme['text_primary'])
lbl_username.grid(row=1, column=0, sticky='w', pady=(15, 15))

lbl_password = Label(form_frame, text="Password :", font=("Microsoft YaHei UI Light", 11, "bold"), 
                    bg=current_theme['bg_frame'], fg=current_theme['text_primary'])
lbl_password.grid(row=2, column=0, sticky='w', pady=(15, 15))

###----------------------------------------------------------------------------------------------------
def on_enter_ip(e):
    if txt_ip.get() == 'Enter IP Address':
        txt_ip.delete(0, 'end')
        txt_ip.config(fg=current_theme['input_fg'])

def on_leave_ip(e):
    if txt_ip.get() == "":
        txt_ip.insert(0, 'Enter IP Address')
        txt_ip.config(fg=current_theme['input_placeholder'])

txt_ip = Entry(form_frame, width=25, bg=current_theme['input_bg'], fg=current_theme['input_placeholder'],
               font=("Microsoft YaHei UI Light", 11), border=0, highlightthickness=1,
               highlightbackground=current_theme['bg_frame'])
txt_ip.grid(row=0, column=1, padx=(15, 0), pady=(0, 15), ipady=8)
txt_ip.insert(0, 'Enter IP Address')
txt_ip.bind('<FocusIn>', on_enter_ip)
txt_ip.bind('<FocusOut>', on_leave_ip)
txt_ip.bind('<Enter>', on_enter_field)
txt_ip.bind('<Leave>', on_leave_field)

###---------------------------------------------------------------------------------------------------------
def on_enter_user(e):
    if txt_username.get() == 'Enter Username':
        txt_username.delete(0, 'end')
        txt_username.config(fg=current_theme['input_fg'])

def on_leave_user(e):
    if txt_username.get() == "":
        txt_username.insert(0, 'Enter Username')
        txt_username.config(fg=current_theme['input_placeholder'])

txt_username = Entry(form_frame, width=25, bg=current_theme['input_bg'], fg=current_theme['input_placeholder'],
                    font=("Microsoft YaHei UI Light", 11), border=0, highlightthickness=1,
                    highlightbackground=current_theme['bg_frame'])
txt_username.grid(row=1, column=1, padx=(15, 0), pady=(15, 15), ipady=8)
txt_username.insert(0, 'Enter Username')
txt_username.bind('<FocusIn>', on_enter_user)
txt_username.bind('<FocusOut>', on_leave_user)
txt_username.bind('<Enter>', on_enter_field)
txt_username.bind('<Leave>', on_leave_field)

###--------------------------------------------------------------------------------------------------------
def on_enter_pass(e):
    if txt_password.get() == 'Enter Password':
        txt_password.delete(0, 'end')
        txt_password.config(fg=current_theme['input_fg'], show='*')

def on_leave_pass(e):
    if txt_password.get() == "":
        txt_password.insert(0, 'Enter Password')
        txt_password.config(fg=current_theme['input_placeholder'], show='')

txt_password = Entry(form_frame, width=25, bg=current_theme['input_bg'], fg=current_theme['input_placeholder'],
                    font=("Microsoft YaHei UI Light", 11), border=0, highlightthickness=1,
                    highlightbackground=current_theme['bg_frame'])
txt_password.grid(row=2, column=1, padx=(15, 0), pady=(15, 15), ipady=8)
txt_password.insert(0, 'Enter Password')
txt_password.config(show='')
txt_password.bind('<FocusIn>', on_enter_pass)
txt_password.bind('<FocusOut>', on_leave_pass)
txt_password.bind('<Enter>', on_enter_field)
txt_password.bind('<Leave>', on_leave_field)

###------------------------------------------------------------------------------------------------------------------------------
# Fungsi-fungsi untuk tombol di dashboard
def tarik_data_transaksi():
    messagebox.showinfo("Tarik Data Transaksi", "Fungsi tarik data transaksi dijalankan!")

def edit_network_conf():
    messagebox.showinfo("Edit Network Configuration", "Membuka editor network configuration...")

def edit_script_penarikan():
    messagebox.showinfo("Edit Script Penarikan Data", "Membuka editor script penarikan data...")

def edit_getsamba():
    messagebox.showinfo("Edit Getsamba", "Membuka konfigurasi getsamba...")

def edit_freeds():
    def load_freetds_config():
        try:
            # Cek apakah file ada dan bisa dibaca
            stdin, stdout, stderr = ssh_client.exec_command('ls -la /etc/freetds/freetds.conf')
            file_info = stdout.read().decode()
            
            if "No such file" in file_info:
                status_label.config(text="File /etc/freetds/freetds.conf tidak ditemukan", fg="red")
                return
            
            # Baca file freetds.conf via SSH
            stdin, stdout, stderr = ssh_client.exec_command('cat /etc/freetds/freetds.conf')
            file_content = stdout.read().decode()
            
            if stderr.read().decode():
                status_label.config(text="Tidak dapat membaca file. Periksa hak akses.", fg="red")
                return
            
            # Tampilkan di text editor
            editor_text.delete(1.0, END)
            editor_text.insert(1.0, file_content)
            status_label.config(text="File berhasil dimuat", fg="green")
            
        except Exception as e:
            status_label.config(text=f"Error memuat file: {str(e)}", fg="red")

    def save_freetds_config():
        try:
            # Dapatkan konten yang diedit
            new_content = editor_text.get(1.0, END).strip()
            
            if not new_content:
                messagebox.showerror("Error", "Konten tidak boleh kosong!")
                return
            
            # Method 1: Coba menggunakan echo dengan sudo -S (membaca password dari stdin)
            password = txt_password.get()  # Password dari login
            
            # Buat file sementara di local system
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.conf') as temp_file:
                temp_file.write(new_content)
                temp_local_path = temp_file.name
            
            try:
                # Upload file menggunakan SCP
                scp_client = ssh_client.open_sftp()
                
                # Upload ke temporary location di remote server
                temp_remote_path = f"/tmp/freetds_temp_{os.getpid()}.conf"
                scp_client.put(temp_local_path, temp_remote_path)
                scp_client.close()
                
                # Coba beberapa method untuk copy dengan hak root
                
                # Method 1: Gunakan sudo dengan echo password
                commands = [
                    f'echo "{password}" | sudo -S cp {temp_remote_path} /etc/freetds/freetds.conf',
                    f'echo "{password}" | sudo -S chmod 644 /etc/freetds/freetds.conf',
                    f'echo "{password}" | sudo -S chown root:root /etc/freetds/freetds.conf'
                ]
                
                success = True
                for cmd in commands:
                    stdin, stdout, stderr = ssh_client.exec_command(cmd)
                    exit_status = stdout.channel.recv_exit_status()
                    error_output = stderr.read().decode()
                    
                    if exit_status != 0 and "password" not in error_output.lower():
                        success = False
                        break
                
                if success:
                    status_label.config(text="File berhasil disimpan!", fg="green")
                    messagebox.showinfo("Success", "freetds.conf berhasil diperbarui!")
                    
                    # Bersihkan file temporary
                    ssh_client.exec_command(f'rm -f {temp_remote_path}')
                    os.unlink(temp_local_path)
                    
                    return
                
                # Method 2: Jika method 1 gagal, coba dengan expect
                status_label.config(text="Mencoba method alternatif...", fg="orange")
                
                # Gunakan tee dengan sudo
                command = f'cat {temp_remote_path} | sudo tee /etc/freetds/freetds.conf > /dev/null'
                stdin, stdout, stderr = ssh_client.exec_command(command)
                exit_status = stdout.channel.recv_exit_status()
                
                if exit_status == 0:
                    # Set permission
                    ssh_client.exec_command('sudo chmod 644 /etc/freetds/freetds.conf')
                    ssh_client.exec_command('sudo chown root:root /etc/freetds/freetds.conf')
                    
                    status_label.config(text="File berhasil disimpan!", fg="green")
                    messagebox.showinfo("Success", "freetds.conf berhasil diperbarui!")
                else:
                    error_msg = stderr.read().decode()
                    status_label.config(text=f"Gagal menyimpan: {error_msg}", fg="red")
                    messagebox.showerror("Error", f"Gagal menyimpan file: {error_msg}")
                
                # Bersihkan file temporary
                ssh_client.exec_command(f'rm -f {temp_remote_path}')
                os.unlink(temp_local_path)
                
            except Exception as e:
                # Bersihkan file temporary jika ada error
                try:
                    os.unlink(temp_local_path)
                    ssh_client.exec_command(f'rm -f /tmp/freetds_temp_*.conf')
                except:
                    pass
                raise e
                
        except Exception as e:
            status_label.config(text=f"Error menyimpan file: {str(e)}", fg="red")
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

    def check_sudo_access():
        """Cek apakah user memiliki akses sudo"""
        try:
            stdin, stdout, stderr = ssh_client.exec_command('sudo -n true')
            exit_status = stdout.channel.recv_exit_status()
            return exit_status == 0
        except:
            return False

    # Buat window editor
    editor_window = Toplevel()
    editor_window.title("Edit Freetds Configuration - /etc/freetds/freetds.conf")
    editor_window.geometry("800x600")
    editor_window.configure(bg=current_theme['bg_main'])

    # Header
    header_frame = Frame(editor_window, bg=current_theme['bg_header'], height=60)
    header_frame.pack(fill=X)
    header_frame.pack_propagate(False)
    
    Label(header_frame, text="Edit Freetds Configuration", 
          font=("Microsoft YaHei UI Light", 16, "bold"),
          bg=current_theme['bg_header'], fg=current_theme['text_primary']).pack(expand=True)
    
    Label(header_frame, text="/etc/freetds/freetds.conf", 
          font=("Microsoft YaHei UI Light", 10),
          bg=current_theme['bg_header'], fg=current_theme['text_secondary']).pack(expand=True)

    # Toolbar dengan tombol
    toolbar = Frame(editor_window, bg=current_theme['bg_frame'], height=40)
    toolbar.pack(fill=X, padx=10, pady=5)
    toolbar.pack_propagate(False)

    btn_load = Button(toolbar, text="📥 Load File", font=("Arial", 10, "bold"),
                     bg="#28a745", fg="white", command=load_freetds_config)
    btn_load.pack(side=LEFT, padx=5)

    btn_save = Button(toolbar, text="💾 Save", font=("Arial", 10, "bold"),
                     bg="#007bff", fg="white", command=save_freetds_config)
    btn_save.pack(side=LEFT, padx=5)

    # Status label
    status_label = Label(toolbar, text="Ready", font=("Arial", 9),
                        bg=current_theme['bg_frame'], fg="gray")
    status_label.pack(side=RIGHT, padx=10)

    # Text editor area
    editor_frame = Frame(editor_window, bg=current_theme['bg_main'])
    editor_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

    # Label untuk line numbers
    line_numbers = Text(editor_frame, width=4, padx=4, takefocus=0, border=0,
                       bg='#2b2b2b', fg='#858585', state='disabled')
    line_numbers.pack(side=LEFT, fill=Y)

    # Main text editor
    editor_text = scrolledtext.ScrolledText(editor_frame, wrap=WORD, 
                                          bg='#1e1e1e', fg='#d4d4d4',
                                          insertbackground='white',
                                          selectbackground='#264f78',
                                          font=("Consolas", 10))
    editor_text.pack(side=LEFT, fill=BOTH, expand=True)

    def update_line_numbers(event=None):
        line_numbers.config(state='normal')
        line_numbers.delete(1.0, END)
        
        # Hitung jumlah baris
        line_count = editor_text.get(1.0, END).count('\n')
        
        # Tambahkan nomor baris
        line_numbers_content = '\n'.join(str(i) for i in range(1, line_count + 1))
        line_numbers.insert(1.0, line_numbers_content)
        line_numbers.config(state='disabled')

    # Bind events untuk update line numbers
    editor_text.bind('<KeyRelease>', update_line_numbers)
    editor_text.bind('<MouseWheel>', update_line_numbers)
    editor_text.bind('<Button-1>', update_line_numbers)

    # Footer info
    footer_frame = Frame(editor_window, bg=current_theme['bg_frame'], height=30)
    footer_frame.pack(fill=X)
    footer_frame.pack_propagate(False)
    
    # Cek sudo access
    sudo_access = check_sudo_access()
    access_text = "Akses root tersedia" if sudo_access else "Akses root diperlukan"
    access_color = "green" if sudo_access else "orange"
    
    info_label = Label(footer_frame, 
                      text=f"Note: {access_text}. File akan disimpan dengan hak akses root",
                      font=("Arial", 8), bg=current_theme['bg_frame'], fg=access_color)
    info_label.pack(expand=True)

    # Load file secara otomatis saat window dibuka
    editor_window.after(100, load_freetds_config)

def delete_file_log():
    result = messagebox.askyesno("Delete File Log", "Apakah Anda yakin ingin menghapus file log?")
    if result:
        messagebox.showinfo("Success", "File log berhasil dihapus!")

def cek_koneksi_ping():
    def ping_host():
        try:
            output = subprocess.check_output(f"ping -c 4 {txt_ip.get()}", shell=True, stderr=subprocess.STDOUT)
            result_text.delete(1.0, END)
            result_text.insert(END, output.decode())
        except subprocess.CalledProcessError as e:
            result_text.delete(1.0, END)
            result_text.insert(END, f"Ping failed:\n{e.output.decode()}")
    
    ping_window = Toplevel(root)
    ping_window.title("Cek Koneksi PING")
    ping_window.geometry("500x300")
    ping_window.configure(bg=current_theme['bg_main'])
    
    Label(ping_window, text=f"PING to {txt_ip.get()}", font=("Arial", 12, "bold"), 
          bg=current_theme['bg_main'], fg=current_theme['text_primary']).pack(pady=10)
    
    result_text = scrolledtext.ScrolledText(ping_window, width=60, height=15)
    result_text.pack(padx=10, pady=10, fill=BOTH, expand=True)
    
    # Jalankan ping di thread terpisah
    threading.Thread(target=ping_host).start()

def telnet_connection():
    messagebox.showinfo("Telnet", "Membuka koneksi Telnet...")

def create_dashboard():
    global dashboard, terminal_text
    dashboard = Toplevel(root)
    dashboard.title("TMD Desktop - Dashboard")
    dashboard.geometry("800x600")
    dashboard.configure(bg=current_theme['bg_main'])
    
    # Header Dashboard
    header_dash = Frame(dashboard, bg=current_theme['bg_header'], height=80)
    header_dash.pack(fill=X)
    header_dash.pack_propagate(False)
    
    Label(header_dash, text="TMD Desktop Dashboard", font=("Microsoft YaHei UI Light", 20, "bold"),
          bg=current_theme['bg_header'], fg=current_theme['text_primary']).pack(expand=True)
    
    Label(header_dash, text=f"Connected to: {txt_ip.get()}", font=("Microsoft YaHei UI Light", 10),
          bg=current_theme['bg_header'], fg=current_theme['text_secondary']).pack(expand=True)
    
    # Main Content
    main_content = Frame(dashboard, bg=current_theme['bg_main'])
    main_content.pack(fill=BOTH, expand=True, padx=20, pady=20)
    
    # Grid untuk tombol-tombol
    buttons = [
        ("📊 Tarik Data Transaksi", tarik_data_transaksi),
        ("🌐 Edit Network Conf", edit_network_conf),
        ("📝 Edit Script Penarikan Data", edit_script_penarikan),
        ("🔄 Edit Getsamba", edit_getsamba),
        ("⚙️ Edit Freeds", edit_freeds),
        ("🗑️ Delete File Log", delete_file_log),
        ("📡 Cek Koneksi (PING)", cek_koneksi_ping),
        ("🔌 Telnet", telnet_connection)
    ]
    
    row, col = 0, 0
    for text, command in buttons:
        btn = Button(main_content, text=text, font=("Microsoft YaHei UI Light", 11, "bold"),
                    bg=current_theme['accent'], fg=current_theme['text_primary'],
                    command=command, width=20, height=2, relief="flat", cursor="hand2")
        btn.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Hover effect
        btn.bind('<Enter>', lambda e, b=btn: b.config(bg='#8BA3FB'))
        btn.bind('<Leave>', lambda e, b=btn: b.config(bg=current_theme['accent']))
        
        col += 1
        if col > 1:  # 2 kolom per baris
            col = 0
            row += 1
    
    # Configure grid weights
    for i in range(2):
        main_content.grid_columnconfigure(i, weight=1)
    for i in range(4):
        main_content.grid_rowconfigure(i, weight=1)
    
    # Terminal/Output Section
    terminal_frame = Frame(dashboard, bg=current_theme['bg_frame'])
    terminal_frame.pack(fill=X, padx=20, pady=10)
    
    Label(terminal_frame, text="Output Terminal", font=("Arial", 10, "bold"),
          bg=current_theme['bg_frame'], fg=current_theme['text_primary']).pack(anchor='w')
    
    terminal_text = scrolledtext.ScrolledText(terminal_frame, height=8, bg='black', fg='white')
    terminal_text.pack(fill=X, padx=5, pady=5)
    terminal_text.insert(END, f"Connected to {txt_ip.get()} via SSH\n")
    terminal_text.config(state=DISABLED)

def click():
    global ssh_client
    username = txt_username.get()
    password = txt_password.get()
    ip_address = txt_ip.get()
    
    # Validasi input
    if ip_address == "" or ip_address == "Enter IP Address":
        messagebox.showerror("Input Error", "Please enter a valid IP address")
        return
        
    if username == "" or username == "Enter Username":
        messagebox.showerror("Input Error", "Please enter a username")
        return
        
    if password == "" or password == "Enter Password":
        messagebox.showerror("Input Error", "Please enter a password")
        return
    
    # Coba koneksi SSH
    if username == "pinisi" and password == "royal32":
        try:
            # Buat koneksi SSH
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(ip_address, username=username, password=password, allow_agent=False, timeout=10)
            
            messagebox.showinfo("Success", "Login successful! Opening dashboard...")
            root.withdraw()  # Sembunyikan window login
            create_dashboard()
            dashboard.protocol("WM_DELETE_WINDOW", lambda: (ssh_client.close(), dashboard.destroy(), root.destroy()))
            
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect: {str(e)}")
    else:
        messagebox.showerror("Invalid", "Access denied! Please check username or password")

# Button dengan styling yang lebih modern
btnopen = Button(form_frame, text="🚀 Connect to Server", font=("Microsoft YaHei UI Light", 12, "bold"), 
                bg=current_theme['accent'], fg=current_theme['text_primary'], border=0, cursor="hand2", 
                command=click, width=18, height=1, relief="flat")
btnopen.grid(row=3, column=0, columnspan=2, pady=(25, 10))
btnopen.bind('<Enter>', on_enter_button)
btnopen.bind('<Leave>', on_leave_button)

# Footer dengan informasi tambahan
footer_frame = Frame(main_frame, bg=current_theme['bg_frame'], height=30, bd=0, highlightthickness=0)
footer_frame.pack(fill=X, side=BOTTOM)
footer_frame.pack_propagate(False)

footer_label = Label(footer_frame, text="PT Pinisi-Elektra © 2024 | Secure SSH Client", 
                    font=("Microsoft YaHei UI Light", 8), bg=current_theme['bg_frame'], 
                    fg=current_theme['text_secondary'])
footer_label.pack(expand=True)

# Dark Mode Toggle Button
btn_mode = Button(root, text='🌙 Dark Mode', font=("Microsoft YaHei UI Light", 10, "bold"),
                 bg=current_theme['accent'], fg=current_theme['text_primary'], border=0,
                 cursor="hand2", command=toggle_dark_mode, relief="flat")
btn_mode.place(x=350, y=30, width=120, height=30)

# Status indicator
status_label = Label(root, text="● Ready", font=("Microsoft YaHei UI Light", 9),
                    bg=current_theme['bg_main'], fg="#00FF00")
status_label.place(x=50, y=35)

root.mainloop()