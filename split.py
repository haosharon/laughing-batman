import subprocess
import sys

def print_message(message):
    border = '********************************'
    print
    print border
    print message
    print border
    print

def execute_command(cmd):
    print '$ ' + cmd
    sub = subprocess.Popen(cmd, shell=True)
    sub.communicate()
    return

def get_times(file_name):
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

# split video into intermediate files, given a list of time tuples
def split(input_name, times):
    print_message('Splitting video into intermediate files')
    intermediate_names = []
    index = 0
    for time in times:
        intermediate_name = "intermediate_%(index)s" % \
        {'index': index}
        intermediate_names.append(intermediate_name)

        intermediate_file = intermediate_name + '.mp4'

        start = time[0]
        duration = time[1]

        cmd = "ffmpeg -ss %(start)s -i %(input_name)s -t %(duration)s %(output)s" % \
        {'input_name': input_name, 'start': start, 'duration': duration, 'output': intermediate_file}

        print_message('splitting ' + intermediate_name)
        execute_command(cmd)

        index += 1

    return intermediate_names

# converts mp4 files to mpg
def mp4_to_mpg(intermediate_names):
    print_message('Converting intermediate files to mpg')
    for name in intermediate_names:
        cmd = "ffmpeg -i %(intermediate)s -qscale:v 1 %(mpg)s" % \
        {'intermediate': name + '.mp4', 'mpg': name + '.mpg'}

        print_message('converting ' + name)
        execute_command(cmd)

    print_message('Done converting all')

# joins many mpg files together
def concat(intermediate_names):
    print_message('Joining mpg files together')
    file_all = 'intermediate_all.mpg'
    cmd = "cat "
    for name in intermediate_names:
        cmd += name + '.mpg '
    cmd += "> " + file_all

    execute_command(cmd)
    return file_all

# convert final mgp file back to mp4
def mpg_to_mp4(mpg, output):
    print_message("Converting mpg file back to mp4")
    cmd = "ffmpeg -i %(name)s -qscale:v 2 %(output)s" % \
    {'name': mpg, 'output': output}
    execute_command(cmd)

# remove all intermediate files created
def clean_up(intermediate_names, file_all):
    print_message('Removing intermediate files')
    cmd = ''
    for name in intermediate_names:
        cmd += "rm %(name)s.mp4 %(name)s.mpg;" % \
        {'name': name}
    execute_command(cmd)

    cmd = 'rm ' + file_all
    execute_command(cmd)
    return

# main
def main(input_name, times_file, output_name):
    times = get_times(times_file)
    intermediate_names = split(input_name, times)

    mp4_to_mpg(intermediate_names)

    file_all = concat(intermediate_names)

    mpg_to_mp4(file_all, output_name)

    clean_up(intermediate_names, file_all)

    print_message('Done.')

if __name__ == '__main__':
    if len(sys.argv) >= 4:
        input_name = sys.argv[1]
        times_file = sys.argv[2]
        output_name = sys.argv[3]

        main(input_name, times_file, output_name)