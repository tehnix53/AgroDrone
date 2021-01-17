import os
from PIL import Image, ExifTags
import pandas as pd

home_dir = 'static/images'

images = []
for i in os.listdir(home_dir):
    if i.endswith('.JPG'):
        images += [os.path.join(home_dir, i)]

df = pd.DataFrame([], columns=["name", "date", "N_g", "N_m", "N_s", "E_g", "E_m", "E_s", "E", "N"])
for i in images:
    img = Image.open(i)
    exif = {ExifTags.TAGS[k]: v for k, v in img.getexif().items() if k in ExifTags.TAGS}
    gps = exif['GPSInfo']

    name = exif['ImageDescription'].split('\\')[-1]
    date = exif['DateTimeOriginal']
    N = gps[2]
    E = gps[4]
    ng = N[0][0] // N[0][1]
    nm = N[1][0] // N[1][1]
    ns = N[2][0] // N[2][1]
    eg = E[0][0] // E[0][1]
    em = E[1][0] // E[1][1]
    es = E[2][0] // E[2][1]
    E_ten = round(eg + ((em * 100) / 60) / 100 + ((es * 100) / 60) / 10000, 4)
    N_ten = round(ng + ((nm * 100) / 60) / 100 + ((ns * 100) / 60) / 10000, 4)

    df_temp = pd.DataFrame([(name, date, ng, nm, ns, eg, em, es, E_ten, N_ten)],
                           columns=["name", "date", "N_g", "N_m", "N_s", "E_g", "E_m", "E_s", "E", "N"])

    df = df.append(df_temp)
df = df.reset_index()
df['category'] = ['norm', 'weeds', 'wasteland']
df['id'] = [0,1,2]
sorted_file = df.sort_values(['name']).values

