import tempfile
import subprocess
import os
import shutil

temp_dir = tempfile.mkdtemp(prefix='sahyadrushti_clone_test_')
repo_src = r'C:\Documents\SAHYADRUSHTI_INDRADHANU\SAHYADRUSHTI'

print(f'Testing clone in temp directory: {temp_dir}')
try:
    cmd_clone = f'git clone --branch final-loop "{repo_src}" "{temp_dir}"'
    res_clone = subprocess.run(cmd_clone, shell=True, capture_output=True, text=True)
    print('Clone returncode:', res_clone.returncode)
    if res_clone.returncode != 0:
        print('Clone error:', res_clone.stderr)
    else:
        # Copy .env.example to .env in clone (as instructed in README quick start)
        src_env = os.path.join(temp_dir, '.env.example')
        dst_env = os.path.join(temp_dir, '.env')
        if os.path.exists(src_env):
            shutil.copy(src_env, dst_env)
            print('[OK] Copied .env.example to .env in fresh clone directory')

        # Run ps_check in clone
        script_path = os.path.join(temp_dir, 'scripts', 'ps_check.py')
        cmd_check = f'python "{script_path}"'
        res_check = subprocess.run(cmd_check, shell=True, capture_output=True, text=True)
        print('Clone ps_check returncode:', res_check.returncode)
        if res_check.stdout:
            lines = res_check.stdout.strip().splitlines()
            for l in lines[-12:]:
                print('  ', l)
finally:
    try:
        shutil.rmtree(temp_dir, ignore_errors=True)
        print('Cleaned up temporary test directory.')
    except Exception:
        pass
