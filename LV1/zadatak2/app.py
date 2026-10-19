import os
import sys
import time
import threading

import roslibpy
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

HOST = os.environ.get('ROSBRIDGE_HOST', 'localhost')
PORT = int(os.environ.get('ROSBRIDGE_PORT', '9090'))

# Podaci se pune iz roslibpy dretve, a čitaju iz GUI dretve -> lock
lock = threading.Lock()
xs, ys = [], []
current = {'x': 0.0, 'y': 0.0, 'theta': 0.0}


def pose_callback(msg):
    """Poziva se za svaku poruku /turtle1/pose (msg je Python dict)."""
    with lock:
        xs.append(msg['x'])
        ys.append(msg['y'])
        current['x'] = msg['x']
        current['y'] = msg['y']
        current['theta'] = msg['theta']


def main():
    # Spajanje na rosbridge (run() pokreće vezu u pozadinskoj dretvi)
    ros = roslibpy.Ros(host=HOST, port=PORT)
    print(f'Spajam se na rosbridge {HOST}:{PORT} ...')
    ros.run()

    deadline = time.time() + 10
    while not ros.is_connected and time.time() < deadline:
        time.sleep(0.1)
    if not ros.is_connected:
        print('Ne mogu se spojiti na rosbridge. Radi li kontejner iz zadatka 1?')
        ros.terminate()
        sys.exit(1)
    print('Spojeno na rosbridge.')

    # Pretplata na pozu kornjače
    pose_sub = roslibpy.Topic(ros, '/turtle1/pose', 'turtlesim/msg/Pose')
    pose_sub.subscribe(pose_callback)

    # Graf
    fig, ax = plt.subplots()
    ax.set_title('Turtlesim pose visualization')
    ax.set_xlabel('X position')
    ax.set_ylabel('Y position')
    ax.set_xlim(0, 11.1)
    ax.set_ylim(0, 11.1)
    ax.set_aspect('equal')
    ax.grid(True)

    (traj_line,) = ax.plot([], [], 'b-', label='Trajectory')
    (pos_dot,) = ax.plot([], [], 'ro', label='Current position')
    info = ax.text(0.02, 0.98, '', transform=ax.transAxes, va='top', fontsize=9)
    ax.legend(loc='upper right')

    def update(_frame):
        with lock:
            x_data, y_data = list(xs), list(ys)
            cx, cy, th = current['x'], current['y'], current['theta']
        traj_line.set_data(x_data, y_data)
        if x_data:
            pos_dot.set_data([cx], [cy])
        info.set_text(f'X: {cx:.2f}\nY: {cy:.2f}\nTheta: {th:.2f} rad')
        return traj_line, pos_dot, info

    anim = FuncAnimation(fig, update, interval=50, blit=False, cache_frame_data=False)

    try:
        plt.show()  # blokira dok se prozor ne zatvori
    finally:
        pose_sub.unsubscribe()
        ros.terminate()


if __name__ == '__main__':
    main()
