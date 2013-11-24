import subprocess
import sys

def create_split(input_name, times_file, output_name):
    print 'splitting'
    # obj = subprocess.Popen('sh split.sh', shell=True)
    # obj.communicate()
    # obj = subprocess.Popen('echo Done!', shell=True)

if __name__ == '__main__':
    # usage
    # python main.py film.mp4 times.txt output.mp4
    if len(sys.argv) >= 4:
        input_name = sys.argv[1]
        times_file = sys.argv[2]
        output_name = sys.argv[3]

    create_split(input_name, times_file, output_name)