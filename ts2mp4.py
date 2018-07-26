import os, sys

def convert(file_in, file_out):
    if file_in .endswith("ts") and file_out.endswith('mp4'):
        os.system("ffmpeg -n -i {} -acodec copy -vcodec copy -bsf aac_adtstoasc {}".format(file_in, file_out))
        return 0
    else:
        return 1


if __name__ == "__main__":
    file_in = sys.argv[1]
    file_out = file_in.split('.')[0]+'.mp4'
    convert(file_in, file_out)
