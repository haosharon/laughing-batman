import subprocess
import sys

def print_message(message):
    border = '********************************'
    print border
    print border
    print message
    print border
    print border

def get_times(file_name):
    print_message('getting times')
    f = open(file_name, 'r')
    times = []
    for line in f:
        split = line.split(',')
        time = split[0].strip()
        # convert time to seconds
        positions = time.split(':')
        seconds = 0
        for position in positions:
            seconds *= 60
            seconds += int(position)

        tup = (seconds, split[1].strip())

        times.append(tup)
    return times

def split(input_name, times):
    index = 0
    intermediate_names = []
    for time in times:
        intermediate_name = "__intermediate_%(index)s__" % \
        {'index': index}
        start = time[0]
        duration = time[1]
        intermediate_names.append(intermediate_name)
        intermediate_file = intermediate_name + '.mp4'


        cmd = "ffmpeg -ss %(start)s -i %(input_name)s -ss %(start)s -t %(duration)s %(output)s" % \
        {'input_name': input_name, 'start': start, 'duration': duration, 'output': intermediate_file}
        index += 1
        print_message('splitting ' + intermediate_name)
        sub = subprocess.Popen(cmd, shell=True)
        sub.communicate()
        print_message('done spltting ' + intermediate_name)
    print_message('done spltting all')
    return intermediate_names

def convert(intermediate_names):
    print_message('converting')
    for name in intermediate_names:
        cmd = "ffmpeg -i %(intermediate)s -qscale:v 1 %(mpg)s" % \
        {'intermediate': name + '.mp4', 'mpg': name + '.mpg'}
        sub = subprocess.Popen(cmd, shell=True)
        print_message('converting ' + name)
        sub.communicate()
    print_message('done converting all')

def concat(intermediate_names):
    print_message('concating')
    cmd = "cat "
    for name in intermediate_names:
        cmd += name + '.mpg '
    cmd += "> intermediate_all.mpg"
    sub = subprocess.Popen(cmd, shell=True)
    sub.communicate()
    return 'intermediate_all.mpg'

def mpg_to_mp4(mpg, output):
    cmd = "ffmpeg -i %(name)s -qscale:v 2 %(output)s" % \
    {'name': mpg, 'output': output}

    sub = subprocess.Popen(cmd, shell=True)
    sub.communicate()
    print_message('converting')

def clean_up(intermediate_names):
    print_message('cleaning up')
    cmd = ''
    for name in intermediate_names:
        cmd += "rm %(name)s.mp4 %(name)s.mpg;" % \
        {'name': name}
    sub = subprocess.Popen(cmd, shell=True)
    sub.communicate()

    cmd = 'rm intermediate_all.mpg'
    sub = subprocess.Popen(cmd, shell=True)
    sub.communicate()
    return

def create_split(input_name, times_file, output_name):
    times = get_times(times_file)
    intermediate_names = split(input_name, times)

    convert(intermediate_names)

    file_all = concat(intermediate_names)

    mpg_to_mp4(file_all, output_name)

    clean_up(intermediate_names)

    print_message('done with everything!')

if __name__ == '__main__':
    if len(sys.argv) >= 4:
        input_name = sys.argv[1]
        times_file = sys.argv[2]
        output_name = sys.argv[3]

        create_split(input_name, times_file, output_name)