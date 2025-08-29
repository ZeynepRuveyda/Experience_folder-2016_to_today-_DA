import argparse
import os
import subprocess

def parse_args():
    parser = argparse.ArgumentParser(description="Clone a GitHub repository")
    parser.add_argument("--log_dir", default="", help="Directory to save logs")
    parser.add_argument("--repo_url", default="https://github.com/eqasim-org/ile-de-france.git", help="URL of the repository to clone")
    return parser.parse_args()

def git_clone(repo_url: str, clone_dir: str):
    try:
        result = subprocess.run(['git', 'clone', repo_url, clone_dir], check=True, capture_output=True, text=True)
        return result.stdout, None
    except subprocess.CalledProcessError as e:
        return None, e.stderr

def save_log(message: str, log_file: str):
    with open(log_file, 'w') as f:
        f.write(message)

def main():
    args = parse_args()
    clone_dir = os.path.join(args.log_dir, "equasim")
    
    # Ensure the log directory exists
    os.makedirs(args.log_dir, exist_ok=True)
    
    log_file = os.path.join(args.log_dir, 'clone_log.txt')
    
    # Try to clone the repository and capture the output or error
    output, error = git_clone(args.repo_url, clone_dir)
    
    if output:
        log_message = f"Repository {args.repo_url} cloned successfully into {clone_dir}.\n\n{output}"
    else:
        log_message = f"Failed to clone repository {args.repo_url}. Error:\n\n{error}"
    
    # Save the log message to the log file
    save_log(log_message, log_file)
    
    # Print the log message to the console
    print(log_message)
    print(f"Log saved to {log_file}")

if __name__ == "__main__":
    main()
