import tkinter as tk
from tkinter import ttk
import serial.tools.list_ports
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import time
import threading
import serial


class mapping_gui:

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1000x700")
        self.root.configure(bg="#303030")
        self.reading = False
        self.connection = False
        self.reader_thread = None
        self.run_stat = False
        self.utility_bar()
        self.connection_bar()
        self.map()

        self.root.mainloop()

    # ---------------- CONNECTION BAR ----------------
    def connection_bar(self):
        frame = tk.Frame(self.root, bg="#303030")
        frame.pack(fill="x")

        ports = serial.tools.list_ports.comports()
        self.COM_list = [com.device for com in ports]
        self.COM_list.insert(0, "-")

        tk.Label(frame, text="COM", bg="#303030", fg="white").grid(row=0, column=0)
        self.com_var = tk.StringVar(value=self.COM_list[0])
        ttk.OptionMenu(frame, self.com_var, *self.COM_list).grid(row=0, column=1)

        tk.Label(frame, text="Mode", bg="#303030", fg="white").grid(row=1, column=0)
        self.mode_var = tk.StringVar(value="3D Scanning")

        self.modes = ["3D Scanning","Adaptive 3D Scanning","3D Scanning", "2D Rader", "Static Distance"]
        self.mode_bd = ttk.OptionMenu(frame, self.mode_var, *self.modes,command=self.change_mode)
        self.mode_bd.grid(row=1, column=1)

        tk.Label(frame, text="Baud", bg="#303030", fg="white").grid(row=0, column=2)
        self.clicked_bd = tk.StringVar(value="9600")
        ttk.OptionMenu(frame, self.clicked_bd, "9600", "9600").grid(row=0, column=3)

        self.button_conect = ttk.Button(frame, text="Connect", command=self.serial_connect)
        self.button_conect.grid(row=0, column=4)

        self.connect_status = tk.Label(frame, text="Disconnected", fg="red", bg="#303030")
        self.connect_status.grid(row=0, column=5)

    # ---------------- CONNECT ----------------
    def serial_connect(self):
        try:
            self.ser = serial.Serial(self.com_var.get(), int(self.clicked_bd.get()), timeout=0.1)
            time.sleep(2)

            self.connection = True
            self.connect_status.config(text="Online", fg="green")
            print("Connected")

        except:
            self.connect_status.config(text="Error", fg="orange")

    # ---------------- UI ----------------
    def utility_bar(self):
        frame = tk.Frame(self.root, bg="#303030")
        frame.pack(side='bottom', fill='x')

        self.res_var = tk.StringVar(value="10 degrees")
        self.res_options = {"1 degrees": 1, "2 degrees": 2, "5 degrees": 5, "10 degrees": 10}

        ttk.OptionMenu(frame, self.res_var, *self.res_options.keys()).pack(side='left')

        self.start_scanning_bd = tk.Button(frame, text='Start Scanning', command=self.scanning_start)
        self.start_scanning_bd.pack(side='left')

    # ---------------- MAP ----------------
    def map(self):
        self.map_frame = tk.Frame(self.root, bg="#202020")
        self.map_frame.pack(fill="both", expand=True)
        self.create_3d_plot()

    def create_3d_plot(self):
        fig = plt.figure(facecolor="#202020")
        self.ax = fig.add_subplot(111, projection='3d')

        self.xs, self.ys, self.zs = [], [], []

        self.canvas = FigureCanvasTkAgg(fig, master=self.map_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def create_2d_plot(self):
        fig = plt.figure(figsize=(6,8), facecolor='#202020')
        ax = fig.add_subplot(111, projection='polar')

        self.ax = ax
        self.d2_theta_vals = []
        self.d2_r_vals = []

        ax.set_facecolor('black')
        ax.set_theta_zero_location('N')
        ax.set_theta_direction(-1)
        ax.set_rlim(0, 200)

        ax.grid(True, color='lime', linestyle='-', linewidth=0.5)
        ax.tick_params(colors='lime')

        self.canvas = FigureCanvasTkAgg(fig, master=self.map_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def create_static_display(self):
        self.distance_label = tk.Label(
            self.map_frame,
            text="Distance: --- mm",
            font=("Segoe UI", 30, "bold"),
            fg="lime",
            bg="#202020"
        )
        self.distance_label.pack(expand=True)

    def change_mode(self, val=None) -> None:
        mode = self.mode_var.get()

        for widget in self.map_frame.winfo_children():
            widget.destroy()

        if mode in ["3D Scanning", "Adaptive 3D Scanning"]:
            self.create_3d_plot()

        elif mode == "2D Rader":
            self.create_2d_plot()

        elif mode == "Static Distance":
            self.create_static_display()

    # ---------------- START / STOP ----------------
    def scanning_start(self):

        if self.start_scanning_bd['text'] == 'Start Scanning':
            self.mode_bd["state"] = "disabled"
            if not self.connection:
                print("Not connected")
                return

            mode = self.mode_var.get()
            precision = self.res_options[self.res_var.get()]

            # 🔥 NEW COMMAND SYSTEM
            if mode in ["3D Scanning", "Adaptive 3D Scanning"]:
                self.ser.write(b'3')
            elif mode == "2D Rader":
                self.ser.write(b'2')
            elif mode == "Static Distance":
                self.ser.write(b'1')
            else:
                return

            self.ser.flush()
            time.sleep(0.05)

            self.ser.write(f'P{precision}\n'.encode())
            self.ser.flush()
            time.sleep(0.05)

            if self.reader_thread is None or not self.reader_thread.is_alive():
                self.run_stat = True
                self.reader_thread = threading.Thread(target=self.serial_reader, daemon=True)
                self.reader_thread.start()

            self.reading = True
            self.start_scanning_bd['text'] = 'Stop Scanning'

        else:
            print("STOP")
            self.reading = False
            self.run_stat = False
            self.start_scanning_bd['text'] = 'Start Scanning'
            self.mode_bd["state"] = "normal"

    # ---------------- SERIAL ----------------
    def serial_reader(self):
        while self.connection and self.run_stat:
            try:
                if self.reading:
                    self.ser.write(b'S')
                time.sleep(0.02)   # 🔥 ADD THIS
                line = self.ser.readline().decode(errors='ignore').strip()
                print(line)
                if not line:
                    print('noline')
                    continue

                print("line ->", line)
                self.process_data(line)

            except Exception as e:
                print(e)

    # ---------------- DATA ----------------
    def process_data(self, line):
        parts = line.split(",")

        if parts[0] == "RESET":
            print("RESET received")
            return

        try:
            if parts[0] == "1D":
                if parts[1] == "OUT":
                    return
                self.update_1d(float(parts[1]))

            elif parts[0] == "2D":
                if parts[2] == "OUT":
                    return
                self.update_2d(float(parts[1]), float(parts[2]))

            elif parts[0] == "3D":
                if parts[3] == "OUT":
                    return
                self.update_3d(float(parts[1]), float(parts[2]), float(parts[3]))

        except:
            pass

    # ---------------- UPDATE ----------------
    def update_1d(self, d):
        def s():
            self.distance_label['text'] = f"Distance: {d} mm"
        self.root.after(0, s)

    def update_2d(self, phi, d):
        theta_rad = np.radians(phi)

        self.d2_theta_vals.append(theta_rad)
        self.d2_r_vals.append(d)

        if len(self.d2_theta_vals) % 10 != 0:
            return

        def draw():
            self.ax.clear()
            self.ax.set_theta_zero_location('N')
            self.ax.set_theta_direction(-1)
            self.ax.set_rlim(0, 1000)

            self.ax.scatter(self.d2_theta_vals, self.d2_r_vals, s=10)
            self.canvas.draw()

        self.root.after(0, draw)

    def update_3d(self, theta, phi, d):
        x = d * np.sin(np.radians(theta)) * np.cos(np.radians(phi))
        y = d * np.sin(np.radians(theta)) * np.sin(np.radians(phi))
        z = d * np.cos(np.radians(theta))

        self.xs.append(x)
        self.ys.append(y)
        self.zs.append(z)

        def draw():
            self.ax.clear()

            # Axis limits
            self.ax.set_xlim(-1000, 1000)
            self.ax.set_ylim(-1000, 1000)
            self.ax.set_zlim(-1000, 1000)

            # Compute color values
            r = np.sqrt(np.array(self.xs)**2 +
                        np.array(self.ys)**2 +
                        np.array(self.zs)**2)

            # Scatter plot
            sc = self.ax.scatter(self.xs, self.ys, self.zs,
                                s=5, c=r, cmap='rainbow',vmin=0,vmax=1000)

            fig = self.ax.get_figure()

            # ✅ SAFE COLORBAR HANDLING
            if not hasattr(self.ax, "_cbar") or self.ax._cbar is None:
                self.ax._cbar = fig.colorbar(sc, ax=self.ax,
                                            label="Distance from origin(in mm)")
            else:
                try:
                    self.ax._cbar.update_normal(sc)
                except Exception:
                    # fallback if matplotlib got confused
                    try:
                        self.ax._cbar.remove()
                    except Exception:
                        pass
                    self.ax._cbar = fig.colorbar(sc, ax=self.ax,
                                                label="Distance from origin")

            self.canvas.draw_idle()   # smoother than draw()

        self.root.after(0, draw)


if __name__ == "__main__":
    mapping_gui()
