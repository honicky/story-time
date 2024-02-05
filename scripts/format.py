
import subprocess

# find the git base

git_base = subprocess.check_output(["git", "rev-parse", "--show-toplevel"]).decode("utf-8").strip()
storyviz_base = git_base + "/story-viz"
storyviz_backend = storyviz_base + "/backend"

# run black

subprocess.check_call(["black", "-l", "120", "-S", storyviz_backend])




