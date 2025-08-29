import argparse
import os
import subprocess
import time

def parse_args():
    parser = argparse.ArgumentParser(description="Simulation")
    parser.add_argument("--log_dir", default="", help="Directory to save logs")
    return parser.parse_args()

args = parse_args()
clone_dir = os.path.join(str(args.log_dir), "equasim")
os.mkdir(clone_dir) 
def git_clone(repo_url: str = 'https://github.com/eqasim-org/ile-de-france.git', clone_dir: str= clone_dir):
    # Always try to clone the repository
    subprocess.run(['git', 'clone', repo_url, clone_dir], check=True)
    print(f"Repository {repo_url} cloned successfully into {clone_dir}.")


def main():

    git_clone()
    time.sleep(5)
    
if __name__ == "__main__":
    main()
