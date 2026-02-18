import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
import qrcode
from PIL import Image, ImageTk

# -----------------------------------------------------------
# GLOBAL SETTINGS (PURE WHITE THEME)
# -----------------------------------------------------------
BG = "#87CEEB"
FG = "#000000"

qr_fg_color = "black"
qr_bg_color = "white"

last_qr_img = None


# -----------------------------------------------------------
# MAIN WINDOW
# -----------------------------------------------------------
root = tk.Tk()
root.title("QR Generator")
root.geometry("1200x700")
root.configure(bg=BG)

style = ttk.Style()
style.theme_use("clam")
style.configure("TNotebook", background=BG)
style.configure("TFrame", background=BG)
style.configure("TNotebook.Tab", background=BG, foreground=FG)

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)


# -----------------------------------------------------------
# PREVIEW LABEL (CREATED ONCE — FIXES DOUBLE CLICK ISSUE)
# -----------------------------------------------------------
preview_label = tk.Label(root, bg=BG)
preview_label.pack(pady=10)


# -----------------------------------------------------------
# PREVIEW FUNCTION
# -----------------------------------------------------------
def show_qr_preview(img_original):
    preview_size = 400
    img = img_original.resize((preview_size, preview_size), Image.LANCZOS)
    tk_img = ImageTk.PhotoImage(img)

    preview_label.config(image=tk_img)
    preview_label.image = tk_img


# -----------------------------------------------------------
# COLOR CHOOSER
# -----------------------------------------------------------
def choose_fg_color():
    global qr_fg_color
    color = colorchooser.askcolor(title="Choose QR Color")[1]
    if color:
        qr_fg_color = color

def choose_bg_color():
    global qr_bg_color
    color = colorchooser.askcolor(title="Choose Background")[1]
    if color:
        qr_bg_color = color


# -----------------------------------------------------------
# UNIVERSAL QR GENERATOR
# -----------------------------------------------------------
def generate_qr(data, ec_level="M"):
    global last_qr_img

    ec_map = {
        "L": qrcode.constants.ERROR_CORRECT_L,
        "M": qrcode.constants.ERROR_CORRECT_M,
        "Q": qrcode.constants.ERROR_CORRECT_Q,
        "H": qrcode.constants.ERROR_CORRECT_H
    }

    qr = qrcode.QRCode(
        version=None,
        box_size=12,
        border=4,
        error_correction=ec_map.get(ec_level)
    )

    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(
        fill_color=qr_fg_color,
        back_color=qr_bg_color
    ).convert("RGB")

    last_qr_img = img
    show_qr_preview(img)


# -----------------------------------------------------------
# SAVE FUNCTION
# -----------------------------------------------------------
def save_qr():
    if last_qr_img is None:
        messagebox.showerror("Error", "Generate a QR first!")
        return

    save_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        initialfile="my_qr.png",
        filetypes=[("PNG Files", "*.png")]
    )

    if save_path:
        last_qr_img.save(save_path, dpi=(300, 300))


# -----------------------------------------------------------
# HELPER FUNCTIONS
# -----------------------------------------------------------
def make_label(parent, text):
    return tk.Label(parent, text=text, bg=BG, fg=FG, font=("Arial", 11))

def create_ec_dropdown(parent):
    make_label(parent, "Error Correction:").pack(pady=5)
    ec_cb = ttk.Combobox(parent, values=["L", "M", "Q", "H"])
    ec_cb.set("M")
    ec_cb.pack()
    return ec_cb

def add_color_buttons(parent):
    frame = tk.Frame(parent, bg=BG)
    frame.pack(pady=10)

    tk.Button(frame, text="QR Color", command=choose_fg_color)\
        .grid(row=0, column=0, padx=10)

    tk.Button(frame, text="Background", command=choose_bg_color)\
        .grid(row=0, column=1, padx=10)


