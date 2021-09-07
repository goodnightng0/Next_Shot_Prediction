from datetime import timedelta
import os
import subprocess
from datetime import datetime
import json

import youtube_dl
from youtube_dl.utils import (DownloadError, ExtractorError)

target_classes = [
    'main',
    'drone',
    'offside line',
    'behind the goal',
    'crowd',
    'close-up player or referee',
    'close-up corner',
    'beside the goal',
    'close-up side staff',
    'player back'
]

# cut videos into pieces through ffmpeg
def download_video(url, start, dur, output):
    output_tmp = os.path.join(r"C:\Users\yurik\Documents\study\video_data", os.path.basename(output))
    try:
        # From https://stackoverflow.com/questions/57131049/is-it-possible-to-download-a-specific-part-of-a-file
        with youtube_dl.YoutubeDL({'format': 'best'}) as ydl:
            result = ydl.extract_info(url, download=False)
            video = result['entries'][0] if 'entries' in result else result

        url = video['url']
        if start < 5:
            offset = start
        else:
            offset = 5
        start -= offset
        offset_dur = dur + offset
        start_str = str(timedelta(seconds=start))
        dur_str = str(timedelta(seconds=offset_dur))

        cmd = ['ffmpeg', '-ss', start_str, '-i', url,  '-t', dur_str, '-c:v',
               'copy', '-c:a', 'copy', output_tmp]
        subprocess.call(cmd)

        start_str_2 = str(timedelta(seconds=offset))
        dur_str_2 = str(timedelta(seconds=dur))

        cmd = ['ffmpeg','-ss', start_str_2, '-i', output_tmp,  '-t', dur_str_2, output]
        subprocess.call(cmd)
        return True

    except (DownloadError, ExtractorError) as e:
        print("Failed to download %s" % output)
        return False

#downloading train/test/val
def download(mode,max_samples):
    # 폴더 이름이 중복될 경우 뒤에 숫자를 붙인다
    classes_count = {c: 0 for c in target_classes}
    i = 1

    data_dir = "./videos/"+mode
    os.makedirs(data_dir)

    data_array=load_json(mode)

    for fn, data in data_array:
        #choose labels to sort by
        label = data["next_category2"]

        # 초단위로 변경
        try:
            pt = datetime.strptime(data["start"], '%H:%M:%S')
        except:
            pt = datetime.strptime(data["start"], '%M:%S')
        start_seconds = pt.second + pt.minute * 60 + 1

        try:
            pt = datetime.strptime(data["end"], '%H:%M:%S')
        except:
            pt = datetime.strptime(data["end"], '%M:%S')
        end_seconds = pt.second + pt.minute * 60

        segment = [start_seconds, end_seconds]

        url = "https://youtu.be/" + data["video_url"]
        dur = end_seconds - start_seconds

        # 2초 이하, 10초 이상 영상은 편집
        if dur <= 2: continue

        # current_cateogry2에 있는 항목들을 각각 max_samples만큼만 뽑는다
        if label in classes_count and classes_count[label] < max_samples:

            # os.path.join은 인수에 전달된 2개의 문자열을 결합하여, 1개의 경로로 할 수 있다
            c_dir = os.path.join(data_dir, label)

            # 폴더 이름이 존재하면 뒤에 숫자를 더해준다
            if os.path.exists(c_dir):
                label_number = label + str(i)
                # c_dir = os.path.join(data_dir, label_number)
                i += 1

            # c_dir경로가 없으면 새로 만들어준다
            if not os.path.exists(c_dir):
                os.makedirs(c_dir)
                label_number = label

            start = segment[0]
            output = os.path.join(c_dir, "%s_%s.mp4" % (label_number.replace(" ", "_"), fn))
            print(output)

            results = True
            if not os.path.exists(output):
                result = download_video(url, start, dur, output)
            if result:
                classes_count[label] += 1

    print("Finished downloading videos!")

def load_json(mode):
    # 폴더 안에 있는 json 파일들 읽어오기
    path="json_new_format/"+mode
    file_list = os.listdir(path)

    data_array = []
    for i in file_list:
        with open(path+"/" + i, "r") as f:
            mode_data = json.load(f)
            if "info" in mode_data.keys():
                del mode_data["info"]
            data_array = data_array + mode_data["annotations"]

    # 비디오 loader 형식 맞춰주기
    data_array2 = []
    for i in range(0, len(data_array)):
        x = [data_array[i]['video_url'], data_array[i]]
        data_array2.append(x)

    data_array = data_array2.copy()
    return data_array