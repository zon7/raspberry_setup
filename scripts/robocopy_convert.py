"""
Make a robocopy of a folder and converts:
    -Old video formats to MP4 with h264
    -WAV files to MP3
Usage
    python robocopy_convert.py INPUT_PATH OUTPUT_PATH
"""
import os
import subprocess
import shutil
import logging
from sys import argv

if len(argv)<3 or len(argv)>1:
    print("Missing parameters. Usage:\n\tpython robocopy_convert.py INPUT_PATH OUTPUT_PATH")
    exit(0)
inpath = argv[1]
outpath = argv[2]

if not inpath.endswith("/"):
    inpath = inpath + "/"
if not outpath.endswith("/"):
    outpath = outpath + "/"

# List of files to be ignored
ignore_files = [
    'Thumbs.db',
    '.DS_Store',
]

# List of extensions to be ignored
ignore_ext = [
    '.THM',
    '.PYC'
]

# Create logger
logging.basicConfig(format='[%(asctime)s] %(message)s', datefmt='%I:%M:%S')
logger = logging.getLogger("Robocopy")
logger.setLevel(logging.INFO)

logger.info("----------------INICIO---------------")

list_of_files = {}
for (root, dirnames, filenames) in os.walk(inpath):
    total_files = len(filenames)
    logger.info( "Total folder files " + str(total_files))

    '''
    for dirname in dirnames:
        full_path = os.path.join(root, dirname)
        rel_path = full_path.replace(inpath, "")
        out_path = os.path.join(outpath, rel_path)
        #print(out_path)
        os.makedirs(out_path, exist_ok=True)
    '''
    # Obtain folder path relative to inpath
    rel_path = root.replace(inpath, "")
    # Create output path with outpath and rel_path
    out_path = os.path.join(outpath, rel_path)    
    os.makedirs(out_path, exist_ok=True)

    for filename in filenames:
        # Obtain full path and file extension
        full_path = os.path.join(root, filename)
        # print(full_path)

        # Obtain file destination path
        rel_path = full_path.replace(inpath, "")
        out_path = os.path.join(outpath, rel_path)
        file_wo_ext, ext = os.path.splitext(out_path)

        if filename in ignore_files:
            logger.info("[IGNORE]" + filename)
        elif ext.upper() in ignore_ext:
            logger.info("[IGNORE]" + filename)
        elif ext in ['.wav','.WAV',]:
            out_path = file_wo_ext + '.mp3'

            # If already exists ignore
            if os.path.exists(out_path):
                logger.info("[EXISTS]" + rel_path)
            else:
                logger.info("[CONVERT]" + rel_path + " -> MP3")
                subprocess.call([
                    'ffmpeg','-i', full_path, 
                    '-vn', '-b:a','128k',
                    # Make less verbose
                    '-hide_banner',
                    '-loglevel', 'error',
                    out_path
                ])

        elif ext in ['.mov','.MOV','.MPG','.mpg','.avi','.AVI','.m2v','.MOD','.wm','.rv', '.flv','.VOB']:
            out_path = file_wo_ext + '.mp4'

            # If already exists ignore
            if os.path.exists(out_path):
                logger.info("[EXISTS]" + rel_path)
            else:
                logger.info("[CONVERT]" + rel_path + " -> MP4")
                subprocess.call([
                    'ffmpeg','-i', full_path, 
                    '-vcodec','h264', '-acodec','aac',
                    # Make less verbose
                    '-hide_banner',
                    '-loglevel', 'error',
                    out_path
                ])
        else:
            # If already exists ignore
            if os.path.exists(out_path):
                logger.info("[EXISTS]" + rel_path)
            else:
                logger.info("[COPY]" + rel_path)
                shutil.copyfile(full_path, out_path)

logger.info("FIN")
