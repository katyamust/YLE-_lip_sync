import pandas as pd
import json

with open('config.json') as json_config_file:
    config = json.load(json_config_file)


# video_file = config["saga"]["input_video"]
# audio_file = config["saga"]["input_audio"]
# output_dataset_file = config["saga"]["output"]

video_file = config["oddsat"]["input_video"]
audio_file = config["oddsat"]["input_audio"]
output_dataset_file = config["oddsat"]["output"]

video_features_df = pd.read_csv(video_file)
video_features_df=video_features_df.drop(columns=['Index'])
print(video_features_df.head(26))

audio_features_df = pd.read_csv(audio_file)#
audio_features_df=audio_features_df.drop(columns=['Index'])

print(audio_features_df.columns)
audio_features_df=audio_features_df.drop(columns=['RMS','8Hz', '12.5Hz', '16Hz', '20Hz', '25Hz','31.5Hz', '40Hz', '50Hz', '63Hz', '80Hz','5000Hz','6300Hz', '8000Hz', '10000Hz', '12500Hz', '16000Hz', '20000Hz'])
print(audio_features_df.columns)

print(audio_features_df.head(26))

# create sync dataset

# 1. merge video_and audio files
merge_df = video_features_df.join(audio_features_df)

print("joined audio and video sync before concatenate")
print(merge_df.head(30))

def concat_by_frame_25(merge_df):
    sync_df_list = [[]]
    for i in range(0,int(merge_df.shape[0]/25)):
        df_25 = merge_df.iloc[i*25:(i+1)*25]
        list_25 = list(df_25.values.flatten())
        sync_df_list.append(list_25)

    df_con = pd.DataFrame(sync_df_list)

    return df_con

#2. roll out each 25 rows(one video frame) into one row
sync_dataset_df = concat_by_frame_25(merge_df)

#3. add  1 label
sync_dataset_df['sync'] = pd.Series(1, index=sync_dataset_df.index)

# create (generate artificial) non sync dataset
shifted_audio_df = audio_features_df.iloc[4:]

    #shifted_audio_df["Index"] = shifted_audio_df['Index'].apply(lambda x : x-4)

shifted_audio_df = shifted_audio_df.reset_index(drop=True);
    #shifted_audio_df = shifted_audio_df.drop(columns=['Index'])
    #shifted_audio_df = shifted_audio_df.drop(columns=['index'])
    #video_features_df= video_features_df.reset_index(drop=True);

merge_df_non_sync = video_features_df.join(shifted_audio_df)

print("joined video audio not in sync before concatenate")
print(merge_df_non_sync.head(30))

non_sync_dataset_df = concat_by_frame_25(merge_df_non_sync)

#3. add 0 label
non_sync_dataset_df['sync'] = pd.Series(0, index=non_sync_dataset_df.index)

# generate artifitual non sync dataset
# shift audio features 4 frames forward
print("Summary")
print("sync_dataset_df concat")
print(sync_dataset_df.shape)
print(sync_dataset_df.head(30))

print("non_sync_dataset_df concat")
print(non_sync_dataset_df.shape)
print(non_sync_dataset_df.head(30))

df_list = [sync_dataset_df,non_sync_dataset_df]

final_df = pd.concat(df_list, axis =0, ignore_index = True)

final_df.to_csv(output_dataset_file)

print("Done")



