import argparse
import os
import subprocess

def parse_args():
    parser = argparse.ArgumentParser(description="Simulation")
    parser.add_argument("--log_dir", default="", help="Directory to save logs")
    return parser.parse_args()

args = parse_args()
working_directory = os.path.join(str(args.log_dir), "equasim")

def run_synpp(working_dir: str = working_directory):
    # Ensure the working directory exists
    if not os.path.exists(working_dir):
        print(f"Working directory {working_dir} does not exist.")
        return

    # Running synpp command
    command = ['python3', '-m', 'synpp']
    try:
        subprocess.run(command, check=True, cwd=working_dir)
        print("Synpp command executed successfully.")
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except subprocess.CalledProcessError as e:
        print(f"Synpp command failed with error: {e}")

def main():
    run_synpp()

if __name__ == "__main__":
    main()