# -----------------------------------------------------------
# TAB 1: TEXT QR
# -----------------------------------------------------------
text_frame = ttk.Frame(notebook)
notebook.add(text_frame, text="Text QR")

make_label(text_frame, "Enter Text:").pack(pady=10)
text_input = tk.Entry(text_frame, width=45)
text_input.pack()

ec_text = create_ec_dropdown(text_frame)
add_color_buttons(text_frame)

def generate_text_qr():
    msg = text_input.get().strip()
    if msg:
        generate_qr(msg, ec_text.get())

tk.Button(text_frame, text="Generate QR",
          command=generate_text_qr).pack(pady=20)


# -----------------------------------------------------------
# TAB 2: WIFI QR
# -----------------------------------------------------------
wifi_frame = ttk.Frame(notebook)
notebook.add(wifi_frame, text="WiFi QR")

make_label(wifi_frame, "WiFi Name (SSID):").pack(pady=5)
ssid_entry = tk.Entry(wifi_frame, width=45)
ssid_entry.pack()

make_label(wifi_frame, "Password:").pack(pady=5)
password_entry = tk.Entry(wifi_frame, width=45)
password_entry.pack()

make_label(wifi_frame, "Security:").pack(pady=5)
security_cb = ttk.Combobox(wifi_frame, values=["WPA", "WEP", "nopass"])
security_cb.set("WPA")
security_cb.pack()

ec_wifi = create_ec_dropdown(wifi_frame)
add_color_buttons(wifi_frame)

def generate_wifi_qr():
    data = f"WIFI:T:{security_cb.get()};S:{ssid_entry.get()};P:{password_entry.get()};;"
    generate_qr(data, ec_wifi.get())

tk.Button(wifi_frame, text="Generate QR",
          command=generate_wifi_qr).pack(pady=20)


# -----------------------------------------------------------
# TAB 3: CONTACT QR
# -----------------------------------------------------------
contact_frame = ttk.Frame(notebook)
notebook.add(contact_frame, text="Contact Info")

make_label(contact_frame, "Name:").pack(pady=5)
c_name = tk.Entry(contact_frame, width=45)
c_name.pack()

make_label(contact_frame, "Phone:").pack(pady=5)
c_phone = tk.Entry(contact_frame, width=45)
c_phone.pack()

make_label(contact_frame, "Email:").pack(pady=5)
c_email = tk.Entry(contact_frame, width=45)
c_email.pack()

ec_contact = create_ec_dropdown(contact_frame)
add_color_buttons(contact_frame)

def generate_contact_qr():
    vcard = f"""
BEGIN:VCARD
VERSION:3.0
FN:{c_name.get()}
TEL:{c_phone.get()}
EMAIL:{c_email.get()}
END:VCARD
"""
    generate_qr(vcard, ec_contact.get())

tk.Button(contact_frame, text="Generate QR",
          command=generate_contact_qr).pack(pady=20)


# -----------------------------------------------------------
# TAB 4: EMAIL QR
# -----------------------------------------------------------
email_frame = ttk.Frame(notebook)
notebook.add(email_frame, text="Email QR")

make_label(email_frame, "Email To:").pack(pady=5)
email_to = tk.Entry(email_frame, width=45)
email_to.pack()

make_label(email_frame, "Subject:").pack(pady=5)
email_sub = tk.Entry(email_frame, width=45)
email_sub.pack()

ec_email = create_ec_dropdown(email_frame)
add_color_buttons(email_frame)

def generate_email_qr():
    mail = f"mailto:{email_to.get()}?subject={email_sub.get()}"
    generate_qr(mail, ec_email.get())

tk.Button(email_frame, text="Generate QR",
          command=generate_email_qr).pack(pady=20)


# -----------------------------------------------------------
# SAVE BUTTON
# -----------------------------------------------------------
tk.Button(root, text="SAVE QR",
          command=save_qr).pack(pady=10)


# -----------------------------------------------------------
# RUN APP
# -----------------------------------------------------------
root.mainloop()
