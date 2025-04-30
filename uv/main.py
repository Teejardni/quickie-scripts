import subprocess
import time
import shutil
import os
import csv

REQUIREMENTS_FILE = "requirements.txt"
VENV_DIR_PIP = "venv_pip"
VENV_DIR_UV = "venv_uv"
RESULTS_CSV = "results.csv"


def run(cmd, check=True):
    print("➤", " ".join(cmd))
    subprocess.run(cmd, check=check)


def delete_venv(venv_dir):
    if os.path.exists(venv_dir):
        shutil.rmtree(venv_dir)


def pip_flow(venv_dir):
    print(f"\n Starting pip flow ({venv_dir})")
    delete_venv(venv_dir)
    start = time.time()
    run(["python3", "-m", "venv", venv_dir])
    pip_path = os.path.join(venv_dir, "Scripts" if os.name == "nt" else "bin", "pip")
    run([pip_path, "install", "-r", REQUIREMENTS_FILE])
    total = time.time() - start
    return total


def uv_flow(venv_dir):
    print(f"\n⚡ Starting uv flow ({venv_dir})")
    delete_venv(venv_dir)

    start = time.time()
    run(["uv", "venv", venv_dir])
    python_path = os.path.join(venv_dir, "Scripts" if os.name == "nt" else "bin", "python")
    run(["uv", "pip", "install", "-r", REQUIREMENTS_FILE, "--python", python_path])

    total = time.time() - start
    return total


def write_csv(pip_time, uv_time):
    with open(RESULTS_CSV, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Tool", "Time (seconds)"])
        writer.writerow(["pip", f"{pip_time:.2f}"])
        writer.writerow(["uv", f"{uv_time:.2f}"])
    print(f"\n📁 CSV written to {RESULTS_CSV}")


# def plot_results(pip_time, uv_time):
#     import matplotlib.pyplot as plt
#     tools = ['pip', 'uv']
#     times = [pip_time, uv_time]

#     plt.bar(tools, times, color=['blue', 'green'])
#     plt.ylabel("Time (seconds)")
#     plt.title("pip vs uv Setup Time")
#     for i, v in enumerate(times):
#         plt.text(i, v + 0.5, f"{v:.2f}s", ha='center', fontweight='bold')
#     plt.tight_layout()
#     plt.show()


def main():
    pip_time = pip_flow(VENV_DIR_PIP)
    uv_time = uv_flow(VENV_DIR_UV)
    print(f"pip total: {pip_time:.2f} seconds")
    print(f"uv  total: {uv_time:.2f} seconds")

    write_csv(pip_time, uv_time)
    plot_results(pip_time, uv_time)


if __name__ == "__main__":
    main()
